import yt_dlp
import os
import sys
import time
import shutil
import subprocess
from typing import Dict, Any
from datetime import datetime
from config import get_format_options
from utils import progress_hook, get_error_message

class MediaDownloader:
    def __init__(self):
        self.ydl_opts: Dict[str, Any] = {}
        self.start_time = datetime.utcnow()
        # 下载历史文件路径
        self.download_history_file = os.path.join(
            os.path.expanduser('~/Downloads'), 
            'media_downloader_history.txt'
        )
        # cookies 文件路径 (与项目文件在同一目录)
        self.cookies_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'cookies.txt'
        )

    def check_cookies(self) -> bool:
        """检查 cookies 文件是否存在且有效"""
        if not os.path.exists(self.cookies_file):
            return False
            
        try:
            with open(self.cookies_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                # 仅检查文件是否为 Netscape 格式且包含 YouTube domain
                is_valid = (content.startswith('# Netscape HTTP Cookie File') and
                          '.youtube.com' in content)
                if is_valid:
                    print("已找到有效的 cookies 文件")
                return is_valid
        except Exception as e:
            print(f"检查 cookies 文件时出错: {str(e)}")
            return False

    def download_media(self, url: str, format_choice: str) -> None:
        max_retries = 3
        retry_count = 0
        last_error = None
        title = "未知标题"
        
        while retry_count < max_retries:
            try:
                output_path = os.path.expanduser('~/Downloads')
                if not os.path.exists(output_path):
                    os.makedirs(output_path)
                
                # 配置下载选项
                self.ydl_opts = get_format_options(format_choice)
                
                # 基本配置
                base_opts = {
                    'progress_hooks': [progress_hook],
                    'outtmpl': f'{output_path}/%(title)s.%(ext)s',
                    'fragment-retries': 10,
                    'retries': 10,
                    'file_access_retries': 10,
                    'quiet': False,
                    'verbose': False,
                    'no_warnings': True,
                    'socket_timeout': 30,
                    'concurrent_fragment_downloads': 1,
                    'http_chunk_size': 10485760,
                    'extract_flat': False,
                    'cookiesfrombrowser': None,  # 禁用浏览器 cookies
                    'http_headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Language': 'en-us,en;q=0.5',
                        'Sec-Fetch-Mode': 'navigate',
                        'Accept-Encoding': 'gzip, deflate',
                        'DNT': '1',
                    }
                }
                
                # 添加 cookies 支持
                if self.check_cookies():
                    base_opts['cookiefile'] = self.cookies_file
                    print("成功加载 cookies 文件")
                else:
                    print("警告: 未找到有效的 cookies 文件，某些视频可能无法下载")
                
                # 添加代理支持
                proxy_settings = self.get_proxy_settings()
                if proxy_settings:
                    base_opts.update(proxy_settings)
                    print(f"使用代理: {proxy_settings['proxy']}")
                
                # 更新下载选项
                self.ydl_opts.update(base_opts)
                
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
                
                if 'Sign in to confirm' in str(e):
                    print("\n需要 YouTube cookies 来验证身份，请：")
                    print("1. 确保已登录 YouTube")
                    print("2. 输入 'w' 重新导入 cookies")
                    break
                
                if retry_count < max_retries:
                    wait_time = 5 * retry_count
                    print(f'将在 {wait_time} 秒后重试...')
                    time.sleep(wait_time)
                    print('正在重试...')
                else:
                    print('\n下载失败，建议：')
                    print('1. 检查网络连接是否稳定')
                    print('2. 尝试使用其他格式选项（如选项4：最低质量）')
                    print('3. 确认视频是否可以正常访问')
                    print('4. 更新 cookies 文件')
                    print('5. 检查 VPS 是否可以访问 YouTube')
                    print('6. 检查代理设置是否正确')
                    self.log_download(url, title, False, last_error)
                    break

    # [其余方法保持不变...]

def main():
    downloader = MediaDownloader()
    print_welcome()
    
    while True:
        try:
            url = input('\n请输入媒体URL (输入 q 退出, w 加载cookies, e 配置代理): ').strip()
            
            if url.lower() == 'q':
                print('\n感谢使用，再见！')
                break
            elif url.lower() == 'w':
                # 删除旧的 cookies 文件
                if os.path.exists(downloader.cookies_file):
                    os.remove(downloader.cookies_file)
                    print("已删除旧的 cookies 文件")
                load_cookies()
                continue
            elif url.lower() == 'e':
                configure_proxy()
                continue
            
            if not url:
                continue
                
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