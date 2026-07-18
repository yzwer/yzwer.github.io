import urllib.request
import json

url = "https://api.github.com/repos/YaoFANGUK/video-subtitle-extractor/releases/latest"
req = urllib.request.Request(url)
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode())

print(f"Tag: {data['tag_name']}")
print(f"Name: {data['name']}")
print()
for asset in data['assets']:
    print(f"  {asset['name']}  ({asset['size'] // 1024 // 1024}MB)")
    print(f"    URL: {asset['browser_download_url']}")
