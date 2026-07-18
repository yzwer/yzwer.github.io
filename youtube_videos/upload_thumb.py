import json, urllib.request, urllib.parse, sys, base64
sys.stdout.reconfigure(encoding='utf-8')

APPID = "wxabc1784dbf87c3de"
SECRET = "10d4335f33efcb36d3f27551870595d5"

def get_token():
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={SECRET}"
    with urllib.request.urlopen(url, timeout=10) as r:
        d = json.loads(r.read().decode())
    return d['access_token']

def upload_thumb(token, image_path):
    """上传封面图，返回 media_id"""
    boundary = b'----OpenClawBoundary7MA4YWxkTrZu0gW'
    with open(image_path, 'rb') as f:
        img_data = f.read()
    body = b'--' + boundary + b'\r\n'
    body += b'Content-Disposition: form-data; name="media"; filename="thumb.jpg"\r\n'
    body += b'Content-Type: image/jpeg\r\n\r\n'
    body += img_data
    body += b'\r\n--' + boundary + b'--\r\n'
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"
    req = urllib.request.Request(url, data=body, method='POST')
    req.add_header('Content-Type', f'multipart/form-data; boundary={boundary.decode()}')
    req.add_header('Content-Length', str(len(body)))
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            d = json.loads(r.read().decode())
        return d.get('media_id')
    except Exception as e:
        print(f"上传失败: {e}")
        return None

token = get_token()
print(f"✅ token 获取成功\n")

# 先创建一个简单的封面图（1x1像素JPEG）
# 实际上应该用视频截图，但先测试API
import struct, zlib

def create_minimal_jpeg(path):
    """创建一个最小的合法JPEG文件"""
    # Minimal JPEG: SOI + DHT + DQT + SOF0 + SOS + EOI
    # 这是一个1x1像素的灰色JPEG
    jpeg = b'\xff\xd8'  # SOI
    # APP0 (JFIF)
    jpeg += b'\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00\x00\x00\x00\x00\x00'
    # DQT
    jpeg += b'\xff\xdb\x00\x43\x00' + b'\x08' * 64
    # SOF0 (baseline)
    jpeg += b'\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x03\x01\x22\x00\x02\x11\x01\x03\x11\x01'
    # DHT
    jpeg += b'\xff\xc4\x00\x1f\x00' + b'\x00' * 16 + b'\x01' * 11 + b'\x00' * 4
    # SOS
    jpeg += b'\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00'
    # EOI
    jpeg += b'\xff\xd9'
    
    with open(path, 'wb') as f:
        f.write(jpeg)
    return path

# 创建临时封面
thumb_path = "temp_thumb.jpg"
create_minimal_jpeg(thumb_path)
print(f"✅ 创建临时封面: {thumb_path}\n")

# 上传封面
print("正在上传封面图...")
thumb_media_id = upload_thumb(token, thumb_path)
if thumb_media_id:
    print(f"✅ 封面上传成功! media_id: {thumb_media_id}")
else:
    print("❌ 封面上传失败")
    sys.exit(1)
