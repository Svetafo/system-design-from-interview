#!/usr/bin/env python3
"""Генерирует ссылку на PlantUML Web Server из .puml файла(ов).
Использование: python3 plantuml-url.py file1.puml [file2.puml ...] [--svg]
"""
import sys, zlib

def enc6(b):
    if b < 10: return chr(48 + b)
    b -= 10
    if b < 26: return chr(65 + b)
    b -= 26
    if b < 26: return chr(97 + b)
    b -= 26
    return '-' if b == 0 else ('_' if b == 1 else '?')

def enc3(b1, b2, b3):
    c1 = b1 >> 2
    c2 = ((b1 & 3) << 4) | (b2 >> 4)
    c3 = ((b2 & 15) << 2) | (b3 >> 6)
    c4 = b3 & 63
    return enc6(c1 & 63) + enc6(c2 & 63) + enc6(c3 & 63) + enc6(c4 & 63)

def encode(text):
    data = zlib.compress(text.encode('utf-8'))[2:-4]  # raw deflate
    r = ''
    for i in range(0, len(data), 3):
        ch = data[i:i+3]
        b = [ch[j] if j < len(ch) else 0 for j in range(3)]
        r += enc3(b[0], b[1], b[2])
    return r

def main():
    args = [a for a in sys.argv[1:] if a != '--svg']
    fmt = 'svg' if '--svg' in sys.argv else 'png'
    if not args:
        print(__doc__); sys.exit(1)
    for p in args:
        txt = open(p, encoding='utf-8').read()
        print(f"{p} -> https://www.plantuml.com/plantuml/{fmt}/{encode(txt)}")

if __name__ == '__main__':
    main()
