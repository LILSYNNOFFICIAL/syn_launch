#!/usr/bin/env python3
"""SYN_LAUNCH: catalog-first security toolkit manager for Termux."""
from __future__ import annotations
import argparse, json, os, platform, re, selectors, shutil, signal, subprocess, sys, time
from pathlib import Path

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

def say(message=""):
    if RICH: console.print(message, markup=False)
    else: print(str(message))

def title():
    if RICH: console.print(Panel.fit("[bold bright_cyan]S Y N _ L A U N C H[/bold bright_cyan]\n[dim]Termux Security Toolkit • Android-aware[/dim]", border_style="bright_cyan"))
    else: print("\nS Y N _ L A U N C H\nTermux Security Toolkit • Android-aware\n")

def validate_catalog(data):
    if not isinstance(data, dict) or not isinstance(data.get("tools"), list) or not isinstance(data.get("categories"), list):
        raise ValueError("catalog must contain tools and categories lists")
    if data.get("tool_count") != len(data["tools"]): raise ValueError("tool_count does not match actual entries")
    ids, categories = set(), set()
    for t in data["tools"]:
        if not isinstance(t, dict): raise ValueError("each tool must be an object")
        for field in ("id","name","category","executable","install_kind","description","source","caveat"):
            if not isinstance(t.get(field),str) or not t[field].strip(): raise ValueError(f"missing/invalid {field}: {t.get('name','<unnamed>')}")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*",t["id"]): raise ValueError(f"invalid id: {t['id']}")
        if t["id"] in ids: raise ValueError(f"duplicate id: {t['id']}")
        ids.add(t["id"]); categories.add(t["category"])
        if t["install_kind"] not in INSTALL_KINDS: raise ValueError(f"invalid install kind: {t['name']}")
        if not t["source"].startswith("https://"): raise ValueError(f"source must use HTTPS: {t['name']}")
        expected=t["install_kind"] in {"pkg","pip","go","cargo","npm"}
        if bool(t.get("installable")) != expected: raise ValueError(f"installable flag mismatch: {t['name']}")
        if expected:
            package=t.get("package")
            regex={"pkg":PKG_RE,"pip":PIP_RE,"go":GO_RE,"cargo":CARGO_RE,"npm":NPM_RE}[t["install_kind"]]
            if not isinstance(package,str) or not regex.fullmatch(package): raise ValueError(f"unsafe package/module syntax: {t['name']}")
    if set(data["categories"]) != categories: raise ValueError("categories list does not match catalog entries")
    return data

def load_catalog():
    data = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    if CUSTOM_PATH.exists():
        custom = json.loads(CUSTOM_PATH.read_text(encoding="utf-8"))
        if not isinstance(custom, list):
            raise ValueError("custom_tools.json must contain a JSON list")
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
    if installed(t): return "INSTALLED"
    return {"pkg":"TERMUX PKG","pip":"PYTHON/PIP","go":"GO BUILD","cargo":"CARGO BUILD","npm":"NPM PACKAGE","manual":"MANUAL","root":"ROOT/HW"}.get(t["install_kind"],"UNKNOWN")

def run(command, label, timeout=900, env=None):
    if not isinstance(command,(list,tuple)) or not command or not all(isinstance(x,str) and x for x in command):
        say("Refusing invalid command arguments."); return False
    logfile=LOG_DIR/(time.strftime("%Y%m%d-%H%M%S")+"-"+str(os.getpid())+".log")
    say(f"\n→ {label}\nCommand: {' '.join(command)}\nLog: {logfile}")
    child_env=os.environ.copy()
    if env: child_env.update(env)
    proc=None
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
                        decoded=chunk.decode("utf-8",errors="replace")
                        sys.stdout.write(decoded); sys.stdout.flush(); log.write(decoded); log.flush()
            code=proc.wait(timeout=max(0.1,deadline-time.monotonic()))
            if code: say(f"Command exited with status {code}.")
            return code==0
    except subprocess.TimeoutExpired:
        say(f"Timed out after {timeout}s; terminating the process.")
        try:
            if proc and proc.poll() is None:
                os.killpg(proc.pid,signal.SIGKILL) if os.name=="posix" else proc.kill()
                proc.wait(timeout=5)
        except (OSError,subprocess.TimeoutExpired): pass
        return False
    except (OSError,ValueError) as exc:
        say(f"Could not run command: {exc}")
        return False

