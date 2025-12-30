import urllib.parse
import webbrowser
import time
from colorama import Fore, Style, init

init(autoreset=True)

class ImageInvestigator:
    def __init__(self):
        pass

    def open_browser_tabs(self, image_url):
        encoded_url = urllib.parse.quote(image_url)

        print(f"\n{Style.BRIGHT}{Fore.CYAN}=== AUTO BROWSER OPENER ==={Fore.RESET}")
        print(f"Target: {image_url[:50]}...\n")

        # Daftar URL Pencarian
        urls = {
            "Google Lens": f"https://lens.google.com/uploadbyurl?url={encoded_url}",
            "Yandex Images": f"https://yandex.com/images/search?rpt=imageview&url={encoded_url}",
            "Bing Visual": f"https://www.bing.com/images/search?view=detailv2&iss=sbi&form=SBIHMP&q=imgurl:{encoded_url}",
            "FaceCheck.ID": "https://facecheck.id/" # Ini manual upload, kita buka homenya saja
        }

        print(f"{Fore.YELLOW}[*] Membuka {len(urls)} tab browser secara otomatis...{Fore.RESET}")
        
        for name, url in urls.items():
            print(f"    -> Membuka {name}...")
            webbrowser.open_new_tab(url)
            # Kasih jeda sedikit agar browser tidak nge-lag buka banyak tab sekaligus
            time.sleep(0.5) 
            
        print(f"\n{Fore.GREEN}[v] Selesai! Silakan cek browser Anda.{Fore.RESET}")

    def run(self):
        print(f"{Fore.WHITE}Paste URL Foto Profil Target:")
        target_img = input(f"{Fore.GREEN}> {Fore.RESET}").strip()
        
        if not target_img.startswith("http"):
            print(f"{Fore.RED}[!] URL tidak valid.")
            return

        self.open_browser_tabs(target_img)

if __name__ == "__main__":
    tool = ImageInvestigator()
    tool.run()