import sys
from typing import Dict, Any

def progress_hook(d: Dict[str, Any]) -> None:
    if d['status'] == 'downloading':
        # 计算下载进度
        total_bytes = d.get('total_bytes')
        downloaded_bytes = d.get('downloaded_bytes', 0)
        
        if total_bytes:
            percentage = (downloaded_bytes / total_bytes) * 100
            # 创建进度条
            progress = int(percentage / 2)
            progress_bar = f'[{"=" * progress}{" " * (50 - progress)}]'
            
            # 计算下载速度
            speed = d.get('speed', 0)
            if speed:
                speed_str = f'{speed/1024/1024:.1f} MB/s'
            else:
                speed_str = 'N/A'
                
            # 打印进度信息
            sys.stdout.write(f'\r{progress_bar} {percentage:.1f}% | Speed: {speed_str}')
            sys.stdout.flush()
            
    elif d['status'] == 'finished':
        sys.stdout.write('\n下载完成，正在处理...\n')
        sys.stdout.flush()

def format_bytes(bytes: int) -> str:
    '''将字节数转换为人类可读的格式'''
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024:
            return f'{bytes:.1f} {unit}'
        bytes /= 1024
    return f'{bytes:.1f} TB'

def get_error_message(error: Exception) -> str:
    '''获取友好的错误信息'''
    error_str = str(error)
    if 'HTTP Error 404' in error_str:
        return '找不到视频，请检查URL是否正确'
    elif 'HTTP Error 403' in error_str:
        return '无权访问此视频，可能需要登录或视频已被设为私有'
    elif 'Unsuitable URL' in error_str:
        return '不支持的URL格式，请检查URL是否正确'
    else:
        return f'发生错误: {error_str}'