def show_local_docs(t):
    exe=t["executable"]; path=shutil.which(exe) if re.fullmatch(r"[A-Za-z0-9_.+-]+",exe) else None
    if not path: return
    say("\nLocal command documentation from installed executable:")
    for flags,label in ((("--version","-V"),"Version"),(("--help","-h"),"Help")):
        output=""
        for flag in flags:
            try:
                r=subprocess.run([path,flag],stdin=subprocess.DEVNULL,capture_output=True,text=True,timeout=5,errors="replace",check=False)
                candidate=(r.stdout+"\n"+r.stderr).strip()
                if candidate: output=candidate; break
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
    if installed(t): show_local_docs(t)
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
    if not run([str(pip),"install","--upgrade",package],"Installing Python tool "+t["name"],1800): return False
    return installed(t)

def install_go(t):
    if installed(t): say(f"{t['name']} already appears in PATH."); return True
    module=t.get("package","")
    if not GO_RE.fullmatch(module): say("Refusing invalid Go module path."); return False
    go=shutil.which("go")
    if not go: say("Go missing. Install the Go runtime first."); return False
    return run([go,"install",module],"Building "+t["name"],3600,{"GOBIN":str(BIN_DIR)})

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
    return run([npm,"install","--global",package],"Installing npm tool "+t["name"],1800)

def install_one(t,confirmed=False):
    kind=t["install_kind"]
    if kind in {"manual","root"}: say("No automatic install configured. Review source and compatibility notes."); return False
    if not confirmed:
        say("Security note: package installation executes third-party code/build scripts. Verify the upstream project and package.")
        if ask("Type INSTALL to continue: ")!="INSTALL": say("Cancelled."); return False
    return {"pkg":install_pkg,"pip":install_pip,"go":install_go,"cargo":install_cargo,"npm":install_npm}[kind](t)

def choose(data,tools=None):
    tools=tools or data["tools"]; show_list(tools)
    value=ask("Tool number: ")
    if not value.isdigit() or int(value)==0: return
    i=int(value)-1
    if i<0 or i>=len(tools): say("Invalid number."); return
    t=tools[i]; show_tool(t); action=ask("[i]nstall / [h]elp / [f]avorite / [b]ack: ").lower()
    if action=="i": install_one(t)
    elif action=="h": say("Review the example and source; replace placeholders only with authorized test values." if t.get("example") else "No example supplied. Read upstream documentation.")
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

def progress(items,worker,label,confirmed=False):
    if not items: say("No items to install."); return
    good=0; failed=[]
    def attempt(t):
        return worker(t,confirmed=confirmed) if worker is install_one else worker(t)
    if RICH:
        with Progress(SpinnerColumn(),TextColumn("[progress.description]{task.description}"),BarColumn(),TextColumn("{task.completed}/{task.total}"),TimeElapsedColumn(),console=console,transient=False) as bar:
            task=bar.add_task(label,total=len(items))
            for t in items:
                bar.update(task,description=label+": "+t["name"]); ok=attempt(t); good+=int(bool(ok))
                if not ok: failed.append(t["name"])
                bar.advance(task)
    else:
        for i,t in enumerate(items,1):
            print(f"\n[{i}/{len(items)}] {label}: {t['name']}"); ok=attempt(t); good+=int(bool(ok))
            if not ok: failed.append(t["name"])
    summary={"succeeded":good,"failed":failed,"total":len(items),"timestamp":time.strftime("%Y-%m-%d %H:%M:%S")}
    p=STATE_DIR/"last_install_summary.json"; p.write_text(json.dumps(summary,indent=2),encoding="utf-8")
    try: p.chmod(0o600)
    except OSError: pass
    say(f"Finished: {good}/{len(items)} successful attempts.")
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
    if not re.fullmatch(r"[A-Za-z0-9_.+-]+",executable):
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
    example=ask("Example/help command (optional, not auto-executed): ")
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

