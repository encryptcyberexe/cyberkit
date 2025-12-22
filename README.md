# 🔒 CyberKit - All-in-One Cybersecurity Toolkit

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Kali%20Linux-blue?style=for-the-badge&logo=kali-linux">
  <img src="https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge">
</p>

**CyberKit**, Kali Linux için geliştirilmiş, siber güvenlik işlemlerini hızlandıran modüler bir araç setidir. Penetrasyon testi, güvenlik değerlendirmesi ve CTF yarışmaları için idealdir.

---

## ✨ Özellikler

### 🌐 Network Scanner
- Hızlı/Tam port taraması
- Servis ve versiyon tespiti
- OS Detection
- Vulnerability scanning (NSE)
- Stealth/SYN tarama
- UDP tarama
- ARP/Ping sweep

### 🕸️ Web Scanner
- Directory/File bruteforce (Gobuster, Ffuf)
- Nikto web vulnerability scanner
- SQL Injection (SQLMap)
- XSS tarama
- Subdomain enumeration
- SSL/TLS analizi
- WordPress scanning (WPScan)
- HTTP header analizi

### 🔍 OSINT / Information Gathering
- WHOIS sorgulama
- DNS enumeration
- Email harvesting (theHarvester)
- Google Dork generator
- Shodan search
- Username check (Sherlock)
- IP geolocation
- Certificate transparency logs

### 🔑 Password Tools
- Hash identifier
- Hash generator (MD5, SHA1, SHA256, etc.)
- John The Ripper entegrasyonu
- Hashcat entegrasyonu
- Hydra brute force
- Wordlist generator (Crunch, CeWL)
- Password strength checker

### 💀 Exploitation
- Metasploit Framework entegrasyonu
- SearchSploit (Exploit-DB)
- Reverse shell generator
- Payload generator (msfvenom)
- Netcat listener
- File transfer helpers
- Privilege escalation checkers

### 📄 Report Generator
- Metin rapor şablonları
- HTML rapor oluşturma
- Markdown rapor oluşturma
- Tarama sonuçlarını birleştirme

---

## 🚀 Kurulum

### Gereksinimler
- Kali Linux (önerilir) veya Debian tabanlı Linux
- Python 3.8+
- Root yetkisi (bazı özellikler için)

### Adımlar

```bash
# Repository'yi klonlayın veya dosyaları kopyalayın
cd /opt
git clone <repository-url> cyberkit
cd cyberkit

# Çalıştırma iznini verin
chmod +x cyberkit.py

# Çalıştırın
sudo python3 cyberkit.py
```

### Symbolic Link Oluşturma (Opsiyonel)

```bash
sudo ln -s /opt/cyberkit/cyberkit.py /usr/local/bin/cyberkit
```

Artık terminalde sadece `cyberkit` yazarak çalıştırabilirsiniz.

---

## 📖 Kullanım

### İnteraktif Mod
```bash
sudo python3 cyberkit.py
```

### Komut Satırı Seçenekleri
```bash
python3 cyberkit.py -h        # Yardım
python3 cyberkit.py -v        # Versiyon
python3 cyberkit.py -c        # Araç durumu kontrolü
```

### Menü Yapısı

```
[1] Network Scanner      - Nmap tabanlı ağ taramaları
[2] Web Scanner          - Web uygulama güvenlik testleri
[3] OSINT / Recon        - Bilgi toplama araçları
[4] Password Tools       - Şifre ve hash araçları
[5] Exploitation         - Exploit ve payload araçları
[6] Report Generator     - Rapor oluşturma
[7] Hızlı Tarama         - Tek komutla temel taramalar
[8] Cheatsheet           - Faydalı komutlar
[9] Araç Durumu          - Yüklü araçları kontrol et
[0] Çıkış
```

---

## 🔧 Gerekli Araçlar

CyberKit, Kali Linux'ta varsayılan olarak bulunan araçları kullanır:

| Araç | Kurulum | Kullanım Alanı |
|------|---------|----------------|
| nmap | `apt install nmap` | Network scanning |
| gobuster | `apt install gobuster` | Directory bruteforce |
| nikto | `apt install nikto` | Web vulnerability |
| sqlmap | `apt install sqlmap` | SQL injection |
| hydra | `apt install hydra` | Brute force |
| john | `apt install john` | Password cracking |
| hashcat | `apt install hashcat` | Password cracking |
| metasploit | `apt install metasploit-framework` | Exploitation |
| whatweb | `apt install whatweb` | Web fingerprinting |
| theharvester | `apt install theharvester` | Email harvesting |
| sherlock | `apt install sherlock` | Username OSINT |

Tüm araçları yüklemek için:
```bash
sudo apt update
sudo apt install nmap gobuster nikto sqlmap hydra john hashcat \
    metasploit-framework whatweb theharvester sherlock ffuf \
    sslscan dnsrecon sublist3r wpscan
```

---

## 📂 Çıktı Dizini Yapısı

```
output/
├── network/      # Nmap tarama sonuçları
├── web/          # Web tarama sonuçları
├── osint/        # OSINT sonuçları
├── passwords/    # Hash/password sonuçları
├── exploits/     # Payload ve exploit dosyaları
└── reports/      # Oluşturulan raporlar
```

---

## ⚠️ Yasal Uyarı

Bu araç **sadece yasal ve etik** amaçlar için kullanılmalıdır:

- ✅ Kendi sistemlerinizde güvenlik testi
- ✅ Yazılı izin alınmış penetrasyon testleri
- ✅ CTF yarışmaları ve lab ortamları
- ✅ Eğitim amaçlı kullanım

- ❌ İzinsiz sistemlere saldırı
- ❌ Yasadışı aktiviteler
- ❌ Zararlı amaçlı kullanım

**Sorumlu kullanım sizin sorumluluğunuzdadır.**

---

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/YeniOzellik`)
3. Commit edin (`git commit -m 'Yeni özellik eklendi'`)
4. Push edin (`git push origin feature/YeniOzellik`)
5. Pull Request açın

---

## 📜 Lisans

MIT License - Detaylar için `LICENSE` dosyasına bakın.

---

## 📞 İletişim

Sorular ve öneriler için issue açabilirsiniz.

---

<p align="center">
  <b>🛡️ Güvenli Hackleyin! 🛡️</b>
</p>
