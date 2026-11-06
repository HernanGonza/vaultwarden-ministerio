#!/usr/bin/env python3
"""Genera los íconos del sitio (favicon, apple-touch, android) con la flor del lapacho.
Uso: python3 branding/tools/generar-iconos.py      (necesita Pillow: pip install pillow)
Salida: branding/favicon/*  y  branding/images/safari-pinned-tab.svg
"""
import math, os
from PIL import Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(AQUI, "..", "favicon")
SS = 8  # supersampling para bordes suaves

# Pétalo (viewBox 0..100), igual al de la Wiki: M50 50 C37 41 28 22 36 11 C41 5 47 8 50 12 C53 8 59 5 64 11 C72 22 63 41 50 50 Z
SEGS = [((50, 50), (37, 41), (28, 22), (36, 11)), ((36, 11), (41, 5), (47, 8), (50, 12)),
        ((50, 12), (53, 8), (59, 5), (64, 11)), ((64, 11), (72, 22), (63, 41), (50, 50))]

def bezier(p0, p1, p2, p3, n=24):
    for i in range(n):
        t = i / n
        u = 1 - t
        yield (u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0],
               u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1])

PETALO = [pt for s in SEGS for pt in bezier(*s)]

def rotar(pt, grados):
    a = math.radians(grados); x, y = pt[0] - 50, pt[1] - 50
    return (50 + x*math.cos(a) - y*math.sin(a), 50 + x*math.sin(a) + y*math.cos(a))

def lerp(a, b, t): return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))
STOPS = [(0.0, (0xC9, 0x34, 0x6C)), (0.55, (0xE9, 0x70, 0x9A)), (1.0, (0xF5, 0xA5, 0xBF))]
def color(r):
    r = min(max(r, 0), 1)
    for (t0, c0), (t1, c1) in zip(STOPS, STOPS[1:]):
        if r <= t1: return lerp(c0, c1, (r - t0) / (t1 - t0))
    return STOPS[-1][1]

def flor(px, fondo=None, margen=0.0):
    """Devuelve la flor en un lienzo de px×px (RGBA). margen = fracción de borde vacío."""
    W = px * SS
    esc = W * (1 - 2 * margen) / 100.0
    off = W * margen
    mascara = Image.new("L", (W, W), 0)
    d = ImageDraw.Draw(mascara)
    for k in range(5):
        d.polygon([(off + x*esc, off + y*esc) for x, y in (rotar(p, 72*k) for p in PETALO)], fill=255)
    # degradé radial centrado en (50,50), radio 55
    grad = Image.new("RGB", (W, W))
    gp = grad.load()
    cx = off + 50*esc
    radio = 55 * esc
    for y in range(W):
        for x in range(W):
            gp[x, y] = color(math.hypot(x - cx, y - cx) / radio)
    img = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    img.paste(grad, (0, 0), mascara)
    d2 = ImageDraw.Draw(img)
    r = 5.2 * esc
    d2.ellipse([cx - r, cx - r, cx + r, cx + r], fill=(255, 255, 255, 255))
    img = img.resize((px, px), Image.LANCZOS)
    if fondo:
        base = Image.new("RGBA", (px, px), fondo)
        base.alpha_composite(img)
        img = base
    return img

def guardar(nombre, img): img.save(os.path.join(OUT, nombre)); print("ok", nombre)

os.makedirs(OUT, exist_ok=True)
guardar("favicon-16x16.png", flor(16, margen=0.02))
guardar("favicon-32x32.png", flor(32, margen=0.02))
guardar("apple-touch-icon.png", flor(180, fondo=(255, 255, 255, 255), margen=0.16))
guardar("android-chrome-192x192.png", flor(192, fondo=(255, 255, 255, 255), margen=0.16))
guardar("android-chrome-512x512.png", flor(512, fondo=(255, 255, 255, 255), margen=0.16))
flor(48, margen=0.02).save(os.path.join(OUT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
print("ok favicon.ico")

# Silueta monocroma (pestaña fijada de Safari)
petalos = "".join(f'<path transform="rotate({72*k} 50 50)" d="M50 50 C37 41 28 22 36 11 C41 5 47 8 50 12 C53 8 59 5 64 11 C72 22 63 41 50 50Z"/>' for k in range(5))
open(os.path.join(OUT, "safari-pinned-tab.svg"), "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><g fill="#000">{petalos}</g></svg>\n')
print("ok safari-pinned-tab.svg")
