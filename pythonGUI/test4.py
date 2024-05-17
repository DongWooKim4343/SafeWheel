import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Advanced Camera Stream Selector")
        self.geometry("800x600")

        # 비디오 캡처 객체 초기화 (사용 가능한 카메라로 설정하세요)
        self.caps = {
            "서라운드 카메라": cv2.VideoCapture(0),
            "좌측 카메라": cv2.VideoCapture(1),
            "우측 카메라": cv2.VideoCapture(2),
            "후방 카메라": cv2.VideoCapture(3)
        }

        # 사용되지 않는 캡처를 검사하고 해제
        for name, cap in self.caps.items():
            if not cap.isOpened():
                print(f"{name} 카메라를 열 수 없습니다.")
                cap.release()
        
        self.left_frame = ttk.Frame(self, width=200)
        self.left_frame.pack(side="left", fill="both", expand=False)

        button_names = ["서라운드 카메라", "좌측 카메라", "우측 카메라", "후방 카메라"]

        for name in button_names:
            button = ttk.Button(self.left_frame, text=name, command=lambda n=name: self.select_camera(n))
            button.pack(side="top", fill="both", expand=True, padx=20, pady=10)

        self.right_frame = ttk.Frame(self)
        self.right_frame.pack(side="right", fill="both", expand=True)

        self.new_video_label = ttk.Label(self.right_frame)
        self.new_video_label.pack(side="left", fill="both", expand=True)
        self.prev_video_label = ttk.Label(self.right_frame)
        self.prev_video_label.pack(side="right", fill="both", expand=True)

        self.current_camera = None
        self.prev_cap = None
        self.current_cap = None

        self.update_video()

    def select_camera(self, name):
        if self.current_camera == name:
            return
        
        self.prev_cap = self.current_cap
        self.current_camera = name
        self.current_cap = self.caps.get(name, None)

    def update_video(self):
        if self.current_cap and self.current_cap.isOpened():
            ret, frame = self.current_cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                im = Image.fromarray(frame)
                img = ImageTk.PhotoImage(image=im)
                self.new_video_label.imgtk = img
                self.new_video_label.configure(image=img)

        if self.prev_cap and self.prev_cap.isOpened():
            ret, frame = self.prev_cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                im = Image.fromarray(frame)
                img = ImageTk.PhotoImage(image=im)
                self.prev_video_label.imgtk = img
                self.prev_video_label.configure(image=img)

        self.after(10, self.update_video)

    def on_closing(self):
        for cap in self.caps.values():
            cap.release()
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()