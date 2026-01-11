# 🔒 CyberKit - All-in-One Cybersecurity Toolkit

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Kali%20Linux-blue?style=for-the-badge&logo=kali-linux">
  <img src="https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge">
</p>

**CyberKit** is a modular cybersecurity toolkit designed for Kali Linux that speeds up common security operations. Perfect for penetration testing, security assessments, and CTF competitions.

---

## ✨ Features

### 🌐 Network Scanner
- Quick/Full port scanning
- Service and version detection
- OS Detection
- Vulnerability scanning (NSE scripts)
- Stealth/SYN scanning
- UDP scanning
- ARP/Ping sweep

### 🕸️ Web Scanner
- Directory/File bruteforce (Gobuster, Ffuf)
- Nikto web vulnerability scanner
- SQL Injection (SQLMap)
- XSS scanning
- Subdomain enumeration
- SSL/TLS analysis
- WordPress scanning (WPScan)
- HTTP header analysis

### 🔍 OSINT / Information Gathering
- WHOIS lookup
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
- John The Ripper integration
- Hashcat integration
- Hydra brute force
- Wordlist generator (Crunch, CeWL)
- Password strength checker

### 💀 Exploitation
- Metasploit Framework integration
- SearchSploit (Exploit-DB)
- Reverse shell generator
- Payload generator (msfvenom)
- Netcat listener
- File transfer helpers
- Privilege escalation checkers

### 📄 Report Generator
- TXT report templates
- HTML report generation
- Markdown report generation
- Merge scan results

---

## 🚀 Installation

### Requirements
- Kali Linux (recommended) or Debian-based Linux
- Python 3.8+
- Root privileges (for some features)

### Steps

```bash
# Clone the repository
git clone https://github.com/encryptcyberexe/cyberkit.git
cd cyberkit

# Make executable
chmod +x cyberkit.py

# Run
sudo python3 cyberkit.py
```

### Create Symbolic Link (Optional)

```bash
sudo ln -s $(pwd)/cyberkit.py /usr/local/bin/cyberkit
```

Now you can run `cyberkit` from anywhere.

---

## 📖 Usage

### Interactive Mode
```bash
sudo python3 cyberkit.py
```

### Command Line Options
```bash
python3 cyberkit.py -h        # Help
python3 cyberkit.py -v        # Version
python3 cyberkit.py -c        # Check tool status
```

### Menu Structure

```
[1]  Network Scanner      - Nmap-based network scanning
[2]  Web Scanner          - Web application security testing
[3]  OSINT / Recon        - Information gathering tools
[4]  Password Tools       - Hash and password utilities
[5]  Exploitation         - Exploit and payload tools
[6]  Report Generator     - Generate security reports
[7]  Quick Scan           - Fast basic reconnaissance
[8]  Cheatsheet           - Useful commands reference
[9]  Tool Status          - Check installed tools
[10] Popular Tools        - Most used security tools
[0]  Exit
```

---

## 🔥 Most Used Tools

| Category | Tool | Description |
|----------|------|-------------|
| **Scanning** | nmap | Port scanning, service detection |
| **Scanning** | masscan | Fast port scanner |
| **Web** | burpsuite | Web proxy & scanner |
| **Web** | gobuster | Directory bruteforce |
| **Web** | ffuf | Fast web fuzzer |
| **Web** | sqlmap | SQL injection |
| **Web** | nikto | Web vulnerability scanner |
| **Password** | john | Hash cracker |
| **Password** | hashcat | GPU hash cracker |
| **Password** | hydra | Online bruteforce |
| **Exploit** | metasploit | Exploitation framework |
| **OSINT** | theHarvester | Email/subdomain harvesting |

---

## 🔧 Required Tools

CyberKit uses tools commonly found in Kali Linux:

```bash
# Install all recommended tools
sudo apt update
sudo apt install nmap gobuster nikto sqlmap hydra john hashcat \
    metasploit-framework whatweb theharvester sherlock ffuf \
    sslscan dnsrecon wpscan netcat-openbsd
```

---

## 📂 Output Directory Structure

```
output/
├── network/      # Nmap scan results
├── web/          # Web scan results
├── osint/        # OSINT results
├── passwords/    # Hash/password results
├── exploits/     # Payloads and exploits
├── quick_scan/   # Quick scan results
└── reports/      # Generated reports
```

---

## ⚠️ Legal Disclaimer

This tool is intended for **legal and ethical use only**:

- ✅ Security testing on your own systems
- ✅ Authorized penetration testing
- ✅ CTF competitions and lab environments
- ✅ Educational purposes

- ❌ Unauthorized access to systems
- ❌ Illegal activities
- ❌ Malicious purposes

**You are responsible for your actions.**

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/NewFeature`)
3. Commit changes (`git commit -m 'Add new feature'`)
4. Push to branch (`git push origin feature/NewFeature`)
5. Open a Pull Request

---

## 📜 License

MIT License - See `LICENSE` file for details.

---

## 📞 Contact

**🌐 Website:** [synticasoftware.com.tr](https://synticasoftware.com.tr)  
**📧 Email:** info@synticasoftware.com.tr  
**📱 Instagram:** [@synticasoftware](https://instagram.com/synticasoftware)  
**💻 GitHub:** [github.com/encryptcyberexe/cyberkit](https://github.com/encryptcyberexe/cyberkit)  

For questions and suggestions, open an issue on GitHub.

---

<p align="center">
  <b>Developed by Syntica Software</b><br>
  <b>🛡️ Hack Responsibly! 🛡️</b>
</p>
