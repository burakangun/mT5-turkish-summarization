import pandas as pd
import requests

# API anahtarınızı buraya ekleyin.
API_KEY = '8d4b3788-67e8-4eb9-862d-0782d2ef39b0'
DEEPL_URL = 'https://api.deepl.com/v2/translate'

# Orijinal CSV dosyasını yükleyin.
data = pd.read_csv('../dataset/test.csv', engine='python')
data = data.drop(['id'],axis=1)

# Çevrilmiş verileri tutmak için boş bir liste oluşturuyoruz.
translated_rows = []

def translate_text(text, target_lang='TR'):
    """DeepL API'si ile metni belirtilen dile çevirir."""
    try:
        params = {
            'auth_key': API_KEY,
            'text': text,
            'target_lang': target_lang
        }
        response = requests.post(DEEPL_URL, data=params)
        if response.status_code == 200:
            return response.json()['translations'][0]['text']
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Hata: {e}")
        return None

# Veriyi iteratif olarak çeviriyoruz ve her 10 çeviriden sonra CSV'yi güncelliyoruz.
for index, row in data.iterrows():
    translated_article = translate_text(row['article'])
    translated_highlights = translate_text(row['highlights'])

    # Çevrilen satırı listeye ekle.
    translated_rows.append({
        'translated_article': translated_article,
        'translated_highlights': translated_highlights
    })

    # Her 10 satırda bir CSV dosyasını güncelle.
    if (index + 1) % 50 == 0 or (index + 1) == len(data):
        # Listeyi DataFrame'e dönüştür ve CSV'ye kaydet.
        translated_data = pd.DataFrame(translated_rows)
        translated_data.to_csv('../dataset/translated_test.csv', index=False, encoding='utf-8-sig')
        print(f"{index + 1} satır çevrildi ve dosya güncellendi.")

print("Çeviri işlemi tamamlandı ve dosya başarıyla kaydedildi.")
