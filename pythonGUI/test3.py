import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Tkinter with Video Streaming and Camera Select")
        self.geometry("800x600")

        # 왼쪽 프레임 (버튼들)
        self.left_frame = ttk.Frame(self, width=200)
        self.left_frame.pack(side="left", fill="both", expand=False)

        # 카메라 버튼 이름
        button_names = ["서라운드 카메라", "좌측 카메라", "우측 카메라", "후방 카메라"]

        # 버튼 추가
        for name in button_names:
            button = ttk.Button(self.left_frame, text=name, command=lambda n=name: self.select_camera(n))
            button.pack(side="top", fill="both", expand=True, padx=20, pady=10)

        # 오른쪽 프레임 (비디오)
        self.right_frame = ttk.Frame(self)
        self.right_frame.pack(side="right", fill="both", expand=True)
        
        # 레이블 생성 (비디오가 재생될 곳)
        self.video_label = ttk.Label(self.right_frame)
        self.video_label.pack(fill="both", expand=True)

        # 비디오 캡처
        self.cap = cv2.VideoCapture(0)  # 0은 컴퓨터의 웹 카메라를 의미
        self.update_video()  # 비디오 업데이트 시작

    def select_camera(self, name):
        """선택된 카메라 이름에 따라 처리합니다."""
        print(f"{name} 선택됨")

    def update_video(self):
        """비디오 프레임을 업데이트합니다."""
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # OpenCV -> PIL 컬러 변환
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)

            self.video_label.imgtk = img
            self.video_label.configure(image=img)
            self.video_label.after(10, self.update_video)  # 계속해서 video_label을 업데이트

    def on_closing(self):
        """창을 닫을 때 리소스를 해제합니다."""
        self.cap.release()
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()