@echo off
pyinstaller --noconsole --onefile --add-data "florence;florence" main.py
