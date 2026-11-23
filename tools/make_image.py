#!/usr/bin/env python3
"""
Generate a 1024x1024 PNG newspaper front page for Sunday November 23, 2026.
Uses only Python standard library (zlib, struct).
"""

import zlib
import struct
import os

WIDTH = 1024
HEIGHT = 1024

def write_png(path, pixels):
    """Write RGBA pixels as PNG using stdlib only."""
    # PNG signature
    png = b'\x89PNG\r\n\x1a\n'
    
    # IHDR chunk
    ihdr_data = struct.pack('>IIBBBBB', WIDTH, HEIGHT, 8, 6, 0, 0, 0)
    ihdr_crc = zlib.crc32(b'IHDR' + ihdr_data) & 0xffffffff
    png += struct.pack('>I', len(ihdr_data)) + b'IHDR' + ihdr_data + struct.pack('>I', ihdr_crc)
    
    # IDAT chunk - compress scanlines
    raw = bytearray()
    for y in range(HEIGHT):
        raw.append(0)  # filter type 0 (none)
        row_start = y * WIDTH * 4
        raw.extend(pixels[row_start:row_start + WIDTH * 4])
    
    compressed = zlib.compress(bytes(raw), 9)
    idat_crc = zlib.crc32(b'IDAT' + compressed) & 0xffffffff
    png += struct.pack('>I', len(compressed)) + b'IDAT' + compressed + struct.pack('>I', idat_crc)
    
    # IEND chunk
    iend_crc = zlib.crc32(b'IEND') & 0xffffffff
    png += struct.pack('>I', 0) + b'IEND' + struct.pack('>I', iend_crc)
    
    with open(path, 'wb') as f:
        f.write(png)

