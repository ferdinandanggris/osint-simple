import time
import os
import requests
import urllib.parse
import base64
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from colorama import Fore, Style, init

init(autoreset=True)

class LensScraper:
    def __init__(self):
        self.download_folder = "evidence_images"
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)
        
        # Header agar download gambar tidak diblokir server (403 Forbidden)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    def setup_driver(self):
        print(f"{Fore.CYAN}[*] Menyiapkan Chrome Driver...{Fore.RESET}")
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        return driver

    def save_image(self, src, index):
        """Menangani penyimpanan gambar baik URL biasa maupun Base64"""
        filename = f"{self.download_folder}/match_{index}.jpg"
        
        try:
            # KASUS 1: Gambar adalah Base64 (Data URI)
            if "data:image" in src:
                # Format: data:image/jpeg;base64,/9j/4AAQSk...
                header, encoded = src.split(",", 1)
                data = base64.b64decode(encoded)
                with open(filename, "wb") as f:
                    f.write(data)
                return filename

            # KASUS 2: Gambar adalah URL HTTP biasa
            elif src.startswith("http"):
                response = requests.get(src, headers=self.headers, timeout=10)
                if response.status_code == 200:
                    with open(filename, "wb") as f:
                        f.write(response.content)
                    return filename
        except Exception as e:
            print(f"{Fore.RED}    [!] Gagal save gambar: {e}{Fore.RESET}")
        
        return None

    def click_visual_matches(self, driver):
        keywords = ["kecocokan visual", "kecocokan persis", "visual matches", "exact matches", "telusuri", "temukan sumber gambar"]
        print(f"{Fore.YELLOW}[*] Mencari Filter 'Kecocokan Visual'...{Fore.RESET}")
        
        driver.execute_script("window.scrollBy(0, 150);")
        time.sleep(1)

        try:
            elements = driver.find_elements(By.XPATH, "//*[text()]")
            for el in elements:
                if not el.is_displayed(): continue
                txt = el.text.strip().lower()
                if any(k in txt for k in keywords) and len(txt) < 30:
                    print(f"{Fore.GREEN}[v] Filter ditemukan: '{el.text}'. Mengklik...{Fore.RESET}")
                    driver.execute_script("arguments[0].click();", el)
                    time.sleep(3)
                    return
            print(f"{Fore.RED}[!] Filter tidak ditemukan. Menggunakan hasil default.{Fore.RESET}")
        except:
            pass

    def run(self, image_url):
        driver = self.setup_driver()
        results_data = [] # List untuk menampung data lengkap (Title, Link, Image)

        try:
            encoded_url = urllib.parse.quote(image_url)
            lens_url = f"https://lens.google.com/uploadbyurl?url={encoded_url}"
            
            print(f"{Fore.YELLOW}[*] Membuka Google Lens...{Fore.RESET}")
            driver.get(lens_url)
            time.sleep(4)

            self.click_visual_matches(driver)

            print(f"{Fore.CYAN}[*] Scrolling & Scraping Data...{Fore.RESET}")
            
            # Scroll beberapa kali
            for _ in range(3):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

            # --- LOGIKA SCRAPING BARU ---
            # Kita cari elemen <a> (Link) yang membungkus hasil pencarian
            # Biasanya link hasil pencarian Google punya atribut href yang valid
            links = driver.find_elements(By.TAG_NAME, "a")
            
            print(f"    Menganalisis {len(links)} link di halaman...")
            
            count = 0
            for link in links:
                try:
                    href = link.get_attribute('href')
                    if not href or "google.com" in href or "javascript" in href:
                        continue # Skip link internal Google

                    # Cari elemen gambar di DALAM link tersebut
                    try:
                        img_tag = link.find_element(By.TAG_NAME, "img")
                        src = img_tag.get_attribute('src')
                    except:
                        continue # Kalau link gak ada gambarnya, skip

                    # Filter ukuran gambar (biar gak ambil icon kecil)
                    width = int(img_tag.get_attribute('naturalWidth') or img_tag.size['width'])
                    if width < 80: continue

                    # Ambil Judul/Deskripsi
                    # Biasanya text ada di div di dalam link, atau text dari link itu sendiri
                    title = link.text.replace("\n", " ").strip()
                    if not title:
                        title = link.get_attribute("aria-label") or "No Title"

                    # SAVE GAMBAR
                    count += 1
                    saved_path = self.save_image(src, count)

                    if saved_path:
                        print(f"{Fore.GREEN}[+] #{count} Ditemukan: {title[:30]}...{Fore.RESET}")
                        print(f"    Link: {href}")
                        
                        # Simpan ke memori
                        results_data.append({
                            "id": count,
                            "title": title,
                            "source_url": href,
                            "local_image": saved_path
                        })

                    if count >= 20: break

                except Exception as e:
                    continue

            # --- SIMPAN LAPORAN TEXT & JSON ---
            if results_data:
                # 1. Simpan JSON (Untuk data rapi)
                json_path = f"{self.download_folder}/laporan_lengkap.json"
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(results_data, f, indent=4)

                # 2. Simpan TXT (Untuk kemudahan baca)
                txt_path = f"{self.download_folder}/laporan_links.txt"
                with open(txt_path, 'w', encoding='utf-8') as f:
                    f.write(f"LAPORAN GOOGLE LENS - {time.ctime()}\n")
                    f.write("="*60 + "\n\n")
                    for item in results_data:
                        f.write(f"[{item['id']}] {item['title']}\n")
                        f.write(f"Link : {item['source_url']}\n")
                        f.write(f"File : {item['local_image']}\n")
                        f.write("-" * 40 + "\n")

                print(f"\n{Fore.GREEN}[v] Selesai! {count} hasil tersimpan.{Fore.RESET}")
                print(f"    Laporan: {txt_path}")
                os.startfile(os.path.abspath(self.download_folder))
            else:
                print(f"{Fore.RED}[!] Tidak ada data relevan yang terambil.{Fore.RESET}")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            input(f"\n{Style.BRIGHT}Tekan Enter untuk menutup browser...{Style.RESET_ALL}")
            driver.quit()

if __name__ == "__main__":
    print(f"{Fore.WHITE}Paste URL Foto Target:")
    target = input(f"{Fore.GREEN}> {Fore.RESET}").strip()
    
    if target.startswith("http"):
        scraper = LensScraper()
        scraper.run(target)
    else:
        print("URL tidak valid.")