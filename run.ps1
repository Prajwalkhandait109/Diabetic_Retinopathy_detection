Write-Host "== Starting Diabetic Retinopathy App =="

# Activate venv if present
$venvPath = ".\.venv"
if (Test-Path $venvPath) {
    $activate = Join-Path $venvPath "Scripts\Activate.ps1"
    if (Test-Path $activate) { . $activate }
}

# Run Flask app
$env:FLASK_ENV = "production"
python app.py