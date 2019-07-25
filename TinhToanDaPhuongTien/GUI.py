from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import LZW
import huffman

class GUI(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.root = root

        self.xForButton = 430
        self.xForEntry = 120
        self.xForLabel = 10

        self.quality = 95

        self.AlgorithmLossLesses = ("Huffman coding", "LZW")
        
        self.algorithmChoose = self.AlgorithmLossLesses[0]
        self.fileName = ""

    def setWindow(self):
        self.root.title("Compress Picture")
        Width = 800
        height = 600
        self.root.geometry(('%dx%d') %(Width, height))

        Label1 = Label(self.root, text = "UIT - KHCL2017", font = ("Century Gothic", 16, "bold"), fg = "#FF0099")
        Label1.place(x = 10, y = 5)
        Label2 = Label(self.root, text = "CS232.J21.KHCL", font = ("Century Gothic", 16, "bold"), fg = "#FF0099")
        Label2.place(x = 5, y = 30)
        Label3 = Label(self.root, text = "Multimedia Computing", font = ("Century Gothic", 14, "bold"), fg = "#FF0099")
        Label3.place(x = 370, y = 5) 
        Label4 = Label(self.root, text = "Lossless compress for picture", font = ("Century Gothic", 14), fg = "#FF0099")
        Label4.place(x = 355, y = 30)

        #Info HungAn
        HungAn = Image.open("D:/TinhToanDaPhuongTien/hinh/HungAn.jpg")
        HungAnpic = ImageTk.PhotoImage(HungAn)
        labelAn = Label(self.root, image=HungAnpic)
        labelAn.image = HungAnpic
        labelAn.place(x = 50, y = 55)

        Label5 = Label(self.root, text = "An Minh Hùng", font = ("Century Gothic", 14, "bold"), fg = "#FF0099")
        Label5.place(x = 210, y = 100)
        Label6 = Label(self.root, text = "17520531", font = ("Century Gothic", 14, "bold"), fg = "#FF0099")
        Label6.place(x = 210, y = 135)
        Label7 = Label(self.root, text = "Cài đặt thuật toán", font = ("Century Gothic", 14, "bold"), fg = "#FF0099")
        Label7.place(x = 210, y = 170)

        #info DuyTan
        DuyTan = Image.open("D:/TinhToanDaPhuongTien/hinh/DuyTan.jpg")
        DuyTanpic = ImageTk.PhotoImage(DuyTan)
        labelTan = Label(self.root, image=DuyTanpic)
        labelTan.image = DuyTanpic
        labelTan.place(x = 428, y = 55)

        Label8 = Label(self.root, text = "Võ Duy Tân", font = ("Century Gothic", 14, "bold"), fg = "#FF0099")
        Label8.place(x = 583, y = 100)
        Label9 = Label(self.root, text = "17521021", font = ("Century Gothic", 14, "bold"), fg = "#FF0099")
        Label9.place(x = 583, y = 135)
        Label10 = Label(self.root, text = "Viết báo cáo", font = ("Century Gothic", 14, "bold"), fg = "#FF0099")
        Label10.place(x = 583, y = 170)

    def drawUI(self):
        # open image
        LabelFileName = Label(self.root, text = "File Name", font = ("Century Gothic", 12, "bold"), fg = "#FF0099")
        LabelFileName.place(x = self.xForLabel, y = 255) #105

        entry = Entry(self.root, textvariable = "",  font = ("Century Gothic", 12), width = 32)
        entry.pack()
        entry.insert(0, "")
        entry.place(x = self.xForEntry, y = 255)  #105

        buttonOpenFile = Button(self.root, text = "Select File", width = 10, height = 2, bg = "#FF0099", fg = "#FFFFFF", command=lambda:self.onOpen(entry))
        buttonOpenFile.place(x = self.xForButton, y = 250) #100

        LabelFileDecode = Label(self.root, text = "Type File Decode", font = ("Century Gothic", 12, "bold"), fg = "#FF0099")
        LabelFileDecode.place(x = self.xForButton + 100, y = 270)  #150
        typeFile = Entry(self.root, textvariable = "",  font = ("Century Gothic", 12), width =10)
        typeFile.pack()
        typeFile.insert(0, ".bmp")
        typeFile.place(x = self.xForButton + 125, y = 300) #180

        # log, notification and status
        infoText = Text(root, font = ("Century Gothic", 12), width = 55, height = 10)
        infoText.pack()
        infoText.place(x = 100, y = 380)  #x=100 y=330
        infoText.insert(INSERT, "")

        # choose algorithm lossless
        LabelAlgorithmLL = Label(self.root, text = "Algorithm\nLossless", font = ("Century Gothic", 12, "bold"), fg = "#FF0099")
        LabelAlgorithmLL.place(x = self.xForLabel, y = 300)  #200

        cbbLossless = ttk.Combobox(self.root, values=self.AlgorithmLossLesses, font = ("Century Gothic", 12), state='readonly', width = 30, height = 20)
        cbbLossless.set(self.AlgorithmLossLesses[0])
        cbbLossless.bind('<<ComboboxSelected>>', self.onSelect)
        cbbLossless.place(x = self.xForEntry, y = 315)  #215
        
        ButtonLossless = Button(self.root, text = "Lossless\nCompress", width = 10, height = 2, bg = "#FF0099", fg = "#FFFFFF", command=lambda:self.actionLosslessCompress(infoText))
        ButtonLossless.place(x = self.xForButton, y = 310)  #210

        ButtonDeLossless = Button(self.root, text = "Lossless\nDecompress", width = 10, height = 2, bg = "#FF0099", fg = "#FFFFFF", command=lambda:self.actionLosslessDecompress(typeFile.get(), infoText))
        ButtonDeLossless.place(x = self.xForButton + 250, y = 280) #142

    def onOpen(self, entry):
        self.fileName = filedialog.askopenfilename(initialdir = "/",title = "Select Picture",filetypes = (("Bitmap Image File","*.BMP"),
                                                                                                ("JPEG", "*.JPEG;*.JPG;*.JPE"),
                                                                                                ("PNG", "*.PNG"),
                                                                                                ("BIN", "*.BIN"),
                                                                                                ("Numpy array Python", "*.npy"),
                                                                                                ("All Files","*")))
        FileCSV = self.fileName
        entry.delete(0, END)
        entry.insert(0, FileCSV)

    def onSelect(self, event=None):
        print('----------------------------')

        if event: # <-- this works only with bind because `command=` doesn't send event
            self.algorithmChoose = event.widget.get()
            print("choose alogorthm:", self.algorithmChoose)

    
    def print_value(self, val):
        self.quality = val

    def actionLosslessCompress(self, showLog):
        try: 
            #Huffman coding  
            if (self.algorithmChoose == self.AlgorithmLossLesses[0]):
                h = huffman.HuffmanCoding()
                outputPath, log = h.compress(self.fileName) 

                print(log)
                showLog.delete('1.0', END)
                showLog.insert(INSERT, log)     
            #LZW
            elif (self.algorithmChoose == self.AlgorithmLossLesses[1]):
                l = LZW.LZW()
                outputPath, log = l.encode(self.fileName)

                print(log)
                showLog.delete('1.0', END)
                showLog.insert(INSERT, log)

        except:
            showLog.delete('1.0', END)
            showLog.insert(INSERT, "Compress error!")

    def actionLosslessDecompress(self, typeFile, showLog):
        try:
            #Huffman coding        
            if (self.algorithmChoose == self.AlgorithmLossLesses[0]):
                h = huffman.HuffmanCoding()

                fileName, FileExtension = os.path.splitext(self.fileName)

                outputPath, log = h.decompress(self.fileName, typeFile)

                print(log)
                showLog.delete('1.0', END)
                showLog.insert(INSERT, log)
            #LZW
            if (self.algorithmChoose == self.AlgorithmLossLesses[1]):
                l = LZW.LZW()
                log = l.decode(self.fileName, typeFile) 

                print(log)
                showLog.delete('1.0', END)
                showLog.insert(INSERT, log)
            
        except:
            showLog.delete('1.0', END)
            showLog.insert(INSERT, "Decompress error!")

root = Tk()
app = GUI(root)
app.setWindow()
app.drawUI()
root.mainloop()
