import requests
from getpass import getpass

# 配置
login_url = "https://pypi.org/account/login/"
account_url = "https://pypi.org/manage/account/"
token_url = "https://pypi.org/manage/account/api-tokens/"

session = requests.Session()

# 第一步：获取登录页的 CSRF token
print("正在获取登录页面...")
r = session.get(login_url)
if 'name="csrfmiddlewaretoken"' not in r.text:
    print("❌ 无法加载登录页面")
    exit(1)

csrf_login = r.text.split('name="csrfmiddlewaretoken" value="')[1].split('"')[0]

# 第二步：输入账号密码
username = input("PyPI Username: ")
password = getpass("PyPI Password: ")

# 第三步：执行登录
print("正在登录...")
login_resp = session.post(
    login_url,
    data={
        "csrfmiddlewaretontoken": csrf_login,  # 注意：这里故意写错，看下面说明
        "login": username,
        "password": password,
        "next": "/manage/account/"
    }
)

# 修正：实际字段名是 'csrfmiddlewaretoken'
login_resp = session.post(
    login_url,
    data={
        "csrfmiddlewaretoken": csrf_login,
        "login": username,
        "password": password,
        "next": "/manage/account/"
    }
)

if "Invalid username or password" in login_resp.text:
    print("❌ 用户名或密码错误！")
    exit(1)

if "/manage/account/" not in login_resp.url:
    print("❌ 登录失败，请检查账号密码")
    print("响应 URL:", login_resp.url)
    exit(1)

print("✅ 登录成功！")

# 第四步：获取账户页的 CSRF token
r2 = session.get(account_url)
if 'name="csrfmiddlewaretoken"' not in r2.text:
    print("❌ 无法加载账户页面")
    exit(1)

csrf_account = r2.text.split('name="csrfmiddlewaretoken" value="')[1].split('"')[0]

# 第五步：创建 API Token
print("正在创建 API Token...")
resp = session.post(
    token_url,
    data={
        "csrfmiddlewaretoken": csrf_account,
        "description": "upload-synbio",
        "scope": "all"
    }
)

# 检查结果
if resp.status_code == 200 and 'pypi-' in resp.text:
    # 尝试提取 token
    start = resp.text.find('pypi-')
    if start == -1:
        print("⚠️ Token 创建成功，但无法自动提取。请手动检查响应。")
        print(resp.text[:1000])
    else:
        end = resp.text.find('"', start)
        if end == -1:
            token = resp.text[start:]
        else:
            token = resp.text[start:end]
        print("\n🎉 成功！你的 API Token 是：")
        print(token)
        print("\n📌 请立即复制保存！关闭后无法再次查看。")
else:
    print(f"❌ 创建失败，状态码: {resp.status_code}")
    print("可能原因：需要先启用 2FA，或账号权限未同步。")
    # 输出部分响应以便调试
    print("\n响应片段：")
    print(resp.text[:800])