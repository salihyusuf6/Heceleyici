import time
import json
import os
from pathlib import Path
from gtts import gTTS
from playsound import playsound

# Varsayılan ayar
Base_Settings = {"Base":{"tKisa":1,"tNormal":1,"tUzun":1.5, "molaSikligi":30, "molaSuresi":5}}
Time_Select = ""
Time_Data = {}
Time_Data_SavePath = "Time.json"
molaSikligi = 0
molaSuresi = 0
tKısa = 0
tNormal = 0
tUzun = 0
alinan_path = "Mesaj.txt"

# Dosya varsa okuma işlemi
if Path(Time_Data_SavePath).exists():
    with open(Time_Data_SavePath, "r", encoding="UTF-8") as js_file:
        Time_Data = json.load(js_file)  # Dosya içeriğini yükle
        for eklencek in Time_Data.keys():
            Time_Select += f"\n{eklencek}"
else:
    # Dosya yoksa Base_Settings'i yaz
    with open(Time_Data_SavePath, "w", encoding="UTF-8") as js_file:
        json.dump(Base_Settings, js_file, indent=4)
    Time_Data = Base_Settings  # Yalnızca yazdığımız ayarları kullan
    Time_Select = "Base"

if not Path(alinan_path).exists():
    file = open(alinan_path, "w", encoding="UTF-8")
    file.write("base metin")
    file.close()

def Yazdır(mesaj_liste):
    i = 1
    ses_dosyasi = "mesaj.mp3"
    for mesaj in mesaj_liste:
        print(f"{i}/{len(mesaj_liste)}   :   " + mesaj)
        cikti = gTTS(text=mesaj, lang="tr", slow=False)
        cikti.save(ses_dosyasi)
        playsound(ses_dosyasi)
        if len(mesaj) <= 3:            
            time.sleep(tKısa)           
        elif 4 <= len(mesaj) <= 8:            
            time.sleep(tNormal)
        elif len(mesaj) > 8:            
            time.sleep(tUzun)
        
            

        if i % molaSikligi == 0:
            print("!!!! Ufak Bi Mola !!!!")
            print(f"Sıradaki mola {i + molaSikligi}")
            time.sleep(molaSuresi)
        i += 1

checker = True
while checker:
    girdi = input("1:Terminal yazısı \n 2:txt yazısı \n 3:type ekleme \n --->")
    
    if girdi == "1":        
        mesaj = input("Mesaj ---->")
        Time_Selected = input("Girdi tipi seçiniz \n" + Time_Select + "\n --->")
        try:
            tKısa = Time_Data[Time_Selected]["tKisa"]
            tUzun = Time_Data[Time_Selected]["tUzun"]
            tNormal = Time_Data[Time_Selected]["tNormal"]
            molaSikligi = Time_Data[Time_Selected]["molaSikligi"]
            molaSuresi = Time_Data[Time_Selected]["molaSuresi"]
        except KeyError:
            print("Aradığınız tip bulunamadı, büyük harflere dikkat edin.")
            continue

        mesaj_splited = mesaj.split(" ")
        print(f"Harf sayısı {len(mesaj)} \nKelime sayısı {len(mesaj_splited)}")
        print("Heceleme 3 saniye içinde başlıyor")
        time.sleep(3)
        Yazdır(mesaj_splited)        
    
    elif girdi == "2":
        with open(alinan_path, "r", encoding="UTF-8") as mesaj_dosya:
            mesaj = mesaj_dosya.read()
            mesaj_splited = mesaj.split(" ")

        Time_Selected = input("Girdi tipi seçiniz \n" + Time_Select + "\n --->")
        try:
            tKısa = Time_Data[Time_Selected]["tKisa"]
            tUzun = Time_Data[Time_Selected]["tUzun"]
            tNormal = Time_Data[Time_Selected]["tNormal"]
            molaSikligi = Time_Data[Time_Selected]["molaSikligi"]
            molaSuresi = Time_Data[Time_Selected]["molaSuresi"]
        except KeyError:
            print("Aradığınız tip bulunamadı, büyük harflere dikkat edin.")
            continue

        print(f"Harf sayısı {len(mesaj)} \nKelime sayısı {len(mesaj_splited)}")
        print("Heceleme 3 saniye içinde başlıyor")
        time.sleep(3)
        Yazdır(mesaj_splited)

    elif girdi == "3":
        with open(Time_Data_SavePath, "r", encoding="UTF-8") as js_file:
            Time_Data = json.load(js_file)

        isim = input("Girdi tipi adı giriniz -->")
        molaSikligi = int(input("Mola sıklığı giriniz -->"))
        molaSuresi = float(input("Mola süresi giriniz -->"))
        tKısa = float(input("Kısa kelime yazım süresi giriniz -->"))
        tNormal = float(input("Normal kelime yazım süresi giriniz -->"))
        tUzun = float(input("Uzun kelime yazım süresi giriniz -->"))

        new_dictinory = {isim: {
            "tKisa": tKısa,
            "tNormal": tNormal,
            "tUzun": tUzun,
            "molaSikligi": molaSikligi,
            "molaSuresi": molaSuresi
        }}

        # Güncellenmiş veriyi yazma
        Time_Data.update(new_dictinory)
        with open(Time_Data_SavePath, "w", encoding="UTF-8") as js_file:
            json.dump(Time_Data, js_file, indent=4)
            print("Girdi kaydedildi")

    else:
        print("Yanlış girdi algılandı, tekrar deneyiniz.")
        continue
    
    a = input("Heceleme bitti :) devam etmek için ENTER basınız")
    checker = False
