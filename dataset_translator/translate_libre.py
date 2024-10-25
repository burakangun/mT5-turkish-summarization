import os
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Selenium Setup
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.maximize_window()
driver.get("https://www.deepl.com/en/translator")

def csv_isle_ve_kaydet(giris_dosya, cikis_dosya):
    # CSV dosyasını oku
    df = pd.read_csv('../dataset/test.csv', on_bad_lines='skip', engine='python')
    df = df.drop(['id'],axis=1)

    new_csv_data = {'id' : [], 'translated_article': [], 'translated_highlights': []}
    df_new = pd.DataFrame(new_csv_data)

    # İşlenecek veriler listesi
    yeni_veriler = []

    i = 0

    # CSV dosyasındaki her bir satırı gezinme
    for index, row in df.iterrows():
        article = row['article']
        summary = row['highlights']


        # Çeviri işlemi
        translated_article = translate('article',article)
        translated_summary = translate('summary',summary)

        df_new.loc[i] = [i, translated_article, translated_summary]



        '''# Yeni verileri listeye ekleme
        yeni_veriler.append({
            'translated_article': cevrilmis_article,
            'translated_summary': cevrilmis_summary
        })

            
        # Yeni DataFrame oluşturma
        yeni_df = pd.DataFrame(yeni_veriler)'''
        
        if i % 5 == 0:
            # Dosya yoksa başlıklarıyla birlikte yeni bir CSV dosyası oluştur
            if not os.path.isfile(cikis_dosya):
                print(f"Dosya '{cikis_dosya}' oluşturuluyor...")
                df_new.to_csv(cikis_dosya, mode='w', header=True, index=False)
            else:  # Dosya varsa üzerine veri ekle
                print(f"Dosya '{cikis_dosya}' mevcut. Veriler ekleniyor...")
                df_new.to_csv(cikis_dosya, mode='a', header=False, index=False)
          

        i += 1

    
def translate(category, text):
    try:
        # Çeviri alanına tıklamak için bekle
        input_area = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="textareasContainer"]/div[1]/section/div/div[1]/d-textarea/div[1]')
            )
        )
        input_area.click()

        # Kategori ve metni loglamak için
        print(f"{category}: {text}")

        # JavaScript ile metni doğrudan alana yerleştir
        driver.execute_script(
            "arguments[0].innerHTML = arguments[1];", input_area, text.replace('\n', '<br>')
        )

        # 15 saniye bekleme (Çevirinin tamamlanması için)
        time.sleep(15)

        # Çevirilen metni alma
        output_area = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="textareasContainer"]/div[3]/section/div[1]/d-textarea/div/p')
            )
        )
        translated_text = output_area.get_attribute('innerText')
        print("Çevirilen Metin:", translated_text)
        return translated_text
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        return text  # Hata olursa orijinal metni döndür


# Çalıştırma
csv_isle_ve_kaydet(
    r'C:\Users\Burak\Desktop\turkish_summarization\dataset\test.csv',  
    r'C:\Users\Burak\Desktop\turkish_summarization\dataset\translated_test.csv'
)