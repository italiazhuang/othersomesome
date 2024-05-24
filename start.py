import requests
import json
import base64
import pyaudio
import wave
import pyttsx3
import random
import datetime

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

# 从 JSON 文件中读取输入内容和输出内容
def load_conversation(filename):
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

# 使用 ChatGPT 处理用户输入
def process_input_with_openai_chatgpt(text):
    # 这里应该添加调用OpenAI ChatGPT的代码
    pass

# 语音识别函数
def recognize_input(audio_data):
    print("正在识别...")
    recognized_text = baidu_speech_recognition(audio_data)
    return recognized_text

# 生成回复函数
def generate_response(recognized_text, conversation_data):
    inputs = conversation_data.get("inputs", {})
    default_response = conversation_data.get("default_response", "抱歉，我不明白你的意思")
    
    for key, value in inputs.items():
        if key in recognized_text:
            return value
    return default_response

# 获取当前时间
def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 获取当前日期
def get_current_date():
    return datetime.datetime.now().strftime("%Y-%m-%d")

# 获取当前星期
def get_current_weekday():
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    return weekdays[datetime.datetime.now().weekday()]

# 主函数
def main():
    try:
        conversation_data = load_conversation("conversation.json")
        while True:
            audio_data = record_audio()
            recognized_text = recognize_input(audio_data)
            if any(keyword in recognized_text for keyword in ["退出", "关闭"]) and len(recognized_text) < 5:
                print("退出程序")
                break
            elif "现在几点" in recognized_text:
                current_time = get_current_time()
                print("机器人：" + current_time)
                text_to_speech(current_time)
            elif "几号" in recognized_text:
                current_date = get_current_date()
                print("机器人：" + current_date)
                text_to_speech(current_date)
            elif "星期几" in recognized_text:
                current_weekday = get_current_weekday()
                print("机器人：" + current_weekday)
                text_to_speech(current_weekday)
            else:
                response = generate_response(recognized_text, conversation_data)
                print("机器人：" + response)
                text_to_speech(response)
    except Exception as e:
        print("发生错误：", e)

# 调用主函数
if __name__ == "__main__":
    main()
