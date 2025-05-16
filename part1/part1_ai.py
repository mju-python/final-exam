import tkinter as tk
from part3.part3_main import part3_main

def part1_ai(root, data):
   # 전체 프레임 초기화
    for widget in root.winfo_children():
        widget.destroy()
    
    data={"에시데이터 입니다."}
    root.after(3000,lambda: part3_main(root, data))

