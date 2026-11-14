# Working together with Git and GitHub

## One-time setup (per person)
```bash
git config --global user.name  "Your Name"
git config --global user.email "you@example.com"
```
Authenticate to GitHub with an SSH key (`ssh-keygen -t ed25519`, then add `~/.ssh/id_ed25519.pub`
at GitHub > Settings > SSH keys) or with the GitHub CLI (`gh auth login`).

## Creating the repository (ONE person does this)
1. On github.com click **New repository**, name it `trafic-intelligent`, keep it **empty**
   (no README, no .gitignore, we already have them), private or public.
2. In the project folder:
```bash
git init -b main
git add .
git commit -m "Initial project structure"
git remote add origin git@github.com:<USER>/trafic-intelligent.git
git push -u origin main
```
3. Repo **Settings > Collaborators**: add your teammates.

## Daily workflow
Never work directly on `main`. Use one branch per task.
```bash
git checkout main && git pull            # get the latest version
git checkout -b feature/line-counting    # new branch for your task
# ... edit, test ...
git add <files>
git commit -m "Add virtual line counting"
git push -u origin feature/line-counting
```
Then open a **Pull Request** on GitHub and ask a teammate to review it before merging.
Reviewing each other's code is one of the best ways to learn the whole pipeline.

## Rules of thumb
- Small, frequent commits with clear messages.
- Never commit videos, model weights (`*.pt`), passwords or `.venv`; `.gitignore` covers them.
- Resolve conflicts calmly: `git pull`, edit the conflicted files, `git add`, `git commit`.
- Share videos through a shared drive and note the link in `docs/DATA.md`.
