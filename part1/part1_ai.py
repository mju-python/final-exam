import tkinter as tk
from part3.part3_main import part3_main
import requests
import os
import json
import re
from dotenv import load_dotenv
from PIL import Image, ImageTk, ImageSequence

load_dotenv()
frames = []  # GIF 프레임 저장용
resultData = {}

# OpenRouter API 키
OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")  

dummyData = [
    {"destination": "발리, 인도네시아", "airportCode": "DPS"},
    {"destination": "푸꾸옥, 베트남", "airportCode": "PQC"},
    {"destination": "세부, 필리핀", "airportCode": "CEB"},
    {"destination": "코사무이, 태국", "airportCode": "USM"},
    {"destination": "다낭, 베트남", "airportCode": "DAD"}
]
def animate_gif(label, frame_index=0):
    frame = frames[frame_index]
    label.configure(image=frame)
    label.image = frame
    next_index = (frame_index + 1) % len(frames)
    label.after(100, lambda: animate_gif(label, next_index)) 

def send_request(root, data):
    global isLoading, isSuccess, resultData  # resultData도 global 선언 필요

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json"
    }

    budget = data.get('예산')
    location_type = data.get('여행지 유형')
    purpose = data.get('여행 목적')
    climate = data.get('선호하는 기후')

    print(budget, location_type, purpose, climate)

    messages = [
        {
            "role": "system",
            "content": (
                "당신은 여행 컨설턴트입니다. 사용자가 입력한 조건을 바탕으로 여행지 5곳을 추천하세요.\n"
                "반드시 다음 형식을 지켜서 JSON 형식으로만 응답해 주세요:\n\n"
                "{\n"
                "  \"recommendations\": [\n"
                "    {\"destination\": \"장소명\", \"airportCode\": \"공항코드\"},\n"
                "    ... (총 5개)\n"
                "  ]\n"
                "}\n\n"
                "조건: 예산, 위치, 목적, 기후를 반영"
            )
        },
        {
            "role": "user",
            "content": (
                f"예산: {budget}원\n"
                f"위치: {location_type}\n"
                f"목적: {purpose}\n"
                f"선호 기후: {climate}"
            )
        }
    ]

    payload = {
        "model": "deepseek/deepseek-chat-v3-0324:free",
        "messages": messages
    }

    isLoading = True

    try:
        response = requests.post(url, headers=headers, json=payload)
        print("🔁 응답 상태 코드:", response.status_code)
        print("📄 응답 본문:", response.text)

        if response.status_code != 200:
            print("❌ API 요청 실패 - 상태코드가 200이 아님")
            return

        result = response.json()
        content = result["choices"][0]["message"]["content"]
        print("🧾 모델 응답 내용:", content)

        cleaned = re.sub(r"^```json|```$", "", content.strip(), flags=re.MULTILINE).strip()

        ai_data = json.loads(cleaned)
        print("📦 파싱된 데이터:", ai_data)

        resultData = ai_data.get("recommendations", [])
        part3_main(root, resultData)
        isSuccess = True
    except Exception as e:
        isSuccess = False
        print("❌ 분석 실패:", str(e))

    finally:
        isLoading = False

def part1_ai(root, data):
    global isSuccess
    isSuccess = False

    def retry():
        # 실패 시 다시 요청하는 함수
        # 기존 화면을 지우고 다시 part1_ai 호출해서 재요청
        for widget in root.winfo_children():
            widget.destroy()
        part1_ai(root, data)

    # 1000ms (1초) 후에 API 요청 실행
    root.after(0, lambda: send_request(root, data))

    global frames

    for widget in root.winfo_children():
        widget.destroy()

    # GIF 이미지 경로
    current_dir = os.path.dirname(os.path.abspath(__file__))
    gif_path = os.path.join(current_dir, "..", "assets", "loading.gif")
    gif_path = os.path.normpath(gif_path)

    # GIF 로딩
    image = Image.open(gif_path)
    frames = [ImageTk.PhotoImage(frame.copy().resize((200, 200))) for frame in ImageSequence.Iterator(image)]

    # 라벨에 첫 프레임 설정
    gif_label = tk.Label(root)
    gif_label.pack(pady=200)

    # 애니메이션 시작
    animate_gif(gif_label)

    # 라벨
    title_label = tk.Label(root, text="AI 분석중입니다....",font=("Arial", 25, "bold"))
    title_label.pack()
 
    # 잠시 대기 후 결과 확인해서 성공/실패 처리
    def check_result():
        if isSuccess:
            print("성공적으로 분석이 완료되었습니다.")
        else:
            print("분석실패")
            part3_main(root, dummyData)
            # button1 = tk.Button(root, text="다시 요청하기", command=retry)
            # button1.pack()

     # 3초 뒤 결과 확인 (API 요청이 비동기라 잠시 기다림)
    root.after(3000, check_result)
