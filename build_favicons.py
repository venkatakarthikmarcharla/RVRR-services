from PIL import Image
import base64
import io
import os

def main():
    im = Image.open('Logo In White Background.jpeg').convert('RGB')
    gray = im.convert('L')
    bbox = gray.point(lambda p: 255 if p < 240 else 0).getbbox()
    content = im.crop(bbox)
    cw = bbox[2] - bbox[0]
    ch = bbox[3] - bbox[1]

    # Build square master canvas
    size = 1024
    margin = int(size * 0.05) # 5% margin
    target_w = size - 2 * margin
    scale = target_w / cw
    target_h = int(ch * scale)
    scaled_content = content.resize((target_w, target_h), Image.Resampling.LANCZOS)

    master = Image.new('RGB', (size, size), (255, 255, 255))
    ox = (size - target_w) // 2
    oy = (size - target_h) // 2
    master.paste(scaled_content, (ox, oy))

    # Standard PNG icons
    master.resize((512, 512), Image.Resampling.LANCZOS).save('favicon.png', 'PNG', optimize=True)
    master.resize((512, 512), Image.Resampling.LANCZOS).save('favicon-512x512.png', 'PNG', optimize=True)
    master.resize((192, 192), Image.Resampling.LANCZOS).save('favicon-192x192.png', 'PNG', optimize=True)
    master.resize((180, 180), Image.Resampling.LANCZOS).save('apple-touch-icon.png', 'PNG', optimize=True)
    master.resize((32, 32), Image.Resampling.LANCZOS).save('favicon-32x32.png', 'PNG', optimize=True)
    master.resize((16, 16), Image.Resampling.LANCZOS).save('favicon-16x16.png', 'PNG', optimize=True)

    # Multi-size ICO
    master.save('favicon.ico', format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])

    # SVG Favicon with high-res PNG embedded
    buf = io.BytesIO()
    master.resize((512, 512), Image.Resampling.LANCZOS).save(buf, format='PNG', optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode('utf-8')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
  <defs>
    <clipPath id="squircle">
      <rect width="512" height="512" rx="80" fill="#ffffff"/>
    </clipPath>
  </defs>
  <rect width="512" height="512" rx="80" fill="#ffffff"/>
  <image href="data:image/png;base64,{b64}" width="512" height="512" clip-path="url(#squircle)" preserveAspectRatio="xMidYMid meet"/>
</svg>
'''
    with open('favicon.svg', 'w', encoding='utf-8') as f:
        f.write(svg)

    if os.path.exists('test_canvas.png'):
        os.remove('test_canvas.png')

    print("Favicons generated successfully!")

if __name__ == '__main__':
    main()
