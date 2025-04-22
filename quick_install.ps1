Write-Host "=== Media Downloader 一键安装脚本 ===" -ForegroundColor Green

# 安装 yt-dlp
python -m pip install --upgrade yt-dlp

# 克隆项目
if (Test-Path "media-downloader") {
    Remove-Item "media-downloader" -Recurse -Force
}
git clone https://github.com/anjwee/media-downloader.git
Set-Location media-downloader

# 安装依赖
python -m pip install -r requirements.txt

# 创建下载目录
if (-not (Test-Path "downloads")) {
    New-Item -ItemType Directory -Path "downloads"
}

# 运行程序
python src/downloader.py
