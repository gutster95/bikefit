@echo off
rem Double-click to start Bikefit in the browser (Windows). The first start
rem installs Python and all packages via uv, without admin rights.
setlocal
cd /d "%~dp0"
chcp 65001 >nul
set "PYTHON_VERSION=3.13"
set "VPY=.venv\Scripts\python.exe"

if not exist "%VPY%" echo First start: setting up Bikefit (a few minutes) ...

call :find_uv
if not defined UV (
  echo Installing uv ^(downloads Python, no admin rights needed^) ...
  powershell -NoProfile -ExecutionPolicy ByPass -Command "$env:UV_NO_MODIFY_PATH=1; irm https://astral.sh/uv/install.ps1 | iex" >nul
  call :find_uv
)

if defined UV (
  if not exist "%VPY%" (
    echo Setting up Python %PYTHON_VERSION% ...
    "%UV%" venv --quiet --python %PYTHON_VERSION% .venv || goto fail
  )
  echo Checking packages ...
  "%UV%" pip install --quiet --python "%VPY%" -r requirements.txt || goto fail
) else (
  rem no uv (e.g. offline): fall back to an existing environment or the system Python
  if not exist "%VPY%" (
    where py >nul 2>nul && (py -3 -m venv .venv || goto fail)
    if not exist "%VPY%" (where python >nul 2>nul && (python -m venv .venv || goto fail))
    if not exist "%VPY%" goto nopython
  )
  echo Checking packages ...
  "%VPY%" -m pip install --quiet -r requirements.txt || goto fail
)

"%VPY%" -c "from bikefit.pose import model_path; model_path('heavy'); model_path('full')" || goto fail
if not exist videos mkdir videos

echo Starting Bikefit, the browser opens in a moment ...
"%VPY%" -m bikefit web
pause
exit /b 0

:find_uv
set "UV="
for /f "delims=" %%i in ('where uv 2^>nul') do if not defined UV set "UV=%%i"
if not defined UV if exist "%USERPROFILE%\.local\bin\uv.exe" set "UV=%USERPROFILE%\.local\bin\uv.exe"
if not defined UV if exist "%USERPROFILE%\.cargo\bin\uv.exe" set "UV=%USERPROFILE%\.cargo\bin\uv.exe"
exit /b 0

:nopython
echo Could not install Python. Check the internet connection and start start.bat again.
pause
exit /b 1

:fail
echo Setup failed. Check the internet connection and start start.bat again.
pause
exit /b 1
