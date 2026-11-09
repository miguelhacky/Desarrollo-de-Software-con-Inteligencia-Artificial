# Demo Vibe

Prototipo local con datos ficticios para la auditoría del taller. No usar en producción.

## Ejecutar en PowerShell

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:SECRET_KEY = "clave-de-prueba"
python app.py
```

Abrir http://127.0.0.1:5000.

