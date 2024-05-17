import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Advanced Camera Stream Selector")
        self.geometry("800x600")

        # 스타일 설정
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Helvetica', 12))
        self.style.configure('TButton', font=('Helvetica', 12, 'bold'), background='light gray', borderwidth=2)

        # 어플리케이션 메인 타이틀
        self.title_label = ttk.Label(self, text="카메라 스트림 선택기", font=('Helvetica', 16, 'bold'))
        self.title_label.pack(side='top', pady=10)

        self.caps = {
            "서라운드 카메라": cv2.VideoCapture(0),
            "좌측 카메라": cv2.VideoCapture(1),
            "우측 카메라": cv2.VideoCapture(2),
            "후방 카메라": cv2.VideoCapture(3)
        }

        self.left_frame = ttk.Frame(self, width=200, relief='raised', borderwidth=2)
        self.left_frame.pack(side="left", fill="both", expand=False)

        # 버튼 생성
        button_names = ["서라운드 카메라", "좌측 카메라", "우측 카메라", "후방 카메라"]
        
        for name in button_names:
            button = ttk.Button(self.left_frame, text=name, 
                                command=lambda n=name: self.select_camera(n))
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
            self.previous_camera = self.current_camera
            self.current_camera = selected_camera
            self.left_video_label.pack(side="left", fill="both", expand=True)
            self.right_video_label.pack(side="right", fill="both", expand=True)
            self.is_split_screen = True

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