def make_image():
    # Create white background
    pixels = bytearray([255, 255, 255, 255] * (WIDTH * HEIGHT))
    
    def set_pixel(x, y, r, g, b, a=255):
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            idx = (y * WIDTH + x) * 4
            pixels[idx] = r
            pixels[idx + 1] = g
            pixels[idx + 2] = b
            pixels[idx + 3] = a
    
    def draw_rect(x, y, w, h, r, g, b, a=255):
        for dy in range(h):
            for dx in range(w):
                set_pixel(x + dx, y + dy, r, g, b, a)
    
    def draw_line(x1, y1, x2, y2, r, g, b, a=255):
        # Simple Bresenham
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        while True:
            set_pixel(x1, y1, r, g, b, a)
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy
    
    def draw_text_simple(x, y, text, r, g, b, scale=1):
        """Very simple bitmap font rendering."""
        # 5x7 font for basic ASCII
        font = {
            'A': [0x1F, 0x11, 0x1F, 0x11, 0x11],
            'B': [0x1E, 0x11, 0x1E, 0x11, 0x1E],
            'C': [0x0E, 0x11, 0x10, 0x11, 0x0E],
            'D': [0x1E, 0x11, 0x11, 0x11, 0x1E],
            'E': [0x1F, 0x10, 0x1E, 0x10, 0x1F],
            'F': [0x1F, 0x10, 0x1E, 0x10, 0x10],
            'G': [0x0E, 0x11, 0x13, 0x11, 0x0E],
            'H': [0x11, 0x11, 0x1F, 0x11, 0x11],
            'I': [0x1F, 0x04, 0x04, 0x04, 0x1F],
            'J': [0x1F, 0x01, 0x01, 0x11, 0x0E],
            'K': [0x11, 0x12, 0x1C, 0x12, 0x11],
            'L': [0x10, 0x10, 0x10, 0x10, 0x1F],
            'M': [0x11, 0x1B, 0x15, 0x11, 0x11],
            'N': [0x11, 0x19, 0x15, 0x13, 0x11],
            'O': [0x0E, 0x11, 0x11, 0x11, 0x0E],
            'P': [0x1E, 0x11, 0x1E, 0x10, 0x10],
            'Q': [0x0E, 0x11, 0x11, 0x15, 0x0E],
            'R': [0x1E, 0x11, 0x1E, 0x12, 0x11],
            'S': [0x0F, 0x10, 0x0E, 0x01, 0x1E],
            'T': [0x1F, 0x04, 0x04, 0x04, 0x04],
            'U': [0x11, 0x11, 0x11, 0x11, 0x0E],
            'V': [0x11, 0x11, 0x11, 0x0A, 0x04],
            'W': [0x11, 0x11, 0x15, 0x15, 0x0A],
            'X': [0x11, 0x0A, 0x04, 0x0A, 0x11],
            'Y': [0x11, 0x0A, 0x04, 0x04, 0x04],
            'Z': [0x1F, 0x02, 0x04, 0x08, 0x1F],
            '0': [0x0E, 0x11, 0x13, 0x15, 0x0E],
            '1': [0x04, 0x0C, 0x04, 0x04, 0x0E],
            '2': [0x0E, 0x11, 0x02, 0x04, 0x1F],
            '3': [0x1E, 0x01, 0x0E, 0x01, 0x1E],
            '4': [0x02, 0x06, 0x0A, 0x1F, 0x02],
            '5': [0x1F, 0x10, 0x1E, 0x01, 0x1E],
            '6': [0x0E, 0x10, 0x1E, 0x11, 0x0E],
            '7': [0x1F, 0x01, 0x02, 0x04, 0x04],
            '8': [0x0E, 0x11, 0x0E, 0x11, 0x0E],
            '9': [0x0E, 0x11, 0x0F, 0x01, 0x0E],
            '.': [0x00, 0x00, 0x00, 0x00, 0x04],
            ',': [0x00, 0x00, 0x00, 0x04, 0x04],
            ':': [0x00, 0x04, 0x00, 0x04, 0x00],
            '-': [0x00, 0x00, 0x0E, 0x00, 0x00],
            '/': [0x01, 0x02, 0x04, 0x08, 0x10],
            ' ': [0x00, 0x00, 0x00, 0x00, 0x00],
            '\'': [0x02, 0x04, 0x00, 0x00, 0x00],
            '%': [0x1C, 0x12, 0x04, 0x09, 0x13],
            '$': [0x04, 0x0F, 0x04, 0x1E, 0x04],
        }
        
        cx = x
        for ch in text.upper():
            if ch in font:
                glyph = font[ch]
                for col in range(5):
                    bits = glyph[col]
                    for row in range(7):
                        if bits & (1 << (6 - row)):
                            for sy in range(scale):
                                for sx in range(scale):
                                    set_pixel(cx + col * scale + sx, y + row * scale + sy, r, g, b)
                cx += 6 * scale
            else:
                cx += 6 * scale
    
    # Page border
    border_color = (30, 30, 30)
    draw_rect(0, 0, WIDTH, 4, *border_color)
    draw_rect(0, HEIGHT - 4, WIDTH, 4, *border_color)
    draw_rect(0, 0, 4, HEIGHT, *border_color)
    draw_rect(WIDTH - 4, 0, 4, HEIGHT, *border_color)
    
    # Masthead background
    draw_rect(4, 4, WIDTH - 8, 80, 20, 20, 20)
    
    # Masthead text
    draw_text_simple(50, 20, "THE DAILY WIRE", 255, 215, 0, 3)
    
    # Date
    draw_text_simple(WIDTH - 300, 35, "SUNDAY, NOVEMBER 23, 2026", 200, 200, 200, 1)
    
    # Main headline block background
    draw_rect(40, 100, WIDTH - 80, 180, 255, 255, 240)
    draw_rect(40, 100, WIDTH - 80, 4, 0, 0, 0)
    draw_rect(40, 276, WIDTH - 80, 4, 0, 0, 0)
    draw_rect(40, 100, 4, 180, 0, 0, 0)
    draw_rect(WIDTH - 44, 100, 4, 180, 0, 0, 0)
    
    # Big headline
    draw_text_simple(60, 120, "COP31 TALKS COLLAPSE", 0, 0, 0, 3)
    draw_text_simple(60, 170, "ANTHROPIC $81.3B IPO FALLS 9%", 0, 0, 0, 2)
    draw_text_simple(60, 210, "S. KOREA KOSPI LOW - ED MINISTER QUITS", 0, 0, 0, 2)
    
    # Column rules (vertical lines separating columns)
    col_width = (WIDTH - 120) // 4
    for i in range(1, 4):
        x = 60 + i * col_width
        draw_line(x, 300, x, HEIGHT - 60, 150, 150, 150)
    
    # Section headers and story text lines (thin rectangles)
    stories = [
        # Column 1
        (60, 300, "CHINA-JAPAN TENSIONS RISE", [
            "Nvidia spy campaign uncovered",
            "SEC probe into chip exports",
            "Diplomatic talks stall in Tokyo",
            "Trade restrictions loom large",
        ]),
        # Column 2
        (60 + col_width, 300, "EL CHAPO ISIDRO CAPTURED", [
            "Mexican navy nabs cartel head",
            "After 15-year manhunt ends",
            "Extradition to US expected",
            "Violence spikes in Sinaloa",
        ]),
        # Column 3
        (60 + 2*col_width, 300, "RUSSIAN STRIKE ON LVIV", [
            "Missiles hit western Ukraine",
            "Civilian casualties reported",
            "Power grid damaged severely",
            "Zelensky calls for more aid",
        ]),
        # Column 4
        (60 + 3*col_width, 300, "LAHORE AQI HITS 500+", [
            "Hazardous air chokes city",
            "Schools closed indefinitely",
            "Crop burning blamed again",
            "Emergency measures enacted",
        ]),
    ]
    
    # Bottom story spanning columns
    bottom_y = 600
    draw_rect(60, bottom_y, WIDTH - 120, 4, 0, 0, 0)
    draw_text_simple(60, bottom_y + 10, "HONDA RECALLS 810K VEHICLES", 0, 0, 0, 2)
    draw_text_simple(60, bottom_y + 40, "Fuel pump defect risks engine stall - Civic, Accord, CR-V models affected", 0, 0, 0, 1)
    
    for col_x, start_y, header, lines in stories:
        # Section header background
        draw_rect(col_x, start_y, col_width - 10, 30, 0, 0, 0)
        draw_text_simple(col_x + 5, start_y + 5, header, 255, 255, 255, 1)
        
        # Text lines as thin rectangles
        line_y = start_y + 40
        for line in lines:
            # Draw line background
            draw_rect(col_x, line_y, col_width - 10, 18, 245, 245, 245)
            # Draw text
            draw_text_simple(col_x + 3, line_y + 3, line[:35], 30, 30, 30, 1)
            line_y += 22
    
    # Add some decorative horizontal rules
    draw_line(60, 290, WIDTH - 60, 290, 0, 0, 0)
    draw_line(60, 580, WIDTH - 60, 580, 0, 0, 0)
    draw_line(60, HEIGHT - 60, WIDTH - 60, HEIGHT - 60, 0, 0, 0)

    # WORLD IN BRIEF boxed section
    brief_x = 60
    brief_y = 720
    brief_w = WIDTH - 120
    brief_h = 100
    # background
    draw_rect(brief_x, brief_y, brief_w, brief_h, 240, 240, 240)
    # border
    draw_rect(brief_x, brief_y, brief_w, 4, 0, 0, 0)
    draw_rect(brief_x, brief_y + brief_h - 4, brief_w, 4, 0, 0, 0)
    draw_rect(brief_x, brief_y, 4, brief_h, 0, 0, 0)
    draw_rect(brief_x + brief_w - 4, brief_y, 4, brief_h, 0, 0, 0)
    # header
    draw_text_simple(brief_x + 10, brief_y + 5, "WORLD IN BRIEF", 0, 0, 0, 2)
    # bullet rows
    bullets = ["- Item A", "- Item B", "- Item C", "- Item D"]
    bullet_y = brief_y + 30
    for b in bullets:
        draw_text_simple(brief_x + 10, bullet_y, b, 0, 0, 0, 1)
        bullet_y += 20

    # Folio line with page number
    draw_text_simple(WIDTH - 70, HEIGHT - 30, "3", 0, 0, 0, 2)

    return pixels

if __name__ == "__main__":
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assets_dir = os.path.join(repo_root, "assets")
    os.makedirs(assets_dir, exist_ok=True)
    output_path = os.path.join(assets_dir, "entry.png")
    
    print(f"Generating {WIDTH}x{HEIGHT} newspaper PNG...")
    pixels = make_image()
    write_png(output_path, pixels)
    
    size = os.path.getsize(output_path)
    print(f"Written to {output_path} ({size} bytes, {size/1024:.1f} KB)")
    if size > 1024 * 1024:
        print("WARNING: File exceeds 1MB limit!")
    else:
        print("File size OK (< 1MB)")