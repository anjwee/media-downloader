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
        # ... 前面的代码保持不变 ...

def configure_proxy():
    """配置代理"""
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
    """加载 cookies"""
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
    print('- 输入 w 文件加载 cookies')
    print('- 输入 e 配置代理')
    print('- 输入 q 可随时退出程序')

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
                load_cookies()
                continue
            elif url.lower() == 'e':
                configure_proxy()
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