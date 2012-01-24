#coding:utf8

class aligner:
	def __init__(self, in_fh, out_fh):
		self.in_fh = in_fh
		self.out_fh = out_fh

	def align_write(self, width, height):
		in_fh = self.in_fh
		out_fh = self.out_fh
		zero_num = (width/4 + 1) * 4 - width
		for i in range(0, width * height):
			raw = in_fh.read(width)
			out_fh.write(raw)
			out_fh.write(chr(0x00) * zero_num)

	def align_write_raw_data(self, width, height):
		data = self.in_fh
		out_fh = self.out_fh
		zero_num = (width/4 + 1) * 4 - width
		start = 0
		for i in range(0, height):
			raw = data[start:(start + width)]
			out_fh.write(raw)
			out_fh.write(chr(0x00) * zero_num)
			start = i * width
			
