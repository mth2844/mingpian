# 壁纸图库

一个纯静态、可预览、带水印、禁右键下载的壁纸展示站。以后加图只需要「丢文件 + 跑一次脚本」。

## 目录结构

```
图库/
├── index.html       # 页面
├── style.css        # 样式
├── app.js           # 交互（灯箱、水印、禁下载）
├── build.py         # 扫描图片 → 生成缩略图 + manifest.json + data.js
├── manifest.json    # 图片清单（由 build.py 自动生成，勿手改）
├── data.js          # 图片清单的 JS 版（让双击 index.html 也能直接预览）
├── images/          # 放原始壁纸（数字命名，如 001.jpg、010.png）
└── thumbs/          # 自动生成的缩略图（可删，重新生成）
```

## 使用方法

1. 把壁纸按数字命名放进 `images/`，例如 `001.jpg`、`002.jpg`、`010.png`。
   命名会按数字排序（2 排在 10 前面）。
2. 运行生成脚本（需要 Python + Pillow）：

   ```bash
   python build.py
   ```

   它会自动生成 `thumbs/` 缩略图和 `manifest.json`。
3. 打开 `index.html` 即可预览（点缩略图看大图，方向键 / Esc 切换与关闭）。

以后加新图：把图丢进 `images/`，再跑一次 `python build.py` 即可，无需改任何代码。

## 水印

- 你的原图本身已带水印（推荐，这是最有效的保护）。
- 页面在「缩略图」和「大图预览」上还会叠加一层半透明平铺水印文字，
  文字在 `app.js` 顶部的 `CONFIG.watermarkText` 里改。
- 想要在生成的缩略图上再烘焙一层水印，把 `build.py` 里的
  `BAKE_WATERMARK = True`，并设置 `WATERMARK_TEXT`。

## 不提供下载

已做的抑制（均为客户端手段）：

- 禁用右键菜单（contextmenu）
- 禁用图片拖拽（dragstart）
- 大图上方覆盖一层透明层，长按/右键无法直接命中图片本身

说明：浏览器要显示图片就必须把图片发到访客设备，所以无法 100% 阻止截图、
开发者工具、抓包下载。**水印才是真正的保护**，前端抑制只是提高门槛。

## 部署给别人看

### 方式一：GitHub Pages（免费，推荐）
1. 把整个目录推到 GitHub 仓库。
2. 仓库 Settings → Pages → 选择分支（main）→ 保存。
3. 几分钟后得到 `https://你的用户名.github.io/仓库名/`，即可分享。

### 方式二：Vercel / Netlify（免费，最简单）
- Vercel：`npx vercel` 或网页导入仓库即可。
- Netlify：把文件夹拖到 netlify.com 的部署面板即可。

### 方式三：自己服务器 / Nginx
把目录放到服务器上，Nginx 指向该目录即可，无需后端。

### 方式四：本机局域网给别人看
```bash
cd 图库目录
python -m http.server 8080
```
同一局域网访问 `http://你的IP:8080`。

## 依赖

- 运行站点：无依赖，纯 HTML/CSS/JS。
- 生成缩略图：Python 3 + Pillow（`pip install Pillow`）。
