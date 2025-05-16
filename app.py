import tkinter as tk
from part1.part1_main import part1_main

def main():
    root = tk.Tk()
    root.title("여행지 추천 서비스")
    root.geometry("800x700")
    part1_main(root)
    root.mainloop()

if __name__ == "__main__":
    main()
