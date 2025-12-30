import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from colorama import Fore, init

init(autoreset=True)

def auto_screenshot(url):
    print(f"{Fore.CYAN}[*] Menyiapkan Robot Browser (Chrome)...")
    
    # Setup Chrome Options (Supaya window terbuka maximised)
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless") # Aktifkan ini jika ingin jalan di background tanpa layar
    
    # Auto-install driver Chrome yang cocok
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        print(f"{Fore.YELLOW}[*] Mengakses: {url}")
        driver.get(url)
        
        # Tunggu loading (bisa diganti dengan WebDriverWait yang lebih canggih nanti)
        time.sleep(5) 
        
        # Scroll ke bawah sedikit agar lazy-load images muncul
        driver.execute_script("window.scrollTo(0, 500);")
        time.sleep(2)
        
        # Ambil Screenshot
        filename = f"evidence_{int(time.time())}.png"
        driver.save_screenshot(filename)
        print(f"{Fore.GREEN}[+] Bukti tersimpan: {filename}")
        
        # Biarkan terbuka sebentar (5 detik) sebelum tutup
        time.sleep(5)
        
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}")
    finally:
        print("[*] Menutup browser...")
        driver.quit()

if __name__ == "__main__":
    target = input("Masukkan URL Target (LinkedIn/IG/Web): ")
    auto_screenshot(target)