from tkinter import *
from tkinter import filedialog


def domenu():
    print("OK")


def load_image():
    file_name = filedialog.askopenfilenames(initialdir="/", title="Select file",
                                            filetypes=(
                                            ("JPEG files", "*.jpeg,*.png"),
                                            ("all files", "*.*")))
    print(file_name)


def load_folder():
    folder_name = filedialog.askdirectory(parent=root, initialdir="/",
                                          title='Please select a directory')
    print(folder_name)


root = Tk()
root.title('Masking ID')
root.geometry('400x200')
root.resizable(width=0, height=0)
menubar = Menu(root)  # 윈도우에 메뉴바 추가
filemenu = Menu(menubar, tearoff=0)  # 상위 메뉴 탭 항목 추가
menubar.add_cascade(label="환경설정", menu=filemenu)  # 상위 메뉴 탭 설정   # 항목 추가
filemenu.add_command(label="파일 지정", command=load_image)
filemenu.add_command(label="폴더 지정", command=load_folder)
filemenu.add_command(label="옵션", command=domenu)
filemenu.add_separator()  # 분리선 추가
filemenu.add_command(label="종료", command=root.quit)

helpmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="도움말", menu=helpmenu)
helpmenu.add_command(label="정보", command=domenu)

root.config(menu=menubar)  # 생성된 객체를 위에서 생성된 메뉴바에 연결
root.mainloop()
