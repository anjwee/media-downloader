#!/bin/bash
echo "=== Media Downloader 一键安装脚本 ==="

# 安装必需的包
if command -v apt-get &> /dev/null; then
    echo "正在安装必要的软件包..."
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip git python-is-python3
elif command -v yum &> /dev/null; then
    echo "正在安装必要的软件包..."
    sudo yum install -y python3 python3-pip git
fi

# 安装 yt-dlp
echo "正在安装 yt-dlp..."
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade yt-dlp

# 克隆项目
echo "正在克隆项目..."
rm -rf media-downloader
git clone https://github.com/anjwee/media-downloader.git
cd media-downloader

# 安装依赖
echo "正在安装依赖..."
python3 -m pip install -r requirements.txt

# 创建下载目录
mkdir -p downloads

# 创建快捷命令
echo "创建快捷命令 'yt'..."
echo 'alias yt="python3 '$(pwd)'/src/downloader.py"' >> ~/.bashrc
echo 'alias yt="python3 '$(pwd)'/src/downloader.py"' >> ~/.zshrc
source ~/.bashrc 2>/dev/null || source ~/.zshrc 2>/dev/null

# 运行程序
echo "启动下载器..."
python3 src/downloader.py

echo -e "\n安装完成！现在您可以使用 'yt' 命令来启动下载器。"
echo "如果 'yt' 命令不生效，请重新打开终端或运行 'source ~/.bashrc'"
