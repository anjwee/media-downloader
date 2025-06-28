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

def extract_filename_from_url(url):
    import os
    url_path = url.split('?')[0]
    base = os.path.basename(url_path)
    name, _ = os.path.splitext(base)
    return name or 'output'

def check_installation():
    try:
        result = subprocess.run(['pip', 'list'], capture_output=True, text=True)
        if 'media-downloader' in result.stdout:
            return True
        else:
            print("警告: media-downloader 未正确安装")
            return False
    except Exception as e:
        print(f"检查安装状态时出错: {str(e)}")
        return False

def print_welcome():
    print('='*50)
    print('欢迎使用 Media Downloader!')
    print(f'当前用户: anjwee')
    print(f'版本: 1.0.0')
    print(f'时间: 2025-04-22 20:06:32 UTC')
    print('='*50)
    print('\n提示:')
    print('- 所有文件将保存到系统下载文件夹')
    print('- 如遇下载问题，将自动重试')
    print('- 输入 w 加载cookies')
    print('- 输入 e 配置代理')
    print('- 输入 q 可随时退出程序')

def show_menu():
    print('\n请选择下载格式：')
    print('1. 最高质量的视频和音频')
    print('2. 最佳视频和音频（分别下载后合并）')
    print('3. 仅下载音频（MP3格式）')
    print('4. 最低质量（节省空间）')
    print('5. 卸载程序')
    return input('请输入选项 (1-5): ')

class MediaDownloader:
    def __init__(self):
        self.ydl_opts: Dict[str, Any] = {}
        self.start_time = datetime.utcnow()
        self.has_ffmpeg = False
        
        try:
            subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.has_ffmpeg = True
        except FileNotFoundError:
            print("\n警告: 未检测到 ffmpeg，某些功能可能受限")
            print("建议安装 ffmpeg:")
            print("- Debian/Ubuntu: sudo apt-get install ffmpeg")
            print("- CentOS/RHEL: sudo yum install ffmpeg")
            print("- Alpine: apk add ffmpeg\n")
        
        self.download_history_file = os.path.join(
            os.path.expanduser('~/Downloads'), 
            'media_downloader_history.txt'
        )
        self.cookies_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'cookies.txt'
        )

    def check_cookies(self) -> bool:
        if not os.path.exists(self.cookies_file):
            return False
        try:
            with open(self.cookies_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                is_valid = (content.startswith('# Netscape HTTP Cookie File') and
                          '.youtube.com' in content)
                if is_valid:
                    print("已找到有效的 cookies 文件")
                return is_valid
        except Exception as e:
            print(f"检查 cookies 文件时出错: {str(e)}")
            return False

    def log_download(self, url: str, title: str, success: bool, error_msg: str = None):
        try:
            if not os.path.exists(os.path.dirname(self.download_history_file)):
                os.makedirs(os.path.dirname(self.download_history_file))
            with open(self.download_history_file, 'a', encoding='utf-8') as f:
                timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
                status = "成功" if success else "失败"
                log_entry = f"[{timestamp}] {status} - {title}\nURL: {url}\n"
                if error_msg:
                    log_entry += f"错误: {error_msg}\n"
                f.write(log_entry + "-"*50 + "\n")
        except Exception as e:
            print(f"警告: 无法记录下载历史 - {str(e)}")

    def get_proxy_settings(self) -> Dict[str, str]:
        proxy_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'proxy.txt'
        )
        if os.path.exists(proxy_file):
            try:
                with open(proxy_file, 'r') as f:
                    proxy_url = f.read().strip()
                if proxy_url:
                    return {'proxy': proxy_url}
            except Exception as e:
                print(f"读取代理设置失败: {str(e)}")
        return {}

    def download_media(self, url: str, format_choice: str) -> None:
        max_retries = 3
        retry_count = 0
        last_error = None
        title = "未知标题"
        output_path = os.path.expanduser('~/Downloads')
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        while retry_count < max_retries:
            try:
                if format_choice == '2':
                    # 方案：用yt-dlp自动合并，不手动拼文件名
                    base_name = extract_filename_from_url(url)
                    ydl_opts = {
                        'format': 'bv*[height<=1080]+ba[ext=m4a]/bestvideo+bestaudio/best',
                        'outtmpl': f'{output_path}/{base_name}.%(ext)s',
                        'merge_output_format': 'mp4',
                        'quiet': False,
                        'progress_hooks': [progress_hook],
                        'no_warnings': True,
                        'ignoreerrors': True,
                    }
                    if self.check_cookies():
                        ydl_opts['cookiefile'] = self.cookies_file
                        print("成功加载 cookies 文件")
                    proxy_settings = self.get_proxy_settings()
                    if proxy_settings:
                        ydl_opts.update(proxy_settings)
                        print(f"使用代理: {proxy_settings['proxy']}")
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        print(f'\n正在获取媒体信息... (尝试 {retry_count + 1}/{max_retries})')
                        info = ydl.extract_info(url, download=False)
                        if not info:
                            raise Exception("无法获取视频信息")
                        title = info.get('title', '未知标题')
                        duration = info.get('duration')
                        print(f'\n标题: {title}')
                        if duration:
                            minutes = duration // 60
                            seconds = duration % 60
                            print(f'时长: {minutes}分{seconds}秒')
                        print('\n开始下载...')
                        print('下载过程中请勿关闭窗口...')
                        ydl.download([url])
                        print(f'\n下载成功并自动合并！文件已保存为: {output_path}/{base_name}.mp4')
                        self.log_download(url, title, True)
                        return
                else:
                    if format_choice == '3':
                        outtmpl = f'{output_path}/%(title)s.%(ext)s'
                        postprocessors = [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }]
                    else:
                        outtmpl = f'{output_path}/%(title)s.%(ext)s'
                        postprocessors = []
                    self.ydl_opts = {
                        'format': {
                            '1': 'bv*+ba/b',
                            '3': 'ba/b',
                            '4': 'worst'
                        }.get(format_choice, 'bv*+ba/b'),
                        'outtmpl': outtmpl,
                        'progress_hooks': [progress_hook],
                        'quiet': False,
                        'no_warnings': True,
                        'ignoreerrors': True
                    }
                    if postprocessors:
                        self.ydl_opts['postprocessors'] = postprocessors
                    if self.check_cookies():
                        self.ydl_opts['cookiefile'] = self.cookies_file
                        print("成功加载 cookies 文件")
                    proxy_settings = self.get_proxy_settings()
                    if proxy_settings:
                        self.ydl_opts.update(proxy_settings)
                        print(f"使用代理: {proxy_settings['proxy']}")
                    with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                        print(f'\n正在获取媒体信息... (尝试 {retry_count + 1}/{max_retries})')
                        info = ydl.extract_info(url, download=False)
                        if not info:
                            raise Exception("无法获取视频信息")
                        title = info.get('title', '未知标题')
                        duration = info.get('duration')
                        print(f'\n标题: {title}')
                        if duration:
                            minutes = duration // 60
                            seconds = duration % 60
                            print(f'时长: {minutes}分{seconds}秒')
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
                    wait_time = 5 * retry_count
                    print(f'将在 {wait_time} 秒后重试...')
                    time.sleep(wait_time)
                    print('正在重试...')
                else:
                    print('\n下载失败，建议：')
                    print('1. 直接使用命令: yt-dlp "视频URL"')
                    print('2. 检查网络连接是否稳定')
                    print('3. 尝试更新 yt-dlp: pip install --upgrade yt-dlp')
                    print('4. 检查代理设置是否正确')
                    self.log_download(url, title, False, last_error)
                    break

