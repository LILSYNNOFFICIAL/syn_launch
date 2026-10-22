#!/usr/bin/env python3
"""SYN_LAUNCH: catalog-first security toolkit manager for Termux."""
from __future__ import annotations
import argparse, json, os, platform, re, selectors, shutil, signal, subprocess, sys, time
from pathlib import Path
from urllib.parse import urlsplit
from workflow_planner import WORKFLOWS, build_workflow_plan
from workflow_adapters import run_workflow_adapter

APP_DIR = Path(__file__).resolve().parent
CATALOG_PATH = APP_DIR / "catalog.json"
STATE_DIR = Path(os.environ.get("SYN_LAUNCH_HOME", str(Path.home() / ".syn_launch"))).expanduser()
LOG_DIR, BIN_DIR, VENV_DIR = STATE_DIR / "logs", Path.home() / ".local" / "bin", STATE_DIR / "venv"
CUSTOM_PATH, FAVORITES_PATH = STATE_DIR / "custom_tools.json", STATE_DIR / "favorites.json"
for directory in (STATE_DIR, LOG_DIR, BIN_DIR):
    directory.mkdir(parents=True, exist_ok=True)
    try: directory.chmod(0o700 if directory != BIN_DIR else 0o755)
    except OSError: pass
os.environ["PATH"] = os.pathsep.join([str(BIN_DIR), str(VENV_DIR / "bin"), os.environ.get("PATH", "")])

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
    from rich.table import Table
    RICH, console = True, Console()
except Exception:
    RICH, console = False, None

INSTALL_KINDS = {"pkg", "pip", "go", "cargo", "npm", "manual", "root"}
PKG_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9.+_-]{0,127}$")
PIP_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
GO_RE = re.compile(r"^[A-Za-z0-9._/-]+@[A-Za-z0-9._-]+$")
CARGO_RE = re.compile(r"^[A-Za-z0-9_-]+$")
NPM_RE = re.compile(r"^(?:@[A-Za-z0-9._-]+/)?[A-Za-z0-9._-]+$")
EXECUTABLE_RE = re.compile(r"^[A-Za-z0-9_.+-]{1,128}$")
MAX_COMMAND_OUTPUT_BYTES = 10 * 1024 * 1024
LAST_COMMAND_RESULT = {"command": None, "label": None, "exit_code": None, "timed_out": False, "launch_error": None}

def say(message=""):
    if RICH: console.print(message, markup=False)
    else: print(str(message))

def title():
    if RICH: console.print(Panel.fit("[bold bright_cyan]S Y N _ L A U N C H[/bold bright_cyan]\n[dim]Termux Security Toolkit • Android-aware[/dim]", border_style="bright_cyan"))
    else: print("\nS Y N _ L A U N C H\nTermux Security Toolkit • Android-aware\n")

