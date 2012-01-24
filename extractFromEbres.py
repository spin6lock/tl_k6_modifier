#!/usr/bin/env python
#-*- coding:utf8 -*-
import struct

start_point = 0x200 - 5
end_mark = '8BPP'

def find_width_and_height():
	global fh
	width_and_height = fh.read(8)
#import ipdb; ipdb.set_trace()
	fmt = 'll' #long, long, each in 4 bytes	
	return struct.unpack(fmt, width_and_height)

def extract_data(width, height):
	global fh
	size = width * height
	return fh.read(size)

def skip_zero():
	global fh
	char = fh.read(1)
	while char == chr(0x00):
		char = fh.read(1)
	fh.seek(-1, 1)	

if __name__ == '__main__':
	start_name = 1
	fh = open('./ebres.BIN', 'rb')
	fh.seek(start_point, 0)
	while fh:
		skip_zero()
#print hex(fh.tell())
		width, height = find_width_and_height()
		offset = fh.tell()
		print width, height, offset
		raw = extract_data(width, height)
		with open(str(start_name)+".bmp", 'wb') as out_fh:
			out_fh.write(raw)
		start_name += 1
		fh.read(len(end_mark)) #throw away 8BPP
