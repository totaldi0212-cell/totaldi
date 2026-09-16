@echo off
REM 윈도우용 - 더블클릭하면 클로드 코드가 열리면서 바로 블로그를 씁니다.
cd /d "%~dp0.."
where claude >nul 2>nul
if errorlevel 1 (
  echo 클로드 코드가 설치되어 있지 않습니다.
  echo 설치: https://claude.com/claude-code
  pause
  exit /b 1
)
if "%1"=="--headless" (
  claude -p "/blog-daily" --permission-mode acceptEdits
) else (
  claude "/blog-daily"
)
