const GALLERY = document.getElementById('gallery');
const EMPTY = document.getElementById('empty');
const LIGHTBOX = document.getElementById('lightbox');
const LB_IMG = document.getElementById('lb-img');
const LB_CAPTION = document.getElementById('lb-caption');
const COUNT = document.getElementById('count');

// ===== 配置 =====
const CONFIG = {
  // 预览层叠加的水印文字（叠加在原图水印之上，增强保护）
  watermarkText: '© 芸芸大王',
  watermarkOpacity: 0.16,
};

let images = [];
let current = -1;

function watermarkBg(text, opacity) {
  const svg =
    `<svg xmlns="http://www.w3.org/2000/svg" width="260" height="180">` +
    `<text x="50%" y="50%" fill="rgba(255,255,255,${opacity})" font-size="22" ` +
    `font-family="sans-serif" text-anchor="middle" dominant-baseline="middle" ` +
    `transform="rotate(-28 130 90)">${text}</text></svg>`;
  return `url("data:image/svg+xml,${encodeURIComponent(svg)}")`;
}

async function load() {
  // 优先读取 data.js（双击打开也能用）；否则回退到 fetch manifest.json（需本地服务器）
  let data = window.WALLPAPERS;
  if (!data) {
    try {
      const res = await fetch('manifest.json');
      data = await res.json();
    } catch (e) {
      COUNT.textContent = '加载失败';
      EMPTY.textContent = '请先运行 build.py 生成 data.js / manifest.json。';
      EMPTY.hidden = false;
      return;
    }
  }
  images = data.images || [];
  const wm = data.watermark || CONFIG.watermarkText;
  render(wm);
}

function render(wm) {
  GALLERY.innerHTML = '';
  const bg = watermarkBg(wm, CONFIG.watermarkOpacity);
  COUNT.textContent = `共 ${images.length} 张壁纸`;

  if (!images.length) {
    EMPTY.hidden = false;
    return;
  }
  EMPTY.hidden = true;

  images.forEach((img, i) => {
    const card = document.createElement('figure');
    card.className = 'card';
    card.innerHTML =
      `<div class="thumb-wrap">` +
      `<img src="${img.thumb}" alt="${img.name}" loading="lazy" draggable="false">` +
      `<div class="thumb-wm" style="background-image:${bg}"></div>` +
      `</div><figcaption>${img.name}</figcaption>`;
    card.addEventListener('click', () => open(i));
    GALLERY.appendChild(card);
  });

  const lbWm = document.querySelector('.wm-overlay');
  if (lbWm) lbWm.style.backgroundImage = bg;
}

function open(i) {
  current = i;
  update();
  LIGHTBOX.hidden = false;
  document.body.classList.add('no-scroll');
}

function update() {
  const img = images[current];
  LB_IMG.src = img.src;
  LB_CAPTION.textContent = `${img.name}　(${current + 1} / ${images.length})`;
}

function close() {
  LIGHTBOX.hidden = true;
  LB_IMG.src = '';
  document.body.classList.remove('no-scroll');
}

function nav(d) {
  if (!images.length) return;
  current = (current + d + images.length) % images.length;
  update();
}

document.querySelector('.lb-close').addEventListener('click', close);
document.querySelector('.lb-bg').addEventListener('click', close);
document.querySelector('.lb-prev').addEventListener('click', () => nav(-1));
document.querySelector('.lb-next').addEventListener('click', () => nav(1));
document.addEventListener('keydown', (e) => {
  if (LIGHTBOX.hidden) return;
  if (e.key === 'Escape') close();
  if (e.key === 'ArrowLeft') nav(-1);
  if (e.key === 'ArrowRight') nav(1);
});

// 防下载（客户端抑制：禁用右键菜单与拖拽；水印才是真正的保障）
document.addEventListener('contextmenu', (e) => {
  if (e.target.closest('.gallery, .lightbox')) e.preventDefault();
});
document.addEventListener('dragstart', (e) => {
  if (e.target.closest('.gallery, .lightbox')) e.preventDefault();
});

load();
