import pandas as pd
from googletrans import Translator

# Translator nesnesi oluşturun
translator = Translator()

# Veriyi yükleyin
df = pd.read_csv('../dataset/train.csv')

# Çeviri fonksiyonunu tanımlayın
def translate_text(text):
    if pd.isna(text) or text == '':
        print("Boş veya geçersiz metin bulundu.")
        return text  # Boş veya geçersiz metin döndürülüyor
    
    try:
        # Metni İngilizceden Türkçeye çevirir
        translated = translator.translate(text, src='en', dest='tr')
        return translated.text
    except Exception as e:
        print(f"Çeviri hatası: {e}")
        return text

# 'article' ve 'highlights' sütunlarını çevirin
df['article'] = df['article'].apply(translate_text)
df['highlights'] = df['highlights'].apply(translate_text)

# Çevirilmiş dosyayı kaydedin
df.to_csv('translated_dataset.csv', index=False)

print("Çeviri işlemi tamamlandı!")
