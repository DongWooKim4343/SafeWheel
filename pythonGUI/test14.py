import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import os

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Advanced Camera Stream Selector")
        self.geometry("800x600")

        # 스타일 설정
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Helvetica', 12))
        self.style.configure('TButton', font=('Helvetica', 10), background='gray')

        # 로고 및 타이틀
        logo = Image.open("logo.png")  # 로고 이미지 파일
        logo = logo.resize((100, 100), Image.ANTIALIAS)
        logo_img = ImageTk.PhotoImage(logo)
        logo_label = ttk.Label(self, image=logo_img)
        logo_label.image = logo_img
        logo_label.pack(side='top', pady=10)
        
        self.title_label = ttk.Label(self, text="카메라 스트림 선택기", font=('Helvetica', 16))
        self.title_label.pack(side='top', pady=10)

        self.caps = {
            "서라운드 카메라": cv2.VideoCapture(0),
            "좌측 카메라": cv2.VideoCapture(1),
            "우측 카메라": cv2.VideoCapture(2),
            "후방 카메라": cv2.VideoCapture(3)
        }

        self.left_frame = ttk.Frame(self, width=200, relief='raised', borderwidth=2)
        self.left_frame.pack(side="left", fill="both", expand=False)

        # 버튼에 아이콘 추가
        button_names = ["서라운드 카메라", "좌측 카메라", "우측 카메라", "후방 카메라"]
        icons = ["icon1.png", "icon2.png", "icon3.png", "icon4.png"]  # 아이콘 파일명 더미
        
        for name, icon in zip(button_names, icons):
            img = Image.open(icon)
            img = img.resize((50, 50), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(img)
            button = ttk.Button(self.left_frame, text=name, image=photo, compound="top",
                                command=lambda n=name: self.select_camera(n))
            button.image = photo
            button.pack(side="top", fill="both", expand=True, padx=20, pady=10)

        self.right_frame = ttk.Frame(self)
        self.right_frame.pack(side="right", fill="both", expand=True)

        self.left_video_label = ttk.Label(self.right_frame)
        self.right_video_label = ttk.Label(self.right_frame)

        self.current_camera = None
        self.previous_camera = None
        self.is_split_screen = False

        self.update_video()

    def select_camera(self, selected_camera):
        self.left_video_label.pack_forget()
        self.right_video_label.pack_forget()

        if self.current_camera == selected_camera:
            self.left_video_label.pack(fill="both", expand=True)
            self.is_split_screen = False
        elif self.is_split_screen:
            self.left_video_label.pack(side="left", fill="both", expand=True)
            self.right_video_label.pack(side="right", fill="both", expand=True)
        else:
            self.previous_camera=self.current_camera
            self.current_camera=selected_camera
            self.left_video_label.pack(side="left", fill="both", expand=True)
            self.right_video_label.pack(side="right", fill="both", expand=True)
            self.is_split_screen=True

    def update_video(self):
        if self.current_camera and self.caps[self.current_camera].isOpened():
            ret, frame = self.caps[self.current_camera].read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = ImageTk.PhotoImage(Image.fromarray(frame))
                self.left_video_label.imgtk = img
                self.left_video_label.configure(image=img)

        if self.previous_camera and self.caps[self.previous_camera].isOpened():
            ret, frame = self.caps[self.previous_camera].read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = ImageTk.PhotoImage(Image.fromarray(frame))
                self.right_video_label.imgtk = img
                self.right_video_label.configure(image=img)

        self.after(10, self.update_video)

    def on_closing(self):
        for cap in self.caps.values():
            cap.release()
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()