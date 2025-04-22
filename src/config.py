from typing import Dict, Any
from datetime import datetime

VIDEO_FORMATS = {
    '1': 'best',  # 最高质量的视频和音频
    '2': 'bestvideo+bestaudio',  # 最佳视频和音频（分别下载后合并）
    '3': 'bestaudio/best',  # 最佳音频
    '4': 'worstvideo+worstaudio'  # 最低质量（节省空间）
}

def get_format_options(format_choice: str) -> Dict[str, Any]:
    """
    获取下载格式选项
    
    Args:
        format_choice: 用户选择的格式选项 ('1', '2', '3', '4')
        
    Returns:
        Dict[str, Any]: 下载选项配置字典
    """
    current_time = datetime.utcnow().strftime('%Y%m%d')
    
    base_options = {
        'format': VIDEO_FORMATS.get(format_choice, 'best'),
        'outtmpl': '%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'http_headers': {
            'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'X-Client-Data': current_time  # 添加动态时间戳
        },
        'socket_timeout': 30,
        'retries': 10,
        'file_access_retries': 10,
        'fragment_retries': 10,
        'retry_sleep_functions': {'http': lambda n: 5 * n},  # 重试延迟
        'max_sleep_interval': 30,  # 最大重试间隔
        'overwrites': False,  # 不覆盖已存在的文件
        'ignoreerrors': True,  # 忽略错误继续下载
        'quiet': False,
        'no_warnings': False,
        'verbose': True,
        'extract_flat': True,
        'concurrent_fragment_downloads': 1,  # 并发下载片段数
        'http_chunk_size': 10485760,  # 块大小：10MB
        'buffersize': 1024,  # 缓冲区大小
        # YouTube 特定选项
        'youtube_include_dash_manifest': True,
        'youtube_include_hls_manifest': True,
        'prefer_free_formats': True,
        'check_formats': True,
    }
    
    # 音频选项特殊处理
    if format_choice == '3':
        base_options.update({
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }, {
                # 添加元数据处理器
                'key': 'FFmpegMetadata',
                'add_metadata': True,
            }],
            'extract_audio': True,
            'audio_format': 'mp3',
            'audio_quality': 0,  # 最高质量
        })
    
    # 高质量视频特殊处理
    elif format_choice in ['1', '2']:
        base_options.update({
            'format_sort': [
                'res:1080',
                'ext:mp4:m4a',
                'codec:h264:aac',
                'lang'
            ],
            'postprocessors': [{
                # 添加元数据处理器
                'key': 'FFmpegMetadata',
                'add_metadata': True,
            }]
        })
    
    return base_options
