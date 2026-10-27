#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""扫描 images/ 文件夹，生成缩略图和 manifest.json。

用法：
    python build.py
"""
import os
import json
import re

from PIL import Image, ImageDraw, ImageFont

IMAGES_DIR = "images"
THUMBS_DIR = "thumbs"
MANIFEST = "manifest.json"
THUMB_MAX = 480          # 缩略图最长边（像素）
JPEG_QUALITY = 82

# 是否在生成的缩略图上再烘焙一层水印（True=叠加；原图已有水印可设为 False）
BAKE_WATERMARK = False
WATERMARK_TEXT = "© 芸芸大王"
WATERMARK_OPACITY = 70   # 0-255

EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".avif"}


def natural_key(name):
    """按文件名开头的数字排序，例如 2.jpg < 10.jpg。"""
    m = re.match(r"^(\d+)", name)
    return (int(m.group(1)), name) if m else (10**9, name)


def bake_watermark(im):
    """在图片上铺一层斜向半透明水印文字。"""
    im = im.convert("RGBA")
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    try:
        font = ImageFont.truetype("arial.ttf", max(18, im.width // 20))
    except Exception:
        font = ImageFont.load_default()

    bbox = d.textbbox((0, 0), WATERMARK_TEXT, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    step_x, step_y = max(tw * 2, 80), max(th * 4, 80)

    for y in range(-im.height, im.height, step_y):
        for x in range(-im.width, im.width, step_x):
            d.text((x, y), WATERMARK_TEXT, font=font,
                   fill=(255, 255, 255, WATERMARK_OPACITY))

    layer = layer.rotate(-28, expand=1, resample=Image.BICUBIC)
    lw, lh = layer.size
    left = (lw - im.width) // 2
    top = (lh - im.height) // 2
    layer = layer.crop((left, top, left + im.width, top + im.height))
    return Image.alpha_composite(im, layer)


def main():
    if not os.path.isdir(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)
        print(f"已创建 {IMAGES_DIR}/ 文件夹，请把壁纸放进去后再运行本脚本。")
    os.makedirs(THUMBS_DIR, exist_ok=True)

    files = [f for f in os.listdir(IMAGES_DIR)
             if os.path.splitext(f)[1].lower() in EXTS and not f.startswith('.')]
    files.sort(key=natural_key)

    images = []
    for f in files:
        src_path = os.path.join(IMAGES_DIR, f)
        ext = os.path.splitext(f)[1].lower()
        try:
            im = Image.open(src_path)
            im.thumbnail((THUMB_MAX, THUMB_MAX))
            if BAKE_WATERMARK:
                im = bake_watermark(im)

            # 有透明通道才保留 PNG，否则用 JPG（体积小很多，220 张加载更快）
            has_alpha = im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)
            if ext in (".gif", ".webp") or has_alpha:
                thumb_name = os.path.splitext(f)[0] + ".png"
                im = im.convert("RGBA")
            else:
                thumb_name = os.path.splitext(f)[0] + ".jpg"
                im = im.convert("RGB")

            thumb_path = os.path.join(THUMBS_DIR, thumb_name)
            im.save(thumb_path, quality=JPEG_QUALITY)
        except Exception as e:
            print(f"跳过 {f}: {e}")
            continue

        images.append({
            "name": f,
            "thumb": thumb_path.replace("\\", "/"),
            "src": src_path.replace("\\", "/"),
        })

    data = {"watermark": WATERMARK_TEXT, "images": images}
    with open(MANIFEST, "w", encoding="utf-8") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=2)

    # 同时生成 data.js，便于双击 index.html 直接预览（file:// 下无法 fetch）
    js = "window.WALLPAPERS = " + json.dumps(data, ensure_ascii=False) + ";\n"
    with open("data.js", "w", encoding="utf-8") as fp:
        fp.write(js)

    print(f"完成：共 {len(images)} 张壁纸 → 已生成缩略图、{MANIFEST} 和 data.js")


if __name__ == "__main__":
    main()
