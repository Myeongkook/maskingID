import tkinter
from tkinter import filedialog
import do_something
import threading
import os


def domenu():
    print("OK")


def load_image():
    file_name = filedialog.askopenfilenames(initialdir="/", title="Select file",
                                            filetypes=(
                                            ("Image files", ".jpg .jpeg .png"),
                                            ("all files", "*.*")))
    for i in file_name:
        file_list.append(i)
    insert_list(file_list)
    return file_list


def load_folder():
    folder_name = filedialog.askdirectory(parent=root, initialdir="/",
                                          title='Please select a directory')
    condition = (".jpg", ".jpeg", ".png")
    if len(file_list) < 1:
        list_dir = os.listdir(folder_name)
        for file in list_dir:
            if file.endswith(condition):
                file_list.append(file)
    insert_list(file_list)
    return file_list


def insert_list(list_image):
    my_listbox.delete(0, tkinter.END)
    for i in range(len(list_image)):
        my_listbox.insert(i, list_image[i])
    my_listbox.pack(pady=30)


def do_masking():
    for i in range(len(file_list)):
        threading.Thread(target=do_something.callAPI, args=file_list[i])
        try:
            api = do_something.callAPI(file_list[i])
            do_something.maskingImage(api.json(), file_list[i])
        except Exception as e:
            print(e)


root = tkinter.Tk()
root.title('Masking ID')
root.geometry('500x400')
root.resizable(width=0, height=0)
menubar = tkinter.Menu(root)  # 윈도우에 메뉴바 추가
filemenu = tkinter.Menu(menubar, tearoff=0)  # 상위 메뉴 탭 항목 추가
menubar.add_cascade(label="Menu", menu=filemenu)  # 상위 메뉴 탭 설정   # 항목 추가
filemenu.add_command(label="Setting", command=domenu)
filemenu.add_separator()  # 분리선 추가
filemenu.add_command(label="Exit", command=root.quit)
my_listbox = tkinter.Listbox(root, width=60, height=10, activestyle="none")
my_listbox.pack(pady=25)
file_list = []
root.config(menu=menubar)  # 생성된 객체를 위에서 생성된 메뉴바에 연결
button_1 = tkinter.Button(root, width=15, command=load_image, text='파일 불러오기')
button_1.pack()
button_2 = tkinter.Button(root, width=15, command=load_folder, text='폴더 불러오기')
button_2.pack()
button_3 = tkinter.Button(root, width=15, command=lambda: do_masking(),
                          text='확인')
button_3.pack()
root.mainloop()
