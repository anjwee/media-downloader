import yt_dlp
import os
import sys
import time
import shutil
from typing import Dict, Any
from datetime import datetime
from config import get_format_options
from utils import progress_hook, get_error_message

class MediaDownloader:
    def __init__(self):
        self.ydl_opts: Dict[str, Any] = {}
        self.start_time = datetime.utcnow()
        self.download_history_file = os.path.join(
            os.path.expanduser('~/Downloads'), 
            'media_downloader_history.txt'
        )
    
    def log_download(self, url: str, title: str, success: bool, error_msg: str = None):
        """记录下载历史"""
        try:
            with open(self.download_history_file, 'a', encoding='utf-8') as f:
                timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
                status = "成功" if success else "失败"
                log_entry = f"[{timestamp}] {status} - {title}\nURL: {url}\n"
                if error_msg:
                    log_entry += f"错误: {error_msg}\n"
                f.write(log_entry + "-"*50 + "\n")
        except Exception as e:
            print(f"警告: 无法记录下载历史 - {str(e)}")

    def download_media(self, url: str, format_choice: str) -> None:
        max_retries = 3
        retry_count = 0
        last_error = None
        title = "未知标题"
        
        while retry_count < max_retries:
            try:
                # 使用系统下载文件夹
                output_path = os.path.expanduser('~/Downloads')
                if not os.path.exists(output_path):
                    os.makedirs(output_path)
                
                # 配置下载选项
                self.ydl_opts = get_format_options(format_choice)
                self.ydl_opts.update({
                    'progress_hooks': [progress_hook],
                    'outtmpl': f'{output_path}/%(title)s.%(ext)s',
                    'fragment-retries': 10,        # 片段重试次数
                    'retries': 10,                 # 整体重试次数
                    'file_access_retries': 10,     # 文件访问重试次数
                    'quiet': False,                # 显示详细日志
                    'verbose': True,               # 显示更多调试信息
                    'socket_timeout': 30,          # 套接字超时时间
                    'concurrent_fragment_downloads': 1,  # 并发下载数
                    'http_chunk_size': 10485760,   # 10MB 块大小
                })
                
                with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                    print(f'\n正在获取媒体信息... (尝试 {retry_count + 1}/{max_retries})')
                    info = ydl.extract_info(url, download=False)
                    title = info.get('title', '未知标题')
                    duration = info.get('duration')
                    filesize = info.get('filesize')
                    
                    print(f'\n标题: {title}')
                    if duration:
                        minutes = duration // 60
                        seconds = duration % 60
                        print(f'时长: {minutes}分{seconds}秒')
                    if filesize:
                        size_mb = filesize / (1024 * 1024)
                        print(f'文件大小: {size_mb:.1f} MB')
                    
                    print('\n开始下载...')
                    print('下载过程中请勿关闭窗口...')
                    ydl.download([url])
                    
                    print('\n下载成功！')
                    self.log_download(url, title, True)
                    return
                    
            except Exception as e:
                retry_count += 1
                last_error = str(e)
                error_msg = get_error_message(e)
                print(f'\n下载出错 (尝试 {retry_count}/{max_retries}): {error_msg}')
                
                if retry_count < max_retries:
                    wait_time = 5 * retry_count  # 递增等待时间
                    print(f'将在 {wait_time} 秒后重试...')
                    time.sleep(wait_time)
                    print('正在重试...')
                else:
                    print('\n下载失败，建议：')
                    print('1. 检查网络连接是否稳定')
                    print('2. 尝试使用其他格式选项（如选项4：最低质量）')
                    print('3. 确认视频是否可以正常访问')
                    print('4. 尝试更新 yt-dlp (pip install --upgrade yt-dlp)')
                    print('5. 检查是否需要使用代理')
                    self.log_download(url, title, False, last_error)
                    break

def uninstall():
    """卸载程序"""
    try:
        # 删除 Windows 的快捷命令
        bat_path = "C:\\Windows\\yt.bat"
        if os.path.exists(bat_path):
            try:
                os.remove(bat_path)
                print("已删除快捷命令...")
            except PermissionError:
                print("无法删除快捷命令，需要管理员权限...")
        
        # 获取当前目录的上级目录（项目根目录）
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # 删除整个项目目录
        shutil.rmtree(current_dir)
        
        print("\n卸载成功！感谢您的使用！")
        print("按任意键退出...")
        input()
        sys.exit(0)
    except Exception as e:
        print(f"\n卸载过程中出现错误: {str(e)}")
        print("请手动删除项目文件夹。")
        print("按任意键退出...")
        input()
        sys.exit(1)

def show_menu():
    """显示菜单选项"""
    print('\n请选择下载格式：')
    print('1. 最高质量的视频和音频')
    print('2. 最佳视频和音频（分别下载后合并）')
    print('3. 仅下载音频（MP3格式）')
    print('4. 最低质量（节省空间）')
    print('5. 卸载程序')
    return input('请输入选项 (1-5): ')

def print_welcome():
    """打印欢迎信息"""
    print('='*50)
    print('欢迎使用 Media Downloader!')
    print(f'当前用户: {os.getenv("USERNAME", "未知用户")}')
    print(f'版本: 1.0.0')
    print(f'时间: {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")}')
    print('='*50)
    print('\n提示:')
    print('- 所有文件将保存到系统下载文件夹')
    print('- 如遇下载问题，将自动重试')
    print('- 输入 q 可随时退出程序')

def main():
    downloader = MediaDownloader()
    print_welcome()
    
    while True:
        try:
            url = input('\n请输入媒体URL (输入 q 退出): ')
            if url.lower() == 'q':
                print('\n感谢使用，再见！')
                break
                
            format_choice = show_menu()
            if format_choice == '5':
                confirm = input('\n确定要卸载程序吗？这将删除所有程序文件 (y/n): ')
                if confirm.lower() == 'y':
                    uninstall()
                continue
                
            if format_choice not in ['1', '2', '3', '4']:
                print('无效的选项，使用默认选项1')
                format_choice = '1'
                
            downloader.download_media(url, format_choice)
            print('\n文件已保存到:', os.path.expanduser('~/Downloads'))
            
        except KeyboardInterrupt:
            print('\n\n程序被用户中断')
            print('感谢使用，再见！')
            break
        except Exception as e:
            print(f'\n程序出错: {str(e)}')
            print('请重试或检查网络连接')
            continue

if __name__ == '__main__':
    main()