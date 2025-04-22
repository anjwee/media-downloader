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
    print("2. cookies 必须包含以下关键值：")
    print("   - CONSENT")
    print("   - SID")
    print("   - HSID")
    print("   - SSID")
    print("   - APISID")
    print("   - SAPISID")
    print("   - LOGIN_INFO")
    print("   - __Secure-1PSID")
    print("   - __Secure-3PSID")
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
        
        # 验证必要的 cookies 是否存在
        required_cookies = ['CONSENT', 'SID', 'HSID', 'SSID', 'APISID', 'SAPISID', 
                          'LOGIN_INFO', '__Secure-1PSID', '__Secure-3PSID']
        missing_cookies = []
        
        for cookie in required_cookies:
            if cookie not in cookies_text:
                missing_cookies.append(cookie)
        
        if missing_cookies:
            print("\n警告: 缺少以下重要的 cookies:")
            for cookie in missing_cookies:
                print(f"- {cookie}")
            print("\n这可能会导致某些视频无法下载或出现人机验证")
            confirm = input("是否仍要继续保存？(y/n): ").strip().lower()
            if confirm != 'y':
                print("已取消保存")
                return False
            
        # 保存 cookies
        with open(cookies_file, 'w', encoding='utf-8') as f:
            f.write(cookies_text)
            
        print(f"\nCookies 已成功保存到: {cookies_file}")
        print("提示: 如果仍然出现人机验证，请尝试:")
        print("1. 确保已在浏览器中登录 YouTube")
        print("2. 重新导出完整的 cookies")
        print("3. 使用代理服务器")
        return True
        
    except Exception as e:
        print(f"\n保存 cookies 失败: {str(e)}")
        return False

if __name__ == '__main__':
    import_cookies()