Param(
    [switch]$Lock
)

Write-Host "== Diabetic Retinopathy App Setup =="

# Ensure Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python is not installed or not in PATH. Install Python 3.9+ and retry."
    exit 1
}

# Create virtual environment
$venvPath = ".\.venv"
if (-not (Test-Path $venvPath)) {
    Write-Host "Creating virtual environment at $venvPath"
    python -m venv $venvPath
}

# Activate
$activate = Join-Path $venvPath "Scripts\Activate.ps1"
if (-not (Test-Path $activate)) {
    Write-Error "Virtualenv activation script not found: $activate"
    exit 1
}
. $activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
if ($Lock) {
    if (Test-Path "requirements-lock.txt") {
        Write-Host "Installing exact locked dependencies"
        pip install -r requirements-lock.txt
    } else {
        Write-Warning "requirements-lock.txt not found; installing from requirements.txt"
        pip install -r requirements.txt
    }
} else {
    pip install -r requirements.txt
}

# Git LFS for model files
if (Test-Path ".gitattributes") {
    Write-Host "Ensuring Git LFS is installed and pulling large files"
    if (Get-Command git -ErrorAction SilentlyContinue) {
        git lfs install | Out-Null
        try { git lfs pull | Out-Null } catch { Write-Warning "git lfs pull failed. If models are missing, fetch manually." }
    }
}

Write-Host "✅ Setup complete. To run: .\\run.ps1"