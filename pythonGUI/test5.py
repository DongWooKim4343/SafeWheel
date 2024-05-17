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

        # 버튼 초기화
        button_names = ["서라운드 카메라", "좌측 카메라", "우측 카메라", "후방 카메라"]
        for name in button_names:
            button = ttk.Button(self.left_frame, text=name, command=lambda n=name: self.select_camera(n))
            button.pack(side="top", fill="both", expand=True, padx=20, pady=10)

        # 오른쪽 프레임 (비디오 출력)
        self.right_frame = ttk.Frame(self)
        self.right_frame.pack(side="right", fill="both", expand=True)

        # 비디오 레이블: 하나는 새로운 카메라, 하나는 이전 카메라.
        self.video_label = ttk.Label(self.right_frame)
        self.video_label.pack(fill="both", expand=True)

        self.current_camera = None
        self.current_cap = None

        self.update_video()

    def select_camera(self, name):
        """선택된 카메라로 비디오 출력을 전환합니다."""
        self.current_camera = name
        self.current_cap = self.caps[name]
        # 화면을 전체로 송출을 위해 레이블 크기 조정
        self.video_label.pack_forget()
        self.video_label.pack(fill="both", expand=True)

    def update_video(self):
        """비디오 프레임을 실시간으로 업데이트합니다."""
        if self.current_cap and self.current_cap.isOpened():
            ret, frame = self.current_cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                im = Image.fromarray(frame)
                img = ImageTk.PhotoImage(image=im)
                self.video_label.imgtk = img
                self.video_label.configure(image=img)
                self.video_label.update()

        self.after(10, self.update_video)

    def on_closing(self):
        """창을 닫을 때 리소스를 해제합니다."""
        for cap in self.caps.values():
            cap.release()
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()