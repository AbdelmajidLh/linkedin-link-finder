@echo off
rem Créer un environnement virtuel
python -m venv mon_env

rem Activer l'environnement virtuel (sous Windows)
call mon_env\Scripts\activate.bat

rem Installer les packages à partir du fichier requirements.txt
pip install -r ../requirements.txt

rem Lancer le build de l'application avec PyInstaller
pyinstaller --onefile ../main.py

rem Désactiver l'environnement virtuel
deactivate

rem Déplacer le fichier exécutable dans le dossier parent
Move-Item -Path .\Windows\dist\main.exe -Destination .\ -Force