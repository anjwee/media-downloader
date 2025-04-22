import yt_dlp
import os
from typing import Dict, Any
from config import get_format_options
from utils import progress_hook, get_error_message

class MediaDownloader:
    def __init__(self):
        self.ydl_opts: Dict[str, Any] = {}
    
    def download_media(self, url: str, format_choice: str, output_path: str = './downloads') -> None:
        try:
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            
            # 获取下载选项并添加进度钩子
            self.ydl_opts = get_format_options(format_choice)
            self.ydl_opts.update({
                'progress_hooks': [progress_hook],
                'outtmpl': f'{output_path}/%(title)s.%(ext)s'
            })
            
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                print('正在获取媒体信息...')
                info = ydl.extract_info(url, download=False)
                title = info.get('title', '未知标题')
                duration = info.get('duration')
                
                print(f'\n标题: {title}')
                if duration:
                    minutes = duration // 60
                    seconds = duration % 60
                    print(f'时长: {minutes}分{seconds}秒')
                
                print('\n开始下载...')
                ydl.download([url])
                
        except Exception as e:
            error_msg = get_error_message(e)
            print(f'\n{error_msg}')

def show_menu():
    print('\n请选择下载格式：')
    print('1. 最高质量的视频和音频')
    print('2. 最佳视频和音频（分别下载后合并）')
    print('3. 仅下载音频（MP3格式）')
    print('4. 最低质量（节省空间）')
    return input('请输入选项 (1-4): ')

def main():
    downloader = MediaDownloader()
    print('='*50)
    print('欢迎使用 Media Downloader!')
    print('='*50)
    
    while True:
        url = input('\n请输入媒体URL (输入 q 退出): ')
        if url.lower() == 'q':
            print('\n感谢使用，再见！')
            break
            
        format_choice = show_menu()
        if format_choice not in ['1', '2', '3', '4']:
            print('无效的选项，使用默认选项1')
            format_choice = '1'
            
        output_path = os.path.join(os.getcwd(), 'downloads')
        downloader.download_media(url, format_choice, output_path)
        print('\n文件已保存到:', output_path)

if __name__ == '__main__':
    main()
