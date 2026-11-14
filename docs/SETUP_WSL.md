# Setting up WSL2 (Windows)

Do these steps **once per person**. Each teammate does them on their own PC.

## 1. Install WSL2 with Ubuntu
Open **PowerShell as administrator** and run:
```powershell
wsl --install -d Ubuntu-24.04
```
Reboot if asked, then open "Ubuntu" from the Start menu and create a Linux username and password.
Check that it is version 2:
```powershell
wsl -l -v
```
If VERSION shows 1: `wsl --set-version Ubuntu-24.04 2`.

## 2. (Optional) GPU
If you have an NVIDIA GPU, update the **Windows** NVIDIA driver. Do **not** install a Linux driver
inside WSL. Test inside Ubuntu with `nvidia-smi`. No GPU? Everything still works on CPU.

## 3. Work in the Linux filesystem
Clone the project in your Linux home (`~`), **not** in `/mnt/c/...`. Disk access across the
Windows boundary is very slow, and videos make it worse.

## 4. Install the tools
```bash
cd ~
git clone <URL_OF_YOUR_REPO> trafic-intelligent
cd trafic-intelligent
bash setup_wsl.sh
```
The script installs system packages, creates `.venv`, installs the Python libraries and prints a
version check.

## 5. Use VS Code with WSL
Install VS Code on Windows and the "WSL" extension. From Ubuntu: `code .` opens the project
with Linux tools. In VS Code choose the interpreter `.venv/bin/python`.

## 6. PostgreSQL (needed from the database step onwards)
```bash
sudo service postgresql start
sudo -u postgres psql -c "CREATE USER trafic WITH PASSWORD 'choose_a_password';"
sudo -u postgres psql -c "CREATE DATABASE trafic OWNER trafic;"
psql -h localhost -U trafic -d trafic -f src/db/schema.sql
```
Never commit the password. Put connection settings in a local `.env` file (already ignored by Git).
WSL does not always start services automatically: rerun `sudo service postgresql start` after a reboot.

## Troubleshooting
- `ImportError: libGL.so.1`: run `sudo apt install -y libgl1 libglib2.0-0`.
- `cv2.imshow` shows nothing: needs Windows 11 (WSLg). On Windows 10, write videos to files instead.
- Very slow disk: the project is probably under `/mnt/c`. Move it to `~`.