def configure_proxy():
    print("\n配置代理")
    print("请输入代理地址，例如：")
    print("http://username:password@proxy.example.com:8080")
    print("socks5://127.0.0.1:1080")
    proxy = input("\n请输入代理地址 (直接回车取消): ").strip()
    if not proxy:
        print("已取消代理配置")
        return
    try:
        proxy_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'proxy.txt'
        )
        with open(proxy_file, 'w', encoding='utf-8') as f:
            f.write(proxy)
        print("代理配置已保存！")
    except Exception as e:
        print(f"保存代理配置失败: {str(e)}")

def load_cookies():
    try:
        script_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'scripts',
            'import_cookies.py'
        )
        if os.path.exists(script_path):
            subprocess.run([sys.executable, script_path], check=True)
        else:
            print(f"错误: 找不到脚本文件 {script_path}")
    except subprocess.CalledProcessError as e:
        print(f"运行 cookies 导入脚本失败: {str(e)}")
    except Exception as e:
        print(f"加载 cookies 时出错: {str(e)}")

def uninstall():
    try:
        bat_path = "C:\\Windows\\yt.bat"
        if os.path.exists(bat_path):
            try:
                os.remove(bat_path)
                print("已删除快捷命令...")
            except PermissionError:
                print("无法删除快捷命令，需要管理员权限...")
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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

def main():
    check_installation()
    downloader = MediaDownloader()
    print_welcome()
    while True:
        try:
            url = input('\n请输入媒体URL (输入 q 退出, w 加载cookies, e 配置代理): ').strip()
            if url.lower() == 'q':
                print('\n感谢使用，再见！')
                break
            elif url.lower() == 'w':
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
