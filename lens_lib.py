import time
import os
import base64
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class LensLib:
    def __init__(self):
        pass

    def setup_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        return driver

    def scan(self, mode, input_data):
        """
        mode: 'url' atau 'file'
        input_data: Link URL atau Absolute Path File di komputer
        """
        driver = self.setup_driver()
        results = []

        try:
            if mode == 'url':
                # Cara Lama: Lewat URL
                encoded_url = requests.utils.quote(input_data)
                lens_url = f"https://lens.google.com/uploadbyurl?url={encoded_url}"
                driver.get(lens_url)
            
            elif mode == 'file':
                # Cara Baru: Lewat Google Images -> Upload
                driver.get("https://www.google.com/imghp?hl=en")
                time.sleep(2)
                
                # 1. Klik Ikon Kamera
                cam_btn = driver.find_element(By.CSS_SELECTOR, "div[aria-label='Search by image']")
                cam_btn.click()
                time.sleep(1)
                
                # 2. Kirim File ke Input Tersembunyi (Tanpa klik tombol upload manual)
                # Input type file biasanya tersembunyi, kita cari input name='encoded_image'
                file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
                file_input.send_keys(input_data) # Kirim path file lokal
                
            # Tunggu loading hasil
            time.sleep(5)
            
            # --- SCRAPING LOGIC (Sama seperti sebelumnya) ---
            # Kita cari tombol "Visual matches" dulu
            try:
                driver.execute_script("window.scrollBy(0, 150);")
                elements = driver.find_elements(By.XPATH, "//*[text()]")
                for el in elements:
                    if "visual matches" in el.text.lower() or "kecocokan visual" in el.text.lower():
                        driver.execute_script("arguments[0].click();", el)
                        time.sleep(3)
                        break
            except: pass

            # Ambil Link Hasil
            links = driver.find_elements(By.TAG_NAME, "a")
            count = 0
            for link in links:
                if count >= 10: break
                href = link.get_attribute('href')
                if href and "http" in href and "google" not in href:
                    title = link.text.strip() or "Result"
                    try:
                        img = link.find_element(By.TAG_NAME, "img").get_attribute('src')
                    except:
                        img = ""
                    
                    results.append({"title": title, "link": href, "img": img})
                    count += 1
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            driver.quit()
        
        return results