import tkinter as tk;
from part2.part2_main import part2_main 

def part1_main(root):
    # 전체 프레임 초기화
    for widget in root.winfo_children():
        widget.destroy()

    root.title("여행지 추천")

    # 제목
    title_label = tk.Label(root, text="여행지 추천 서비스", font=("Arial", 24, "bold"))
    title_label.pack(pady=50)

    # 시작 버튼
    start_button = tk.Button(
        root,
        text="설문 시작하기",
        font=("Arial", 14),
        command=lambda: part2_main(root)
    )
    start_button.pack(pady=20)
