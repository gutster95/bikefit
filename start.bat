@echo off
rem Doppelklick startet Bikefit im Browser (Windows). Beim ersten Mal wird alles installiert.
setlocal
cd /d "%~dp0"
chcp 65001 >nul

if exist ".venv\Scripts\python.exe" goto run

echo Erster Start: Bikefit wird eingerichtet (einige Minuten) ...
set "PY="
where py >nul 2>nul && set "PY=py -3"
if not defined PY (where python >nul 2>nul && set "PY=python")
if not defined PY goto nopython
%PY% -m venv .venv || goto fail
".venv\Scripts\python.exe" -m pip install --upgrade pip || goto fail
".venv\Scripts\python.exe" -m pip install -r requirements.txt || goto fail
".venv\Scripts\python.exe" -c "from bikefit.pose import model_path; model_path('heavy'); model_path('full')" || goto fail
if not exist videos mkdir videos

:run
echo Pruefe Pakete ...
".venv\Scripts\python.exe" -m pip install -q -r requirements.txt
echo Starte Bikefit, der Browser oeffnet sich gleich ...
".venv\Scripts\python.exe" -m bikefit web
pause
exit /b 0

:nopython
echo Python fehlt. Bitte von https://www.python.org/downloads/ installieren
echo und dabei "Add python.exe to PATH" anhaken. Danach start.bat erneut doppelklicken.
pause
exit /b 1

:fail
echo Installation fehlgeschlagen. Ordner .venv loeschen und start.bat erneut starten.
if exist ".venv" rmdir /s /q ".venv"
pause
exit /b 1
