# Editverse AI Studio

A Streamlit-based media studio that removes photo backgrounds with `rembg` and applies basic video effects (Black & White, speed change, mirror) using MoviePy. The UI now reports how much background was removed and runs on [Streamlit](https://streamlit.io).

## Prerequisites
- Python 3.11 (matching the virtual environment and Streamlit Cloud runtime)
- Git
- [Streamlit Cloud](https://streamlit.io/cloud) account for deployment (optional; the project also runs locally)

## Setup (local)
1. Clone the repo and enter it:
   ```bash
   git clone https://github.com/AnmolBudhewar8995/Editverse.git
   cd Editverse
   ```
2. Create and activate a Python 3.11 virtual environment (the repo already includes `.venv` in `.gitignore`):
   ```bash
   python3.11 -m venv .venv
   source .venv/bin/activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Streamlit app locally:
   ```bash
   streamlit run app.py
   ```
   The first run downloads the `u2net.onnx` model to `~/.u2net`. Background removal will show the percentage of fully transparent pixels.

## Git workflow
- Before pushing, make sure the remote is in sync with the latest commits:
  ```bash
  git fetch origin
  git pull --rebase origin main
  ```
  This avoids the rejection you saw because the remote already had commits.
- Commit your changes:
  ```bash
  git add .gitignore requirements.txt app.py README.md
  git commit -m "chore: document deployment"
  ```
- Push to GitHub (after resolving any upstream changes):
  ```bash
  git push -u origin main
  ```

## Deployment (Streamlit Cloud)
1. Log into [Streamlit Cloud](https://streamlit.io/cloud) and select "New app." Connect to the `AnmolBudhewar8995/Editverse` repo and choose the `main` branch.
2. Set the "Main file" to `app.py` and the Python version to 3.11.
3. Streamlit Cloud will install from `requirements.txt` and run `streamlit run app.py`. The app caches the `u2net` model after the first launch, so deployments may take slightly longer initially.

## Notes
- The app uses `rembg` for images and MoviePy for video edits; both can be resource intensive, so avoid very large uploads.
- Keep `.venv/`, `.u2net/`, and model artifacts out of Git (`.gitignore` already handles this).
- For improved startup speed, you can pre-download `u2net.onnx` in a build step or within Streamlit Cloud using an `init` script.
