import requests
import base64
import json
import os
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from colorama import Fore, Style, init

init(autoreset=True)

class PddiktiInvestigator:
    def __init__(self):
        self.KEY_B64 = "ecHyOABV9jgO2/+dzE49cfexQpr/H4SiAYWrHLD7PQ0="
        self.IV_B64  = "Gu3qsglYJhOOm0eXf6aN2w=="
        self.SEARCH_URL = "https://api-pddikti.kemdiktisaintek.go.id/pencarian/enc/all/{}"
        self.DETAIL_BASE = "https://api-pddikti.kemdiktisaintek.go.id/detail/{}/{}"
        
        # Headers sesuai request terakhir Anda (Working)
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
            'Connection': 'keep-alive',
            'Host': 'api-pddikti.kemdiktisaintek.go.id',
            'Origin': 'https://pddikti.kemdiktisaintek.go.id',
            'Referer': 'https://pddikti.kemdiktisaintek.go.id/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
            'X-User-IP': '125.164.233.49',
            'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }

    def _decrypt_payload(self, encrypted_text):
        try:
            key_bytes = base64.b64decode(self.KEY_B64)
            iv_bytes = base64.b64decode(self.IV_B64)
            enc_bytes = base64.b64decode(encrypted_text)
            cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
            decrypted_bytes = unpad(cipher.decrypt(enc_bytes), AES.block_size)
            return json.loads(decrypted_bytes.decode('utf-8'))
        except Exception:
            return None

    def save_evidence(self, data, kategori, nama_target):
        """Menyimpan hasil temuan ke file TXT"""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # Bersihkan nama file dari karakter aneh
        safe_name = "".join([c for c in nama_target if c.isalnum() or c in (' ', '_')]).strip().replace(' ', '_')
        filename = f"REPORT_{safe_name}_{timestamp}.txt"
        
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("="*60 + "\n")
                f.write(f"OSINT EVIDENCE REPORT - PDDIKTI\n")
                f.write(f"Target: {nama_target}\n")
                f.write(f"Date  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*60 + "\n\n")
                
                f.write(json.dumps(data, indent=4, sort_keys=True))
                
                f.write("\n\n" + "="*60 + "\n")
                f.write("END OF REPORT\n")
            
            print(f"\n{Fore.GREEN}[v] Evidence Report tersimpan: {filename}{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}[!] Gagal menyimpan report: {e}")

    def get_details(self, id_unik, kategori, nama_asli):
        print(f"\n{Fore.CYAN}[*] Mengambil data detail...{Fore.RESET}")
        url = self.DETAIL_BASE.format(kategori, id_unik)
        try:
            response = requests.get(url, headers=self.headers, timeout=20)
            if response.status_code == 200:
                data = self._decrypt_payload(response.text)
                if not data:
                    try: data = response.json()
                    except: return
                
                self._display_deep_info(data)
                
                # --- AUTO SAVE ---
                self.save_evidence(data, kategori, nama_asli)
            else:
                print(f"{Fore.RED}[!] Gagal. Status: {response.status_code}")
        except Exception as e:
            print(f"{Fore.RED}[!] Error Koneksi: {e}")

    def _display_deep_info(self, data):
        print(f"\n{Style.BRIGHT}{Fore.WHITE}=== INFORMASI MENDALAM ==={Style.RESET_ALL}")
        # Tampilkan ringkasan saja di layar agar tidak penuh
        umum = data
        print(f"Nama     : {umum.get('nm_pd', '-')}")
        print(f"Lahir    : {umum.get('tmpt_lahir', '-')} / {umum.get('tgl_lahir', '-')}")
        print(f"PT       : {umum.get('namapt', '-')}")
        print(f"Prodi    : {umum.get('namaprodi', '-')}")
        print(f"Mulai    : {umum.get('mulai_smt', '-')}")
        print(f"Status   : {Fore.YELLOW}{umum.get('ket_keluar', 'Aktif/Belum Lulus')}{Fore.RESET}")
        
        history = data.get('riwayat_status_kuliah', [])
        if history:
             last_stat = history[0] # Ambil semester terakhir
             print(f"Stat Terakhir: {last_stat.get('nm_smt')} - {last_stat.get('nm_stat_mhs')}")

    def run_search(self):
        target_name = input(f"{Fore.GREEN}Masukkan Nama Lengkap Target: {Fore.RESET}")
        print(f"{Fore.CYAN}[*] Searching...{Fore.RESET}")
        try:
            url = self.SEARCH_URL.format(target_name)
            response = requests.get(url, headers=self.headers, timeout=20)
            data = self._decrypt_payload(response.text)
            
            if not data:
                print(f"{Fore.RED}[!] Data tidak ditemukan.")
                return

            all_results = []
            mhs_list = data.get('mahasiswa', [])
            if mhs_list:
                print(f"\n{Fore.YELLOW}=== MAHASISWA ({len(mhs_list)}) ==={Fore.RESET}")
                for m in mhs_list:
                    info = {'type': 'mhs', 'id': m['id'], 'nama': m['nama'], 'desc': f"NIM: {m['nim']} | {m['nama_pt']}"}
                    all_results.append(info)
                    print(f"[{len(all_results)}] {info['nama']} - {info['desc']}")

            dosen_list = data.get('dosen', [])
            if dosen_list:
                print(f"\n{Fore.MAGENTA}=== DOSEN ({len(dosen_list)}) ==={Fore.RESET}")
                for d in dosen_list:
                    info = {'type': 'dosen', 'id': d['id'], 'nama': d['nama'], 'desc': f"NIDN: {d['nidn']} | {d['nama_pt']}"}
                    all_results.append(info)
                    print(f"[{len(all_results)}] {info['nama']} - {info['desc']}")

            if not all_results: return

            choice = input(f"\n{Style.BRIGHT}Pilih nomor (0 keluar): {Style.RESET_ALL}")
            if choice.isdigit() and int(choice) > 0:
                sel = all_results[int(choice)-1]
                self.get_details(sel['id'], sel['type'], sel['nama'])
            
        except Exception as e:
            print(f"Critical Error: {e}")

if __name__ == "__main__":
    app = PddiktiInvestigator()
    app.run_search()