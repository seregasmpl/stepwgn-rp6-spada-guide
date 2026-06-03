# Публикация справочника на GitHub (seregasmpl)
# Запуск из корня репозитория:  .\tools\publish-github.ps1
$ErrorActionPreference = "Stop"
$Owner = "seregasmpl"
$Repo = "stepwgn-rp6-spada-guide"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $Root
Write-Host "Repo root: $Root" -ForegroundColor Cyan

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Host "Установите GitHub CLI: winget install GitHub.cli" -ForegroundColor Red
    exit 1
}

$auth = gh auth status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Нужен вход в GitHub (откроется браузер)..." -ForegroundColor Yellow
    gh auth login -h github.com -p https -w
}

git remote set-url origin "https://github.com/$Owner/$Repo.git"

$exists = gh repo view "$Owner/$Repo" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Создаю репозиторий $Owner/$Repo ..." -ForegroundColor Cyan
    gh repo create $Repo --public --source=. --remote=origin --description "Honda STEP WGN RP6 SPADA — справочник JP→RU (приборка, салон, Honda CONNECT)"
} else {
    Write-Host "Репозиторий уже есть: https://github.com/$Owner/$Repo" -ForegroundColor Green
}

Write-Host "Push (~100 MB, несколько минут)..." -ForegroundColor Cyan
git push -u origin main

Write-Host "Включаю GitHub Pages (Actions)..." -ForegroundColor Cyan
gh api -X POST "repos/$Owner/$Repo/pages" -f build_type=workflow 2>$null

Write-Host ""
Write-Host "Готово. Сайт появится через 1-3 мин после Actions:" -ForegroundColor Green
Write-Host "  https://$Owner.github.io/$Repo/" -ForegroundColor White
Write-Host "  https://$Owner.github.io/$Repo/STEPWGN-SPADA-guide-iphone.html" -ForegroundColor White
Write-Host "Проверка: https://github.com/$Owner/$Repo/actions" -ForegroundColor DarkGray
