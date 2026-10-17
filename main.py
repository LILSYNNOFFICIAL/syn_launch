#!/usr/bin/env python3
"""SYN_LAUNCH: catalog-first security toolkit manager for Termux."""
import json, os, platform, shutil, subprocess, sys, time
from pathlib import Path
APP_DIR=Path(__file__).resolve().parent
CATALOG_PATH=APP_DIR/"catalog.json"
STATE_DIR=Path(os.environ.get("SYN_LAUNCH_HOME",str(Path.home()/".syn_launch")))
LOG_DIR=STATE_DIR/"logs"; BIN_DIR=Path.home()/".local"/"bin"; VENV_DIR=STATE_DIR/"venv"
STATE_DIR.mkdir(parents=True,exist_ok=True); LOG_DIR.mkdir(parents=True,exist_ok=True); BIN_DIR.mkdir(parents=True,exist_ok=True)
try:
 from rich.console import Console
 from rich.panel import Panel
 from rich.progress import Progress,SpinnerColumn,BarColumn,TextColumn,TimeElapsedColumn
 from rich.table import Table
 RICH=True; console=Console()
except Exception:
 RICH=False; console=None
def say(s=""):
 if RICH: console.print(s)
 else: print(str(s))
def title():
 if RICH: console.print(Panel.fit("[bold bright_cyan]S Y N _ L A U N C H[/bold bright_cyan]\n[dim]Termux Security Toolkit • Android-aware[/dim]",border_style="bright_cyan"))
 else: print("\nS Y N _ L A U N C H\nTermux Security Toolkit • Android-aware\n")
def load_catalog():
 data=json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
 if not isinstance(data.get("tools"),list): raise ValueError("catalog.json has no tools list")
 ids=[t.get("id") for t in data["tools"]]
 if len(ids)!=len(set(ids)): raise ValueError("catalog has duplicate IDs")
 return data
def installed(t):
 exe=t.get("executable","")
 return bool(exe and not any(c in exe for c in " /$;|&") and shutil.which(exe))
def status(t):
 if installed(t): return "INSTALLED"
 return {"pkg":"TERMUX PKG","pip":"PYTHON/PIP","go":"GO BUILD","manual":"MANUAL","root":"ROOT/HW"}.get(t["install_kind"],"UNKNOWN")
def show_local_docs(t):
 exe=t.get("executable","")
 path=shutil.which(exe) if exe and not any(c in exe for c in " /$;|&") else None
 if not path: return
 say("\nLocal command documentation (from the installed executable):")
 version_output=""
 for flag in ("--version","-V","version"):
  try:
   r=subprocess.run([path,flag],capture_output=True,text=True,timeout=5,errors="replace")
   output=(r.stdout+"\n"+r.stderr).strip()
   if output:
    version_output=output
    break
  except (OSError,subprocess.TimeoutExpired): continue
 if version_output: say("Version / version response:\n"+version_output[:2500])
 help_output=""
 for flag in ("--help","-h"):
  try:
   r=subprocess.run([path,flag],capture_output=True,text=True,timeout=5,errors="replace")
   output=(r.stdout+"\n"+r.stderr).strip()
   if output:
    help_output=output
    break
  except (OSError,subprocess.TimeoutExpired): continue
 if help_output:
  lines=help_output.splitlines()
  say("Installed CLI help (first 70 lines):")
  say("\n".join(lines[:70]))
  if len(lines)>70: say(f"... {len(lines)-70} additional lines omitted; run {exe} --help directly for full output.")
 else:
  say("The installed command did not return version/help text using standard flags. Check the source link for current documentation.")
def show_tool(t,n=None):
 say("\n"+(f"{n}. " if n else "")+t["name"])
 say(f"Category: {t['category']} | Status: {status(t)}")
 say(t["description"]); say("Install method: "+t["install_kind"]+(f" ({t['package']})" if t.get("package") else ""))
 say("Compatibility: "+t["caveat"]); say("Source: "+t["source"])
 if t.get("example"): say("Example: "+t["example"])
 if installed(t): show_local_docs(t)
 say("Only test systems, accounts, apps, and networks you own or have explicit permission to assess.")
def ask(s="> "):
 try: return input(s).strip()
 except (EOFError,KeyboardInterrupt): print(); return "0"
