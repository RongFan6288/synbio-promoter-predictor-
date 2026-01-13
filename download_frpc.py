import urllib.request
import os

url = "https://bio-oss.oss-cn-beijing.aliyuncs.com/frpc_windows_amd64_v0.3"
save_path = os.path.expanduser(r"～\.cache\huggingface\gradio\frpc\frpc_windows_amd64_v0.3")

# 创建目录
os.makedirs(os.path.dirname(save_path), exist_ok=True)

print("正在下载 frpc...")
urllib.request.urlretrieve(url, save_path)
print(f"✅ 已保存到: {save_path}")