import requests
import base64
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

class PddiktiLib:
    def __init__(self):
        self.KEY_B64 = "ecHyOABV9jgO2/+dzE49cfexQpr/H4SiAYWrHLD7PQ0="
        self.IV_B64  = "Gu3qsglYJhOOm0eXf6aN2w=="
        self.SEARCH_URL = "https://api-pddikti.kemdiktisaintek.go.id/pencarian/enc/all/{}"
        self.DETAIL_BASE = "https://api-pddikti.kemdiktisaintek.go.id/detail/{}/{}"
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Host': 'api-pddikti.kemdiktisaintek.go.id',
            'Origin': 'https://pddikti.kemdiktisaintek.go.id',
            'Referer': 'https://pddikti.kemdiktisaintek.go.id/'
        }

    def _decrypt_payload(self, encrypted_text):
        try:
            key_bytes = base64.b64decode(self.KEY_B64)
            iv_bytes = base64.b64decode(self.IV_B64)
            enc_bytes = base64.b64decode(encrypted_text)
            cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
            decrypted_bytes = unpad(cipher.decrypt(enc_bytes), AES.block_size)
            return json.loads(decrypted_bytes.decode('utf-8'))
        except:
            return None

    def search(self, keyword):
        """Mencari nama dan mengembalikan list hasil"""
        try:
            url = self.SEARCH_URL.format(keyword)
            response = requests.get(url, headers=self.headers, timeout=10)
            data = self._decrypt_payload(response.text)
            return data if data else {}
        except Exception as e:
            return {"error": str(e)}

    def get_detail(self, id_unik, kategori):
        """Mengambil detail mahasiswa/dosen"""
        try:
            url = self.DETAIL_BASE.format(kategori, id_unik)
            response = requests.get(url, headers=self.headers, timeout=10)
            data = self._decrypt_payload(response.text)
            if not data:
                # Fallback jika tidak terenkripsi
                try: data = response.json()
                except: pass
            return data
        except Exception as e:
            return {"error": str(e)}