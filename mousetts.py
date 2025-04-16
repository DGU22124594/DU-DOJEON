import pyttsx3
import uiautomation as auto
import win32api
import ctypes
import time
import multiprocessing

# DPI 설정 (고해상도 대응)
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

# TTS 재생 함수 (별도 프로세스에서 호출)
def speak_text(text):
    engine = pyttsx3.init(driverName='sapi5')
    engine.setProperty('rate', 180)
    engine.setProperty('volume', 1.0)
    engine.say(text)
    engine.runAndWait()

# 글로벌 변수 (프로세스 관리)
current_process = None
last_spoken_text = ""  # 마지막으로 읽은 텍스트

def mouse_element_auto_reader():
    global current_process, last_spoken_text
    print("[마우스 요소 읽기 스레드 시작됨]")
    last_control = None
    last_pos = (-1, -1)
    while True:
        try:
            x, y = win32api.GetCursorPos()  # (x,y) 튜플
            if (x, y) != last_pos:
                control = auto.ControlFromPoint(x, y)  # 좌표를 언팩하여 전달
                # 동일한 컨트롤이면(미세한 움직임 시) 대체로 같은 텍스트일 가능성이 높음
                if control != last_control:
                    name = control.Name or ""
                    value = getattr(control, "Value", "") or ""
                    text_to_read = name if name else value
                    print(f"[마우스 요소 읽기] {text_to_read}")
                    
                    # 만약 새 텍스트가 이전에 읽은 텍스트와 같다면 무시
                    if text_to_read and text_to_read != last_spoken_text:
                        # 이전 프로세스가 살아 있으면 종료하여 음성을 중단시킴
                        if current_process is not None and current_process.is_alive():
                            current_process.terminate()
                            current_process.join()
                        
                        # 새로운 텍스트 재생 프로세스 시작
                        current_process = multiprocessing.Process(target=speak_text, args=(text_to_read,))
                        current_process.start()
                        last_spoken_text = text_to_read

                    last_control = control
                    last_pos = (x, y)
        except Exception as e:
            print(f"[마우스 요소 읽기 오류] {e}")
        time.sleep(0.1)

if __name__ == "__main__":
    # 멀티프로세싱 시작 방식 지정 (Windows에서는 'spawn' 권장)
    multiprocessing.set_start_method('spawn')
    mouse_element_auto_reader()
