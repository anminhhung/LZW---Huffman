import heapq
import os
from functools import total_ordering
import base64
import numpy as np
import zipfile
import time

@total_ordering
class HeapNode:
	def __init__(self, char, freq):
		self.char = char
		self.freq = freq
		self.left = None
		self.right = None

	# defining comparators less_than and equals
	def __lt__(self, other):
		return self.freq < other.freq

	def __eq__(self, other):
		if(other == None):
			return False
		if(not isinstance(other, HeapNode)):
			return False
		return self.freq == other.freq

class HuffmanCoding:
	def __init__(self):
		self.heap = []
		self.codes = {}
		self.reverse_mapping = dict()

	def convertImageToBase64(self):
		with open(self.imageFile, "rb") as imageFile:
			stringImage = base64.b64encode(imageFile.read())
		
		self.ImageByteArray = bytearray(stringImage)

	def makeFrequencyDict(self, text):
		frequency = {}
		for character in text:
			if not character in frequency:
				frequency[character] = 0
			frequency[character] += 1
		return frequency

	def makeHeap(self, frequency):
		for key in frequency:
			node = HeapNode(key, frequency[key])
			heapq.heappush(self.heap, node)

	def margeNodes(self):
		while(len(self.heap)>1):
			node1 = heapq.heappop(self.heap)
			node2 = heapq.heappop(self.heap)

			merged = HeapNode(None, node1.freq + node2.freq)
			merged.left = node1
			merged.right = node2

			heapq.heappush(self.heap, merged)

	def makeCodesHelper(self, root, currentCode):
		if(root == None):
			return

		if(root.char != None):
			self.codes[root.char] = currentCode
			self.reverse_mapping[currentCode] = root.char
			return

		self.makeCodesHelper(root.left, currentCode + "0")
		self.makeCodesHelper(root.right, currentCode + "1")

	def make_codes(self):
		root = heapq.heappop(self.heap)
		currentCode = ""
		self.makeCodesHelper(root, currentCode)

	def getEncodedText(self, text):
		encodedText = ""
		for character in text:
			encodedText += self.codes[character]
		return encodedText

	def padEncodedText(self, encodedText):
		extraPadding = 8 - len(encodedText) % 8
		for _ in range(extraPadding):
			encodedText += "0"

		paddedInfo = "{0:08b}".format(extraPadding)
		encodedText = paddedInfo + encodedText
		return encodedText

	def getByteArray(self, paddedEncodedText):
		if(len(paddedEncodedText) % 8 != 0):
			print("Encoded text not padded properly")
			exit(0)

		b = bytearray()
		for i in range(0, len(paddedEncodedText), 8):
			byte = paddedEncodedText[i:i+8]
			b.append(int(byte, 2))
		return b

	def compress(self, imageFile = ""):
		filename, fileExtension = os.path.splitext(imageFile) 

		startEncode = time.time()
		self.imageFile = imageFile

		self.convertImageToBase64()

		text = self.ImageByteArray.decode()

		#---------------------------------
		frequency = self.makeFrequencyDict(text)
		self.makeHeap(frequency)
		self.margeNodes()
		self.make_codes()

		encodedText = self.getEncodedText(text)
		paddedEncodedText = self.padEncodedText(encodedText)

		b = self.getByteArray(paddedEncodedText)

		#---------------------------------
		outputPath = filename + ".bin"

		fileSaveBits = "huff_bits.bin"
		output = open(fileSaveBits, "wb")
		output.write(bytes(b))
		output.close()

		fileSaveDict = "huff_dict" + ".npy"

		np.save(fileSaveDict, self.reverse_mapping)
		endEncode = time.time()
		elapsedEncode = endEncode - startEncode

		#---------------------------------

		zipf = zipfile.ZipFile(outputPath, 'w', zipfile.ZIP_DEFLATED)

		zipf.write(fileSaveDict)
		zipf.write(fileSaveBits)
		zipf.close()

		os.remove(fileSaveBits)
		os.remove(fileSaveDict)
		#---------------------------------

		log = "Huffman: \n" + "Input File: " + imageFile + "\n OutputPath: " + outputPath + "\n Time Encode: " + str(elapsedEncode)

		return outputPath, log

	def remove_padding(self, paddedEncodedText):
		paddedInfo = paddedEncodedText[:8]
		extraPadding = int(paddedInfo, 2)

		paddedEncodedText = paddedEncodedText[8:] 
		encodedText = paddedEncodedText[:-1*extraPadding]

		return encodedText

	def decode_text(self, encodedText):
		currentCode = ""
		decodedText = ""

		for bit in encodedText:
			currentCode += bit
			if(currentCode in self.reverse_mapping):
				character = self.reverse_mapping[currentCode]
				decodedText += character
				currentCode = ""

		return decodedText

	def decompress(self, fileEncode, typeFile):
		with zipfile.ZipFile(fileEncode, 'r') as zip_file:
			zip_file.extractall("huffman_temp_zip")

		fileDict = "huffman_temp_zip\\huff_dict.npy"
		fileBits = "huffman_temp_zip\\huff_bits.bin"
		# save np.load
		np_load_old = np.load

		# modify the default parameters of np.load
		np.load = lambda *a,**k: np_load_old(*a, allow_pickle=True, **k)
		#---
		self.reverse_mapping = dict(enumerate(np.load(fileDict).flatten()))
		self.reverse_mapping = self.reverse_mapping[0]
		#---
		np.load = np_load_old
		filename, fileExtension = os.path.splitext(fileEncode)

		startDecode = time.time()
		result = ""
		with open(fileBits, 'rb') as f:
			bitString = ""

			byte = f.read(1)
			while(len(byte) > 0):
				byte = ord(byte)
				bits = bin(byte)[2:].rjust(8, '0')
				bitString += bits
				byte = f.read(1)

			encodedText = self.remove_padding(bitString)

			decompressedText = self.decode_text(encodedText)

			result += decompressedText
		
		fileContent = decompressedText.encode()
		out = filename + "_decode" + typeFile

		with open(out, "wb") as f:
			temp = base64.decodebytes(fileContent)
			f.write(temp)

		endDecode = time.time()
		elapsedDecode = endDecode - startDecode
		log = "Huffman: \n" + "file encode: " + fileEncode +"\n output: " + out + "\n Time Decode: " + str(elapsedDecode)

		import shutil
		shutil.rmtree("huffman_temp_zip")

		return out, log

if __name__ == "__main__":
	h = HuffmanCoding()
	outputPath, log = h.compress("D:/TinhToanDaPhuongTien/hinh/lena.bmp") 
	print(log)
	output, log = h.decompress( "D:/TinhToanDaPhuongTien/hinh/lena.bin", ".bmp") 
	print(log)