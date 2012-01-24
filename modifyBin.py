#!/usr/bin/env python
#-*- coding:utf8 -*-
import mmap

offset = 990304
width = 600 
height = 800

with open('raw', 'rb') as img_data_fh:
	raw = img_data_fh.read()
with open('ebres.BIN', 'r+b') as fh:
	map_file = mmap.mmap(fh.fileno(), 0)
	map_file[offset : offset + width * height] = raw
