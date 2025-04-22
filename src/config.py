from typing import Dict, Any

VIDEO_FORMATS = {
    '1': 'best',  # 最高质量的视频和音频
    '2': 'bestvideo+bestaudio',  # 最佳视频和音频（分别下载后合并）
    '3': 'bestaudio/best',  # 最佳音频
    '4': 'worstvideo+worstaudio'  # 最低质量（节省空间）
}

def get_format_options(format_choice: str) -> Dict[str, Any]:
    base_options = {
        'format': VIDEO_FORMATS.get(format_choice, 'best'),
        'outtmpl': '%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
    }
    
    if format_choice == '3':  # 音频选项
        base_options.update({
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        })
    
    return base_options
