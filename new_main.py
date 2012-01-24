#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk
import os
import mmap
import struct

import add_header
import align
import extractFromWinBMP

class view(object):
	def __init__(self):
		builder = gtk.Builder()
		self.builder = builder
		builder.add_from_file("tlk6.glade")
		builder.connect_signals(self)
		self.init_model()
		self.init_widget()
		self.window = builder.get_object("window")
		self.window.show()
	
	def init_widget(self):
		for widget in self.builder.get_objects():
			if issubclass(type(widget), gtk.Buildable):
				name = gtk.Buildable.get_name(widget)
				setattr(self, name, widget)

	def init_model(self):
		self.model = None
		self.index = 0
		self.scale = False
		self.image = gtk.Image()

	def load_image(self, filename):
		if self.scale:
			pixbuf = gtk.gdk.pixbuf_new_from_file(filename)
			ratio = pixbuf.get_width() / float(pixbuf.get_height())
			pixbuf = pixbuf.scale_simple(600, int(600/ratio), gtk.gdk.INTERP_BILINEAR)
			self.image.set_from_pixbuf(pixbuf)
		else:
			self.image.set_from_file(filename)

	def load_firmware(self, widget):
		filename = widget.get_filename()
		self.model = Model(filename)
		self.model.find_and_build_image()
		#display image
		self.next_firmware_pic('t')

	def modify_firmware(self, widget):
		filename = widget.get_filename()
		self.load_image(filename)
		self.model.extract_winbmp(filename)
		self.model.modify_firmware_pic(self.index - 1)

	def prev_firmware_pic(self, widget):
		self.index -= 1
		if self.index < 1:
			self.index = 1
		filename = os.path.join('temp_pic', str(self.index) + ".bmp")
		self.load_image(filename)

	def next_firmware_pic(self, widget):
		self.index += 1
		if self.index > len(self.model.pic_info):
			self.index = len(self.model.pic_info)
		filename = os.path.join('temp_pic', str(self.index) + ".bmp")
		self.load_image(filename)

	def on_destroy(self, widget, data=None):
		gtk.main_quit()

class Model:
	def __init__(self, filename):
		self.pic_info = None #list of tuple (addr, width, height)
		self.new_pic = None
		self.firmware = filename

	def find_and_build_image(self):
		#build dir
		if not os.path.exists('temp_pic'):
			os.makedirs('temp_pic')
		#scan and extract raw data
		ebres_data = util_extract_ebres(self.firmware)	
		ebres_data.extract_gray_data()
		#gen pic
		gen_pic = util_gen_pic(ebres_data)
		gen_pic.gen_pic()
		self.pic_info = ebres_data.pic_info

	def extract_winbmp(self, filename):
		with open(filename, 'rb') as new_pic:
			new_pic = extractFromWinBMP.extractWinBmp(new_pic)
			new_pic.extract_raw_data()
		self.new_pic = new_pic

	def modify_firmware_pic(self, pic_index):
		offset, width, height = self.pic_info[pic_index]
		with open(self.firmware, 'r+b') as firmware:
			map_file = mmap.mmap(firmware.fileno(), 0)
			map_file[offset: (offset + width * height)] = self.new_pic.raw_data

class util_extract_ebres:
	def __init__(self, filename):
		self.fh = open(filename, 'rb')
		self.gray_data = []
		self.pic_info = []

	def find_width_and_height(self):
		fh = self.fh
		width_and_height = fh.read(8)
		fmt = 'll' #long, long, each in 4 bytes	
		return struct.unpack(fmt, width_and_height)

	def read_an_image(self, width, height):
		fh = self.fh
		size = width * height
		return fh.read(size)

	def skip_zero(self):
		fh = self.fh
		char = fh.read(1)
		while char == chr(0x00):
			char = fh.read(1)
		fh.seek(-1, 1)	

	def extract_gray_data(self):
		len_of_end_mark = len('8BPP')
		fh = self.fh
		fh.seek(200-5, 0)
		try:
			while fh:
				self.skip_zero()
				width, height = self.find_width_and_height()
				offset = fh.tell()
				raw = self.read_an_image(width, height)
				self.pic_info.append((offset, width, height))
				self.gray_data.append(raw)
				fh.read(len_of_end_mark)
		except:
			pass

class util_gen_pic:
	def __init__(self, ebres_obj, path="temp_pic"):
		self.path = path
		self.info = ebres_obj.pic_info
		self.data = ebres_obj.gray_data
		
	def gen_pic(self):
		for i, o_w_h in enumerate(self.info, 1):
			offset, width, height = o_w_h
			with open(os.path.join(self.path, str(i) + ".bmp"), "wb") as img_out_fh:
				head_info_obj = add_header.header_info(img_out_fh)
				head_info_obj.gen_header(width, height)
				raw = self.data[i-1]
				if width % 4 == 0:
					img_out_fh.write(raw)
				else:
					align_obj = align.aligner(raw, img_out_fh)
					align_obj.align_write_raw_data(width, height)



if __name__ == "__main__":
	app = view()
	gtk.main()
