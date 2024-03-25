import requests
import json
import base64
import pyaudio
import wave
import pyttsx3
import random

# 百度语音识别API的URL
API_URL = "https://vop.baidu.com/pro_api"
# 获取Access Token的URL
TOKEN_URL = "https://openapi.baidu.com/oauth/2.0/token"

# 您的API Key和Secret Key
API_KEY = 'fN6AyFbD1X6vdz8tMhTXfZAs'
SECRET_KEY = 'OINoqelBBvRU510aB680qbJosWEz1Sfb'

# 获取Access Token
def get_access_token():
    params = {
        'grant_type': 'client_credentials',
        'client_id': API_KEY,
        'client_secret': SECRET_KEY
    }
    response = requests.get(TOKEN_URL, params=params)
    token = response.json()['access_token']
    return token

# 调用百度语音识别API
def baidu_speech_recognition(audio_data):
    token = get_access_token()
    headers = {
        'Content-Type': 'audio/pcm;rate=16000'
    }
    params = {
        'dev_pid': 80001,  # 普通话(纯中文识别)
        'format': 'pcm',
        'rate': 16000,
        'token': token,
        'cuid': 'baidu_workshop',
        'channel': 1,
        'len': len(audio_data),
        'speech': base64.b64encode(audio_data).decode('utf-8')
    }
    response = requests.post(API_URL, headers=headers, data=json.dumps(params))
    result = response.json()
    if result['err_no'] == 0:
        print("识别结果：", result['result'][0])
        return result['result'][0]
    else:
        print("识别失败，错误信息：", result['err_msg'])

# 录音并返回PCM数据
def record_audio():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RECORD_SECONDS = 5
    RATE = 16000

    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("请说话...")
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("录音结束")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    return b"".join(frames)

# 文本转语音
def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# 随机祝福语生成器
def generate_wish():
    wishes = [
        "祝你今天过得愉快！",
        "愿你拥有一个美好的一天！",
        "希望你的每一天都充满快乐！",
        "愿阳光照亮你的每一步！",
        "祝你好运连连！",
        "愿你的笑容永远灿烂！",
        "祝你事业成功，家庭幸福！",
        "愿你健康快乐，万事如意！"
    ]
    return random.choice(wishes)

# 主函数
def main():
    try:
        while True:
            print("录音开始...")
            audio_data = record_audio()
            print("正在识别...")
            recognized_text = baidu_speech_recognition(audio_data)
            if recognized_text == "你好":
                response = "你也好"
            elif recognized_text == "再见":
                response = "88"
                print("机器人：" + response)
                text_to_speech(response)
                break
            else:
                response = generate_wish()
            print("机器人：" + response)
            text_to_speech(response)
    except Exception as e:
        print("发生错误：", e)

if __name__ == "__main__":
    main()
