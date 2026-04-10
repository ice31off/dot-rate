import requests
import base64
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io
import urllib.request

DOT_API_KEY = os.environ['DOT_API_KEY']
DEVICE_ID = os.environ['DEVICE_ID']

res = requests.get('https://api.frankfurter.app/latest?from=USD&to=JPY')
data = res.json()
rate = data['rates']['JPY']

now = datetime.now()
date_str = f"{now.month:02d}月{now.day:02d}日  {now.hour:02d}:{now.minute:02d}時点"

W, H = 296, 128

# 日本語フォントをダウンロード
font_url = "https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTF/Japanese/NotoSansCJKjp-Bold.otf"
font_path = "/tmp/NotoSansCJK.otf"
urllib.request.urlretrieve(font_url, font_path)

img = Image.new('RGB', (W, H), color='#5BB8F5')
draw = ImageDraw.Draw(img)

font_small = ImageFont.truetype(font_path, 14)
font_large = ImageFont.truetype(font_path, 48)

draw.text((12, 8), "USD/JPY", font=font_small, fill='black')

date_bbox = draw.textbbox((0, 0), date_str, font=font_small)
date_w = date_bbox[2] - date_bbox[0]
draw.text((W - date_w - 12, 8), date_str, font=font_small, fill='black')

draw.line([(12, 30), (W - 12, 30)], fill='black', width=1)

rate_str = f"{rate:.2f} 円"
rate_bbox = draw.textbbox((0, 0), rate_str, font=font_large)
rate_w = rate_bbox[2] - rate_bbox[0]
rate_h = rate_bbox[3] - rate_bbox[1]
draw.text(((W - rate_w) / 2, (H - rate_h) / 2 + 18), rate_str, font=font_large, fill='black')

buffer = io.BytesIO()
img.save(buffer, format='PNG')
img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

response = requests.post(
    f'https://dot.mindreset.tech/api/authV2/open/device/{DEVICE_ID}/image',
    headers={
        'Authorization': f'Bearer {DOT_API_KEY}',
        'Content-Type': 'application/json'
    },
    json={
        'refreshNow': True,
        'image': img_base64,
        'ditherType': 'NONE'
    }
)

print(f"レート: {rate:.2f}円")
print(f"送信結果: {response.json()}")
