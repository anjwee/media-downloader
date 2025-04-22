# Media Downloader

一个简单的媒体下载工具，支持从多个平台下载视频和音频。

## 功能特点

- 支持多种下载质量选项
- 支持视频和音频下载
- 实时显示下载进度
- 友好的命令行界面
- 支持错误处理和提示

### Linux/Mac 用户
打开终端，复制粘贴下面的命令：
```bash
curl -fsSL https://raw.githubusercontent.com/anjwee/media-downloader/main/quick_install.sh | bash

### Windows 用户 
打开 PowerShell，复制粘贴下面的命令：
```bash
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/anjwee/media-downloader/main/quick_install.ps1" -OutFile "quick_install.ps1"; .\quick_install.ps1

## 安装说明

1. 安装yt-dlp（必需）：
pip install yt-dlp

Code

2. 克隆仓库：
git clone https://github.com/anjwee/media-downloader.git cd media-downloader

Code

3. 安装其他依赖：
pip install -r requirements.txt

Code

## 前置要求

- Python 3.6 或更高版本
- pip（Python包管理器）
- yt-dlp（视频下载核心组件）
- FFmpeg（用于视频处理，如果需要下载最佳质量视频）

## 使用方法

1. 运行程序：
python src/downloader.py

Code

2. 按照提示输入视频URL
3. 选择下载质量选项：
- 1: 最高质量的视频和音频
- 2: 最佳视频和音频（分别下载后合并）
- 3: 仅下载音频（MP3格式）
- 4: 最低质量（节省空间）

## 注意事项

- 确保所有依赖都已正确安装
- 如果遇到视频处理错误，请确认是否已安装FFmpeg
- 下载的文件将保存在 downloads 目录中
- 某些视频可能因版权限制无法下载

## 故障排除

如果遇到 "yt-dlp command not found" 错误：
1. 确保已执行 'pip install yt-dlp'
2. 重启命令行或终端
3. 如果仍然报错，尝试使用 'python -m pip install yt-dlp'

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License
