import pyttsx3
import uiautomation as auto
import keyboard
import threading
import win32api
import ctypes
import time

# DPI 인식 설정
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

# TTS 초기화
def init_tts():
    engine = pyttsx3.init()
    engine.setProperty('rate', 180)  # 음성 속도 설정
    engine.setProperty('volume', 1.0)  # 볼륨 설정 (0.0 ~ 1.0)
    return engine

# TTS 테스트용 출력 함수
def speak_text(text, engine):
    engine.say(text)
    engine.runAndWait()

# 키보드 후킹 테스트
def keyboard_hook():
    def on_key_event(e):
        print(f'[키보드 입력] {e.name}')
    keyboard.on_press(on_key_event)

# 마우스 위치 테스트 함수 (향후 F1 누를 때 요소 읽기에 활용)
def mouse_position_debug():
    while True:
        pos = win32api.GetCursorPos()
        print(f'[마우스 위치] {pos}')
        time.sleep(1)

# 초기화
def initialize():
    print("[초기화] TTS 엔진 초기화 중...")
    tts_engine = init_tts()
    speak_text("스크린리더 초기화 완료", tts_engine)

    print("[초기화] 키보드 후킹 시작...")
    keyboard_hook()

    print("[초기화] UIAutomation 준비 완료")
    
    return tts_engine

if __name__ == "__main__":
    tts_engine = initialize()

    # 마우스 위치 디버그 스레드 실행 (비동기)
    threading.Thread(target=mouse_position_debug, daemon=True).start()

    # 메인 루프 (종료 안 함)
    print("[실행 중] 종료하려면 Ctrl+C")
    while True:
        time.sleep(1)
