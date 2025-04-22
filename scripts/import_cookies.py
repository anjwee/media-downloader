import os
import sys
import time

def import_cookies():
    """导入 cookies"""
    cookies_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'cookies.txt'
    )
    
    print("\n=== 导入 Cookies ===")
    print("1. 请从浏览器导出 YouTube cookies")
    print("2. cookies 最好包含以下值（不是所有都必需）：")
    print("   - VISITOR_INFO1_LIVE")
    print("   - PREF")
    print("   - GPS")
    print("   - YSC")
    print("   - DEVICE_INFO")
    print("   - VISITOR_PRIVACY_METADATA")
    print("3. 粘贴完成后按 Enter 换行")
    print("4. 然后按以下快捷键结束输入：")
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
        
        # 验证是否包含 .youtube.com 域名的 cookie
        if '.youtube.com' not in cookies_text:
            print("错误: 未找到 YouTube cookies")
            print("请确保从 YouTube 网站导出 cookies")
            return False
            
        # 保存 cookies
        with open(cookies_file, 'w', encoding='utf-8') as f:
            f.write(cookies_text)
            
        print(f"\nCookies 已成功保存到: {cookies_file}")
        print("\n提示: 如果下载时遇到问题，可以尝试:")
        print("1. 确保已在浏览器中登录 YouTube")
        print("2. 重新导出完整的 cookies")
        print("3. 使用代理服务器")
        return True
        
    except Exception as e:
        print(f"\n保存 cookies 失败: {str(e)}")
        return False

if __name__ == '__main__':
    import_cookies()