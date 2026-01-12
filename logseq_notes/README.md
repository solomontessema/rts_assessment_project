# Project Setup Instructions

Follow the steps below to set up the project environment and Jupyter kernel.

## 1. Create and activate the virtual environment

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1     # Windows PowerShell
```

## 2. Install dependencies

```bash
pip install -r requirements.txt

```

## 3. Register the Jupyter kernel

```bash
python -m ipykernel install --user --name rts_env --display-name "Python (rts_env)"
```