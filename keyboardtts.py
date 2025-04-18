import keyboard
import win32clipboard
import time
import pyttsx3

chosung_dict = {
    'ㄱ': '기역', 'ㄲ': '쌍기역', 'ㄴ': '니은', 'ㄷ': '디귿', 'ㄸ': '쌍디귿',
    'ㄹ': '리을', 'ㅁ': '미음', 'ㅂ': '비읍', 'ㅃ': '쌍비읍', 'ㅅ': '시옷',
    'ㅆ': '쌍시옷', 'ㅇ': '이응', 'ㅈ': '지읒', 'ㅉ': '쌍지읒', 'ㅊ': '치읓',
    'ㅋ': '키읔', 'ㅌ': '티읕', 'ㅍ': '피읖', 'ㅎ': '히읗'
}

# 클립보드에서 텍스트 가져오기
def get_clipboard_text():
    win32clipboard.OpenClipboard()
    try:
        data = win32clipboard.GetClipboardData()
    except:
        data = ''
    win32clipboard.CloseClipboard()
    return data

# 텍스트를 음성으로 출력하기
def speak_text(text):
    engine = pyttsx3.init()
    processed_text = ' '.join([chosung_dict.get(char, char) for char in text])
    engine.say(processed_text)
    engine.runAndWait()

# F2 키 이벤트 처리 함수
def on_f2_press(event):
    if event.event_type == 'down':
        keyboard.press_and_release('ctrl+a')  # 전체 선택
        time.sleep(0.05)
        keyboard.press_and_release('ctrl+c')  # 복사
        time.sleep(0.05)
        keyboard.press_and_release('right')   # 오른쪽 방향키 눌러 커서 이동
        text = get_clipboard_text()
        if text:
            speak_text(text)

# F2 키 이벤트 리스너 등록
keyboard.hook_key('F2', on_f2_press)

print("F2를 누를 때마다 입력된 텍스트를 읽습니다. 종료하려면 ESC를 누르세요.")
keyboard.wait('esc')
