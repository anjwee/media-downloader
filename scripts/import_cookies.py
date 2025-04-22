import os
import sys
import json

def import_cookies(cookies_text: str) -> bool:
    """导入 cookies 文本到文件"""
    try:
        cookies_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'cookies.txt'
        )
        
        with open(cookies_file, 'w', encoding='utf-8') as f:
            f.write(cookies_text)
        
        print(f"Cookies 已成功保存到: {cookies_file}")
        return True
    except Exception as e:
        print(f"保存 cookies 失败: {str(e)}")
        return False

def main():
    print("请粘贴 Netscape 格式的 cookies 文本 (粘贴完成后按 Ctrl+D):")
    cookies_text = sys.stdin.read().strip()
    
    if not cookies_text:
        print("错误: 未提供 cookies 文本")
        return
    
    if import_cookies(cookies_text):
        print("Cookies 导入成功！")
    else:
        print("Cookies 导入失败！")

if __name__ == '__main__':
    main()