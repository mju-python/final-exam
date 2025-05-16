import tkinter as tk
from part1.part1_ai import part1_ai

data = {'예산' : 1000000, '위치': "국내", "여행의 목적": "맛집탐방", "선호하는 기후": "열대야"}
def part2_main(root):
  # 전체 프레임 초기화
  for widget in root.winfo_children():
    widget.destroy()
      
  #여기에 설문조사 받는 ui 그려주시면 되고
  #data에 들어간 데이터는 더미데이터로 실제로 받은 값을 data에 추가해주시면 됩니다.




  next_button = tk.Button(
      root,
      text="다음으로",
      font=("Arial", 14),     
      width=10,
      height=2,
      command=lambda: part1_ai(root, data)
  )
  next_button.pack(pady=10)
