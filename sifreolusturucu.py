import random
import string

def generate_random_passwords(isim, ig_nick, tt_nick, num_passwords):
    """
    Rastgele şifreler oluşturur ve kullanıcı bilgilerini içerebilir.
    
    :param isim: Kullanıcının ismi
    :param ig_nick: Instagram nick'i
    :param tt_nick: TikTok nick'i
    :param num_passwords: Oluşturulacak şifre sayısı
    :return: Oluşturulan şifreler listesi
    """
    def generate_single_password():
        # Şifre için karakter setleri
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special_chars = '!@#$%^&*()_+-=[]{}|;:,.<>?'
        
       
        user_chars = (isim.lower() + ig_nick.lower() + tt_nick.lower())
        
       
        length = random.randint(12, 16)
        
        
        password_type = random.choice([
            'random',  # Tamamen rastgele
            'with_user_info',  # Kullanıcı bilgilerinden karakterler
            'mixed'  # Karışık
        ])
        
        if password_type == 'random':
            #Ariva Saplar
            characters = lowercase + uppercase + digits + special_chars
            password = ''.join(random.choice(characters) for _ in range(length))
        elif password_type == 'with_user_info':
            # Ariva Saplar
            base_chars = user_chars
            password = ''.join(random.choice(base_chars) for _ in range(length//2))
            password += ''.join(random.choice(lowercase + uppercase + digits + special_chars) for _ in range(length - len(password)))
        else:
            # ARİVA Saplar
            password = random.choice(user_chars) if user_chars else random.choice(lowercase)
            password += ''.join(random.choice(lowercase + uppercase + digits + special_chars) for _ in range(length - 1))
        
        # Ariva Saplar
        password_list = list(password)
        password_list[0] = random.choice(uppercase)
        password_list[1] = random.choice(digits)
        password_list[2] = random.choice(special_chars)
        
        # ARİVA Saplar 
        random.shuffle(password_list)
        return ''.join(password_list)
    
    # Ariva Saplar
    passwords = set()
    while len(passwords) < num_passwords:
        passwords.add(generate_single_password())
    
    return list(passwords)

def main():
    print("Rastgele Şifre Üretici Programına Hoş Geldiniz!")
    
    # Ariva Saplar
    isim = input("İsminizi girin: ").strip()
    ig_nick = input("Instagram nickini girin: ").strip()
    tt_nick = input("TikTok nickini girin: ").strip()
    
    # ARİVA Saplar 
    while True:
        try:
            sifre_adedi = int(input("Kaç adet şifre üretilsin? (1000-9000 arası): "))
            if 1000 <= sifre_adedi <= 9000:
                break
            else:
                print("Lütfen 1000 ile 9000 arasında bir sayı girin.")
        except ValueError:
            print("Lütfen geçerli bir sayı girin.")
    
    # ARİVA Saplar
    sifreler = generate_random_passwords(isim, ig_nick, tt_nick, sifre_adedi)
    
    # ARİVA Saplar
    with open('sifreler.txt', 'w', encoding='utf-8') as dosya:
        dosya.write(f"Bilgiler:\n")
        dosya.write(f"İsim: {isim}\n")
        dosya.write(f"Instagram Nick: {ig_nick}\n")
        dosya.write(f"TikTok Nick: {tt_nick}\n")
        dosya.write(f"\nOluşturulan Şifre Adedi: {len(sifreler)}\n\n")
        dosya.write("Şifreler:\n")
        for i, sifre in enumerate(sifreler, 1):
            dosya.write(f"{i}. {sifre}\n")
    
    print(f"\n{len(sifreler)} adet şifre 'sifreler.txt' dosyasına kaydedildi.")

if __name__ == "__main__":
    main()
