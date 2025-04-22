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
    print("   - CONSENT（必需）")
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
    print("\n注意: ")
    print("- 第一行必须是 '# Netscape HTTP Cookie File'")
    print("- CONSENT cookie 是必需的，其他cookie可选但建议都包含")
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
        required_cookies = ['CONSENT']  # CONSENT 是必需的
        recommended_cookies = ['SID', 'HSID', 'SSID', 'APISID', 'SAPISID', 
                           'LOGIN_INFO', '__Secure-1PSID', '__Secure-3PSID']
        
        missing_required = []
        missing_recommended = []
        
        # 检查必需的 cookies
        for cookie in required_cookies:
            if cookie not in cookies_text:
                missing_required.append(cookie)
        
        # 检查推荐的 cookies
        for cookie in recommended_cookies:
            if cookie not in cookies_text:
                missing_recommended.append(cookie)
        
        if missing_required:
            print("\n错误: 缺少以下必需的 cookies:")
            for cookie in missing_required:
                print(f"- {cookie}")
            print("\n这些 cookie 是必需的，请确保包含它们")
            return False
        
        if missing_recommended:
            print("\n警告: 缺少以下推荐的 cookies:")
            for cookie in missing_recommended:
                print(f"- {cookie}")
            print("\n虽然这些 cookie 不是必需的，但缺少它们可能会导致:")
            print("1. 某些视频无法下载")
            print("2. 出现人机验证")
            print("3. 无法访问会员内容")
            confirm = input("是否仍要继续保存？(y/n): ").strip().lower()
            if confirm != 'y':
                print("已取消保存")
                return False
            
        # 保存 cookies
        with open(cookies_file, 'w', encoding='utf-8') as f:
            f.write(cookies_text)
            
        print(f"\nCookies 已成功保存到: {cookies_file}")
        
        if missing_recommended:
            print("\n提示: 建议重新获取完整的 cookies，步骤如下:")
            print("1. 确保已在浏览器中登录 YouTube")
            print("2. 使用浏览器扩展（如 'Cookie Editor'）导出所有 cookies")
            print("3. 确保导出格式为 'Netscape HTTP Cookie File'")
        return True
        
    except Exception as e:
        print(f"\n保存 cookies 失败: {str(e)}")
        return False

if __name__ == '__main__':
    import_cookies()