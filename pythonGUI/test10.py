import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Advanced Camera Stream Selector")
        self.geometry("800x600")

        self.caps = {
            "서라운드 카메라": cv2.VideoCapture(0),
            "좌측 카메라": cv2.VideoCapture(1),
            "우측 카메라": cv2.VideoCapture(2),
            "후방 카메라": cv2.VideoCapture(3)
        }

        self.left_frame = ttk.Frame(self, width=200)
        self.left_frame.pack(side="left", fill="both", expand=False)

        button_names = ["서라운드 카메라", "좌측 카메라", "우측 카메라", "후방 카메라"]
        for name in button_names:
            button = ttk.Button(self.left_frame, text=name,
                                command=lambda n=name: self.select_camera(n))
            button.pack(side="top", fill="both", expand=True, padx=20, pady=10)

        self.right_frame = ttk.Frame(self)
        self.right_frame.pack(side="right", fill="both", expand=True)

        # 하나의 레이블만 사용하여 전체 프레임 처리
        self.video_label = ttk.Label(self.right_frame)
        self.video_label.pack(fill="both", expand=True)

        self.current_camera = None

        self.update_video()

    def select_camera(self, selected_camera):
        """ 선택된 카메라로 비디오 출력을 전환합니다. """
        if self.current_camera != selected_camera:
            self.current_camera = selected_camera
        # 동일한 카메라를 선택한 경우에는 전체 화면으로 유지

    def update_video(self):
        """ 비디오 프레임을 실시간으로 업데이트합니다. """
        if self.current_camera and self.caps[self.current_camera].isOpened():
            ret, frame = self.caps[self.current_camera].read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = ImageTk.PhotoImage(Image.fromarray(frame))
                self.video_label.imgtk = img
                self.video_label.configure(image=img)

        self.after(10, self.update_video)

    def on_closing(self):
        """ 창을 닫을 때 리소스를 해제합니다. """
        for cap in self.caps.values():
            if cap.isOpened():
                cap.release()
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()