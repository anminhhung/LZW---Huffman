import base64
import os
import numpy as np
import time

class LZW:
    def __init__(self):
        self.imageByteArray = None

    def convertImageToBase64(self, image):
        with open(image, "rb") as f:
            data = f.read()
            stringImage = base64.b64encode(data)
        self.imageByteArray = str(stringImage)[2:]

    def encode(self, imageFile):
        self.convertImageToBase64(imageFile)
        filename, fileExtension = os.path.splitext(imageFile)

        startEncode = time.time()
        result = []

        inputText = self.imageByteArray
        dictSize = 256
        dictionary = {chr(i):i for i in range(dictSize)}

        s = ""
        for c in inputText:
            temp = s + c
            if temp in dictionary:
                s = temp
            else:
                result.append(dictionary[s])
                dictionary[temp] = dictSize
                dictSize += 1
                s = c
        if s:
            result.append(dictionary[s])

        newArrayNumpy = np.array(result)

        fileSaveDic = filename + ".npy"
        np.save(fileSaveDic, newArrayNumpy)
        endEncode = time.time()
        elapsedEncode = endEncode - startEncode
        log = "LZW: \n" + "   Input File: " + imageFile + "\n   Output File: " + fileSaveDic + "\n Time Encode: " + str(elapsedEncode)
        return  fileSaveDic, log

    def decode(self, inputPath, typeFile):
        filename, fileExtension = os.path.splitext(inputPath)
        outputFilename = filename + "_decode" + typeFile

        inputCode = list(np.load(inputPath))
        startDecode = time.time()
        dictSize = 256
        dictionary = {i: chr(i) for i in range(dictSize)}
        result = chr(inputCode.pop(0))
        s = result
        for k in inputCode:
            if k in dictionary:
                entry = dictionary[k]
            elif k == dictSize:
                entry = s + s[0]
            else:
                raise ValueError('Bad compressed k: %s' % k)
            result += entry

            dictionary[dictSize] = s + entry[0]
            dictSize += 1

            s = entry
        temp = result.encode()
        dataToWriteFile = base64.b64decode(temp)

        with open(outputFilename, "wb") as f:
            f.write(dataToWriteFile)
        
        endDecode = time.time()
        elapsedDecode = endDecode - startDecode
        log = "LZW: \n" + "   Input File: " + inputPath + "\n   Output File: " + outputFilename + "\n Time Decode: " + str(elapsedDecode)
        return outputFilename, log

if __name__ == "__main__":
    lzw = LZW()
    image = "D:/TinhToanDaPhuongTien/hinh/lena.bmp"
    encode = "D:/TinhToanDaPhuongTien/hinh/lena.npy"
    re, log = lzw.encode(image)
    print(log)
    re, log = lzw.decode(encode, ".bmp")
    print(log)