def menu(label,opts):
 say("\n"+label)
 for i,x in enumerate(opts,1): say(f" {i:>2}. {x}")
 say("  0. Back / exit")
 return ask()
def run(command,label,timeout=900,env=None):
 logfile=LOG_DIR/(time.strftime("%Y%m%d-%H%M%S")+".log")
 say(f"\n→ {label}\nCommand: {' '.join(command)}\nLog: {logfile}")
 try:
  with logfile.open("a",encoding="utf-8") as log:
   p=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,errors="replace",env=env)
   start=time.time()
   while True:
    line=p.stdout.readline() if p.stdout else ""
    if line:
     print(line,end=""); log.write(line); log.flush()
    elif p.poll() is not None: break
    elif time.time()-start>timeout:
     p.kill(); say("Timed out; inspect the log and retry individually."); return False
   rest=p.stdout.read() if p.stdout else ""
   if rest: print(rest,end=""); log.write(rest)
   return p.wait()==0
 except FileNotFoundError:
  say("Missing command: "+command[0]); return False
def install_pkg(t):
 if installed(t): return True
 if not shutil.which("pkg"): say("pkg not found; run this option in Termux."); return False
 return run(["pkg","install","-y",t["package"]],"Installing "+t["name"]) if t.get("package") else False
def ensure_venv():
 if not VENV_DIR.exists(): return run([sys.executable,"-m","venv",str(VENV_DIR)],"Creating isolated Python environment")
 return True
def install_pip(t):
 if installed(t): return True
 if not ensure_venv(): return False
 pip=VENV_DIR/"bin"/"pip"
 ok=run([str(pip),"install","--upgrade",t["package"]],"Installing Python tool "+t["name"],1800)
 if ok:
  for p in (VENV_DIR/"bin").iterdir():
   if p.is_file() and os.access(p,os.X_OK) and p.name not in {"python","python3","pip","pip3"}:
    target=BIN_DIR/p.name
    try:
     if not target.exists(): target.symlink_to(p)
    except OSError: pass
  return installed(t) or (BIN_DIR/t["executable"]).exists()
 return False
def install_go(t):
 if installed(t): return True
 if not shutil.which("go"): say("Go is missing. Install Termux package golang first."); return False
 env=os.environ.copy(); env["GOBIN"]=str(BIN_DIR)
 return run(["go","install",t["package"]],"Building "+t["name"],2400,env=env) if t.get("package") else False
def install_one(t):
 kind=t["install_kind"]
 if kind=="pkg": return install_pkg(t)
 if kind=="pip": return install_pip(t)
 if kind=="go": return install_go(t)
 say("No verified automatic installer for this entry. Check source and compatibility notes."); return False
def show_list(data,tools):
 if RICH:
  tab=Table("No.","Tool","Category","Status")
  for i,t in enumerate(tools,1): tab.add_row(str(i),t["name"],t["category"],status(t))
  console.print(tab)
 else:
  for i,t in enumerate(tools,1): print(f"{i:3}. {t['name']:<23} {t['category']:<34} {status(t)}")
def choose(data,tools=None):
 tools=tools or data["tools"]; show_list(data,tools)
 value=ask("Tool number: ")
 if not value.isdigit() or int(value)==0:return
 i=int(value)-1
 if i<0 or i>=len(tools): say("Invalid number."); return
 t=tools[i]; show_tool(t)
 action=ask("[i]nstall / [h]elp / [b]ack: ").lower()
 if action=="i":
  if t["install_kind"] in ("manual","root"): say("Catalog only: no verified automatic installer for stock Termux.")
  else: install_one(t)
 elif action=="h" and t.get("example"): say("Review the example and replace placeholders with authorized test values.")
def category(data):
 cats=data["categories"]; c=menu("Browse categories",cats)
 if c.isdigit() and 1<=int(c)<=len(cats): choose(data,[t for t in data["tools"] if t["category"]==cats[int(c)-1]])
def search(data):
 q=ask("Search name/category/description: ").lower()
 matches=[t for t in data["tools"] if q and (q in t["name"].lower() or q in t["category"].lower() or q in t["description"].lower())]
 if matches: choose(data,matches)
 else: say("No matches.")
