#!/usr/bin/env python
#-*- coding:utf8 -*-

import add_header
import align

with open('./res/index.txt', 'r') as fh:
	lines = fh.readlines()
for i, line in enumerate(lines, 1):
	path = './res/'
	filename = str(i)
	with open(path + filename + '.bmp', 'rb') as img_in_fh:
		width, height, offset = line.split()
		width, height, offset = int(width), int(height), int(offset)
		with open(filename + '.out.bmp', 'wb') as img_out_fh:
			head_info_obj = add_header.header_info(img_out_fh)
			head_info_obj.gen_header(width, height)
			if width % 4 == 0:
				raw = img_in_fh.read()
				img_out_fh.write(raw)
			else:
				align_obj = align.aligner(img_in_fh, img_out_fh)
				align_obj.align_write(width, height)
