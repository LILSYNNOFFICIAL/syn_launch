#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
printf '\033[1;36mSYN_LAUNCH bootstrap\033[0m\n'
if [[ ! -d /data/data/com.termux/files/usr ]]; then
  echo "This bootstrap is for Termux on Android. Run main.py with Python elsewhere."
  exit 1
fi
pkg update -y
pkg install -y python git
BASE="$HOME/syn_launch"
if [[ -d "$BASE/.git" ]]; then
  git -C "$BASE" pull --ff-only
elif [[ -e "$BASE" ]]; then
  echo "$BASE exists but is not a Git checkout. Move it aside first."
  exit 1
else
  git clone https://github.com/LILSYNNOFFICIAL/syn_launch.git "$BASE"
fi
mkdir -p "$HOME/.syn_launch" "$HOME/.local/bin"
python -m venv "$HOME/.syn_launch/venv" || { echo "venv creation failed; try pkg reinstall python"; exit 1; }
"$HOME/.syn_launch/venv/bin/pip" install --upgrade pip
"$HOME/.syn_launch/venv/bin/pip" install rich
cat > "$HOME/.local/bin/syn-launch" <<EOF
#!/data/data/com.termux/files/usr/bin/bash
exec "$HOME/.syn_launch/venv/bin/python" "$BASE/main.py" "\$@"
EOF
chmod +x "$HOME/.local/bin/syn-launch"
case ":$PATH:" in *":$HOME/.local/bin:"*) ;; *) echo 'Add to ~/.bashrc: export PATH="$HOME/.local/bin:$PATH"' ;; esac
echo "Files: $BASE"
echo "Run: python $BASE/main.py"
echo "Or: syn-launch (after adding ~/.local/bin to PATH)"
echo "Catalog entries do not guarantee every tool works on every Android device."
