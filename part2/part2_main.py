import tkinter as tk
from tkinter import messagebox  
from part1.part1_ai import part1_ai

def part2_main(root):
    # 전체 프레임 초기화
    for widget in root.winfo_children():
        widget.destroy()

    # 입력값 저장용 변수 선언
    budget = tk.StringVar()
    destination_type = tk.StringVar()
    purpose = tk.StringVar()
    climate = tk.StringVar()

    # 1. 예산 입력
    tk.Label(root, text="가지고 있는 예산이 어떻게 되시나요?", font=("Arial", 12)).pack(pady=(20, 5))
    tk.Entry(root, textvariable=budget, width=40).pack(pady=5)

    # 2. 국내/해외 선택
    tk.Label(root, text="국내와 해외 중 어디를 선호하시나요?", font=("Arial", 12)).pack(pady=(20, 5))
    tk.Radiobutton(root, text="국내", variable=destination_type, value="국내").pack()
    tk.Radiobutton(root, text="해외", variable=destination_type, value="해외").pack()

    # 3. 여행 목적 선택
    tk.Label(root, text="여행의 목적이 어떻게 되나요?", font=("Arial", 12)).pack(pady=(20, 5))
    purpose_options = ["휴식", "관광", "체험", "맛집탐방"]
    purpose.set("")
    tk.OptionMenu(root, purpose, *purpose_options).pack()

    # 4. 선호하는 기후 선택
    tk.Label(root, text="선호하는 기후가 있으신가요?", font=("Arial", 12)).pack(pady=(20, 5))
    climate_options = ["온대", "열대", "한대", "건조", "냉대"]
    climate.set("")
    tk.OptionMenu(root, climate, *climate_options).pack()

    # 5. 입력 확인
    def go_next():
        if not budget.get().strip():
            messagebox.showwarning("입력 오류", "예산을 입력해 주세요.")
            return
        if not destination_type.get():
            messagebox.showwarning("입력 오류", "국내/해외 중 하나를 선택해 주세요.")
            return
        if not purpose.get():
            messagebox.showwarning("입력 오류", "여행 목적을 선택해 주세요.")
            return
        if not climate.get():
            messagebox.showwarning("입력 오류", "선호하는 기후를 선택해 주세요.")
            return

        data = {
            "예산": budget.get(),
            "위치": "",  # 아직 위치 항목 없음
            "여행지 유형": destination_type.get(),
            "여행 목적": purpose.get(),
            "선호하는 기후": climate.get()
        }
        part1_ai(root, data)

    tk.Button(
        root,
        text="다음으로",
        font=("Arial", 14),
        width=10,
        height=2,
        command=go_next
    ).pack(pady=10)
