__author__ = "İlker ŞENER"

import speech_recognition as sr
from datetime import datetime
from smtplib import SMTP
import webbrowser
import time
from gtts import gTTS
from playsound import playsound
import random
import os
import smtplib
import requests
import json

r = sr.Recognizer()


def record(ask=False):
    with sr.Microphone() as source:
        if ask:
            speak(ask)
        audio = r.listen(source)
        voice = ''
        try:
            voice = r.recognize_google(audio, language='tr-TR')
        except sr.UnknownValueError:
            speak('Anlayamadım lütfen tekrar konuşun')
        except sr.RequestError:
            speak('sistem çalışmıyor')
        return voice



def response(voice):
    if 'nasılsın' in voice:
        speak('İyiyim sen nasılsın?')

    elif 'iyiyim' in voice:
        speak('İyi olduğuna sevindim?')

    elif 'kötüyüm' in voice:
        speak('Kötü olduğun için üzgünüm')

    elif 'saat kaç' in voice:
        speak(datetime.now().strftime('%H:%M:%S'))

    elif 'arama yap' in voice:
        search = record('ne aramak istiyorsun?')
        url = 'https://google.com/search?q=' + search
        webbrowser.get().open(url)
        speak(search + ' için bulduklarım')


    elif 'tamamdır' in voice:
        speak('görüşürüz')
        exit()

    elif 'kendini kapat' in voice:
        speak('görüşürüz')
        exit()


    elif 'e-posta gönder' in voice:
        ddd = record('mesaj nedir')
        speak('kullanıcı adını ve şifreni gir')
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        a = str(input('Kullanıcı Adınız:'))
        b = str(input('Şifreniz :'))
        mail.login(a,b)
        c = input('gönderilecek adres :')
        mail.sendmail(a,c,ddd)
        speak('gönderiliyor')

    elif 'hava durumu' in voice:
        city = record('Hangi şehri öğrenmek istiyorsunuz?')
        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=83154ce12848dedc20ff296e496dacc5')
        weatherData = response.json()
        skyDescription = weatherData['weather'][0]['description']
        cityName = weatherData['name']
        skyTypes = ['clear sky', 'few clouds', 'overcast clouds', 'scattered clouds', 'broken clouds', 'shower rain','rain', 'thunderstorm', 'snow', 'mist']
        skyTypesTR = ['Güneşli', 'Az Bulutlu', 'Çok Bulutlu(Kapalı)', 'Alçak Bulutlu', 'Yer Yer Açık Bulutlu','Sağanak Yağmurlu', 'Yağmurlu', 'Gök Gürültülü Fırtına', 'Karlı', 'Puslu']

        for i in range(len(skyTypes)):
            if skyDescription == skyTypes[i]:
                skyDescription = skyTypesTR[i]

        temp = round((weatherData['main']['temp']) - 273.15,2)
        feels_temp = round((weatherData['main']['feels_like'] - 273.15),2)
        temp_min = round((weatherData['main']['temp_min'] - 273.15),2)
        temp_max = round((weatherData['main']['temp_max'] - 273.15), 2)

        havadurumuDict = {
            "Şehir":cityName,
            "Gökyüzü":skyDescription,
            "Sıcaklık":temp,
            "Hissedilen":feels_temp,
            "Minimum":temp_min,
            "Maksimum":temp_max,

        }
        speak(city + 'İçin bugünün hava durumu bilgileri')
        print(havadurumuDict)



def speak(string):
            tts = gTTS(string,lang='tr')
            rand = random.randint(1,10000)
            file = 'audio-'+str(rand)+'.mp3'
            tts.save(file)
            playsound(file)
            os.remove(file)


speak('nasıl yardımcı olabilirim')
time.sleep(1)
while 1:
    voice = record()
    print(voice)
    response(voice)