def installer(data):
    choice=menu("Installer",["Attempt all distinct Termux packages","Install one selected tool","Install Python, Go, Rust and Node.js runtimes","Attempt all Python/Go/Cargo/npm tools (large download/build)","Show last install summary"])
    if choice=="1":
        packages={}
        for t in data["tools"]:
            if t["install_kind"]=="pkg" and t.get("package"): packages.setdefault(t["package"],t)
        say(f"Attempts {len(packages)} distinct packages; availability varies by Termux repo and architecture.")
        if ask("Type YES to continue: ")!="YES": return
        if not shutil.which("pkg"): say("pkg not found. Run inside Termux."); return
        run(["pkg","update","-y"],"Refreshing package indexes",1200)
        progress(list(packages.values()),install_pkg,"Termux packages")
        say("Progress measures completed attempts, not download-byte percentage.")
    elif choice=="2": choose(data)
    elif choice=="3":
        names={"Python","Go","Rust","Node.js"}
        progress([t for t in data["tools"] if t["name"] in names and t["install_kind"]=="pkg"],install_pkg,"Toolchain prerequisites")
    elif choice=="4":
        items=[t for t in data["tools"] if t["install_kind"] in {"pip","go","cargo","npm"}]
        say(f"Attempts {len(items)} third-party installs/builds. Expect large downloads and Android dependency failures.")
        if ask("Type YES to continue: ")!="YES": return
        names={"Python","Go","Rust","Node.js"}
        progress([t for t in data["tools"] if t["name"] in names and t["install_kind"]=="pkg"],install_pkg,"Installing runtimes")
        progress(items,install_one,"Security tool installs",confirmed=True)
    elif choice=="5":
        p=STATE_DIR/"last_install_summary.json"; say(p.read_text(encoding="utf-8") if p.exists() else "No install summary yet.")

def health(data):
    say(f"Python: {sys.version.split()[0]} | Platform: {platform.platform()}")
    say(f"Catalog: {len(data['tools'])} entries across {len(data['categories'])} categories")
    say("Termux pkg: "+("available" if shutil.which("pkg") else "not found"))
    for cmd in ("go","cargo","npm","git"): say(f"{cmd}: "+(shutil.which(cmd) or "not found"))
    say("Rich UI: "+("enabled" if RICH else "plain-text fallback"))
    say("State directory: "+str(STATE_DIR))
    say(f"Detected executables: {sum(installed(t) for t in data['tools'])}/{len(data['tools'])} entries (PATH check only, not full self-tests)")

def main():
    parser=argparse.ArgumentParser(description="SYN_LAUNCH Termux security-tool catalog and installer")
    parser.add_argument("--check",action="store_true",help="validate catalog and print environment status")
    parser.add_argument("--list",action="store_true",help="list catalog entries")
    parser.add_argument("--search",metavar="QUERY",help="search catalog without interactive menu")
    parser.add_argument("--category",metavar="NAME",help="list tools in a category")
    parser.add_argument("--tool",metavar="NAME",help="show status and local help for a tool")
    args=parser.parse_args()
    try: data=load_catalog()
    except (OSError,json.JSONDecodeError,ValueError) as exc:
        print("Catalog validation failed:",exc,file=sys.stderr); return 2
    if args.check: health(data); return 0
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
        c=menu("Main menu",["Browse categories","Search catalog","All tools","Installer","Environment / health","Credits and safety","Custom tools / favorites","Exit"])
        if c=="1": category(data)
        elif c=="2": search(data)
        elif c=="3": choose(data)
        elif c=="4": installer(data)
        elif c=="5": health(data)
        elif c=="6":
            say("SYN_LAUNCH is a catalog/launcher, not the author of listed utilities.")
            say("Each entry links to a maintainer or project page. Respect upstream licenses and API terms.")
            say("Some tools require root, compatible hardware, desktop Linux, API keys, or approved credentials.")
            say("No scans start automatically. Never run active tests outside explicit authorization.")
        elif c=="7": manage_custom_tools(data)\n        elif c in ("0","8"): break
        else: say("Invalid choice.")
    return 0

if __name__=="__main__": raise SystemExit(main())
