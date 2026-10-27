@echo off
setlocal
cd /d "%~dp0"

rem 优先用 DSH 自带的 Python（自带 Pillow），找不到再退回系统 python
set "PY=D:\software\DSH Desktop\resources\office-runtime\primary-runtime\dependencies\python\python.exe"
if not exist "%PY%" set "PY=python"

echo ==========================================
echo  Step 1/3  Generating thumbnails + manifest
echo ==========================================
"%PY%" build.py
if errorlevel 1 (
  echo.
  echo [ERROR] build failed, see message above.
  echo          Maybe the image file is broken.
  pause
  exit /b 1
)

echo.
echo ==========================================
echo  Step 2/3  Committing changes
echo ==========================================
git add -A
git commit -m "update images"

echo.
echo ==========================================
echo  Step 3/3  Pushing to GitHub
echo ==========================================
git push
if errorlevel 1 (
  echo.
  echo [NOTE] If this is the first push, a browser window should open
  echo        asking you to sign in to GitHub.
  echo        Sign in, then double-click this file again.
  echo.
  echo        If it still fails, copy the error message and send it to me.
  pause
  exit /b 1
)

echo.
echo ==========================================
echo  Done! The site will update in 1-2 minutes.
echo ==========================================
pause
