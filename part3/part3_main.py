import tkinter as tk
from part4.part4_main import part4_main

newData={}
def part3_main(root, data):
  # 전체 프레임 초기화
  for widget in root.winfo_children():
    widget.destroy()

  print(data)

  #여기에 받은 데이터 뿌려주는 ui 코드 작성해주시면 되고
  #data로 오는 데이터 활용하면됩니다. 
  #사용자에게 입력받은 거는 newData에 저장하면 됩니다. 
  

  next_button = tk.Button(
    root,
    text="다음으로",
    font=("Arial", 14),     
    width=10,
    height=2,
    command=lambda: part4_main(root, newData)
  )
  next_button.pack(pady=10)