import threading
import tkinter as tk
from bs4 import BeautifulSoup
from datetime import datetime
from playwright.sync_api import sync_playwright

def parse_flight_info(html, is_domestic):
    soup = BeautifulSoup(html, "html.parser")
    results = []

    if is_domestic:
        
        candidates = soup.select("li.itemBlock.current")
        for block in candidates:
            try:
                dep_time = block.select_one("div.airlineTime span.timeWrap > span.time").text.strip()
                arr_time = block.select("div.airlineTime span.timeWrap > span.time")[1].text.strip()
                airline_name = block.select_one("span.airlineName > span.name").text.strip()
                flight_num = block.select_one("span.airlineName > span.num").text.strip()
                route = f"{airline_name} {flight_num}"
                price = block.select_one("div.seatFee span.fee.lowFee").text.strip()
                time = f"{dep_time} - {arr_time}"

                results.append((time, route, price))
            except Exception:
                continue
    else:
        
        candidates = soup.select("div[class*='SzWCt']")
        for block in candidates:
            try:
                time = block.find("div", class_=lambda x: x and "SpPrC" in x).text.strip()
                route = block.find("div", class_=lambda x: x and "hIFrAg" in x).text.strip()
                price = block.find("div", class_=lambda x: x and "jwGHUA" in x).text.strip()
                results.append((time, route, price))
            except AttributeError:
                continue

    return results if results else None

def playwright_task(arr_code, dep_date_str, root, is_domestic, dep_code=None):
    try:
        dep_date_obj = datetime.strptime(dep_date_str, "%Y-%m-%d")
        dep_date = dep_date_obj.strftime("%Y%m%d")
    except ValueError:
        root.after(0, lambda: tk.Label(root, text="날짜 형식 오류 (예: 2025-07-20)", fg="red").pack())
        return

    if is_domestic:
        if not dep_code:
            root.after(0, lambda: tk.Label(root, text="국내선 출발지 코드가 없습니다.", fg="red").pack())
            return
        url = f"https://sky.interpark.com/schedules/domestic/{dep_code}-{arr_code}-{dep_date}?adt=1&chd=0&inf=0&seat=ALL&airline="
    else:
        dep_code = dep_code or "SEL"
        url = f"https://travel.interpark.com/air/search/c:{dep_code}-c:{arr_code}-{dep_date}?adult=1&child=0&infant=0&cabin=ECONOMY"

    print(f"[디버그] 접속 URL: {url}")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                locale="ko-KR",
                timezone_id="Asia/Seoul",
                java_script_enabled=True,
                bypass_csp=True,
            )
            page = context.new_page()
            page.goto(url, timeout=60000)
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(10000)

            html = page.content()

            with open("debug_airpage.html", "w", encoding="utf-8") as f:
                f.write(html)
            print("HTML 저장 완료: debug_airpage.html")

            browser.close()

        flight_data = parse_flight_info(html, is_domestic)

        if not flight_data:
            root.after(0, lambda: tk.Label(root, text="항공권 정보를 찾을 수 없습니다.", fg="red").pack())
            return

        def show_results():
            for time, route, price in flight_data[:5]:
                info = f"시간: {time} | 항공편: {route} | 가격: {price}"
                tk.Label(root, text=info, font=("맑은 고딕", 12)).pack(pady=5)
            # tk.Button(root, text="종료하기", font=("Arial", 14), width=10, height=2, command=root.destroy).pack(pady=10)

        root.after(0, show_results)

    except Exception as e:
        print(f"[에러] {e}")
        root.after(0, lambda: tk.Label(root, text="페이지 로딩 또는 크롤링 실패", fg="red").pack())

def part4_main(root, data):
    # 전체 프레임 초기화
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="항공권 정보를 불러오는 중입니다...", font=("맑은 고딕", 14)).pack(pady=20)

    is_domestic = data.get("isDomestic", False)
    dep_code = data.get("depCode")  

    threading.Thread(
        target=playwright_task,
        args=(data["airportCode"], data["date"], root, is_domestic, dep_code),
        daemon=True
    ).start()

    next_button = tk.Button(
        root,
        text="종료하기",
        font=("Arial", 14),
        width=10,
        height=2,
        command=lambda: root.destroy()
    )
    next_button.pack(pady=10)
