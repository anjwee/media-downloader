from typing import Dict, Any

VIDEO_FORMATS = {
    '1': 'bv*+ba/b',  # 最高质量的视频和音频
    '2': 'bv+ba',     # 最佳视频和音频（分别下载后合并）
    '3': 'ba/b',      # 最佳音频
    '4': 'wv*+wa/w'   # 最低质量（节省空间）
}

def get_format_options(format_choice: str) -> Dict[str, Any]:
    base_options = {
        'format': VIDEO_FORMATS.get(format_choice, 'bv*+ba/b'),
        'outtmpl': '%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'format_sort': ['res:1080', 'ext:mp4:m4a'],
        'prefer_ffmpeg': True,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }]
    }
    
    if format_choice == '3':  # 音频选项
        base_options.update({
            'format': 'bestaudio',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }, {
                'key': 'FFmpegMetadata',
                'add_metadata': True,
            }]
        })
    elif format_choice == '4':  # 低质量选项
        base_options.update({
            'format': 'worstvideo[ext=mp4]+worstaudio[ext=m4a]/worst',
            'format_sort': ['res:360', 'ext:mp4:m4a']
        })
    
    return base_options