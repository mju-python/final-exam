import tkinter
from tkinter import ttk
from part4.part4_main import part4_main
from tkcalendar import DateEntry  

def part3_main(root, data):
  # 전체 프레임 초기화
  for widget in root.winfo_children():
    widget.destroy()

  print("part3",data)
  # 데이터는 아래와 같은 형식으로 올건데, ai 사용횟수가 있어서,
  # ai 429 Client Error: Too Many Requests for url: https://openrouter.ai/api/v1/chat/completions 오류뜨면
  # 아래 dummyData 참고해서 코딩 해주세요.
  # 실제 데이터는 dummyData에 오는게 아니라 data에 오는거라 data를 다뤄야 합니다. 


  title = tkinter.Label(root, text="🤖AI의 분석 결과 추천 여행지 5곳!",  font=("맑은 고딕", 24, "bold"))
  title.pack(pady=15)

  frame= tkinter.Frame(root)
  frame.pack(expand=False, pady=(0, 10))

  selected = tkinter.StringVar()

  travel = []
  for place in data:
    print(place)
    travel.append(place['destination'])
  
  airport = {}
  for place in data:
    airport[place['destination']] = place["airportCode"]

  style = ttk.Style(root)
  style.configure(
    "Radio.TRadiobutton",
    font=("맑은 고딕", 18, "bold"),
    padding=(0, 5, 20, 5)
  )

  for place in travel:
    rb = ttk.Radiobutton(
        frame,
        text=place,          
        value=place,         
        variable=selected,
        style="Radio.TRadiobutton"
    )
    rb.pack(anchor='w', padx=30, pady=3)

  sub = tkinter.Label(root, text="🛫여행을 원하는 날짜",  font=("맑은 고딕", 20, "bold"))
  sub.pack(pady=15)

  style.configure(
    "Date.TEntry",
    foreground='blue',
    padding=(25, 3, 3, 3),
    font=("맑은 고딕", 16, "bold"),
  )

  date = DateEntry(root, font=("맑은 고딕", 16), date_pattern='yyyy-mm-dd', style="Date.TEntry")
  date.pack(pady=5)

  def submit():
    place = selected.get()       
    itinerary = date.get()
    newData={ 
      "airportCode" : airport[place],
      "date" : itinerary 
    } 
    part4_main(root, newData) 

  button = ttk.Button(
    root,
    text="다음으로",           
    command=submit,
    style="Accent.TButton"        
  )
  button.pack(pady=25)