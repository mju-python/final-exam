import os;
import tkinter as tk;
from PIL import Image, ImageTk;
from part2.part2_main import part2_main 

def part1_main(root):
    # 전체 프레임 초기화
    for widget in root.winfo_children():
        widget.destroy()

    root.title("여행지 추천 서비스")

    # 이미지
    current_dir = os.path.dirname(os.path.abspath(__file__))
    assets_path = os.path.join(current_dir, "..", "assets", "logo.png")
    assets_path = os.path.normpath(assets_path)  # 경로 정리
    image = Image.open(assets_path)
    resized_image = image.resize((250,350))
    photo = ImageTk.PhotoImage(resized_image)
    image_label = tk.Label(root, image=photo)
    image_label.image = photo
    image_label.pack(pady=70)

    # 제목
    title_label = tk.Label(root, text="여행지 추천에 오신걸 환영합니다.", font=("Arial", 30, "bold"))
    title_label.pack()

    # 시작 버튼
    start_button = tk.Button(
        root,
        text="설문 시작하기",
        font=("Arial", 14),
        command=lambda: part2_main(root)
    )
    start_button.pack(pady=5)
