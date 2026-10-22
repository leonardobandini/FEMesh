@echo off
rem SPDX-License-Identifier: GPL-2.0-or-later
setlocal
if /I "%~1"=="verify" (
  "%~dp0SQMPluginInstaller.exe" verify
  exit /b
)
"%~dp0SQMPluginInstaller.exe" install
if errorlevel 1 (
  echo Installation failed.
  pause
  exit /b 1
)
pause
