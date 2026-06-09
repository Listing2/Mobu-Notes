# Mobu Python 개발 환경 — pyfbsdk 스텁 설치
# Cursor에서 post/scripts/*.py 편집 시 자동완성용. 실행은 MotionBuilder Python Editor에서.

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Venv = Join-Path $Root ".venv"
$Req = Join-Path $Root "requirements-dev.txt"

py -3 -m venv $Venv
& (Join-Path $Venv "Scripts\python.exe") -m pip install -r $Req
Write-Host "Done. Select interpreter: post/scripts/.venv/Scripts/python.exe"
