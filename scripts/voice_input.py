import speech_recognition as sr
import pyaudio
import numpy
import wave
import keyboard
from pykakasi import kakasi
import re

# pa = pyaudio.PyAudio()
# for i in range(pa.get_device_count()):
#     print(pa.get_device_info_by_index(i))


WAVE_OUTPUT_FILENAME = "voice_tmp.wav" #音声を保存するファイル名
iDeviceIndex = 1 #録音デバイスのインデックス番号

chunk = 1024
FORMAT = pyaudio.paInt16

CHANNELS = 1 #モノラル
RATE = 44100 #サンプルレート（録音の音質）
kakasi = kakasi()


def VoiceRecodeAndRecongnize():
    p = pyaudio.PyAudio()
    start = input("録音開始 [Enter]>>")
    print("録音中...")
    stream = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = chunk)
    sequence = []
    # while True:
    #     data = stream.read(chunk)
    #     sequence.append(data)
    #     if keyboard.is_pressed("esc"):
    #         break
    for i in range(0, int(RATE / chunk * 3)):
        data = stream.read(chunk)
        sequence.append(data)
    print("録音終了")

    stream.close()
    p.terminate()
    wavFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wavFile.setnchannels(CHANNELS)
    wavFile.setsampwidth(p.get_sample_size(FORMAT))
    wavFile.setframerate(RATE)
    wavFile.writeframes(b"".join(sequence))
    wavFile.close()

    r = sr.Recognizer()
    with sr.AudioFile(WAVE_OUTPUT_FILENAME) as source:
        audio = r.record(source)
    word =  r.recognize_google(audio, language='ja')
    #kakasi = kakasi()
    kakasi.setMode('J', 'H')
    kakasi.setMode('K', 'H')
    conv = kakasi.getConverter()
    word_hiragana = conv.do(word)
    print ("----------------------------------------")
    print ("認識結果：" + word)
    print ("認識結果(ひらがなver)：" + word_hiragana)
    print ("----------------------------------------")

    return word_hiragana


def InterfaceVoice():
    while True :
        while True :
            try:
                word = VoiceRecodeAndRecongnize()
                if re.fullmatch(r"[\u3041-\u3094\u30FC]*", word) == None:
                    print ("不適切な文字列です。(英字・空欄などしりとりに適さない文字が入っている可能性があります。)")
                else :
                    break
            except sr.UnknownValueError as e:
                print ("認識エラーが発生しました。もう一度録音してください。")
        yn=0
        while True:
            y_or_n = input ("この認識結果でOK？ [y/n] >>")
            if y_or_n == "y" or y_or_n == "yes":
                yn=0
                break
            elif y_or_n == "n" or y_or_n == "no":
                yn=1
                break
        if yn == 0:
            break

    return word

InterfaceVoice()
