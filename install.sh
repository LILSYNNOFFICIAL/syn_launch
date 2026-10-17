#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

# Do not let inherited Python/pip configuration silently redirect bootstrap code.
unset PYTHONPATH PYTHONHOME PYTHONSTARTUP PIP_INDEX_URL PIP_EXTRA_INDEX_URL PIP_TRUSTED_HOST PIP_CONFIG_FILE PIP_CERT PIP_CLIENT_CERT PIP_NO_VERIFY_CERTS
export GIT_CONFIG_NOSYSTEM=1
export GIT_CONFIG_GLOBAL=/dev/null
printf '\033[1;36mSYN_LAUNCH bootstrap\033[0m\n'
if [[ ! -d /data/data/com.termux/files/usr ]]; then
  echo "This bootstrap is for Termux on Android. Run main.py with Python elsewhere."
  exit 1
fi
pkg update -y
pkg install -y python git
BASE="$HOME/syn_launch"
if [[ -d "$BASE/.git" ]]; then
  ORIGIN="$(git -C "$BASE" remote get-url origin 2>/dev/null || true)"
  if [[ "$ORIGIN" != "https://github.com/LILSYNNOFFICIAL/syn_launch.git" ]]; then
    echo "Refusing update: origin is not the official SYN_LAUNCH HTTPS repository."
    exit 1
  fi
  BRANCH="$(git -C "$BASE" branch --show-current)"
  if [[ "$BRANCH" != "main" ]]; then
    echo "Refusing update: checkout must be on the main branch."
    exit 1
  fi
  if ! git -C "$BASE" diff --quiet || ! git -C "$BASE" diff --cached --quiet || [[ -n "$(git -C "$BASE" ls-files --others --exclude-standard)" ]]; then
    echo "Refusing update: checkout has local changes. Back them up or commit them first."
    exit 1
  fi
  git -C "$BASE" -c core.hooksPath=/dev/null fetch --no-tags origin main
  git -C "$BASE" -c core.hooksPath=/dev/null merge --ff-only FETCH_HEAD
elif [[ -e "$BASE" ]]; then
  echo "$BASE exists but is not a Git checkout. Move it aside first."
  exit 1
else
  git -c core.hooksPath=/dev/null clone --branch main --single-branch -- https://github.com/LILSYNNOFFICIAL/syn_launch.git "$BASE"
fi
mkdir -p "$HOME/.syn_launch" "$HOME/.local/bin"
python -m venv "$HOME/.syn_launch/venv" || { echo "venv creation failed; try pkg reinstall python"; exit 1; }
"$HOME/.syn_launch/venv/bin/python" -m pip install --isolated --disable-pip-version-check --index-url https://pypi.org/simple --upgrade pip
"$HOME/.syn_launch/venv/bin/python" -m pip install --isolated --disable-pip-version-check --index-url https://pypi.org/simple -r "$BASE/requirements.txt"
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
