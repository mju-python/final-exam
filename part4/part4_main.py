import tkinter as tk
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime

city_to_airport = {
    
    "서울(김포)": "GMP",
    "서울(인천)": "ICN",
    "부산": "PUS",
    "제주": "CJU",
    "대구": "TAE",
    "광주": "KWJ",
    "청주": "CJJ",
    "여수": "RSU",
    "울산": "USN",
    "포항": "KPO",
    "양양": "YNY",


    "방콕": "BKK",
    "도쿄": "NRT",
    "오사카": "KIX",
    "후쿠오카": "FUK",
    "타이베이": "TPE",
    "홍콩": "HKG",
    "싱가포르": "SIN",
    "괌": "GUM",
    "하와이(호놀룰루)": "HNL",
    "뉴욕": "JFK",
    "런던": "LHR",
    "파리": "CDG",
    "로스앤젤레스": "LAX",
    "프랑크푸르트": "FRA",
    "시드니": "SYD"
}

def part4_main(root, data):
    # 전체 프레임 초기화
    for widget in root.winfo_children():
        widget.destroy()

    arr_code = data["airportCode"]
    dep_date_str = data["date"]
    dep_code = "ICN"  # 출발지 고정

    try:
        dep_date_obj = datetime.strptime(dep_date_str, "%Y-%m-%d")
        dep_date = dep_date_obj.strftime("%Y%m%d")
    except ValueError:
        tk.Label(root, text="날짜 형식 오류 (예: 2025-07-20)", fg="red").pack()
        return

    tk.Label(
        root,
        text="선택한 날짜와 목적지를 기반으로 편도 항공권을 조회한 결과입니다",
        font=("맑은 고딕", 14)
    ).pack(pady=10)

    url = f"https://travel.interpark.com/air/search/c:{dep_code}-c:{arr_code}-{dep_date}?cabin=ECONOMY&infant=0&child=0&adult=1"

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')  # 메모리 오류 방지
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        # 페이지가 로드될 때까지 최대 10초 대기
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".air_list_item, .domestic_list_item"))
        )
        soup = BeautifulSoup(driver.page_source, "html.parser")

        flights = soup.select(".domestic_list_item") or soup.select(".air_list_item")

        if not flights:
            tk.Label(root, text="항공권 정보를 찾을 수 없습니다.").pack()
        else:
            for flight in flights[:5]:
                try:
                    times = flight.select_one(".route_time")
                    airline = flight.select_one(".airline_name")
                    price = flight.select_one(".price")

                    if not (times and airline and price):
                        continue

                    info = f"출발/도착: {times.text.strip()} | 항공사: {airline.text.strip()} | 가격: {price.text.strip()}"
                    tk.Label(root, text=info, font=("맑은 고딕", 12)).pack(pady=5)
                except Exception as e:
                    print("파싱 중 오류:", e)
                    continue
    finally:
        driver.quit()

    next_button = tk.Button(
        root,
        text="종료하기",
        font=("Arial", 14),
        width=10,
        height=2,
        command=lambda: root.destroy()
    )
    next_button.pack(pady=10)