def progress(items,worker,label):
 if not items: say("No items."); return
 good=0; bad=[]
 if RICH:
  with Progress(SpinnerColumn(),TextColumn("[progress.description]{task.description}"),BarColumn(),TextColumn("{task.completed}/{task.total}"),TimeElapsedColumn(),console=console) as p:
   task=p.add_task(label,total=len(items))
   for t in items:
    p.update(task,description=label+": "+t["name"]); result=worker(t); good+=bool(result)
    if not result: bad.append(t["name"])
    p.advance(task)
 else:
  for i,t in enumerate(items,1):
   print(f"\n[{i}/{len(items)}] {label}: {t['name']}")
   result=worker(t); good+=bool(result)
   if not result: bad.append(t["name"])
 summary={"ok":good,"failed":bad,"time":time.strftime("%Y-%m-%d %H:%M:%S")}
 (STATE_DIR/"last_install_summary.json").write_text(json.dumps(summary,indent=2))
 say(f"Finished: {good} succeeded, {len(bad)} failed/unavailable.")
 if bad: say("Needs attention: "+", ".join(bad))
def installer(data):
 c=menu("Installer",["Attempt every distinct Termux pkg package in the catalog","Install one selected tool","Install Python and Go runtimes","Install all Python/Go catalog tools (large download/build)","Show last install summary"])
 if c=="1":
  packages={}
  for t in data["tools"]:
   if t["install_kind"]=="pkg" and t.get("package"): packages.setdefault(t["package"],t)
  say(f"This attempts {len(packages)} distinct packages. Some may be unavailable for your repository or architecture.")
  if ask("Type YES to continue: ")!="YES":return
  if not shutil.which("pkg"): say("pkg not found; run in Termux."); return
  run(["pkg","update","-y"],"Refreshing package indexes",1200)
  progress(list(packages.values()),install_pkg,"Termux packages")
  say("Progress measures completed package attempts, not download-byte percentage.")
 elif c=="2": choose(data)
 elif c=="3":
  runtime=[t for t in data["tools"] if t["name"] in ("Python","Go")]
  progress(runtime,install_pkg,"Toolchain prerequisites")
 elif c=="4":
  items=[t for t in data["tools"] if t["install_kind"] in ("pip","go")]
  say(f"This attempts {len(items)} Python/Go tool installs. Builds may take a long time, consume storage/data, or fail on Android-incompatible dependencies.")
  if ask("Type YES to continue: ")!="YES": return
  runtime=[t for t in data["tools"] if t["name"] in ("Python","Go")]
  progress(runtime,install_pkg,"Installing toolchain prerequisites")
  progress(items,install_one,"Python/Go catalog tools")
 elif c=="5":
  p=STATE_DIR/"last_install_summary.json"; say(p.read_text() if p.exists() else "No install summary yet.")
def health(data):
 say(f"Python: {sys.version.split()[0]} | Platform: {platform.platform()}")
 say(f"Catalog: {len(data['tools'])} entries across {len(data['categories'])} categories")
 say("Termux pkg: "+("available" if shutil.which("pkg") else "not found"))
 say("Go: "+(shutil.which("go") or "not found")); say("Rich UI: "+("enabled" if RICH else "plain-text fallback"))
 say("State directory: "+str(STATE_DIR))
 say(f"Detected executables: {sum(bool(installed(t)) for t in data['tools'])}/{len(data['tools'])} entries (some share commands)")
def main():
 try:data=load_catalog()
 except Exception as e: print("Catalog error:",e,file=sys.stderr); return 2
 if "--check" in sys.argv: health(data); return 0
 title()
 while True:
  c=menu("Main menu",["Browse categories","Search catalog","All tools","Installer","Environment / health","Credits and safety","Exit"])
  if c=="1":category(data)
  elif c=="2":search(data)
  elif c=="3":choose(data)
  elif c=="4":installer(data)
  elif c=="5":health(data)
  elif c=="6":
   say("SYN_LAUNCH is a launcher/catalog, not the author of the listed utilities.")
   say("Each entry links to a maintainer, package index, or repository search. Respect each project's license.")
   say("Use tools only within explicit authorization. Some entries need root, compatible hardware, or desktop Linux.")
  elif c in ("0","7"):break
  else:say("Invalid choice.")
 return 0
if __name__=="__main__":raise SystemExit(main())
