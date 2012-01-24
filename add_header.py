#!/usr/bin/env python
#-*- coding:utf8 -*-

#this is aims to little-endian system
from struct import pack

class header_info:
	def __init__(self, fh):
		self.fh = fh

	def construct_bitmap_file_header(self, filesz, offset):
		fh = self.fh
		fh.write('BM') #identifier
		fh.write(pack('l', filesz))	#file size	
		fh.write(chr(0) * 4) #reserved
		fh.write(pack('l', 1078))	#bitmap data offset, 可以在调色板数据和bitmap数据之间添加任意数据，只需正确设置offset即可

	def construct_bitmap_info_header(self, width, height):
		fh = self.fh
		fh.write(pack('l', 0x28))	#bitmap header size, 28 is the sign of windows	
		fh.write(pack('l', width)) #width
		fh.write(pack('l', -height)) #height
		fh.write(pack('h', 1)) #planes, unknown function, always 1
		fh.write(pack('h', 8)) #bits per pixel, 8 means 256 palette
		fh.write(pack('l', 0)) #compression, 0 means not compress
#fh.write(pack('l', width * height)) #bitmap data size, 0 for not compress bitmap
		fh.write(pack('l', 0)) #bitmap data size, 0 for not compress bitmap
		fh.write(pack('l', 0xB12)) #height_resolution, or use 0xB12 represent 2834pixel/meter
		fh.write(pack('l', 0xB12)) #vertical_resolution
		fh.write(pack('l', 0)) #used_colors, 0 means all
		fh.write(pack('l', 0)) #important colors 0 means all colors are important

	def construct_palette(self):
		fh = self.fh
		for i in range(0, 256):
			fh.write(pack('l', i * 0x10101))

	def gen_header(self, width, height):
		datasize = width * height
		offset = 14 + 40 + 256 * 4 
		filesize = offset + datasize
		self.construct_bitmap_file_header(filesize, offset)
		self.construct_bitmap_info_header(width, height)
		self.construct_palette()

if __name__ == '__main__':
	with open("head", 'wb') as fh:
		hi_obj = header_info(fh)
		hi_obj.gen_header(600, 800)
