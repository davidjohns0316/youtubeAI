#!/usr/bin/env python3
"""Generate YouTubeAI.app/Contents/Resources/AppIcon.icns from scratch."""
import math, os, shutil, struct, subprocess, zlib

S = 512  # render at 512 — sips will scale for the iconset

R = S / 2  # circle radius
CX, CY = S / 2, S / 2

# Play button triangle (nudged right so it looks optically centered)
HALF = int(S * 0.265)
OX = int(S * 0.04)
AX, AY = int(CX) - HALF + OX, int(CY) - HALF  # top-left
BX, BY = int(CX) - HALF + OX, int(CY) + HALF  # bottom-left
EX, EY = int(CX) + HALF + OX, int(CY)         # right tip


def lerp(a, b, t):
    return max(0, min(255, int(a + (b - a) * t)))


def in_triangle(px, py):
    # Sign test for point-in-triangle
    d1 = (px - BX) * (AY - BY) - (AX - BX) * (py - BY)
    d2 = (px - EX) * (BY - EY) - (BX - EX) * (py - EY)
    d3 = (px - AX) * (EY - AY) - (EX - AX) * (py - AY)
    has_neg = d1 < 0 or d2 < 0 or d3 < 0
    has_pos = d1 > 0 or d2 > 0 or d3 > 0
    return not (has_neg and has_pos)


def make_png(rows, w, h):
    def chunk(tag, data):
        body = tag + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)
    ihdr = chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
    raw = b"".join(b"\x00" + row for row in rows)
    idat = chunk(b"IDAT", zlib.compress(raw, 6))
    iend = chunk(b"IEND", b"")
    return b"\x89PNG\r\n\x1a\n" + ihdr + idat + iend


print(f"Rendering {S}×{S} icon...")
rows = []
for y in range(S):
    row = bytearray()
    t = y / S
    # Background: diagonal gradient purple #7c3aed → deep indigo #3730a3
    bg = (lerp(0x7C, 0x37, t), lerp(0x3A, 0x30, t), lerp(0xED, 0xA3, t))

    for x in range(S):
        dx, dy = x - CX, y - CY
        dist2 = dx * dx + dy * dy

        if dist2 > R * R:
            row += b"\x00\x00\x00\x00"  # outside circle → transparent
            continue

        # Soft antialiased circle edge
        dist = math.sqrt(dist2)
        alpha = 255 if dist < R - 1.5 else int((R - dist) / 1.5 * 255)

        if in_triangle(x, y):
            row += bytes([255, 255, 255, alpha])  # white play button
        else:
            row += bytes([bg[0], bg[1], bg[2], alpha])

    rows.append(bytes(row))

print("Encoding PNG...")
png_512 = make_png(rows, S, S)

# ── Build iconset ──────────────────────────────────────────────────────────
iconset = "YouTubeAI.iconset"
os.makedirs(iconset, exist_ok=True)
master = f"{iconset}/icon_512x512@2x.png"  # treated as 1024 logical

# Write base image at 512 (we'll scale with sips)
with open(master, "wb") as f:
    f.write(png_512)

sizes = {
    16:  ["icon_16x16.png"],
    32:  ["icon_16x16@2x.png", "icon_32x32.png"],
    64:  ["icon_32x32@2x.png"],
    128: ["icon_128x128.png"],
    256: ["icon_128x128@2x.png", "icon_256x256.png"],
    512: ["icon_256x256@2x.png", "icon_512x512.png"],
}

for size, names in sizes.items():
    for name in names:
        out = f"{iconset}/{name}"
        subprocess.run(["sips", "-z", str(size), str(size), master, "--out", out], capture_output=True)

print("Converting to .icns via iconutil...")
resources = "YouTubeAI.app/Contents/Resources"
os.makedirs(resources, exist_ok=True)
result = subprocess.run(
    ["iconutil", "-c", "icns", iconset, "-o", f"{resources}/AppIcon.icns"],
    capture_output=True, text=True
)
if result.returncode != 0:
    print("iconutil error:", result.stderr)
else:
    print(f"✓ Icon saved to {resources}/AppIcon.icns")

shutil.rmtree(iconset)
