#!/usr/bin/env python
#-*- coding:utf8 -*-
from struct import unpack

class extractWinBmp:
	def __init__(self, in_fh):
		self.in_fh = in_fh
		self.raw_data = None
		self.width = None
		self.height = None

	def check_format(self):
		pass

	def extract_width_and_height(self):
		in_fh = self.in_fh
		in_fh.seek(0x12)
		width_data = in_fh.read(4)
		height_data = in_fh.read(4)
		self.width = unpack('l', width_data)[0]
		height = unpack('l', height_data)[0]
		self.height = abs(height)
		return self.width, self.height

	def extract_data_offset(self):
		in_fh = self.in_fh
		in_fh.seek(0xA)
		offset_data = in_fh.read(4)
		offset = unpack('l', offset_data)[0]
		return offset

	def extract_raw_data(self):
		offset = self.extract_data_offset()
		width, height = self.extract_width_and_height()
		#print "offset ", offset
		#print "width, height", width, height
		self.in_fh.seek(offset)
		self.raw_data = self.in_fh.read(width * height)

