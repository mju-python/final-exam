import tkinter as tk

def part4_main(root, data):
  # 전체 프레임 초기화
  for widget in root.winfo_children():
    widget.destroy()

  #여기에 웹 크롤링 및 ui 코드 작성해주시면 됩니다. 

  next_button = tk.Button(
    root,
    text="종료하기",
    font=("Arial", 14),     
    width=10,
    height=2,
    command=lambda: root.destroy()
  )
  next_button.pack(pady=10)  