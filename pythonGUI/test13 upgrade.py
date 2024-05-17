import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Safe Wheel Monitor")
        self.geometry("800x600")

        # 카메라 초기화
        self.caps = {
            "Surround Camera": cv2.VideoCapture(0),
            "Left Camera": cv2.VideoCapture('http://192.168.120.191:8080/video'),
            "Right Camera": cv2.VideoCapture('http://192.168.115.13:8080/video'),
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

    def select_camera(self, selected_camera):
        if self.current_camera == selected_camera and not self.is_split_screen:
            # 현재 전체 화면과 동일한 카메라를 클릭한 경우
            return
        elif self.current_camera == selected_camera and self.is_split_screen:
            # 분할 화면에서 같은 카메라를 클릭한 경우, 전체화면으로 전환
            self.is_split_screen = False
            self.current_camera = selected_camera
            self.previous_camera = None
        elif self.is_split_screen:
            # 분할 화면에서 다른 카메라를 클릭한 경우, 분할 화면 유지
            self.previous_camera = self.current_camera
            self.current_camera = selected_camera
        else:
            # 분할 화면이 아닐 때 다른 카메라를 클릭한 경우, 분할 화면으로 전환
            self.is_split_screen = True
            self.previous_camera = self.current_camera if self.current_camera else selected_camera
            self.current_camera = selected_camera

        self.update_display()

    def update_display(self):
        # 비디오 라벨 컨테이너 정리하기
        self.left_video_label.pack_forget()
        self.right_video_label.pack_forget()

        if self.is_split_screen:
            self.left_video_label.pack(side="left", fill="both", expand=True)
            self.right_video_label.pack(side="right", fill="both", expand=True)
        else:
            self.left_video_label.pack(fill="both", expand=True)

    def update_video(self):
        if self.current_camera and self.caps[self.current_camera].isOpened():
            ret, frame = self.caps[self.current_camera].read()
            if ret:
                frame = cv2.putText(frame, self.current_camera, (10, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.left_video_label.imgtk = img
                self.left_video_label.configure(image=img)

        if self.previous_camera and self.caps[self.previous_camera].isOpened():
            ret, frame = self.caps[self.previous_camera].read()
            if ret:
                frame = cv2.putText(frame, self.previous_camera, (10, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = ImageTk.PhotoImage(image=Image.fromarray(frame))
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