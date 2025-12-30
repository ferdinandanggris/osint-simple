import os
import sys
from time import sleep
from colorama import Fore, Style, init

# Import Modul-modul yang sudah dibuat
# Pastikan nama file .py sesuai dengan import ini
try:
    from pddikti import PddiktiInvestigator
    from social_recon import SherlockGen
    from image_recon import ImageInvestigator
    from lens_scraper import LensScraper
except ImportError as e:
    print(f"Error: Ada file script yang hilang. {e}")
    sys.exit()

init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_screen()
    print(f"{Fore.CYAN}{Style.BRIGHT}")
    print(r"""
   ____  _____  ___   _   __ ______   __    ___    ____ 
  / __ \/ ___/ /   | / | / //_  __/  / /   /   |  / __ )
 / / / /\__ \ / /| |/  |/ /  / /    / /   / /| | / __  |
/ /_/ /___/ // ___ / /|  /  / /    / /___/ ___ |/ /_/ / 
\____//____//_/  |/_/ |_/  /_/    /_____/_/  |_/_____/  
    """)
    print(f"{Fore.WHITE}      Simple Intelligence Tool for Personal Use")
    print(f"{Fore.RED}      [!] USE FOR EDUCATIONAL PURPOSE ONLY [!]")
    print(f"{Fore.CYAN}" + "="*50 + f"{Fore.RESET}\n")

def main_menu():
    while True:
        print_banner()
        print(f"{Fore.YELLOW}[ MENU UTAMA ]{Fore.RESET}")
        print("1. Pddikti Hunter     (Cek Data Kuliah/Dosen & Simpan Laporan)")
        print("2. Social Recon       (Generate Username Permutation)")
        print("3. Visual Opener      (Buka Tab Google/Yandex/Bing Otomatis)")
        print("4. Lens Scraper V4    (Auto Download Gambar & Link Source)")
        print(f"{Fore.RED}0. Keluar{Fore.RESET}")
        
        choice = input(f"\n{Fore.GREEN}Pilih Menu >> {Fore.RESET}")

        if choice == '1':
            tool = PddiktiInvestigator()
            tool.run_search()
        elif choice == '2':
            tool = SherlockGen()
            tool.run()
        elif choice == '3':
            tool = ImageInvestigator()
            tool.run()
        elif choice == '4':
            print(f"\n{Fore.WHITE}Paste URL Foto Target:")
            target = input(f"{Fore.GREEN}> {Fore.RESET}").strip()
            if target.startswith("http"):
                tool = LensScraper()
                tool.run(target)
            else:
                print(f"{Fore.RED}[!] URL tidak valid.")
        elif choice == '0':
            print("Bye.")
            sys.exit()
        else:
            print(f"{Fore.RED}Pilihan tidak valid.")
        
        input(f"\n{Style.DIM}Tekan Enter untuk kembali ke menu...{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nKeluar paksa.")
        sys.exit()