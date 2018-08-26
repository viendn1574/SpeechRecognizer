# -*- coding: utf-8 -*-
import ttk
from Tkinter import *
import codecs
import Edit_box
import utils

# -- Declaration of font styles --- #
font_title = ("Helvetica", 18, "bold")
font_message = ("Helvetica", 14)
font_message_small = ("Helvetica", 11)
font_vKeyboard = ("Helvetica", 10)
font_vKeyboardSpecialKeys = ("Helvetica", 10, "bold")

# -- GUI's main class -- #
Edit_box.object=None
class GUI(Toplevel):
    def __init__(self, root, Listbox):
        Toplevel.__init__(self)

        container = ttk.Frame(self, width=480, height=320)
        container.grid_propagate(0)
        container.pack(fill="both", expand=1)

        ttk.Style().configure("vKeyboard.TButton", font=font_vKeyboard)
        ttk.Style().configure("vKeyboardSpecial.TButton", font=font_vKeyboardSpecialKeys)

        self.frames = {}

        F=EditPage
        page_name = F.__name__
        frame = F(parent=container, root=root, Listbox=Listbox)
        self.frames[page_name] = frame

        frame.grid(row=0, column=0, sticky="nsew")
        self.showFrame("EditPage")
        Edit_box.object=self
        self.grab_set()

    def showFrame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class EditPage(ttk.Frame):
    def __init__(self, parent, root, Listbox):
        ttk.Frame.__init__(self, parent)

        self.root = root
        self.Listbox = Listbox

        label1 = ttk.Label(self, text="Edit", font=font_title)
        label1.pack(side="top", fill="x", pady=7, padx=10)

        self.label1 = ttk.Label(self, text="Enter the name:", font=font_message)
        self.label1.pack(side="top")
        self.entry1 = ttk.Entry(self)
        self.entry1.pack(side="top")

        self.label0 = ttk.Label(self, text="  ", font=font_message)
        self.label0.pack(side="top")
        self.label2 = ttk.Label(self, text="  ", font=font_message)
        self.label2.pack(side="top")

        self.frame1 = ttk.Frame(self, width=480, height=320)
        self.frame1.pack(side="top", pady=30,padx=15)

        self.keysize = 4

        self.entry1.bind("<FocusIn>", lambda e:  self.show_vKeyboard())

        self.kb = vKeyboard(parentPage=self,
                            attach=self.entry1,
                            x=self.entry1.winfo_rootx(),
                            y=self.entry1.winfo_rooty() + self.entry1.winfo_reqheight(),
                            keysize=self.keysize,
                            parent=self.frame1,
                            root=self.root,
                            Listbox=self.Listbox)

    def show_vKeyboard(self):
        self.frame1.destroy()
        self.kb.destroy()

        self.frame1 = ttk.Frame(self, width=480, height=320)
        self.frame1.pack(side="top", pady=30,padx=15)
        self.kb = vKeyboard(parentPage=self,
                            attach=self.entry1,
                            x=self.entry1.winfo_rootx(),
                            y=self.entry1.winfo_rooty() + self.entry1.winfo_reqheight(),
                            keysize=self.keysize,
                            parent=self.frame1,
                            root=self.root,
                            Listbox=self.Listbox)

    def get_entry(self):
        return self.entry1
