import os
import zlib
from pathlib import Path
from PIL import Image
import io
import struct

def image_to_hzc(image_path, output_dir="output"):
	"""
	将各种图片格式转换为hzc格式
	"""
	try:
		# 创建输出目录
		os.makedirs(output_dir, exist_ok=True)
		
		# 使用PIL打开图片
		with Image.open(image_path) as img:
			# 转换为RGB或RGBA模式
			if img.mode in ['P', 'L', '1', 'LA']:  # 调色板、灰度、二值等模式
				img = img.convert('RGBA')
			
			# 决定使用24位还是32位
			if img.mode == 'RGBA':
				bits_per_pixel = 32
				bytes_per_pixel = 4
				hzc_bmpkind = b"\x01\x00"
				# 分离通道并重新排列为BGRA
				if img.mode == 'RGBA':
					r, g, b, a = img.split()
					img = Image.merge("RGBA", (b, g, r, a))
			else:
				# 转换为24位BGR格式
				img = img.convert('RGB')
				bits_per_pixel = 24
				bytes_per_pixel = 3
				hzc_bmpkind = b"\x00\x00"
				# 转换为BGR格式
				r, g, b = img.split()
				img = Image.merge("RGB", (b, g, r))
			
			# 获取图片尺寸
			x_size, y_size = img.size
			bmp_size = x_size * y_size * bytes_per_pixel
			
			# 将图片数据转换为字节流（模拟BMP像素数据）
			img_bytes = img.tobytes()
			
				
	except Exception as e:
		print(f"处理图片 {image_path} 时出错: {e}")
		return None
		
	# 最高压缩级别压缩
	compressed_data = zlib.compress(img_bytes, level=9)
	
	# 重建hzc文件头
	zero_num = 0
	uncertain_part = zero_num.to_bytes(20, 'little')
	new_hzcheader = (b"hzc1" + 
					bmp_size.to_bytes(4, 'little') + 
					b"\x20\x00\x00\x00" + 
					b"NVSG" + 
					b"\x00\x01" + 
					hzc_bmpkind + 
					x_size.to_bytes(2, 'little') + 
					y_size.to_bytes(2, 'little') + 
					uncertain_part)
	
	# 生成输出文件名
	filename = os.path.basename(image_path)
	output_file = os.path.join(output_dir, os.path.splitext(filename)[0] + '.hzc')
	
	# 写入hzc文件
	with open(output_file, 'wb') as f:
		f.write(new_hzcheader)
		f.write(compressed_data)
	
	print(f"已转换: {image_path} -> {output_file}")
	return output_file

def hzc_to_image(hzc_path, output_dir="output"):
	"""
	将hzc文件转换为图片格式（默认为PNG）
	"""
	try:
		# 创建输出目录
		os.makedirs(output_dir, exist_ok=True)
		
		with open(hzc_path, 'rb') as f:
			# 读取文件头
			header = f.read(44)
			
			# 解析文件头
			if header[:4] != b'hzc1':
				print(f"{hzc_path} 不是有效的hzc文件")
				return None
				
			# 解析各个字段
			bmp_size = struct.unpack('<I', header[4:8])[0]
			# header[8:12] 是固定的 0x20 0x00 0x00 0x00
			# header[12:16] 是固定的 'NVSG'
			# header[16:18] 是固定的 0x00 0x01
			bmp_kind = struct.unpack('<H', header[18:20])[0]  # 0=24位, 1=32位
			x_size = struct.unpack('<H', header[20:22])[0]
			y_size = struct.unpack('<H', header[22:24])[0]
			# header[24:44] 是不确定部分
			
			# 读取压缩数据
			compressed_data = f.read()
			
			# 解压数据
			decompressed_data = zlib.decompress(compressed_data)
			
			# 根据bmp类型设置参数
			if bmp_kind == 0:  # 24位
				bytes_per_pixel = 3
				mode = 'RGB'
			elif bmp_kind == 1:  # 32位
				bytes_per_pixel = 4
				mode = 'RGBA'
			else:
				print(f"不支持的BMP类型: {bmp_kind}")
				return None
			
			# 检查数据大小
			expected_size = x_size * y_size * bytes_per_pixel
			if len(decompressed_data) != expected_size:
				print(f"解压后数据大小不匹配: 期望 {expected_size}, 实际 {len(decompressed_data)}")
				return None
			
			
			# 创建PIL图像
			if mode == 'RGB':
				# BGR转RGB
				img = Image.frombytes(mode, (x_size, y_size), decompressed_data)
				b, g, r = img.split()
				img = Image.merge("RGB", (r, g, b))
			else:  # RGBA
				# BGRA转RGBA
				img = Image.frombytes(mode, (x_size, y_size), decompressed_data)
				b, g, r, a = img.split()
				img = Image.merge("RGBA", (r, g, b, a))
				
	except Exception as e:
		print(f"处理hzc文件 {hzc_path} 时出错: {e}")
		return None
	
	# 生成输出文件名
	filename = os.path.basename(hzc_path)
	output_file = os.path.join(output_dir, os.path.splitext(filename)[0] + '.png')
	
	# 保存为PNG
	img.save(output_file, 'PNG')
	print(f"已转换: {hzc_path} -> {output_file}")
	return output_file

def process_all_images(input_dir="image", output_dir="output"):
	"""
	处理指定目录下的所有图片文件，转换为hzc格式
	"""
	if not os.path.exists(input_dir):
		print(f"输入目录 {input_dir} 不存在")
		return
	
	supported_formats = {'.bmp', '.jpg', '.jpeg', '.png'}
	
	for filename in os.listdir(input_dir):
		file_path = os.path.join(input_dir, filename)
		if os.path.isfile(file_path):
			file_ext = os.path.splitext(filename)[1].lower()
			if file_ext in supported_formats:
				try:
					image_to_hzc(file_path, output_dir)
				except Exception as e:
					print(f'处理 {filename} 时出错: {e}')

def process_all_hzc(input_dir="hzcfile", output_dir="output"):
	"""
	处理指定目录下的所有hzc文件，转换为PNG图片
	"""
	if not os.path.exists(input_dir):
		print(f"输入目录 {input_dir} 不存在")
		return
	
	for filename in os.listdir(input_dir):
		file_path = os.path.join(input_dir, filename)
		if os.path.isfile(file_path) and filename.lower().endswith('.hzc'):
			try:
				hzc_to_image(file_path, output_dir)
			except Exception as e:
				print(f'处理 {filename} 时出错: {e}')

if __name__ == '__main__':
	# 创建必要的目录
	os.makedirs("image", exist_ok=True)
	os.makedirs("hzcfile", exist_ok=True)
	os.makedirs("output", exist_ok=True)
	
	print("开始处理图片文件...")
	process_all_images("image", "output")
	
	print("\n开始处理hzc文件...")
	process_all_hzc("hzcfile", "output")
	
	print("\n处理完成！")