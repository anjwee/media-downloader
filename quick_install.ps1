Write-Host "=== Media Downloader 一键安装脚本 ===" -ForegroundColor Green

# 安装 yt-dlp
Write-Host "正在安装 yt-dlp..." -ForegroundColor Yellow
python -m pip install --upgrade yt-dlp

# 克隆项目
Write-Host "正在克隆项目..." -ForegroundColor Yellow
if (Test-Path "media-downloader") {
    Remove-Item "media-downloader" -Recurse -Force
}
git clone https://github.com/anjwee/media-downloader.git
Set-Location media-downloader

# 安装依赖
Write-Host "正在安装依赖..." -ForegroundColor Yellow
python -m pip install -r requirements.txt

# 创建下载目录
if (-not (Test-Path "downloads")) {
    New-Item -ItemType Directory -Path "downloads"
}

# 创建 yt.bat 文件
Write-Host "正在创建快捷命令..." -ForegroundColor Yellow
$scriptPath = $PWD.Path
$batContent = @"
@echo off
cd /d "$scriptPath"
python src/downloader.py
"@

# 创建 yt.bat 在系统 PATH 目录中
$batPath = "C:\Windows\yt.bat"
$batContent | Set-Content -Path $batPath -Encoding ASCII

Write-Host "`n安装完成！" -ForegroundColor Green
Write-Host "您现在可以在任何位置使用 'yt' 命令来启动下载器。" -ForegroundColor Green
Write-Host "是否现在运行下载器？(Y/N)" -ForegroundColor Yellow
$choice = Read-Host "> "

if ($choice -eq "Y" -or $choice -eq "y") {
    python src/downloader.py
} else {
    Write-Host "您可以稍后使用 'yt' 命令启动下载器" -ForegroundColor Cyan
}