def validate_catalog(data):
    if not isinstance(data, dict) or not isinstance(data.get("tools"), list) or not isinstance(data.get("categories"), list):
        raise ValueError("catalog must contain tools and categories lists")
    if type(data.get("tool_count")) is not int or data.get("tool_count") != len(data["tools"]): raise ValueError("tool_count does not match actual entries")
    ids, categories, display_names = set(), set(), set()
    for t in data["tools"]:
        if not isinstance(t, dict): raise ValueError("each tool must be an object")
        for field in ("id","name","category","executable","install_kind","description","source","caveat"):
            if not isinstance(t.get(field),str) or not t[field].strip(): raise ValueError(f"missing/invalid {field}: {t.get('name','<unnamed>')}")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*",t["id"]): raise ValueError(f"invalid id: {t['id']}")
        if len(t["name"]) > 160 or len(t["description"]) > 2000 or len(t["caveat"]) > 2000:
            raise ValueError(f"field exceeds safe length: {t['name']}")
        if not isinstance(t.get("category"), str) or len(t["category"]) > 120:
            raise ValueError(f"invalid category: {t['name']}")
        if not isinstance(t.get("executable"), str) or not EXECUTABLE_RE.fullmatch(t["executable"]):
            raise ValueError(f"invalid executable name: {t['name']}")
        if t["id"] in ids: raise ValueError(f"duplicate id: {t['id']}")
        display_name=t["name"].casefold()
        if display_name in display_names: raise ValueError(f"duplicate display name: {t['name']}")
        ids.add(t["id"]); display_names.add(display_name); categories.add(t["category"])
        if t["install_kind"] not in INSTALL_KINDS: raise ValueError(f"invalid install kind: {t['name']}")
        try:
            parsed_source = urlsplit(t["source"])
            valid_source = parsed_source.scheme == "https" and bool(parsed_source.hostname) and not parsed_source.username and not parsed_source.password and not any(ch.isspace() for ch in t["source"])
            _ = parsed_source.port
        except ValueError:
            valid_source = False
        if not valid_source: raise ValueError(f"source must be a valid HTTPS URL without credentials: {t['name']}")
        if "example" in t and (not isinstance(t["example"], str) or len(t["example"]) > 1000):
            raise ValueError(f"invalid example: {t['name']}")
        compatibility = t.get("compatibility")
        if compatibility is not None:
            if not isinstance(compatibility, dict):
                raise ValueError(f"invalid compatibility metadata: {t['name']}")
            required_compatibility = ("status", "platform", "install_source", "evidence_kind",
                                      "evidence_scope", "architecture_policy", "root_required", "hardware_requirements",
                                      "external_services", "known_blockers", "reviewed_on")
            if any(field not in compatibility for field in required_compatibility):
                raise ValueError(f"incomplete compatibility metadata: {t['name']}")
            if compatibility.get("status") != "source_documented_not_device_verified":
                raise ValueError(f"unsupported compatibility status: {t['name']}")
            if type(compatibility.get("root_required")) is not bool:
                raise ValueError(f"invalid root requirement metadata: {t['name']}")
            for field in ("hardware_requirements", "external_services", "known_blockers"):
                values = compatibility.get(field)
                if not isinstance(values, list) or any(not isinstance(value, str) or not value.strip() or len(value) > 1000 for value in values):
                    raise ValueError(f"invalid compatibility list {field}: {t['name']}")
            for field in ("status", "platform", "evidence_kind", "evidence_scope", "architecture_policy", "reviewed_on"):
                value = compatibility.get(field)
                if not isinstance(value, str) or not value.strip() or len(value) > 500:
                    raise ValueError(f"invalid compatibility field {field}: {t['name']}")
            try:
                evidence_url = urlsplit(compatibility.get("install_source", ""))
                valid_evidence = evidence_url.scheme == "https" and bool(evidence_url.hostname) and not evidence_url.username and not evidence_url.password and not any(ch.isspace() for ch in compatibility["install_source"])
                _ = evidence_url.port
            except (ValueError, TypeError):
                valid_evidence = False
            if not valid_evidence:
                raise ValueError(f"compatibility evidence must be a valid HTTPS URL: {t['name']}")
        security_advisory = t.get("security_advisory")
        if security_advisory is not None:
            if not isinstance(security_advisory, dict):
                raise ValueError(f"invalid security advisory metadata: {t['name']}")
            if security_advisory.get("severity") not in {"critical", "high", "medium", "low"}:
                raise ValueError(f"invalid security advisory severity: {t['name']}")
            if not isinstance(security_advisory.get("published_on"), str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", security_advisory["published_on"]):
                raise ValueError(f"invalid security advisory date: {t['name']}")
            cves = security_advisory.get("cves")
            if not isinstance(cves, list) or not cves or any(not isinstance(cve, str) or not re.fullmatch(r"CVE-\d{4}-\d{4,}", cve) for cve in cves):
                raise ValueError(f"invalid security advisory CVE list: {t['name']}")
            fixed_versions = security_advisory.get("fixed_versions")
            if not isinstance(fixed_versions, dict) or not fixed_versions or any(
                not isinstance(branch, str) or not re.fullmatch(r"\d+\.\d+", branch)
                or not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+\.\d+", version)
                for branch, version in fixed_versions.items()
            ):
                raise ValueError(f"invalid security advisory fixed versions: {t['name']}")
            try:
                advisory_url = urlsplit(security_advisory.get("upstream_advisory", ""))
                valid_advisory_url = advisory_url.scheme == "https" and bool(advisory_url.hostname) and not advisory_url.username and not advisory_url.password and not any(ch.isspace() for ch in security_advisory["upstream_advisory"])
                _ = advisory_url.port
            except (ValueError, TypeError):
                valid_advisory_url = False
            if not valid_advisory_url:
                raise ValueError(f"security advisory must be a valid HTTPS URL: {t['name']}")
            recipe_revision = security_advisory.get("termux_recipe_revision")
            if recipe_revision is not None and (not isinstance(recipe_revision, str) or not re.fullmatch(r"[0-9a-f]{40}", recipe_revision)):
                raise ValueError(f"invalid security advisory source revision: {t['name']}")
            note = security_advisory.get("note")
            if note is not None and (not isinstance(note, str) or not note.strip() or len(note) > 1000):
                raise ValueError(f"invalid security advisory note: {t['name']}")
        expected=t["install_kind"] in {"pkg","pip","go","cargo","npm"}
        if type(t.get("installable")) is not bool or t.get("installable") != expected: raise ValueError(f"installable flag mismatch: {t['name']}")
        if expected:
            package=t.get("package")
            package_pattern={"pkg":PKG_RE,"pip":PIP_RE,"go":GO_RE,"cargo":CARGO_RE,"npm":NPM_RE}[t["install_kind"]]
            if not isinstance(package,str) or not package_pattern.fullmatch(package):
                raise ValueError(f"unsafe package/module syntax: {t['name']}")
        elif t.get("package") is not None:
            raise ValueError(f"manual/root entries must not define an install package: {t['name']}")
    if set(data["categories"]) != categories: raise ValueError("categories list does not match catalog entries")
    return data

def load_catalog():
    data = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    if CUSTOM_PATH.exists():
        custom = json.loads(CUSTOM_PATH.read_text(encoding="utf-8"))
        if not isinstance(custom, list) or not all(isinstance(item, dict) for item in custom):
            raise ValueError("custom_tools.json must contain a list of tool objects")
        data["tools"].extend(custom)
    data["categories"] = list(dict.fromkeys(t.get("category", "") for t in data["tools"]))
    data["tool_count"] = len(data["tools"])
    return validate_catalog(data)

def save_private_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    try: temp.chmod(0o600)
    except OSError: pass
    temp.replace(path)
    try: path.chmod(0o600)
    except OSError: pass

def get_custom_tools():
    if not CUSTOM_PATH.exists(): return []
    value = json.loads(CUSTOM_PATH.read_text(encoding="utf-8"))
    if not isinstance(value, list): raise ValueError("custom_tools.json must contain a JSON list")
    return value

def get_favorites():
    if not FAVORITES_PATH.exists(): return set()
    value = json.loads(FAVORITES_PATH.read_text(encoding="utf-8"))
    if not isinstance(value, list) or not all(isinstance(x, str) for x in value):
        raise ValueError("favorites.json must contain a list of tool IDs")
    return set(value)

def toggle_favorite(tool):
    favorites = get_favorites()
    if tool["id"] in favorites:
        favorites.remove(tool["id"]); save_private_json(FAVORITES_PATH, sorted(favorites)); say("Removed from favorites.")
    else:
        favorites.add(tool["id"]); save_private_json(FAVORITES_PATH, sorted(favorites)); say("Added to favorites.")

def installed(t):
    exe=t.get("executable","")
    return bool(re.fullmatch(r"[A-Za-z0-9_.+-]+",exe) and shutil.which(exe))

def status(t):
    # PATH presence is only a discovery signal, never a successful tool self-test.
    if installed(t): return "PATH MATCH (UNVERIFIED)"
    return {"pkg":"TERMUX PKG","pip":"PYTHON/PIP","go":"GO BUILD","cargo":"CARGO BUILD","npm":"NPM PACKAGE","manual":"MANUAL","root":"ROOT/HW"}.get(t["install_kind"],"UNKNOWN")

PACKAGE_CONFIG_ENV = (
    "PYTHONPATH", "PYTHONHOME", "PYTHONSTARTUP",
    "PIP_INDEX_URL", "PIP_EXTRA_INDEX_URL", "PIP_TRUSTED_HOST", "PIP_CONFIG_FILE",
    "PIP_CERT", "PIP_CLIENT_CERT", "PIP_NO_VERIFY_CERTS",
    "GOPROXY", "GOSUMDB", "GONOSUMDB", "GOPRIVATE", "GOINSECURE", "GOFLAGS", "GOTOOLCHAIN",
    "NPM_CONFIG_REGISTRY", "NPM_CONFIG_STRICT_SSL", "npm_config_registry", "npm_config_strict_ssl",
)

def build_child_env(overrides=None):
    """Remove environment-based package-source overrides before installer subprocesses."""
    child_env=os.environ.copy()
    for key in PACKAGE_CONFIG_ENV:
        child_env.pop(key,None)
    if overrides:
        child_env.update({key:value for key,value in overrides.items() if isinstance(key,str) and isinstance(value,str)})
    return child_env


def run(command, label, timeout=900, env=None):
    if not isinstance(command,(list,tuple)) or not command or not all(isinstance(x,str) and x for x in command):
        say("Refusing invalid command arguments."); return False
    global LAST_COMMAND_RESULT
    LAST_COMMAND_RESULT = {
        "command": list(command), "label": str(label), "started_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "exit_code": None, "timed_out": False, "launch_error": None,
        "output_truncated": False, "output_bytes": 0,
    }
    logfile=LOG_DIR/(time.strftime("%Y%m%d-%H%M%S")+"-"+str(os.getpid())+".log")
    say(f"\n→ {label}\nCommand: {' '.join(command)}\nLog: {logfile}")
    child_env=build_child_env(env)
    proc=None
    total_output=0
    output_truncated=False
    try:
        with logfile.open("a",encoding="utf-8") as log:
            try: logfile.chmod(0o600)
            except OSError: pass
            proc=subprocess.Popen(list(command),stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=False,env=child_env,start_new_session=(os.name=="posix"))
            if proc.stdout is None: proc.kill(); return False
            deadline=time.monotonic()+timeout
            with selectors.DefaultSelector() as selector:
                selector.register(proc.stdout,selectors.EVENT_READ)
                while selector.get_map():
                    remaining=deadline-time.monotonic()
                    if remaining<=0: raise subprocess.TimeoutExpired(command,timeout)
                    events=selector.select(min(remaining,0.5))
                    for key,_ in events:
                        chunk=os.read(key.fd,8192)
                        if not chunk:
                            selector.unregister(key.fileobj); continue
                        remaining_bytes=max(0,MAX_COMMAND_OUTPUT_BYTES-total_output)
                        visible=chunk[:remaining_bytes]
                        if visible:
                            decoded=visible.decode("utf-8",errors="replace")
                            sys.stdout.write(decoded); sys.stdout.flush(); log.write(decoded); log.flush()
                        total_output += len(chunk)
                        if len(chunk)>remaining_bytes and not output_truncated:
                            notice="\n[output truncated after 10 MiB; remaining output is drained but not displayed or logged]\n"
                            sys.stdout.write(notice); sys.stdout.flush(); log.write(notice); log.flush(); output_truncated=True
            proc.stdout.close()
            code=proc.wait(timeout=max(0.1,deadline-time.monotonic()))
            LAST_COMMAND_RESULT.update({
                "exit_code": code, "finished_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "output_bytes": total_output, "output_truncated": output_truncated,
            })
            if code: say(f"Command exited with status {code}.")
            return code==0
    except subprocess.TimeoutExpired:
        LAST_COMMAND_RESULT.update({
            "timed_out": True, "finished_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "output_bytes": total_output, "output_truncated": output_truncated,
        })
        say(f"Timed out after {timeout}s; terminating the process.")
        try:
            if proc and proc.poll() is None:
                os.killpg(proc.pid,signal.SIGKILL) if os.name=="posix" else proc.kill()
                proc.wait(timeout=5)
            if proc and proc.stdout and not proc.stdout.closed: proc.stdout.close()
        except (OSError,subprocess.TimeoutExpired): pass
        return False
    except (OSError,ValueError) as exc:
        LAST_COMMAND_RESULT.update({
            "launch_error": str(exc), "finished_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "output_bytes": total_output, "output_truncated": output_truncated,
        })
        say(f"Could not run command: {exc}")
        return False

def bounded_probe(command, timeout=5, max_bytes=65536, include_returncode=False):
    """Run an explicit help/version probe with time/output caps; optionally return its exit code."""
    empty = ("", False, False, None) if include_returncode else ("", False, False)
    if not isinstance(command, (list, tuple)) or not command or not all(isinstance(x, str) and x for x in command):
        return empty
    proc = None
    output = bytearray()
    truncated = False
    returncode = None
    try:
        proc = subprocess.Popen(list(command), stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, start_new_session=(os.name == "posix"))
        if proc.stdout is None:
            return empty
        deadline = time.monotonic() + timeout
        with selectors.DefaultSelector() as selector:
            selector.register(proc.stdout, selectors.EVENT_READ)
            while selector.get_map():
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise subprocess.TimeoutExpired(command, timeout)
                for key, _ in selector.select(min(remaining, 0.2)):
                    chunk = os.read(key.fd, 8192)
                    if not chunk:
                        selector.unregister(key.fileobj)
                        continue
                    room = max(0, max_bytes - len(output))
                    if room:
                        output.extend(chunk[:room])
                    if len(chunk) > room:
                        truncated = True
        returncode = proc.wait(timeout=max(0.1, deadline - time.monotonic()))
        result = (output.decode("utf-8", errors="replace"), truncated, False, returncode)
        return result if include_returncode else result[:3]
    except subprocess.TimeoutExpired:
        try:
            if proc and proc.poll() is None:
                os.killpg(proc.pid, signal.SIGKILL) if os.name == "posix" else proc.kill()
                proc.wait(timeout=2)
        except (OSError, subprocess.TimeoutExpired):
            pass
        result = (output.decode("utf-8", errors="replace"), truncated, True, None)
        return result if include_returncode else result[:3]
    except OSError:
        result = (output.decode("utf-8", errors="replace"), truncated, False, None)
        return result if include_returncode else result[:3]
    finally:
        if proc and proc.stdout and not proc.stdout.closed:
            proc.stdout.close()


def show_local_docs(t):
    exe=t["executable"]; path=shutil.which(exe) if re.fullmatch(r"[A-Za-z0-9_.+-]+",exe) else None
    if not path: return
    say("\nLocal command documentation from installed executable:")
    for flags,label in ((("--version","-V"),"Version"),(("--help","-h"),"Help")):
        output=""
        for flag in flags:
            try:
                candidate,truncated,timed_out=bounded_probe([path,flag],timeout=5,max_bytes=65536)
                candidate=candidate.strip()
                if candidate or truncated or timed_out:
                    output=candidate+("\n[probe output truncated at 64 KiB]" if truncated else "")+("\n[probe timed out after 5 seconds]" if timed_out else "")
                    break
            except (OSError,subprocess.TimeoutExpired): continue
        if output:
            lines=output.splitlines(); say(label+" output:"); say("\n".join(lines[:70]))
            if len(lines)>70: say(f"... {len(lines)-70} more lines. Run {exe} --help for full output.")
        elif label=="Help": say("No standard help output found; use the upstream documentation link.")
    say("Help probing is best-effort. Inspect unfamiliar executables before running them.")

def show_tool(t,n=None):
    say("\n"+(f"{n}. " if n else "")+t["name"])
    say(f"Category: {t['category']} | Status: {status(t)}")
    say(t["description"]); say("Install method: "+t["install_kind"]+(f" ({t['package']})" if t.get("package") else ""))
    say("Compatibility: "+t["caveat"]); say("Source: "+t["source"])
    if t.get("example"): say("Example: "+t["example"])
    say("Local help/version commands are not executed automatically. Choose Help to run bounded probes.")
    say("Authorized use only: assess systems, accounts, apps, and networks you own or have explicit permission to test.")

def ask(prompt="> "):
    try: return input(prompt).strip()
    except (EOFError,KeyboardInterrupt): print(); return "0"

def menu(label,options):
    say("\n"+label)
    for i,item in enumerate(options,1): say(f" {i:>2}. {item}")
    say("  0. Back / exit")
    return ask()

def show_list(tools):
    if RICH:
        table=Table("No.","Tool","Category","Status")
        for i,t in enumerate(tools,1): table.add_row(str(i),t["name"],t["category"],status(t))
        console.print(table)
    else:
        for i,t in enumerate(tools,1): print(f"{i:3}. {t['name']:<25} {t['category']:<38} {status(t)}")

def install_pkg(t):
    if installed(t): say(f"{t['name']} already appears in PATH."); return True
    if not shutil.which("pkg"): say("pkg not found. Run inside Termux."); return False
    package=t.get("package","")
    if not PKG_RE.fullmatch(package): say("Refusing invalid Termux package name."); return False
    return run(["pkg","install","-y",package],"Installing "+t["name"],1800)

def ensure_venv():
    if (VENV_DIR/"bin"/"python").exists(): return True
    python=shutil.which("python") or shutil.which("python3") or sys.executable
    return run([python,"-m","venv",str(VENV_DIR)],"Creating isolated Python environment",300)

def install_pip(t):
    if installed(t): say(f"{t['name']} already appears in PATH."); return True
    package=t.get("package","")
    if not PIP_RE.fullmatch(package): say("Refusing invalid Python package name."); return False
    if not ensure_venv(): say("Could not create virtual environment. Install Termux's python package first."); return False
    pip=VENV_DIR/"bin"/"pip"
    if not pip.exists(): say("Virtual environment has no pip executable."); return False
    if not run([str(pip),"install","--isolated","--disable-pip-version-check","--index-url","https://pypi.org/simple",package],"Installing Python tool "+t["name"],1800): return False
    return installed(t)

def install_go(t):
    if installed(t): say(f"{t['name']} already appears in PATH."); return True
    module=t.get("package","")
    if not GO_RE.fullmatch(module): say("Refusing invalid Go module path."); return False
    go=shutil.which("go")
    if not go: say("Go missing. Install the Go runtime first."); return False
    return run([go,"install",module],"Building "+t["name"],3600,{"GOBIN":str(BIN_DIR),"GOPROXY":"https://proxy.golang.org,direct","GOSUMDB":"sum.golang.org","GONOSUMDB":"","GOPRIVATE":"","GOINSECURE":"","GOFLAGS":"","GOTOOLCHAIN":"local"})

def install_cargo(t):
    if installed(t): say(f"{t['name']} already appears in PATH."); return True
    crate=t.get("package","")
    if not CARGO_RE.fullmatch(crate): say("Refusing invalid Cargo crate name."); return False
    cargo=shutil.which("cargo")
    if not cargo: say("Cargo missing. Install Rust from Termux repositories first."); return False
    return run([cargo,"install","--locked",crate],"Building "+t["name"],3600)

def install_npm(t):
    if installed(t): say(f"{t['name']} already appears in PATH."); return True
    package=t.get("package","")
    if not NPM_RE.fullmatch(package): say("Refusing invalid npm package name."); return False
    npm=shutil.which("npm")
    if not npm: say("npm missing. Install Termux's nodejs package first."); return False
    return run([npm,"install","--global","--registry=https://registry.npmjs.org","--strict-ssl=true",package],"Installing npm tool "+t["name"],1800)

def install_one(t,confirmed=False):
    kind=t["install_kind"]
    if kind in {"manual","root"}: say("No automatic install configured. Review source and compatibility notes."); return False
    if not confirmed:
        say("Security note: package installation executes third-party code/build scripts. Verify the upstream project and package.")
        if ask("Type INSTALL to continue: ")!="INSTALL": say("Cancelled."); return False
    return {"pkg":install_pkg,"pip":install_pip,"go":install_go,"cargo":install_cargo,"npm":install_npm}[kind](t)

def append_lifecycle_event(event):
    """Append a private, timestamped lifecycle audit record."""
    path = STATE_DIR / "lifecycle_audit.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as stream:
        try:
            path.chmod(0o600)
        except OSError:
            pass
        stream.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
        stream.flush()
        os.fsync(stream.fileno())
    try:
        path.chmod(0o600)
    except OSError:
        pass


def update_one(t, confirmed=False):
    """Update one managed package with an explicit, auditable package-manager call."""
    kind, package = t.get("install_kind"), t.get("package")
    result = {
        "event_schema": 1, "operation": "update", "tool_id": t.get("id"),
        "tool_name": t.get("name"), "install_kind": kind, "requested_package": package,
        "started_at": time.strftime("%Y-%m-%d %H:%M:%S"), "status": "not_started",
        "path_match_before": installed(t), "version_before": collect_resolved_version(t),
        "command": None, "exit_code": None, "timed_out": False, "launch_error": None,
        "path_match_after": None, "version_after": None,
    }
    command, label, timeout, env = None, None, 1800, None
    if kind == "pkg" and isinstance(package, str) and PKG_RE.fullmatch(package) and shutil.which("pkg"):
        command, label = ["pkg", "upgrade", "-y", package], "Updating Termux package " + package
    elif kind == "pip" and isinstance(package, str) and PIP_RE.fullmatch(package) and (VENV_DIR / "bin" / "pip").is_file():
        command = [str(VENV_DIR / "bin" / "pip"), "install", "--upgrade", "--isolated", "--disable-pip-version-check", "--index-url", "https://pypi.org/simple", package]
        label = "Updating isolated Python package " + package
    elif kind == "cargo" and isinstance(package, str) and CARGO_RE.fullmatch(package) and shutil.which("cargo"):
        command, label, timeout = ["cargo", "install", "--locked", "--force", package], "Updating Cargo-installed package " + package, 3600
    elif kind == "npm" and isinstance(package, str) and NPM_RE.fullmatch(package) and shutil.which("npm"):
        command = ["npm", "install", "--global", "--registry=https://registry.npmjs.org", "--strict-ssl=true", package]
        label = "Updating global npm package " + package
    elif kind == "go" and isinstance(package, str) and GO_RE.fullmatch(package) and shutil.which("go"):
        command, label, timeout = ["go", "install", package], "Updating Go module " + package, 3600
        env = {"GOBIN": str(BIN_DIR), "GOPROXY": "https://proxy.golang.org,direct", "GOSUMDB": "sum.golang.org", "GONOSUMDB": "", "GOPRIVATE": "", "GOINSECURE": "", "GOFLAGS": "", "GOTOOLCHAIN": "local"}
    if not confirmed:
        say("Update requires explicit confirmation.")
        result["status"] = "cancelled_not_confirmed"
    elif command is None:
        say("Update unavailable: unsupported method, invalid package metadata, or required package manager is missing.")
        result["status"] = "unsupported_or_unavailable"
    else:
        result["command"] = command
        run(command, label, timeout, env)
        command_result = dict(LAST_COMMAND_RESULT)
        result.update({
            "exit_code": command_result.get("exit_code"),
            "timed_out": bool(command_result.get("timed_out")),
            "launch_error": command_result.get("launch_error"),
            "status": "operation_succeeded" if command_result.get("exit_code") == 0 and not command_result.get("timed_out") else "operation_failed",
        })
    result["finished_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
    result["path_match_after"] = installed(t)
    result["version_after"] = collect_resolved_version(t)
    try:
        append_lifecycle_event(result)
        say("Lifecycle audit appended to " + str(STATE_DIR / "lifecycle_audit.jsonl"))
    except OSError as exc:
        say("WARNING: could not persist lifecycle audit record: " + str(exc))
    say("Update result: " + result["status"] + ". Package-manager success does not guarantee compatibility; rollback is not automatic.")
    return result["status"] == "operation_succeeded"


def uninstall_one(t, confirmed=False):
    """Remove one package only through its matching package manager."""
    kind, package = t.get("install_kind"), t.get("package")
    result = {
        "event_schema": 1,
        "operation": "uninstall",
        "tool_id": t.get("id"),
        "tool_name": t.get("name"),
        "install_kind": kind,
        "requested_package": package,
        "started_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "status": "not_started",
        "path_match_before": installed(t),
        "version_before": collect_resolved_version(t),
        "command": None,
        "exit_code": None,
        "timed_out": False,
        "launch_error": None,
        "path_match_after": None,
        "version_after": None,
    }
    if not confirmed:
        say("Uninstall requires explicit confirmation.")
        result["status"] = "cancelled_not_confirmed"
    elif kind == "pkg" and isinstance(package, str) and PKG_RE.fullmatch(package) and shutil.which("pkg"):
        result["command"] = ["pkg", "uninstall", "-y", package]
        result["status"] = "operation_failed"
        run(result["command"], "Removing Termux package " + package, 1800)
        command_result = dict(LAST_COMMAND_RESULT)
        result.update({
            "exit_code": command_result.get("exit_code"),
            "timed_out": bool(command_result.get("timed_out")),
            "launch_error": command_result.get("launch_error"),
            "status": "operation_succeeded" if command_result.get("exit_code") == 0 and not command_result.get("timed_out") else "operation_failed",
        })
    elif kind == "pip" and isinstance(package, str) and PIP_RE.fullmatch(package) and (VENV_DIR / "bin" / "pip").is_file():
        result["command"] = [str(VENV_DIR / "bin" / "pip"), "uninstall", "--isolated", "-y", package]
        result["status"] = "operation_failed"
        run(result["command"], "Removing isolated Python package " + package, 900)
        command_result = dict(LAST_COMMAND_RESULT)
        result.update({
            "exit_code": command_result.get("exit_code"),
            "timed_out": bool(command_result.get("timed_out")),
            "launch_error": command_result.get("launch_error"),
            "status": "operation_succeeded" if command_result.get("exit_code") == 0 and not command_result.get("timed_out") else "operation_failed",
        })
    elif kind == "cargo" and isinstance(package, str) and CARGO_RE.fullmatch(package) and shutil.which("cargo"):
        result["command"] = ["cargo", "uninstall", package]
        result["status"] = "operation_failed"
        run(result["command"], "Removing Cargo-installed package " + package, 900)
        command_result = dict(LAST_COMMAND_RESULT)
        result.update({
            "exit_code": command_result.get("exit_code"),
            "timed_out": bool(command_result.get("timed_out")),
            "launch_error": command_result.get("launch_error"),
            "status": "operation_succeeded" if command_result.get("exit_code") == 0 and not command_result.get("timed_out") else "operation_failed",
        })
    elif kind == "npm" and isinstance(package, str) and NPM_RE.fullmatch(package) and shutil.which("npm"):
        result["command"] = ["npm", "uninstall", "--global", "--registry=https://registry.npmjs.org", "--strict-ssl=true", package]
        result["status"] = "operation_failed"
        run(result["command"], "Removing global npm package " + package, 900)
        command_result = dict(LAST_COMMAND_RESULT)
        result.update({
            "exit_code": command_result.get("exit_code"),
            "timed_out": bool(command_result.get("timed_out")),
            "launch_error": command_result.get("launch_error"),
            "status": "operation_succeeded" if command_result.get("exit_code") == 0 and not command_result.get("timed_out") else "operation_failed",
        })
    elif kind in {"manual", "root", "go"}:
        say("Automatic uninstall is not supported for this entry; no command was run.")
        result["status"] = "unsupported"
    else:
        say("Uninstall unavailable: invalid package metadata or required package manager is missing.")
        result["status"] = "unavailable_or_invalid"
    result["finished_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
    result["path_match_after"] = installed(t)
    result["version_after"] = collect_resolved_version(t)
    try:
        append_lifecycle_event(result)
        say("Lifecycle audit appended to " + str(STATE_DIR / "lifecycle_audit.jsonl"))
    except OSError as exc:
        say("WARNING: could not persist lifecycle audit record: " + str(exc))
    say("Uninstall result: " + result["status"] + ". A successful package-manager exit is not a functional verification.")
    return result["status"] == "operation_succeeded"

def choose(data,tools=None):
    tools=tools or data["tools"]; show_list(tools)
    value=ask("Tool number: ")
    if not value.isdigit() or int(value)==0: return
    i=int(value)-1
    if i<0 or i>=len(tools): say("Invalid number."); return
    t=tools[i]; show_tool(t); action=ask("[i]nstall / [v]ersion-update / [u]ninstall / [h]elp / [f]avorite / [b]ack: ").lower()
    if action=="i": install_one(t)
    elif action=="v":
        kind, package = t.get("install_kind"), t.get("package")
        if kind not in {"pkg", "pip", "go", "cargo", "npm"} or not isinstance(package, str):
            say("Automatic update is not supported for this tool; no command was run.")
            return
        say("Package manager: " + kind + " | Exact package/module spec: " + package)
        say("Updates may change behavior or dependencies. SYN_LAUNCH does not guarantee rollback.")
        if ask("Type UPDATE " + package + " to confirm: ") == "UPDATE " + package:
            update_one(t, confirmed=True)
        else:
            say("Cancelled. No update command was run.")
    elif action=="u":
        kind, package = t.get("install_kind"), t.get("package")
        if kind not in {"pkg", "pip", "cargo", "npm"} or not isinstance(package, str):
            say("Automatic uninstall is not supported for this tool; no command was run.")
            return
        say("This removes the package named below, not just its launcher. Termux may remove dependencies too.")
        say("Package manager: " + kind + " | Exact package: " + package)
        if ask("Type REMOVE " + package + " to confirm: ") == "REMOVE " + package:
            uninstall_one(t, confirmed=True)
        else:
            say("Cancelled. No uninstall command was run.")
    elif action=="h":
        if installed(t): show_local_docs(t)
        else: say("Executable is not detected in PATH. Review the upstream documentation link and example.")
        say("Use examples only with authorized test values.")
    elif action=="f": toggle_favorite(t)

def category(data,selected=None):
    if selected:
        choose(data,[t for t in data["tools"] if t["category"].lower()==selected.lower()]); return
    cats=data["categories"]; value=menu("Browse categories",cats)
    if value.isdigit() and 1<=int(value)<=len(cats): choose(data,[t for t in data["tools"] if t["category"]==cats[int(value)-1]])

def search(data,query=None):
    q=(query if query is not None else ask("Search name/category/description: ")).lower().strip()
    matches=[t for t in data["tools"] if q and any(q in t.get(k,"").lower() for k in ("name","category","description","caveat"))]
    if matches: choose(data,matches)
    else: say("No matches.")

def requested_package_evidence(tool):
    """Describe the catalog package spec without implying resolution."""
    kind = tool.get("install_kind")
    package = tool.get("package")
    result = {
        "requested_package": package,
        "requested_version": None,
        "version_specification": "unpinned" if package else "not_applicable",
        "resolved_version": None,
        "version_evidence": "not_collected",
    }
    if kind == "go" and isinstance(package, str) and "@" in package:
        module, version = package.rsplit("@", 1)
        result["requested_package"] = module
        result["requested_version"] = version
        result["version_specification"] = "floating_latest" if version == "latest" else "requested_version"
    return result


def reconcile_requested_version(tool, version_result):
    """Compare versions only when the catalog carries an explicit, non-floating request."""
    request = requested_package_evidence(tool)
    requested = request.get("requested_version")
    resolved = version_result.get("resolved_version")
    if request.get("version_specification") == "floating_latest":
        status, basis = "floating_request", "floating_specification"
    elif not requested:
        status, basis = ("unresolved" if not resolved else "not_comparable_unpinned"), "no_exact_requested_version"
    elif not resolved:
        status, basis = "requested_version_unresolved", "exact_string"
    elif requested == resolved:
        status, basis = "exact_match", "exact_string"
    else:
        status, basis = "mismatch", "exact_string"
    return {
        "status": status,
        "requested_version": requested,
        "resolved_version": resolved,
        "comparison_basis": basis,
    }


def collect_resolved_version(tool):
    """Read installed-version metadata from trusted package managers only."""
    kind, package = tool.get("install_kind"), tool.get("package")
    result = {
        "resolved_version": None,
        "version_evidence": "not_supported",
        "version_query_exit_code": None,
    }
    if kind == "pkg" and isinstance(package, str) and PKG_RE.fullmatch(package):
        manager = shutil.which("dpkg-query")
        if not manager:
            result["version_evidence"] = "query_unavailable"
            return result
        command = [manager, "-W", "-f=" + "{Version}", package]
    elif kind == "pip" and isinstance(package, str) and PIP_RE.fullmatch(package):
        manager = VENV_DIR / "bin" / "python"
        if not manager.is_file():
            result["version_evidence"] = "query_unavailable"
            return result
        # Static Python code reads installed metadata and prints only the version.
        command = [
            str(manager), "-c",
            "import importlib.metadata, sys; print(importlib.metadata.version(sys.argv[1]))",
            package,
        ]
    elif kind == "cargo" and isinstance(package, str) and CARGO_RE.fullmatch(package):
        cargo_home = Path(os.environ.get("CARGO_HOME", str(Path.home() / ".cargo"))).expanduser()
        metadata_path = cargo_home / ".crates2.json"
        if not metadata_path.is_file():
            result["version_evidence"] = "query_unavailable"
            return result
        try:
            if metadata_path.stat().st_size > 2 * 1024 * 1024:
                result["version_evidence"] = "metadata_too_large"
                return result
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            installs = metadata.get("installs", {})
            versions = sorted({entry.get("version") for entry in installs.values()
                               if isinstance(entry, dict) and entry.get("crate") == package
                               and isinstance(entry.get("version"), str) and entry.get("version")})
        except (OSError, ValueError, AttributeError):
            result["version_evidence"] = "query_failed"
            return result
        if len(versions) == 1:
            result.update({"resolved_version": versions[0], "version_evidence": "package_manager_metadata"})
        elif len(versions) > 1:
            result["version_evidence"] = "multiple_versions"
        else:
            result["version_evidence"] = "not_found"
        return result
    elif kind == "npm" and isinstance(package, str) and NPM_RE.fullmatch(package):
        npm = shutil.which("npm")
        if not npm:
            result["version_evidence"] = "query_unavailable"
            return result
        output, truncated, timed_out = bounded_probe(
            [npm, "root", "--global"], timeout=5, max_bytes=4096
        )
        if truncated or timed_out or not output.strip():
            result["version_evidence"] = "query_failed"
            return result
        root = Path(output.strip()).resolve()
        package_dir = (root / package).resolve()
        try:
            package_dir.relative_to(root)
        except ValueError:
            result["version_evidence"] = "invalid_package_path"
            return result
        if package_dir == root or not package_dir.is_dir():
            result["version_evidence"] = "invalid_package_path"
            return result
        metadata_path = package_dir / "package.json"
        if not metadata_path.is_file():
            result["version_evidence"] = "not_found"
            return result
        try:
            if metadata_path.stat().st_size > 1024 * 1024:
                result["version_evidence"] = "metadata_too_large"
                return result
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            result["version_evidence"] = "query_failed"
            return result
        version = metadata.get("version") if isinstance(metadata, dict) else None
        if isinstance(version, str) and version.strip():
            result.update({"resolved_version": version.strip(), "version_evidence": "package_manager_metadata"})
        else:
            result["version_evidence"] = "metadata_missing"
        return result
    elif kind == "go" and isinstance(package, str) and GO_RE.fullmatch(package):
        go, executable = shutil.which("go"), shutil.which(tool.get("executable", ""))
        if not go or not executable:
            result["version_evidence"] = "query_unavailable"
            return result
        requested_module = package.rsplit("@", 1)[0]
        output, truncated, timed_out = bounded_probe(
            [go, "version", "-m", executable], timeout=5, max_bytes=65536
        )
        if truncated or timed_out:
            result["version_evidence"] = "query_failed"
            return result
        for line in output.splitlines():
            parts = line.strip().split()
            if len(parts) >= 3 and parts[0] == "mod" and parts[1] == requested_module:
                result.update({"resolved_version": parts[2], "version_evidence": "package_manager_metadata"})
                return result
        result["version_evidence"] = "metadata_missing"
        return result
    else:
        return result
    try:
        completed = subprocess.run(
            command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL, text=True, timeout=5, check=False,
            env=build_child_env(),
        )
    except (OSError, subprocess.TimeoutExpired):
        result["version_evidence"] = "query_failed"
        return result
    result["version_query_exit_code"] = completed.returncode
    if completed.returncode != 0:
        result["version_evidence"] = "not_found" if completed.returncode == 1 else "query_failed"
        return result
    version = completed.stdout.strip()
    if version:
        result.update({"resolved_version": version, "version_evidence": "package_manager_metadata"})
    else:
        result["version_evidence"] = "metadata_missing"
    return result



PHP_VERSION_PATTERN = re.compile(r"^(?:[0-9]+:)?([0-9]+)\.([0-9]+)\.([0-9]+)(?:[-+~].*)?$")


def assess_php_security_version(version_result, advisory):
    """Assess package-manager version metadata against a pinned PHP security advisory."""
    version = version_result.get("resolved_version")
    evidence = version_result.get("version_evidence", "unknown")
    fixed = advisory.get("fixed_versions", {}) if isinstance(advisory, dict) else {}
    report = {
        "advisory_date": advisory.get("published_on") if isinstance(advisory, dict) else None,
        "severity": advisory.get("severity", "unknown") if isinstance(advisory, dict) else "unknown",
        "cves": advisory.get("cves", []) if isinstance(advisory, dict) else [],
        "installed_package_version": version,
        "version_evidence": evidence,
        "fixed_versions": fixed,
        "status": "unknown",
        "checks": {
            "network_requests_made": False,
            "php_executable_run": False,
            "package_changed": False,
            "web_runtime_verified": False,
        },
        "limitations": [
            "This checks Termux dpkg package metadata only; it does not execute PHP or change packages.",
            "The CLI PHP package may differ from the runtime used by PHP-FPM, Apache, CGI, containers, or another web server.",
            "A vendor may backport fixes to an older version string; verify the vendor advisory before treating an older version as vulnerable or fixed.",
        ],
    }
    if not version:
        report["status"] = "not_installed" if evidence == "not_found" else "version_unavailable"
        return report
    match = PHP_VERSION_PATTERN.fullmatch(version.strip())
    if not match:
        report["status"] = "version_unparseable"
        return report
    major, minor, patch = (int(part) for part in match.groups())
    branch = f"{major}.{minor}"
    fixed_version = fixed.get(branch)
    report["parsed_version"] = {"major": major, "minor": minor, "patch": patch}
    report["branch_fixed_version"] = fixed_version
    if isinstance(fixed_version, str):
        fixed_match = re.fullmatch(r"([0-9]+)\.([0-9]+)\.([0-9]+)", fixed_version)
        if not fixed_match:
            report["status"] = "advisory_metadata_invalid"
            return report
        fixed_parts = tuple(int(part) for part in fixed_match.groups())
        report["status"] = "fixed_release_or_newer" if (major, minor, patch) >= fixed_parts else "update_required"
    elif major == 8 and minor < 2:
        report["status"] = "vendor_backport_or_upgrade_required"
    else:
        report["status"] = "release_line_not_assessed"
    return report


def php_security_report(data):
    php_tool = next((tool for tool in data.get("tools", []) if tool.get("id") == "php"), None)
    if not php_tool:
        return {"status": "catalog_entry_missing", "checks": {"network_requests_made": False, "package_changed": False}}
    advisory = php_tool.get("security_advisory", {})
    version_result = collect_resolved_version(php_tool)
    report = assess_php_security_version(version_result, advisory)
    report["tool_id"] = "php"
    report["source"] = "local Termux package-manager metadata"
    report["advisory_url"] = advisory.get("upstream_advisory")
    return report


def progress(items,worker,label,confirmed=False):
    if not items: say("No items to install."); return
    good=0; failed=[]; results=[]
    def attempt(t):
        global LAST_COMMAND_RESULT
        LAST_COMMAND_RESULT = {"command": None, "label": None, "exit_code": None, "timed_out": False, "launch_error": None}
        ok = worker(t,confirmed=confirmed) if worker is install_one else worker(t)
        return ok, dict(LAST_COMMAND_RESULT)
    def record(t,ok,path_before,path_after,command_result):
        if path_before:
            state="already_path_matched_unverified"
        elif path_after:
            state="path_match_unverified_after_attempt"
        elif ok:
            state="operation_succeeded_executable_not_detected"
        else:
            state="operation_failed_or_unavailable"
        # Query package-manager metadata even after an unsuccessful operation: the
        # package may already be installed, or an install may have partially succeeded.
        version_result = collect_resolved_version(t)
        version_reconciliation = reconcile_requested_version(t, version_result)
        post_check = {
            "check_type": "metadata_only",
            "executable_detected": bool(path_after),
            "package_version_detected": bool(version_result.get("resolved_version")),
            "status": (
                "metadata_and_executable_present" if path_after and version_result.get("resolved_version")
                else "executable_path_match_only" if path_after
                else "package_metadata_only" if version_result.get("resolved_version")
                else "no_evidence"
            ) if t.get("install_kind") in {"pkg", "pip", "go", "cargo", "npm"} else "not_applicable",
        }
        results.append({
            "id":t["id"], "name":t["name"], "install_kind":t["install_kind"],
            "package":t.get("package"), **requested_package_evidence(t), **version_result,
            "version_reconciliation": version_reconciliation,
            "post_install_check": post_check,
            "operation_returned_success":bool(ok),
            "path_match_before_attempt":bool(path_before),
            "path_match_after_attempt":bool(path_after),
            "result_state":state, "verification":"not_run",
            "installer_command": command_result.get("command"),
            "installer_label": command_result.get("label"),
            "installer_exit_code": command_result.get("exit_code"),
            "installer_timed_out": bool(command_result.get("timed_out")),
            "installer_launch_error": command_result.get("launch_error"),
            "installer_output_bytes": command_result.get("output_bytes", 0),
            "installer_output_truncated": bool(command_result.get("output_truncated", False)),
            "installer_started_at": command_result.get("started_at"),
            "installer_finished_at": command_result.get("finished_at"),
        })
    if RICH:
        with Progress(SpinnerColumn(),TextColumn("[progress.description]{task.description}"),BarColumn(),TextColumn("{task.completed}/{task.total}"),TimeElapsedColumn(),console=console,transient=False) as bar:
            task=bar.add_task(label,total=len(items))
            for t in items:
                bar.update(task,description=label+": "+t["name"])
                path_before=installed(t); ok,command_result=attempt(t); path_after=installed(t)
                good+=int(bool(ok))
                if not ok: failed.append(t["name"])
                record(t,ok,path_before,path_after,command_result); bar.advance(task)
    else:
        for i,t in enumerate(items,1):
            print(f"\n[{i}/{len(items)}] {label}: {t['name']}")
            path_before=installed(t); ok,command_result=attempt(t); path_after=installed(t)
            good+=int(bool(ok))
            if not ok: failed.append(t["name"])
            record(t,ok,path_before,path_after,command_result)
    summary={
        "summary_schema":2, "succeeded":good, "failed":failed, "total":len(items),
        "operation_success_count":good, "operation_failure_count":len(failed),
        "path_match_after_attempt_count":sum(1 for result in results if result["path_match_after_attempt"]),
        "verified_tools":0, "results":results,
        "timestamp":time.strftime("%Y-%m-%d %H:%M:%S"),
        "note":"succeeded records the install/build operation's return value or an existing PATH match; it does not prove the tool works. Exit codes refer to the captured installer subprocess; pre-existing PATH matches and validation failures have no subprocess exit code. PATH matches remain unverified, and no functional verification was run.",
    }
    p=STATE_DIR/"last_install_summary.json"; save_private_json(p,summary)
    say(f"Finished: {good}/{len(items)} operations returned success. This is not a count of functionally verified tools.")
    if failed: say("Failed/unavailable: "+", ".join(failed))

def add_custom_tool(data):
    say("Add a personal catalog entry. This saves metadata only; it does not install the tool.")
    name=ask("Tool display name: ")
    if not name: say("Name is required."); return
    slug=re.sub(r"[^a-z0-9]+","-",name.lower()).strip("-")
    if not slug or any(t["id"]==slug for t in data["tools"]):
        say("Could not make a unique ID from that name. Choose a different display name."); return
    category_name=ask("Category [Custom Tools]: ") or "Custom Tools"
    executable=ask("Executable/command name (one token): ")
    if not EXECUTABLE_RE.fullmatch(executable):
        say("Executable must be a single command name without spaces or shell syntax."); return
    kinds=["pkg","pip","go","cargo","npm","manual","root"]
    choice=menu("Install method",kinds)
    if not choice.isdigit() or not 1<=int(choice)<=len(kinds): return
    kind=kinds[int(choice)-1]
    package=None
    if kind in {"pkg","pip","go","cargo","npm"}:
        package=ask("Exact package/module name: ")
    description=ask("Purpose/description: ")
    source=ask("HTTPS upstream URL: ")
    example=ask("Example/help command (display only, never auto-executed): ")
    caveat=ask("Termux compatibility/safety caveat: ")
    tool={"id":slug,"name":name,"category":category_name,"executable":executable,"install_kind":kind,"package":package,"installable":kind in {"pkg","pip","go","cargo","npm"},"description":description,"example":example,"source":source,"caveat":caveat}
    custom=get_custom_tools()
    candidate=json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    candidate["tools"].extend(custom+[tool])
    candidate["categories"]=list(dict.fromkeys(t.get("category","") for t in candidate["tools"]))
    candidate["tool_count"]=len(candidate["tools"])
    try: validate_catalog(candidate)
    except (ValueError,TypeError) as exc:
        say("Entry rejected: "+str(exc)); return
    custom.append(tool)
    save_private_json(CUSTOM_PATH,custom)
    data["tools"].append(tool)
    data["categories"]=list(dict.fromkeys(t["category"] for t in data["tools"]))
    data["tool_count"]=len(data["tools"])
    say("Custom entry saved. It will appear in search and category menus next time too.")

def browse_favorites(data):
    ids=get_favorites()
    matches=[t for t in data["tools"] if t["id"] in ids]
    if not matches: say("No favorites yet. Select a tool and choose [f]avorite."); return
    choose(data,matches)

def list_custom_tools(data):
    ids={t["id"] for t in get_custom_tools()}
    matches=[t for t in data["tools"] if t["id"] in ids]
    if matches: choose(data,matches)
    else: say("No custom entries yet.")

def remove_custom_tool(data):
    custom=get_custom_tools()
    if not custom: say("No custom entries to remove."); return
    show_list(custom)
    value=ask("Custom tool number to remove: ")
    if not value.isdigit() or int(value)<1 or int(value)>len(custom): return
    tool=custom[int(value)-1]
    if ask(f"Type DELETE to remove {tool['name']}: ")!="DELETE": say("Cancelled."); return
    custom=[t for t in custom if t["id"]!=tool["id"]]
    save_private_json(CUSTOM_PATH,custom)
    data["tools"]=[t for t in data["tools"] if t["id"]!=tool["id"]]
    data["categories"]=list(dict.fromkeys(t["category"] for t in data["tools"]))
    data["tool_count"]=len(data["tools"])
    favorites=get_favorites(); favorites.discard(tool["id"]); save_private_json(FAVORITES_PATH,sorted(favorites))
    say("Custom entry removed. This does not uninstall its software.")

def manage_custom_tools(data):
    choice=menu("Custom tools and favorites",["Add a custom tool entry","Browse favorites","Browse custom entries","Remove a custom entry"])
    if choice=="1": add_custom_tool(data)
    elif choice=="2": browse_favorites(data)
    elif choice=="3": list_custom_tools(data)
    elif choice=="4": remove_custom_tool(data)


PREFLIGHT_MIN_FREE_BYTES = {
    "termux_packages": 2 * 1024**3,
    "third_party_builds": 1 * 1024**3,
    "runtime_prerequisites": 512 * 1024**2,
}


def build_install_preflight(items, mode, free_bytes, available_commands):
    """Describe bulk-install prerequisites without running installers or catalog tools."""
    if mode not in PREFLIGHT_MIN_FREE_BYTES:
        raise ValueError("unknown install preflight mode")
    commands = set(available_commands)
    kinds = {tool.get("install_kind") for tool in items}
    required = {}
    if kinds.intersection({"pkg"}):
        required["pkg"] = sum(1 for tool in items if tool.get("install_kind") == "pkg")
    for kind, command in (("pip", "python"), ("go", "go"), ("cargo", "cargo"), ("npm", "npm")):
        count = sum(1 for tool in items if tool.get("install_kind") == kind)
        if count:
            required[command] = count
    missing = [{"command": command, "affected_tool_count": count}
               for command, count in sorted(required.items())
               if command not in commands and not (command == "python" and "python3" in commands)]
    threshold = PREFLIGHT_MIN_FREE_BYTES[mode]
    warnings = []
    if free_bytes is None:
        warnings.append("Free storage could not be measured; package/build storage needs are unknown.")
    elif free_bytes < threshold:
        warnings.append(
            f"Free storage is below the {threshold}-byte advisory threshold for {mode.replace('_', ' ')}."
        )
    if missing:
        warnings.append("One or more required package managers or runtimes are missing; affected attempts may fail.")
    return {
        "preflight_schema": 1,
        "mode": mode,
        "tool_count": len(items),
        "distinct_package_count": len({
            (tool.get("install_kind"), tool.get("package"))
            for tool in items if tool.get("package")
        }),
        "free_bytes": free_bytes,
        "recommended_min_free_bytes": threshold,
        "required_commands": required,
        "missing_commands": missing,
        "warnings": warnings,
        "proceed": not ({"pkg"} <= {entry["command"] for entry in missing} and "pkg" in required),
        "verification": "not_run",
        "installers_executed": False,
        "note": "Preflight is advisory. Package sizes and compatibility vary; it does not install or test tools.",
    }


def run_install_preflight(items, mode):
    try:
        free_bytes = shutil.disk_usage(APP_DIR).free
    except OSError:
        free_bytes = None
    commands = {name for name in ("pkg", "python", "python3", "go", "cargo", "npm")
                if shutil.which(name)}
    report = build_install_preflight(items, mode, free_bytes, commands)
    report["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
    save_private_json(STATE_DIR / "last_preflight.json", report)
    say("\nBulk-install preflight (no installers or catalog tools executed):")
    say(f"Mode: {mode} | Selected entries: {report['tool_count']} | Distinct packages/modules: {report['distinct_package_count']}")
    say("Free storage: " + ("unknown" if free_bytes is None else f"{free_bytes:,} bytes"))
    if report["missing_commands"]:
        for entry in report["missing_commands"]:
            say(f"Missing command: {entry['command']} (affects up to {entry['affected_tool_count']} selected entries)")
    for warning in report["warnings"]:
        say("WARNING: " + warning)
    if not report["proceed"]:
        say("Preflight cannot continue: Termux pkg is unavailable.")
        return False
    if report["warnings"] and ask("Type CONTINUE to proceed despite preflight warnings: ") != "CONTINUE":
        say("Cancelled before installation.")
        return False
    return True


def installer(data):
    choice=menu("Installer",["Attempt all distinct Termux packages","Install, update, or remove one selected tool","Install Python, Go, Rust and Node.js runtimes","Attempt all Python/Go/Cargo/npm tools (large download/build)","Show last install summary","Show recent lifecycle audit"])
    if choice=="1":
        packages={}
        for t in data["tools"]:
            if t["install_kind"]=="pkg" and t.get("package"): packages.setdefault(t["package"],t)
        items=list(packages.values())
        say(f"Attempts {len(packages)} distinct packages; availability varies by Termux repo and architecture.")
        if ask("Type YES to continue: ")!="YES": return
        if not run_install_preflight(items, "termux_packages"): return
        run(["pkg","update","-y"],"Refreshing package indexes",1200)
        progress(items,install_pkg,"Termux packages")
        say("Progress measures completed attempts, not download-byte percentage.")
    elif choice=="2": choose(data)
    elif choice=="3":
        names={"Python","Go","Rust","Node.js"}
        items=[t for t in data["tools"] if t["name"] in names and t["install_kind"]=="pkg"]
        if run_install_preflight(items, "runtime_prerequisites"):
            progress(items,install_pkg,"Toolchain prerequisites")
    elif choice=="4":
        items=[t for t in data["tools"] if t["install_kind"] in {"pip","go","cargo","npm"}]
        say(f"Attempts {len(items)} third-party installs/builds. Expect large downloads and Android dependency failures.")
        if ask("Type YES to continue: ")!="YES": return
        names={"Python","Go","Rust","Node.js"}
        runtimes=[t for t in data["tools"] if t["name"] in names and t["install_kind"]=="pkg"]
        if not run_install_preflight(runtimes, "runtime_prerequisites"):
            return
        progress(runtimes,install_pkg,"Installing runtimes")
        if run_install_preflight(items, "third_party_builds"):
            progress(items,install_one,"Security tool installs",confirmed=True)
    elif choice=="5":
        p=STATE_DIR/"last_install_summary.json"; say(p.read_text(encoding="utf-8") if p.exists() else "No install summary yet.")
    elif choice=="6":
        p=STATE_DIR/"lifecycle_audit.jsonl"
        if not p.exists():
            say("No lifecycle audit records yet.")
        else:
            try:
                lines = p.read_text(encoding="utf-8").splitlines()
                say("\\n".join(lines[-20:]) if lines else "Lifecycle audit is empty.")
            except OSError as exc:
                say("Could not read lifecycle audit: " + str(exc))

def load_toolset(name, data):
    """Load and validate a curated toolset against the authoritative catalog."""
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        raise ValueError("toolset name must be a lowercase slug")
    path = APP_DIR / "toolsets" / (name + ".json")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"unknown toolset: {name}") from exc
    if not isinstance(payload, dict) or payload.get("id") != name or payload.get("schema_version") != 1:
        raise ValueError("invalid toolset identity or schema version")
    groups = payload.get("groups")
    if not isinstance(groups, list) or not groups:
        raise ValueError("toolset groups must be a non-empty list")
    catalog = {tool["id"]: tool for tool in data["tools"]}
    ids = []
    for group in groups:
        if not isinstance(group, dict) or not isinstance(group.get("title"), str) or not group["title"].strip():
            raise ValueError("toolset group requires a title")
        tool_ids = group.get("tool_ids")
        if not isinstance(tool_ids, list) or not tool_ids or any(not isinstance(item, str) for item in tool_ids):
            raise ValueError("toolset group tool_ids must be a non-empty string list")
        ids.extend(tool_ids)
    if len(ids) != len(set(ids)):
        raise ValueError("toolset contains duplicate tool IDs")
    missing = sorted(set(ids) - set(catalog))
    if missing:
        raise ValueError("toolset references unknown catalog IDs: " + ", ".join(missing))
    if type(payload.get("tool_count")) is not int or payload["tool_count"] != len(ids):
        raise ValueError("toolset tool_count does not match group membership")
    payload["groups"] = [dict(group, tools=[catalog[item] for item in group["tool_ids"]]) for group in groups]
    payload["tools"] = [catalog[item] for item in ids]
    return payload


def browse_curated_toolsets(data):
    """Interactive browser for catalog-backed curated toolsets."""
    directory = APP_DIR / "toolsets"
    names = sorted(path.stem for path in directory.glob("*.json") if path.is_file())
    if not names:
        say("No curated toolsets are available.")
        return
    labels = []
    for name in names:
        try:
            payload = load_toolset(name, data)
            labels.append(f"{payload['title']} ({payload['tool_count']} tools)")
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            labels.append(f"{name} [invalid: {exc}]")
    selected = menu("Curated toolsets", labels)
    if not selected.isdigit() or not 1 <= int(selected) <= len(names):
        return
    name = names[int(selected) - 1]
    try:
        toolset = load_toolset(name, data)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        say("Could not load curated toolset: " + str(exc))
        return
    say("\n" + toolset["title"])
    say(toolset.get("description", ""))
    say(f"Tools: {toolset['tool_count']} | Groups: {len(toolset['groups'])}")
    say(toolset.get("safety_scope", "Use only tools and targets you are authorized to assess."))
    while True:
        group_names = [f"{group['title']} ({len(group['tools'])})" for group in toolset["groups"]]
        choice = menu("Toolset groups", group_names + ["Show all tools in this toolset"])
        if not choice.isdigit() or int(choice) == 0:
            return
        index = int(choice) - 1
        if index < len(toolset["groups"]):
            choose(data, toolset["groups"][index]["tools"])
        elif index == len(toolset["groups"]):
            choose(data, toolset["tools"])
        else:
            say("Invalid choice.")


def print_toolset(name, data):
    """Emit machine-readable toolset metadata and current PATH/installability signals."""
    try:
        toolset = load_toolset(name, data)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print("Toolset error: " + str(exc), file=sys.stderr)
        return 2
    groups = []
    for group in toolset["groups"]:
        groups.append({"title": group["title"], "tools": [{
            "id": t["id"], "name": t["name"], "category": t["category"],
            "install_kind": t["install_kind"], "installable": t["installable"],
            "present_in_path": bool(installed(t)), "description": t["description"],
            "source": t["source"], "caveat": t["caveat"]
        } for t in group["tools"]]})
    print(json.dumps({"schema_version": 1, "id": toolset["id"], "title": toolset["title"],
        "tool_count": toolset["tool_count"], "reviewed_on": toolset["reviewed_on"],
        "description": toolset["description"], "selection_policy": toolset["selection_policy"],
        "safety_scope": toolset["safety_scope"], "groups": groups,
        "summary": {"catalog_entries_reused": len(toolset["tools"]),
            "present_in_path": sum(bool(installed(t)) for t in toolset["tools"]),
            "installable_by_declared_method": sum(bool(t["installable"]) for t in toolset["tools"]),
            "manual_or_root_only": sum(not bool(t["installable"]) for t in toolset["tools"])},
        "note": "PATH presence is not a functional test. Installability metadata is not proof of Termux compatibility. No tools were installed or executed by this command."}, indent=2, ensure_ascii=False))
    return 0


def normalized_architecture(machine=None):
    """Normalize common Android/Linux machine names without certifying ABI support."""
    machine = (machine or platform.machine() or "unknown").lower()
    aliases = {
        "aarch64": "arm64", "arm64": "arm64", "arm64-v8a": "arm64",
        "armv7l": "armv7", "armv7": "armv7",
        "i686": "x86", "i386": "x86", "x86_64": "x86_64", "amd64": "x86_64",
    }
    return aliases.get(machine, machine)


def environment_profile(data):
    """Report runtime signals only; do not infer individual tool compatibility."""
    prefix = os.environ.get("PREFIX", "")
    termux_root = Path("/data/data/com.termux/files/usr")
    android_markers = bool(os.environ.get("ANDROID_ROOT") or os.environ.get("ANDROID_DATA") or termux_root.exists())
    is_termux = bool(prefix.startswith("/data/data/com.termux/") or termux_root.exists() or shutil.which("termux-info"))
    try:
        disk = shutil.disk_usage(APP_DIR)
        free_bytes, total_bytes = disk.free, disk.total
    except OSError:
        free_bytes = total_bytes = None
    try:
        process_uid_is_zero = os.geteuid() == 0
    except AttributeError:
        process_uid_is_zero = False
    install_counts = {}
    for tool in data["tools"]:
        kind = tool["install_kind"]
        install_counts[kind] = install_counts.get(kind, 0) + 1
    runtimes = {cmd: shutil.which(cmd) for cmd in ("pkg", "apt", "python", "python3", "pip", "go", "cargo", "rustc", "npm", "node", "git", "proot", "docker", "adb")}
    return {
        "application": "SYN_LAUNCH", "profile_schema": 1,
        "os": platform.system(), "os_release": platform.release(),
        "machine_raw": platform.machine() or "unknown",
        "architecture_family": normalized_architecture(),
        "python": platform.python_version(),
        "android_markers_detected": android_markers, "termux_detected": is_termux,
        "termux_prefix": prefix or None, "process_uid_is_zero": process_uid_is_zero,
        "root_note": "UID 0 inside a container/proot does not prove Android host root access.",
        "storage_free_bytes": free_bytes, "storage_total_bytes": total_bytes,
        "runtimes": runtimes, "catalog_entries": len(data["tools"]),
        "catalog_categories": len(data["categories"]),
        "path_match_tool_entries": sum(1 for tool in data["tools"] if installed(tool)),
        "unique_path_match_executables": len({tool["executable"] for tool in data["tools"] if installed(tool)}),
        "install_method_counts": dict(sorted(install_counts.items())),
        "compatibility_note": "Catalog presence and architecture detection are not proof that a tool installs or runs; verify each tool on this device.",
    }


def smoke_evidence_path():
    return STATE_DIR / "smoke_tests.json"


def executable_identity(path):
    """Return lightweight file identity so a replaced binary cannot inherit an old passing probe."""
    if not path:
        return None
    try:
        info = os.stat(path)
        return {"size_bytes": info.st_size, "mtime_ns": info.st_mtime_ns}
    except OSError:
        return None


def load_smoke_evidence():
    """Load private, locally recorded bounded-probe evidence without treating it as device certification."""
    try:
        value = json.loads(smoke_evidence_path().read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    if not isinstance(value, dict):
        return {}
    return {key: item for key, item in value.items()
            if isinstance(key, str) and isinstance(item, dict)
            and item.get("status") in {"passed", "output_observed_nonzero", "timed_out", "no_response", "not_detected"}}


def smoke_test_tool(tool):
    """Run bounded tool-specific help/version probes for one explicitly selected catalog entry."""
    executable = tool.get("executable", "")
    path = shutil.which(executable) if re.fullmatch(r"[A-Za-z0-9_.+-]{1,128}", executable) else None
    record = {
        "tool_id": tool["id"], "tool_name": tool["name"],
        "status": "not_detected", "path": path, "binary_identity": executable_identity(path),
        "probe": None, "exit_code": None, "output_observed": False, "output_bytes": 0,
        "output_truncated": False, "timed_out": False, "attempts": [],
        "tested_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "scope": "Bounded help/version response only; not a functional test of tool features or device compatibility."
    }
    if path:
        attempts = []
        # Keep probe arguments tool-specific where standard flags differ.
        probe_flags = {
            "ssh": ("-V", "--help", "-h"),
            "ip": ("-V", "--help", "-h"),
            "ssh-keygen": ("--help", "-h", "--version"),
            "ssh-keyscan": ("-h", "--help", "--version"),
            "whois": ("--help", "--version", "-h"),
            # `dig --version` may be parsed as a query name; `-v` is local-only.
            "dig": ("-v",),
        }.get(executable, ("--version", "--help", "-h"))
        for flag in probe_flags:
            output, truncated, timed_out, returncode = bounded_probe(
                [path, flag], timeout=5, max_bytes=65536, include_returncode=True
            )
            attempt = {
                "probe": flag, "exit_code": returncode, "output_observed": bool(output.strip()),
                "output_bytes": len(output.encode("utf-8")), "output_truncated": truncated,
                "timed_out": timed_out
            }
            expected_usage_exit = (
                executable in {"ssh-keygen", "ssh-keyscan", "whois"}
                and returncode == 1
                and bool(re.search(r"\busage:", output, re.IGNORECASE))
            )
            attempt["expected_usage_exit"] = expected_usage_exit
            attempts.append(attempt)
            if output.strip() and (returncode == 0 or expected_usage_exit) and not timed_out:
                record.update(attempt)
                record["status"] = "passed"
                break
        else:
            with_output = next((item for item in attempts if item["output_observed"]), None)
            timed = next((item for item in attempts if item["timed_out"]), None)
            representative = with_output or timed
            if representative:
                record.update(representative)
                record["status"] = "output_observed_nonzero" if with_output else "timed_out"
            else:
                record["status"] = "no_response"
        record["attempts"] = attempts
    evidence = load_smoke_evidence()
    evidence[tool["id"]] = record
    save_private_json(smoke_evidence_path(), evidence)
    return record



def functional_evidence_path():
    return STATE_DIR / "functional_checks.json"


def load_functional_evidence():
    """Load functional-check results separately from bounded help/version probes."""
    try:
        value = json.loads(functional_evidence_path().read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    if not isinstance(value, dict):
        return {}
    allowed = {"passed", "failed", "not_detected", "unsupported"}
    return {key: item for key, item in value.items()
            if isinstance(key, str) and isinstance(item, dict) and item.get("status") in allowed}


def run_bounded_local_command(args, *, input_bytes=None, env=None, timeout_seconds=5, output_limit=65536):
    """Run a fixed argv locally, enforcing time and combined-output bounds during execution."""
    proc = subprocess.Popen(
        args,
        stdin=subprocess.PIPE if input_bytes is not None else subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        start_new_session=(os.name == "posix"),
    )
    selector = selectors.DefaultSelector()
    stdout_fd, stderr_fd = proc.stdout.fileno(), proc.stderr.fileno()
    streams = {stdout_fd: bytearray(), stderr_fd: bytearray()}
    for fd in streams:
        os.set_blocking(fd, False)
        selector.register(fd, selectors.EVENT_READ, "read")
    sent = 0
    if input_bytes is not None:
        os.set_blocking(proc.stdin.fileno(), False)
        selector.register(proc.stdin.fileno(), selectors.EVENT_WRITE, "write")
    deadline = time.monotonic() + timeout_seconds
    total = 0
    try:
        while selector.get_map():
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise subprocess.TimeoutExpired(args, timeout_seconds)
            for key, _ in selector.select(min(remaining, 0.1)):
                if key.data == "write":
                    try:
                        sent += os.write(key.fd, input_bytes[sent:sent + 8192])
                    except BrokenPipeError:
                        sent = len(input_bytes)
                    if sent >= len(input_bytes):
                        selector.unregister(key.fd)
                        proc.stdin.close()
                else:
                    chunk = os.read(key.fd, 8192)
                    if not chunk:
                        selector.unregister(key.fd)
                        continue
                    total += len(chunk)
                    if total > output_limit:
                        raise RuntimeError(f"combined stdout/stderr exceeded {output_limit} byte output cap")
                    streams[key.fd].extend(chunk)
        returncode = proc.wait(timeout=max(0.05, deadline - time.monotonic()))
    except (subprocess.TimeoutExpired, RuntimeError):
        try:
            if os.name == "posix":
                os.killpg(proc.pid, signal.SIGKILL)
            else:
                proc.kill()
        except OSError:
            pass
        proc.wait()
        raise
    finally:
        selector.close()
        for stream in (proc.stdin, proc.stdout, proc.stderr):
            if stream is not None:
                stream.close()
    if returncode != 0:
        raise subprocess.CalledProcessError(returncode, args, output=bytes(streams[stdout_fd]), stderr=bytes(streams[stderr_fd]))
    return bytes(streams[stdout_fd])


def functional_check_tool(tool):
    """Run one allowlisted local-only functional check with bounded temporary state."""
    executable = tool.get("executable", "")
    path = shutil.which(executable) if EXECUTABLE_RE.fullmatch(executable) else None
    record = {
        "tool_id": tool["id"], "tool_name": tool["name"], "executable": executable,
        "path": path, "binary_identity": executable_identity(path), "status": "not_detected",
        "check_id": None, "tested_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "scope": "One allowlisted local functional check using temporary files only; not full compatibility or security certification.",
        "network_actions_executed": False, "package_changes": False,
    }
    if not path:
        record["status"] = "not_detected"
        record["detail"] = "Executable not found on PATH."
    else:
        def invoke(args, *, input_bytes=None, env=None):
            return run_bounded_local_command(args, input_bytes=input_bytes, env=env,
                                             timeout_seconds=5, output_limit=65536)
        import tempfile, hashlib, zipfile
        from pathlib import Path as LocalPath

        def require(condition, message):
            if not condition:
                raise AssertionError(message)
        try:
            with tempfile.TemporaryDirectory(prefix="syn-launch-functional-") as tmp:
                root = LocalPath(tmp)
                source = root / "sample.txt"
                source.write_bytes(b"SYN_LAUNCH functional check\nsecond line\n")
                raw = source.read_bytes()
                if executable == "jq":
                    out = invoke([path, "-e", "-n", '{ok:true,items:2} | .ok == true and .items == 2'])
                    require(out.strip() == b"true", "jq predicate did not return true")
                    check_id = "jq-json-assertion"
                elif executable == "rg":
                    search_file = root / "search.txt"
                    search_file.write_text("first\nneedle-one\nmiddle\nneedle-two\n", encoding="utf-8")
                    out = invoke([path, "-n", "needle", str(search_file)])
                    require(out.splitlines() == [b"2:needle-one", b"4:needle-two"],
                            "ripgrep did not return the expected local fixture matches")
                    check_id = "ripgrep-local-fixture-search"
                elif executable == "fd":
                    nested = root / "nested"
                    nested.mkdir()
                    target = nested / "needle.txt"
                    target.write_text("local fixture\n", encoding="utf-8")
                    out = invoke([path, "--type", "f", "needle", str(root)])
                    require(len(out.splitlines()) == 1 and b"needle.txt" in out,
                            "fd did not find the expected local fixture filename")
                    check_id = "fd-local-fixture-find"
                elif executable == "file":
                    out = invoke([path, "-b", str(source)])
                    require(b"ASCII text" in out, "file did not identify the temporary text fixture")
                    check_id = "file-local-text-identification"
                elif executable == "tree":
                    nested = root / "nested"
                    nested.mkdir()
                    target = nested / "needle.txt"
                    target.write_text("local fixture\n", encoding="utf-8")
                    out = invoke([path, "-fi", str(root)])
                    require(str(target).encode("utf-8") in out,
                            "tree did not list the expected nested fixture file")
                    check_id = "tree-local-directory-inventory"
                elif executable == "rsync":
                    target = root / "copy.txt"
                    invoke([path, "-a", str(source), str(target)])
                    require(target.read_bytes() == raw, "rsync copy differs from source")
                    check_id = "rsync-local-copy"
                elif executable == "sqlite3":
                    db = root / "check.db"
                    out = invoke([path, str(db), "CREATE TABLE checks(value TEXT); INSERT INTO checks VALUES('PASS'); SELECT value FROM checks;"])
                    require(out.strip() == b"PASS", "SQLite round trip returned unexpected output")
                    check_id = "sqlite-local-table-roundtrip"
                elif executable == "node":
                    out = invoke([path, "-e", 'const x={ok:true,n:2}; if(JSON.parse(JSON.stringify(x)).ok!==true || x.n!==2) process.exit(1); process.stdout.write("PASS")'])
                    require(out == b"PASS", "Node JSON round trip did not pass")
                    check_id = "node-json-roundtrip"
                elif executable == "ssh-keygen":
                    key = root / "ephemeral_ed25519"
                    invoke([path, "-q", "-t", "ed25519", "-N", "", "-f", str(key)])
                    fingerprint = invoke([path, "-lf", str(key) + ".pub"])
                    derived = invoke([path, "-y", "-f", str(key)]).strip()
                    stored = (root / "ephemeral_ed25519.pub").read_bytes().strip()
                    require(derived == stored and b"ED25519" in fingerprint, "SSH public-key derivation or fingerprint check failed")
                    check_id = "ssh-keygen-ephemeral-ed25519-roundtrip"
                elif executable == "base64":
                    encoded = invoke([path], input_bytes=raw)
                    decoded = invoke([path, "-d"], input_bytes=encoded)
                    require(decoded == raw, "base64 round trip differs from source")
                    check_id = "base64-roundtrip"
                elif executable == "sha256sum":
                    out = invoke([path], input_bytes=b"abc\n").split()[0]
                    require(out.decode("ascii") == hashlib.sha256(b"abc\n").hexdigest(), "sha256sum digest mismatch")
                    check_id = "sha256sum-known-digest"
                elif executable == "gzip":
                    compressed = invoke([path, "-c", str(source)])
                    out = invoke([path, "-dc"], input_bytes=compressed)
                    require(out == raw, "archive/compression round trip differs from source")
                    check_id = "gzip-roundtrip"
                elif executable == "tar":
                    archive = root / "check.tar.gz"
                    invoke([path, "-czf", str(archive), "-C", str(root), "sample.txt"])
                    out = invoke([path, "-xOzf", str(archive), "sample.txt"])
                    require(out == raw, "archive round trip differs from source")
                    check_id = "tar-roundtrip"
                elif executable == "unzip":
                    archive = root / "check.zip"
                    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
                        zf.write(source, "sample.txt")
                    out = invoke([path, "-p", str(archive), "sample.txt"])
                    require(out == raw, "archive round trip differs from source")
                    check_id = "unzip-roundtrip"
                elif executable == "hexdump":
                    out = invoke([path, "-C", str(source)])
                    require(b"SYN_LAUNCH" in out and b"00000000" in out, "hexdump output did not contain expected content")
                    check_id = "hexdump-known-content"
                elif executable == "openssl":
                    out = invoke([path, "dgst", "-sha256"], input_bytes=b"abc\n")
                    require(hashlib.sha256(b"abc\n").hexdigest().encode() in out, "OpenSSL digest mismatch")
                    check_id = "openssl-known-digest"
                elif executable == "git":
                    repo = root / "repo"
                    repo.mkdir()
                    git_env = os.environ.copy()
                    git_env.update({"GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
                                    "GIT_ATTR_NOSYSTEM": "1", "HOME": str(root)})
                    invoke([path, "-C", str(repo), "-c", "core.hooksPath=/dev/null", "init", "-q"], env=git_env)
                    (repo / "sample.txt").write_bytes(raw)
                    invoke([path, "-C", str(repo), "-c", "core.hooksPath=/dev/null", "-c", "user.name=SYN_LAUNCH test", "-c", "user.email=test@example.invalid", "add", "sample.txt"], env=git_env)
                    invoke([path, "-C", str(repo), "-c", "core.hooksPath=/dev/null", "-c", "user.name=SYN_LAUNCH test", "-c", "user.email=test@example.invalid", "commit", "-qm", "functional test"], env=git_env)
                    out = invoke([path, "-C", str(repo), "-c", "core.hooksPath=/dev/null", "status", "--porcelain"], env=git_env)
                    require(not out.strip(), "temporary Git repository has uncommitted changes")
                    check_id = "git-local-repository-roundtrip"
                elif executable == "python":
                    out = invoke([path, "-c", 'import json,hashlib\nx={"ok":True}\nif json.loads(json.dumps(x))["ok"] is not True:\n raise SystemExit(1)\nprint(hashlib.sha256(b"abc").hexdigest())'])
                    require(out.strip() == hashlib.sha256(b"abc").hexdigest().encode(), "Python JSON/SHA-256 check failed")
                    check_id = "python-json-and-sha256"
                elif executable == "curl":
                    out = invoke([path, "--fail", "--silent", "--show-error", "--max-time", "5", source.as_uri()])
                    require(out == raw, "curl local file transfer differs from source")
                    check_id = "curl-local-file-roundtrip"
                elif executable == "vim":
                    invoke([path, "-Nu", "NONE", "-n", "-es", str(source),
                            "-c", "2s/second line/edited line/", "-c", "wq"])
                    require(source.read_bytes() == b"SYN_LAUNCH functional check\nedited line\n",
                            "Vim did not apply the expected edit to the temporary fixture")
                    check_id = "vim-local-ex-mode-edit"
                elif executable == "npm":
                    (root / "package.json").write_text('{"name":"syn-launch-local-probe","version":"1.0.0"}\n', encoding="utf-8")
                    # Keep npm's cache and logging inside this temporary directory and
                    # ignore user/global npm configuration so the probe leaves no home-cache artifacts.
                    npm_user_config = root / ".npmrc-user"
                    npm_global_config = root / ".npmrc-global"
                    npm_user_config.touch()
                    npm_global_config.touch()
                    npm_env = {key: value for key, value in os.environ.items()
                               if not key.lower().startswith("npm_config_")}
                    npm_env.update({
                        "npm_config_cache": str(root / ".npm-cache"),
                        "npm_config_logs": "false",
                        "npm_config_userconfig": str(npm_user_config),
                        "npm_config_globalconfig": str(npm_global_config),
                        "npm_config_update_notifier": "false",
                        "npm_config_fund": "false",
                        "npm_config_audit": "false",
                        "npm_config_progress": "false",
                    })
                    out = invoke([path, "--offline", "--prefix", str(root), "pkg", "get", "name"], env=npm_env)
                    require(out.decode("utf-8").strip().strip("\"") == "syn-launch-local-probe", "npm did not read the temporary package metadata")
                    check_id = "npm-offline-package-metadata"
                elif executable == "make":
                    (root / "Makefile").write_text("all:\n\t@printf 'SYN_LAUNCH_MAKE_PASS\\n'\n", encoding="utf-8")
                    out = invoke([path, "-s", "-C", str(root)])
                    require(out.strip() == b"SYN_LAUNCH_MAKE_PASS", "make did not execute the temporary local target")
                    check_id = "make-local-target"
                elif executable == "ssh":
                    out = invoke([path, "-G", "-F", os.devnull, "syn-launch.invalid"])
                    require(b"hostname syn-launch.invalid" in out and b"port 22" in out,
                            "SSH config expansion did not produce expected host settings")
                    check_id = "ssh-config-expansion-no-connect"
                elif executable == "ps":
                    out = invoke([path, "-p", str(os.getpid()), "-o", "pid=,args="])
                    require(str(os.getpid()).encode() in out, "ps did not list the current SYN_LAUNCH process")
                    check_id = "ps-current-process"
                elif executable == "lsof":
                    with source.open("rb"):
                        out = invoke([path, "-w", "-p", str(os.getpid())])
                    require(str(source).encode() in out, "lsof did not list its open temporary source file")
                    check_id = "lsof-current-process-open-file"
                elif executable in {"clang", "readelf", "strings", "objdump"}:
                    compiler = shutil.which("clang")
                    if not compiler:
                        raise RuntimeError("clang dependency is not available; check was not run")
                    cfile, binary = root / "probe.c", root / "probe"
                    cfile.write_text('#include <stdio.h>\nint main(void){puts("SYN_LAUNCH_PASS");return 0;}\n', encoding="utf-8")
                    invoke([compiler, "-Wall", "-Wextra", "-Werror", str(cfile), "-o", str(binary)])
                    if executable == "clang":
                        out = invoke([str(binary)])
                        require(out.strip() == b"SYN_LAUNCH_PASS", "compiled program returned unexpected output")
                        check_id = "clang-compile-and-run"
                    elif executable == "readelf":
                        out = invoke([path, "-h", str(binary)])
                        require(b"ELF Header" in out and b"Machine:" in out, "readelf output lacks expected ELF header fields")
                        check_id = "readelf-elf-header"
                    elif executable == "strings":
                        out = invoke([path, str(binary)])
                        require(b"SYN_LAUNCH_PASS" in out, "strings did not find embedded test literal")
                        check_id = "strings-known-literal"
                    else:
                        out = invoke([path, "-f", str(binary)])
                        require(b"file format" in out and b"architecture:" in out, "objdump output lacks expected metadata")
                        check_id = "objdump-binary-metadata"
                else:
                    record.update(status="unsupported", check_id=None,
                                  detail="No reviewed local-only functional adapter exists for this executable; no command was run.")
                    check_id = None
                if check_id:
                    record.update(status="passed", check_id=check_id, detail="Specific bounded local functional assertion passed.")
        except (AssertionError, OSError, subprocess.SubprocessError, RuntimeError, ValueError) as exc:
            record.update(status="failed", detail=(str(exc) or type(exc).__name__)[:500])
    evidence = load_functional_evidence()
    evidence[tool["id"]] = record
    save_private_json(functional_evidence_path(), evidence)
    return record

def compatibility_report(data):
    """Separate catalog claims, PATH evidence, source metadata, and recorded bounded smoke tests."""
    profile = environment_profile(data)
    saved_evidence = load_smoke_evidence()
    functional_evidence = load_functional_evidence()
    tools = []
    for tool in data["tools"]:
        executable = tool.get("executable", "")
        path = shutil.which(executable) if re.fullmatch(r"[A-Za-z0-9_.+-]{1,128}", executable) else None
        compatibility = tool.get("compatibility")
        compatibility_is_declared = isinstance(compatibility, dict) and bool(compatibility)
        smoke = saved_evidence.get(tool["id"], {})
        smoke_status = smoke.get("status", "not_run")
        functional = functional_evidence.get(tool["id"], {})
        functional_status = functional.get("status", "not_run")
        current_identity = executable_identity(path)
        if smoke and (smoke.get("path") != path or smoke.get("binary_identity") != current_identity):
            smoke_status = "stale_evidence"
        if functional and (functional.get("path") != path or functional.get("binary_identity") != current_identity):
            functional_status = "stale_evidence"
        tools.append({
            "id": tool["id"],
            "name": tool["name"],
            "category": tool["category"],
            "executable": executable,
            "path": path,
            "status": "path_match_unverified" if path else "not_detected",
            "catalog_installable": bool(tool.get("installable", False)),
            "install_kind": tool["install_kind"],
            "package": tool.get("package"),
            "compatibility_assessment": "declared_but_not_device_verified" if compatibility_is_declared else "not_assessed",
            "compatibility_metadata": compatibility if compatibility_is_declared else None,
            "verification": "not_run",
            "smoke_test": smoke_status,
            "smoke_test_evidence": ({**smoke, "report_status": smoke_status} if smoke else None),
            "functional_check": functional_status,
            "functional_check_evidence": ({**functional, "report_status": functional_status} if functional else None),
            "device_validation": "not_run",
            "caveat": tool["caveat"],
        })
    return {
        "report_schema": 4,
        "application": "SYN_LAUNCH",
        "device_profile": profile,
        "summary": {
            "catalog_entries": len(tools),
            "catalog_installable_entries": sum(1 for tool in tools if tool["catalog_installable"]),
            "path_match_entries": sum(1 for tool in tools if tool["path"]),
            "not_detected_entries": sum(1 for tool in tools if not tool["path"]),
            "unique_path_match_executables": len({tool["executable"] for tool in tools if tool["path"]}),
            "compatibility_assessed_entries": sum(1 for tool in tools if tool["compatibility_assessment"] == "declared_but_not_device_verified"),
            "smoke_tested_entries": sum(1 for tool in tools if tool["smoke_test"] == "passed"),
            "smoke_test_attempted_entries": sum(1 for tool in tools if tool["smoke_test"] in {"passed", "output_observed_nonzero", "timed_out", "no_response"}),
            "functional_check_passed_entries": sum(1 for tool in tools if tool["functional_check"] == "passed"),
            "functional_check_attempted_entries": sum(1 for tool in tools if tool["functional_check"] in {"passed", "failed"}),
            "device_verified_entries": sum(1 for tool in tools if tool["device_validation"] == "verified"),
            "verified_tools": 0,
            "tools_executed_by_report": False,
            "note": "Catalog installability and PATH presence are discovery/metadata only. Smoke tests and functional checks run only when a specific tool is explicitly selected. Functional checks cover only their named local assertion; neither evidence type certifies full tool functionality or device compatibility. Device validation remains not_run unless separately recorded.",
        },
        "tools": tools,
    }


def print_environment_profile(data):
    print(json.dumps(environment_profile(data), indent=2, sort_keys=True))


def print_compatibility_report(data):
    print(json.dumps(compatibility_report(data), indent=2, sort_keys=True))


def health(data, detailed=False):
    profile = environment_profile(data)
    say(f"Python: {sys.version.split()[0]} | Platform: {platform.platform()}")
    say(f"Architecture: {profile['machine_raw']} (family: {profile['architecture_family']})")
    say(f"Android markers: {'detected' if profile['android_markers_detected'] else 'not detected'} | Termux: {'detected' if profile['termux_detected'] else 'not detected'}")
    say(f"Process UID 0: {'yes' if profile['process_uid_is_zero'] else 'no'} (does not prove Android host root)")
    if profile["storage_free_bytes"] is not None:
        say(f"Storage free: {profile['storage_free_bytes'] / (1024 ** 3):.2f} GiB / {profile['storage_total_bytes'] / (1024 ** 3):.2f} GiB")
    say(f"Catalog: {len(data['tools'])} entries across {len(data['categories'])} categories")
    say("Termux pkg: "+("available" if shutil.which("pkg") else "not found"))
    for cmd in ("pkg", "python", "python3", "go", "cargo", "rustc", "npm", "node", "git", "proot", "docker", "adb"):
        say(f"{cmd}: " + (shutil.which(cmd) or "not found"))
    if detailed:
        say("Install-method counts: " + json.dumps(profile["install_method_counts"], sort_keys=True))
        say(profile["compatibility_note"])
    say("Rich UI: "+("enabled" if RICH else "plain-text fallback"))
    say("State directory: "+str(STATE_DIR))
    say(f"Detected executables: {sum(installed(t) for t in data['tools'])}/{len(data['tools'])} entries (PATH check only, not full self-tests)")

def main():
    parser=argparse.ArgumentParser(description="SYN_LAUNCH Termux security-tool catalog and installer")
    parser.add_argument("--check",action="store_true",help="validate catalog and print concise environment status")
    parser.add_argument("--doctor",action="store_true",help="show detailed platform, architecture, runtime, and storage diagnostics")
    parser.add_argument("--profile",action="store_true",help="print machine-readable JSON device/runtime profile")
    parser.add_argument("--compatibility-report",action="store_true",help="print JSON catalog status and separately recorded bounded smoke-test evidence")
    parser.add_argument("--php-security-check",action="store_true",help="check installed Termux PHP package metadata against the pinned 2026-10-21 critical security advisory; read-only")
    parser.add_argument("--smoke-test",metavar="NAME_OR_ID",help="run bounded tool-specific help/version probes for one explicitly selected tool")
    parser.add_argument("--functional-check",metavar="NAME_OR_ID",help="run one allowlisted local-only functional check for an explicitly selected tool")
    parser.add_argument("--list",action="store_true",help="list catalog entries")
    parser.add_argument("--search",metavar="QUERY",help="search catalog without interactive menu")
    parser.add_argument("--category",metavar="NAME",help="list tools in a category")
    parser.add_argument("--tool",metavar="NAME",help="show status and local help for a tool")
    parser.add_argument("--toolset",metavar="ID",help="show a validated curated toolset as JSON (does not install or execute tools)")
    parser.add_argument("--workflow-list",action="store_true",help="list available dry-run assessment workflow plans")
    parser.add_argument("--workflow-plan",metavar="WORKFLOW_ID",help="emit a scope-bound dry-run plan; does not run tools")
    parser.add_argument("--workflow-run",metavar="WORKFLOW_ID",help="run an approved read-only local workflow adapter; unsupported workflows remain plan-only")
    parser.add_argument("--target-scope",metavar="SCOPE",help="explicit assets/environment covered by a workflow plan")
    parser.add_argument("--authorized",action="store_true",help="confirm you have authorization for the declared scope")
    args=parser.parse_args()
    try: data=load_catalog()
    except (OSError,json.JSONDecodeError,ValueError) as exc:
        print("Catalog validation failed:",exc,file=sys.stderr); return 2
    if args.toolset:
        return print_toolset(args.toolset, data)
    if args.workflow_list:
        print(json.dumps([{"id": key, "title": value["title"], "purpose": value["purpose"]} for key, value in sorted(WORKFLOWS.items())], indent=2))
        return 0
    if args.workflow_plan:
        if not args.target_scope:
            print("--workflow-plan requires --target-scope.", file=sys.stderr); return 2
        if not args.authorized:
            print("--workflow-plan requires --authorized. This is an operator declaration, not an authorization check.", file=sys.stderr); return 2
        try:
            plan = build_workflow_plan(args.workflow_plan, args.target_scope, args.authorized)
        except ValueError as exc:
            print("Workflow plan rejected: " + str(exc), file=sys.stderr); return 2
        print(json.dumps(plan, indent=2, ensure_ascii=False))
        return 0
    if args.workflow_run:
        if not args.target_scope:
            print("--workflow-run requires --target-scope.", file=sys.stderr); return 2
        if not args.authorized:
            print("--workflow-run requires --authorized. This is an operator declaration, not an authorization check.", file=sys.stderr); return 2
        try:
            report = run_workflow_adapter(args.workflow_run, args.target_scope)
        except (ValueError, OSError) as exc:
            print("Workflow execution rejected: " + str(exc), file=sys.stderr); return 2
        report_dir = STATE_DIR / "workflow-runs"
        report_dir.mkdir(parents=True, exist_ok=True)
        try: report_dir.chmod(0o700)
        except OSError: pass
        report_path = report_dir / (args.workflow_run + "-" + time.strftime("%Y%m%dT%H%M%S") + "-" + str(time.time_ns()) + ".json")
        save_private_json(report_path, report)
        report["saved_report"] = str(report_path)
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 1 if report.get("request_status") in {"request_failed", "request_rejected"} else 0
    if args.php_security_check:
        report = php_security_report(data)
        print(json.dumps(report, indent=2, ensure_ascii=False))
        if report["status"] in {"fixed_release_or_newer", "not_installed"}:
            return 0
        if report["status"] in {"update_required", "vendor_backport_or_upgrade_required", "release_line_not_assessed", "catalog_entry_missing"}:
            return 1
        return 2
    if args.profile: print_environment_profile(data); return 0
    if args.compatibility_report: print_compatibility_report(data); return 0
    if args.smoke_test:
        matches=[t for t in data["tools"] if t["name"].lower()==args.smoke_test.lower() or t["id"].lower()==args.smoke_test.lower()]
        if not matches:
            print("Tool not found. Use --search to find its exact name or ID.", file=sys.stderr); return 1
        record=smoke_test_tool(matches[0])
        print(json.dumps(record, indent=2, ensure_ascii=False))
        return 0 if record["status"] == "passed" else 1
    if args.functional_check:
        matches=[t for t in data["tools"] if t["name"].lower()==args.functional_check.lower() or t["id"].lower()==args.functional_check.lower()]
        if not matches:
            print("Tool not found. Use --search to find its exact name or ID.", file=sys.stderr); return 1
        record=functional_check_tool(matches[0])
        print(json.dumps(record, indent=2, ensure_ascii=False))
        return 0 if record["status"] == "passed" else 1
    if args.check: health(data); return 0
    if args.doctor: health(data, detailed=True); return 0
    if args.list: show_list(data["tools"]); return 0
    if args.search:
        matches=[t for t in data["tools"] if args.search.lower() in t["name"].lower() or args.search.lower() in t["category"].lower() or args.search.lower() in t["description"].lower()]
        show_list(matches); return 0 if matches else 1
    if args.category:
        matches=[t for t in data["tools"] if t["category"].lower()==args.category.lower()]
        if not matches: print("Unknown category. Available:",", ".join(data["categories"])); return 1
        show_list(matches); return 0
    if args.tool:
        matches=[t for t in data["tools"] if t["name"].lower()==args.tool.lower() or t["id"]==args.tool.lower()]
        if not matches: print("Tool not found. Try --search."); return 1
        show_tool(matches[0]); return 0
    title()
    while True:
        c=menu("Main menu",["Browse categories","Search catalog","All tools","Curated toolsets (Phone + Android Top 75)","Installer","Environment / health","Credits and safety","Custom tools / favorites","Exit"])
        if c=="1": category(data)
        elif c=="2": search(data)
        elif c=="3": choose(data)
        elif c=="4": browse_curated_toolsets(data)
        elif c=="5": installer(data)
        elif c=="6": health(data)
        elif c=="7":
            say("SYN_LAUNCH is a catalog/launcher, not the author of listed utilities.")
            say("Each entry links to a maintainer or project page. Respect upstream licenses and API terms.")
            say("Some tools require root, compatible hardware, desktop Linux, API keys, or approved credentials.")
            say("No scans start automatically. Never run active tests outside explicit authorization.")
        elif c=="8": manage_custom_tools(data)
        elif c in ("0","9"): break
        else: say("Invalid choice.")
    return 0

if __name__=="__main__": raise SystemExit(main())