class vKeyboard(ttk.Frame):
    # --- A frame for the keyboard(s) itself --- #
    def __init__(self, parentPage, parent, attach, x, y, keysize, root, Listbox):
        ttk.Frame.__init__(self, takefocus=0)

        self.attach = attach
        self.keysize = keysize
        self.parent = parent
        self.x = x
        self.y = y
        self.parentPage = parentPage
        self.root = root
        self.Listbox = Listbox

    # --- Different sub-keyboards (e.g. alphabet, symbols..) --- #
        # --- Lowercase alphabet sub-keyboard --- #
        self.alpha_Frame = ttk.Frame(parent)
        self.alpha_Frame.grid(row=0, column=0, sticky="nsew")

        self.row1_alpha = ttk.Frame(self.alpha_Frame)
        self.row2_alpha = ttk.Frame(self.alpha_Frame)
        self.row3_alpha = ttk.Frame(self.alpha_Frame)
        self.row4_alpha = ttk.Frame(self.alpha_Frame)

        self.row1_alpha.grid(row=1)
        self.row2_alpha.grid(row=2)
        self.row3_alpha.grid(row=3)
        self.row4_alpha.grid(row=4)

        # --- Uppercase alphabet sub-keyboard --- #
        self.Alpha_Frame = ttk.Frame(parent)
        self.Alpha_Frame.grid(row=0, column=0, sticky="nsew")

        self.row1_Alpha = ttk.Frame(self.Alpha_Frame)
        self.row2_Alpha = ttk.Frame(self.Alpha_Frame)
        self.row3_Alpha = ttk.Frame(self.Alpha_Frame)
        self.row4_Alpha = ttk.Frame(self.Alpha_Frame)

        self.row1_Alpha.grid(row=1)
        self.row2_Alpha.grid(row=2)
        self.row3_Alpha.grid(row=3)
        self.row4_Alpha.grid(row=4)

        # --- Symbols and numerals sub-keyboard --- #
        self.Symbol_Frame = ttk.Frame(parent)
        self.Symbol_Frame.grid(row=0, column=0, sticky="nsew")

        self.row1_Symbol = ttk.Frame(self.Symbol_Frame)
        self.row2_Symbol = ttk.Frame(self.Symbol_Frame)
        self.row3_Symbol = ttk.Frame(self.Symbol_Frame)
        self.row4_Symbol = ttk.Frame(self.Symbol_Frame)

        self.row1_Symbol.grid(row=1)
        self.row2_Symbol.grid(row=2)
        self.row3_Symbol.grid(row=3)
        self.row4_Symbol.grid(row=4)

        # --- Initialize all sub-keyboards --- #
        self.keyState = 1
        self.init_keys()

        self.alpha_Frame.tkraise()

        self.pack()

    def init_keys(self):
        self.alpha = {
            'row1': ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'Bksp'],
            'row2': ['Sym', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
            'row3': ['ABC', 'z', 'x', 'c', 'v', 'b', 'n', 'm', 'ENTER'],
            'row4': ['<<<', '[ space ]', '>>>', 'BACK']
        }
        self.Alpha = {
            'row1': ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'Bksp'],
            'row2': ['Sym', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            'row3': ['abc', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'ENTER'],
            'row4': ['<<<', '[ space ]', '>>>', 'BACK']
        }
        self.Symbol = {
            'row1': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'Bksp'],
            'row2': ['abc', '!', '"', '$', '%', '&', '/', '(', ')', '[', ']', '='],
            'row3': ['@', '-', '_', '?', '#', '*', '{', '}', ':', ';', 'ENTER'],
            'row4': ['<<<','+', '[ space ]', '.', ',', '>>>', 'BACK']
        }

        for i in range(1, 4):
            if i == 1:
                self.keyStyle = self.alpha
                self.row1 = self.row1_alpha
                self.row2 = self.row2_alpha
                self.row3 = self.row3_alpha
                self.row4 = self.row4_alpha
            elif i == 2:
                self.keyStyle = self.Alpha
                self.row1 = self.row1_Alpha
                self.row2 = self.row2_Alpha
                self.row3 = self.row3_Alpha
                self.row4 = self.row4_Alpha
            elif i == 3:
                self.keyStyle = self.Symbol
                self.row1 = self.row1_Symbol
                self.row2 = self.row2_Symbol
                self.row3 = self.row3_Symbol
                self.row4 = self.row4_Symbol

            for row in self.keyStyle.iterkeys():  # iterate over dictionary of rows
                if row == 'row1':  # TO-DO: re-write this method
                    i = 1  # for readability and functionality
                    for k in self.keyStyle[row]:
                        if k == 'Bksp':
                            ttk.Button(self.row1,
                                       style="vKeyboardSpecial.TButton",
                                       text=k,
                                       width=self.keysize * 2,
                                       command=lambda k=k: self._attach_key_press(k)).grid(row=0, column=i)
                        else:
                            ttk.Button(self.row1,
                                       style="vKeyboard.TButton",
                                       text=k,
                                       width=self.keysize,
                                       command=lambda k=k: self._attach_key_press(k)).grid(row=0, column=i)
                        i += 1
                elif row == 'row2':
                    i = 2
                    for k in self.keyStyle[row]:
                        if k == 'Sym':
                            ttk.Button(self.row2,
                                       style="vKeyboardSpecial.TButton",
                                       text=k,
                                       width=self.keysize * 1.5,
                                       command=lambda k=k: self._attach_key_press(k)).grid(row=0, column=i)
                        elif k == 'abc':
                            ttk.Button(self.row2,
                                       style="vKeyboardSpecial.TButton",
                                       text=k,
                                       width=self.keysize * 1.5,
                                       command=lambda k=k: self._attach_key_press(k)).grid(row=0, column=i)
                        else:
                            ttk.Button(self.row2,
                                       style="vKeyboard.TButton",
                                       text=k,
                                       width=self.keysize,
                                       command=lambda k=k: self._attach_key_press(k)).grid(row=0, column=i)
                        i += 1
                elif row == 'row3':
                    i = 2
                    for k in self.keyStyle[row]:
                        if k == 'ABC':
                            ttk.Button(self.row3,
                                       style="vKeyboardSpecial.TButton",
                                       text=k,
                                       width=self.keysize * 1.5,
                                       command=lambda k=k: self._attach_key_press(k)).grid(row=0, column=i)
                        elif k == 'abc':
                            ttk.Button(self.row3,
                                       style="vKeyboardSpecial.TButton",
                                       text=k,
                                       width=self.keysize * 1.5,
                                       command=lambda k=k: self._attach_key_press(k)).grid(row=0, column=i)
                        elif k == 'ENTER':
                            ttk.Button(self.row3,
                                       style="vKeyboardSpecial.TButton",
                                       text=k,
                                       width=self.keysize * 2.5,
                                       command=lambda k=k: self._attach_key_press(k)).grid(row=0, column=i)
                        else:
                            ttk.Button(self.row3,
                                       style="vKeyboard.TButton",
                                       text=k,
                                       width=self.keysize,
                                       command=lambda k=k: self._attach_key_press(k)).grid(row=0, column=i)
                        i += 1
                else:
                    i = 3
                    for k in self.keyStyle[row]:
                        if k == '[ space ]':
                            ttk.Button(self.row4,
                                       style="vKeyboard.TButton",
                                       text='     ',
                                       width=self.keysize * 6,
                                       command=lambda k=k: self._attach_key_press(k)).grid(row=0, column=i)
                        elif k == 'BACK':
                            ttk.Button(self.row4,
                                       style="vKeyboardSpecial.TButton",
                                       text=k,
                                       width=self.keysize * 2,
                                       command=lambda k=k: self._attach_key_press(k)).grid(row=0, column=i)
                        else:
                            ttk.Button(self.row4,
                                       style="vKeyboard.TButton",
                                       text=k,
                                       width=self.keysize,
                                       command=lambda k=k: self._attach_key_press(k)).grid(row=0, column=i)
                        i += 1
    def _replace_vietnamese(self,charArr,tempArr,word):
        indexChar=-1
        indexFind=-1
        result=False
        for i in tempArr:
            if word.rfind(i.decode('utf-8'))>=0:
                indexFind=word.rfind(i.decode('utf-8'));
                indexChar=tempArr.index(i)
                break
        if (indexFind>=0):
            word=utils.replaceStringByIndex(word,charArr[indexChar].decode('utf-8'),indexFind)
        else:
            for i in charArr:
                if word.rfind(i.decode('utf-8'))>=0:
                    word=utils.replaceStringByIndex(word, tempArr[charArr.index(i)].decode('utf-8'),word.rfind(i.decode('utf-8')))
                    result=True
                    break
        return result,word
    def _check_vietnamese(self,k):
        valueOfEntry=self.attach.get()
        if (valueOfEntry!="" and valueOfEntry[valueOfEntry.__len__()-1]==" "):
            return False
        valueOfEntry=valueOfEntry.split()
        length=valueOfEntry.__len__()
        result=False
        if length>0:
            if valueOfEntry[length-1].rfind(k)!=valueOfEntry[length-1].find(k):
                return False
            elif k=='e' or k=='E':
                cha=["e","E","é","É","è","È","ẻ","Ẻ","ẽ","Ẽ","ẹ","Ẹ"]
                temp=["ê","Ê","ế","Ế","ề","Ề","ể","Ể","ễ","Ễ","ệ","Ẹ"]
                result,valueOfEntry[length-1] = self._replace_vietnamese(charArr=cha,tempArr=temp,word=valueOfEntry[length-1])
            elif k=='o' or k=='O':
                cha=["o","O","ó","Ó","ò","Ò","ỏ","Ỏ","õ","Õ","ọ","Ọ"]
                temp=["ô","Ô","ố","Ố","ồ","Ồ","ổ","Ổ","ỗ","Ỗ","ộ","Ộ"]
                result,valueOfEntry[length-1] = self._replace_vietnamese(charArr=cha,tempArr=temp,word=valueOfEntry[length-1])
            elif k=='a' or k =='A':
                cha=["a","A","á","Á","à","À","ã","Ã","ạ","Ạ","ả","Ả"]
                temp=["â","Â","ấ","Ấ","ầ","Ầ","ẫ","Ẫ","ậ","Ậ","ẩ","Ẩ"]
                result,valueOfEntry[length-1] = self._replace_vietnamese(charArr=cha,tempArr=temp,word=valueOfEntry[length-1])
            elif k=='d' or k=="D":
                cha=["d","D"]
                temp=["đ","Đ"]
                result,valueOfEntry[length-1] = self._replace_vietnamese(charArr=cha,tempArr=temp,word=valueOfEntry[length-1])
            elif k=='s' or k=='S':
                cha=["ươ","Ươ","ƯƠ","a","A","â","Â","ă","Ă","o","O","ô","Ô","ơ","Ơ","e","E","ê","Ê","y","Y","u","U","ư","Ư","i","I"]
                temp=["ướ","Ướ","ƯỚ","á","Á","ấ","Ấ","ắ","Ắ","ó","Ó","ố","Ố","ớ","Ớ","é","É","ế","Ế","ý","Ý","ú","Ú","ứ","Ứ","í","Í"]
                result,valueOfEntry[length-1] = self._replace_vietnamese(charArr=cha,tempArr=temp,word=valueOfEntry[length-1])
            elif k=='f' or k=='F':
                cha=["ươ","Ươ","ƯƠ","a","A","â","Â","ă","Ă","o","O","ô","Ô","ơ","Ơ","e","E","ê","Ê","y","Y","u","U","ư","Ư","i","I"]
                temp=["ườ","Ườ","ƯỜ","à","À","ầ","Ầ","ằ","Ằ","ò","Ò","ồ","Ồ","ờ","Ờ","è","È","ề","Ề","ỳ","Ỳ","ù","Ù","ừ","Ừ","ì","Ì"]
                result,valueOfEntry[length-1] = self._replace_vietnamese(charArr=cha,tempArr=temp,word=valueOfEntry[length-1])
            elif k=='j' or k=='J':
                cha=["ươ","Ươ","ƯƠ","a","A","â","Â","ă","Ă","o","O","ô","Ô","ơ","Ơ","e","E","ê","Ê","y","Y","u","U","ư","Ư","i","I"]
                temp=["ượ","Ượ","ƯỢ","ạ","Ạ","ậ","Ậ","ặ","Ặ","ọ","Ọ","ộ","Ộ","ợ","Ợ","ẹ","Ẹ","ệ","Ệ","ỵ","Ỵ","ụ","Ụ","ự","Ự","ị","Ị"]
                result,valueOfEntry[length-1] = self._replace_vietnamese(charArr=cha,tempArr=temp,word=valueOfEntry[length-1])
            elif k=='r' or k=='R':
                cha=["ươ","Ươ","ƯƠ","a","A","â","Â","ă","Ă","o","O","ô","Ô","ơ","Ơ","e","E","ê","Ê","y","Y","u","U","ư","Ư","i","I"]
                temp=["ưở","Ưở","ƯỞ","ả","Ả","ẩ","Ẩ","ẳ","Ẳ","ỏ","Ỏ","ổ","Ổ","ở","Ở","ẻ","Ẻ","ể","Ể","ỷ","Ỷ","ủ","Ủ","ử","Ử","ỉ","Ỉ"]
                result,valueOfEntry[length-1] = self._replace_vietnamese(charArr=cha,tempArr=temp,word=valueOfEntry[length-1])
            elif k=='x' or k=='X':
                cha=["ươ","Ươ","ƯƠ","a","A","â","Â","ă","Ă","o","O","ô","Ô","ơ","Ơ","e","E","ê","Ê","y","Y","u","U","ư","Ư","i","I"]
                temp=["ưỡ","Ưỡ","ƯỠ","ã","Ã","ẫ","Ẫ","ẵ","Ẵ","õ","Õ","ỗ","Ỗ","ỡ","Ỡ","ẽ","Ẽ","ễ","Ễ","ỹ","Ỹ","ũ","Ũ","ữ","Ữ","ĩ","Ĩ"]
                result,valueOfEntry[length-1] = self._replace_vietnamese(charArr=cha,tempArr=temp,word=valueOfEntry[length-1])
            elif k=='w' or k=="W":
                cha=["uo","Uo","UO","a","A","o","O","u","U"]
                temp=["ươ","Ươ","ƯƠ","ă","Ă","ơ","Ơ","ư","Ư"]
                result,valueOfEntry[length-1] = self._replace_vietnamese(charArr=cha,tempArr=temp,word=valueOfEntry[length-1])
        else: return False
        a=" ".join(item for item in valueOfEntry)
        self.attach.delete(0, END)
        self.attach.insert(0,a)
        return result
    def _attach_key_press(self, k):
        if k == '>>>':
            self.attach.tk_focusNext().focus_set()
        elif k == '<<<':
            self.attach.tk_focusPrev().focus_set()
        elif k == 'Sym':
            self.Symbol_Frame.tkraise()
        elif k == 'abc':
            self.alpha_Frame.tkraise()
        elif k == 'ABC':
            self.Alpha_Frame.tkraise()
        elif k == 'Bksp':
            self.remaining = self.attach.get()[:-1]
            self.attach.delete(0, END)
            self.attach.insert(0, self.remaining)
        elif k == 'ENTER':
            print('feature_support.Enter_click')
            u1 = self.attach.get()
            newrow = []
            selected = self.Listbox.get(ACTIVE)
            with codecs.open('./data/list_person.txt', 'r',"utf-8-sig") as lpfile:
                for person in lpfile:
                    row = person.split()
                    if (row != []):
                        if int(row[0]) == int(selected[0]):
                            row[1] = u1
                        newrow.append(row)
            with open('./data/list_person.txt', 'wb') as lpfile:
                i = 0
                for row in newrow:
                    self.Listbox.delete(i)
                    self.Listbox.insert(i, "%s ----- %s" % (row[0], row[1]))
                    lpfile.write("%s %s\n"%(row[0].encode('utf-8'),row[1].encode('utf-8')))
                    i += 1
            self.Listbox.update()
            self.parentPage.destroy()
            self.root.grab_set()
            Edit_box.object.destroy()

        elif k == 'BACK':
            self.parentPage.destroy()
            self.root.grab_set()
            Edit_box.object.destroy()
        elif k == '[ space ]':
            self.attach.insert(END, ' ')
        else:
            if not self._check_vietnamese(k):
                self.attach.insert(END,k )

if __name__ == "__main__":
    app = GUI()
    app.mainloop()