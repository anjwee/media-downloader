#!/bin/bash
echo "=== Media Downloader 一键安装脚本 ==="

# 设置安装目录
INSTALL_DIR="$HOME/media-downloader"

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

# 创建并进入安装目录
echo "正在创建安装目录..."
rm -rf "$INSTALL_DIR"
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR" || exit 1

# 克隆项目
echo "正在克隆项目..."
git clone https://github.com/anjwee/media-downloader.git .

# 安装依赖
echo "正在安装依赖..."
python3 -m pip install -r requirements.txt

# 创建下载目录
mkdir -p downloads

# 创建快捷命令
echo "创建快捷命令 'yt'..."
COMMAND_ALIAS="alias yt='cd $INSTALL_DIR && python3 src/downloader.py'"

# 添加到多个可能的配置文件中
for config_file in ~/.bashrc ~/.bash_profile ~/.zshrc; do
    if [ -f "$config_file" ]; then
        # 移除旧的别名（如果存在）
        sed -i '/alias yt=/d' "$config_file"
        # 添加新的别名
        echo "$COMMAND_ALIAS" >> "$config_file"
    fi
done

# 创建全局命令
echo "创建全局命令..."
sudo tee /usr/local/bin/yt << EOL
#!/bin/bash
cd "$INSTALL_DIR" && python3 src/downloader.py
EOL

# 使脚本可执行
sudo chmod +x /usr/local/bin/yt

echo -e "\n安装完成！"
echo "您可以使用以下方式运行下载器："
echo "1. 输入 'yt' 命令"
echo "2. 或者进入 media-downloader 目录运行 'python3 src/downloader.py'"
echo -e "\n是否现在运行下载器？(y/n)"
read -p "> " choice

if [[ $choice == "y" || $choice == "Y" ]]; then
    cd "$INSTALL_DIR" && python3 src/downloader.py
else
    echo "您可以稍后使用 'yt' 命令启动下载器"
fi