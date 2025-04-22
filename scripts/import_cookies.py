import os
import sys

def import_cookies():
    """导入 cookies"""
    cookies_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'cookies.txt'
    )
    
    print("\n=== 导入 Cookies ===")
    print("1. 请粘贴 Netscape 格式的 cookies 文本")
    print("2. 粘贴完成后按 Enter 换行")
    print("3. 然后按以下快捷键结束输入：")
    print("   - Linux 系统：按 Ctrl + D")
    print("   - Windows 系统：按 Ctrl + Z 再按 Enter")
    print("\n注意: 第一行必须是 '# Netscape HTTP Cookie File'")
    print("\n现在开始粘贴:")
    
    try:
        # 读取用户输入直到 EOF
        cookies_text = sys.stdin.read().strip()
        
        if not cookies_text:
            print("错误: 未提供 cookies 文本")
            return False
            
        # 验证格式
        if not cookies_text.startswith('# Netscape HTTP Cookie File'):
            print("错误: 无效的 cookies 格式")
            print("第一行必须是: '# Netscape HTTP Cookie File'")
            return False
            
        # 保存 cookies
        with open(cookies_file, 'w', encoding='utf-8') as f:
            f.write(cookies_text)
            
        print(f"\nCookies 已成功保存到: {cookies_file}")
        return True
        
    except Exception as e:
        print(f"\n保存 cookies 失败: {str(e)}")
        return False

if __name__ == '__main__':
    import_cookies()