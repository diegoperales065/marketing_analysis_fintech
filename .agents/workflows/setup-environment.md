---
description: Configuración del entorno de desarrollo Python para el TFM
---

# Setup del Entorno de Desarrollo

## 1. Clonar el repositorio
```bash
git clone https://github.com/diegoperales065/marketing_analysis_fintech.git
cd marketing_analysis_fintech
```

## 2. Crear entorno virtual
```bash
python -m venv .venv
```

## 3. Activar entorno virtual
```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# Windows CMD
.venv\Scripts\activate.bat

# Linux / macOS
source .venv/bin/activate
```

## 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

## 5. Configurar variables de entorno
Crear archivo `.env` en la raíz del proyecto:
```
WORKSPACE=C:\ruta\completa\al\marketing_analysis_fintech
```

## 6. Verificar instalación
```bash
python -c "import pandas; import numpy; import sklearn; import xgboost; print('OK')"
```

## 7. Abrir notebook principal
```bash
jupyter notebook notebooks/TFM.ipynb
```
