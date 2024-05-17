import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Safe Wheel Monitor")
        self.geometry("800x600")

        # 카메라 초기화: 바운더리 문제가 있는 경우 URL을 수정
        self.caps = {
            "Surround Camera": cv2.VideoCapture(0),
            "Left Camera": cv2.VideoCapture('http://192.168.120.191:8080/video', cv2.CAP_FFMPEG),
            "Right Camera": cv2.VideoCapture('http://192.168.115.13:8080/video', cv2.CAP_FFMPEG),
            "Backup Camera": cv2.VideoCapture(3)
        }

        # 왼쪽 명령 버튼 프레임
        self.left_frame = ttk.Frame(self, width=200)
        self.left_frame.pack(side="left", fill="both", expand=False)

        # 카메라 선택 버튼 생성
        button_names = ["Surround Camera", "Left Camera", "Right Camera", "Backup Camera"]
        for name in button_names:
            button = ttk.Button(self.left_frame, text=name, 
                                command=lambda n=name: self.select_camera(n))
            button.pack(side="top", fill="both", expand=True, padx=20, pady=10)

        # 비디오 표시 프레임
        self.right_frame = ttk.Frame(self)
        self.right_frame.pack(side="right", fill="both", expand=True)

        # 비디오 라벨
        self.left_video_label = ttk.Label(self.right_frame)
        self.right_video_label = ttk.Label(self.right_frame)

        self.current_camera = None
        self.previous_camera = None
        self.is_split_screen = False

        self.update_video()

    def update_video(self):
        if self.current_camera and self.caps[self.current_camera].isOpened():
            ret, frame = self.caps[self.current_camera].read()
            if ret:
                img = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
                self.left_video_label.configure(image=img)
                self.left_video_label.imgtk = img  # imgtk를 사용하여 참조 유지

        self.after(10, self.update_video)

    def select_camera(self, selected_camera):
        if self.current_camera != selected_camera:
            self.current_camera = selected_camera
            self.left_video_label.pack(fill="both", expand=True)

    def on_closing(self):
        for cap in self.caps.values():
            cap.release()
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()