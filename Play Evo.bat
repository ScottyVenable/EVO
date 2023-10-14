@echo off

REM Display ASCII art for "EVO"
echo EEEEEE  V       V  OOOOO
echo E       V     V  O     O
echo EEEEEE   V   V   O     O
echo E         V V    O     O
echo EEEEEE     V      OOOOO
echo.

REM Prompt the user for a build number
set /p build_number="Build Number: "

REM Define the path to the builds folder
set "builds_folder=.\builds"

REM Search for the Python script in the builds folder
set "py_script=%builds_folder%\%build_number%.py"

if not exist "%py_script%" (
  echo The Python script %py_script% does not exist. Exiting.
  pause
  exit /b 1
)

echo Running %py_script%...
python "%py_script%"

pause
