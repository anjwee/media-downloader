#!/bin/bash
echo "=== Media Downloader 一键安装脚本 ==="

# 安装必需的包
if command -v apt-get &> /dev/null; then
    sudo apt-get update && sudo apt-get install -y python3 python3-pip git
elif command -v yum &> /dev/null; then
    sudo yum install -y python3 python3-pip git
fi

# 安装 yt-dlp
python3 -m pip install --upgrade yt-dlp

# 克隆项目
rm -rf media-downloader
git clone https://github.com/anjwee/media-downloader.git
cd media-downloader

# 安装依赖
python3 -m pip install -r requirements.txt

# 创建下载目录
mkdir -p downloads

# 运行程序
python3 src/downloader.py
