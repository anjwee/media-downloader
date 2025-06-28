# Media Downloader

一个简单的媒体下载工具，支持从多个平台下载视频和音频。

## 一键安装和运行

### Linux/Mac 用户
打开终端，复制粘贴下面的命令：
```bash
curl -fsSL https://raw.githubusercontent.com/anjwee/media-downloader/main/quick_install.sh | bash
```
### Linux/Mac 强制安装
```bash
pip install yt_dlp --break-system-packages
```

### Windows 用户 
打开 PowerShell，复制粘贴下面的命令：
```powershell
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/anjwee/media-downloader/main/quick_install.ps1" -OutFile "quick_install.ps1"; .\quick_install.ps1
```

## 功能特点

- 支持多种下载质量选项
- 支持视频和音频下载
- 实时显示下载进度
- 友好的命令行界面
- 支持错误处理和提示

## 手动安装说明

1. 安装 yt-dlp（必需）：
```bash
pip install yt-dlp
```
```bash
sudo apt install ffmpeg
```
2. 克隆仓库：
```bash
git clone https://github.com/anjwee/media-downloader.git
cd media-downloader
```

3. 安装其他依赖：
```bash
pip install -r requirements.txt
```

## 前置要求

- Python 3.6 或更高版本
- pip（Python包管理器）
- yt-dlp（视频下载核心组件）
- FFmpeg（用于视频处理，如果需要下载最佳质量视频）

## 使用方法

1. 运行程序：
```bash
python src/downloader.py
```

安装完成后，您可以：

• 直接使用 `yt` 命令启动下载器

• 如果 `yt` 命令不生效，请重新打开终端或运行 `source ~/.bashrc`

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

MIT License © [anjwee](https://github.com/anjwee)
