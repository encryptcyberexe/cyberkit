"""
Report Generator Module - Generate Security Assessment Reports
"""

import os
import sys
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.colors import *
from utils.helpers import *

class ReportGenerator:
    def __init__(self):
        self.output_dir = create_output_dir("output/reports")
    
    def _sanitize_filename(self, name):
        """Sanitize filename"""
        return "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in name)
        
    def show_menu(self):
        while True:
            clear_screen()
            print_banner("""
╔═══════════════════════════════════════════════════════════╗
║                  REPORT GENERATOR                          ║
╚═══════════════════════════════════════════════════════════╝
            """)
            print(f"""
{Colors.CYAN}[1]{Colors.END} Yeni Rapor Oluştur
{Colors.CYAN}[2]{Colors.END} Scan Resultsını Birleştir
{Colors.CYAN}[3]{Colors.END} HTML Rapor Oluştur
{Colors.CYAN}[4]{Colors.END} Markdown Rapor Oluştur
{Colors.CYAN}[5]{Colors.END} Mevcut Raporları Listele
{Colors.CYAN}[0]{Colors.END} Back to Main Menu
            """)
            
            choice = get_input("Your choice")
            
            if choice == "0":
                break
            elif choice == "1":
                self.create_report()
            elif choice == "2":
                self.merge_results()
            elif choice == "3":
                self.generate_html()
            elif choice == "4":
                self.generate_markdown()
            elif choice == "5":
                self.list_reports()
            else:
                print_error("Invalid selection!")
                input("\nPress Enter to continue...")

    def create_report(self):
        clear_screen()
        print_banner("=== YENİ RAPOR OLUŞTUR ===\n")
        
        project_name = get_input("Proje/Target adı")
        assessor = get_input("Değerlendirici adı")
        scope = get_input("Kapsam (IP/Domain listesi)")
        
        timestamp = get_timestamp()
        safe_name = self._sanitize_filename(project_name)
        report_file = f"{self.output_dir}/report_{safe_name}_{timestamp}.txt"
        
        report_content = f"""
================================================================================
                        GÜVENLİK DEĞERLENDİRME RAPORU
================================================================================

Proje Adı: {project_name}
Değerlendirici: {assessor}
Tarih: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Kapsam: {scope}

================================================================================
                              YÜRÜTÜCÜ ÖZETİ
================================================================================

[Bu bölümü doldurun]

================================================================================
                              BULGULAR
================================================================================

Kritik Bulgular:
----------------
[Bulguları buraya ekleyin]

Yüksek Riskli Bulgular:
-----------------------
[Bulguları buraya ekleyin]

Orta Riskli Bulgular:
---------------------
[Bulguları buraya ekleyin]

Düşük Riskli Bulgular:
----------------------
[Bulguları buraya ekleyin]

================================================================================
                              ÖNERİLER
================================================================================

[Önerileri buraya ekleyin]

================================================================================
                              EK BELGELER
================================================================================

Scan Resultsı: output/ dizininde
Ekran Görüntüleri: [Yol ekleyin]

================================================================================
"""
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print_success(f"Report created: {report_file}")
        if os.path.exists(report_file):
            print_info(f"File size: {os.path.getsize(report_file)} bytes")
        input("\nPress Enter to continue...")

    def merge_results(self):
        clear_screen()
        print_banner("=== SONUÇLARI BİRLEŞTİR ===\n")
        
        print_info("Output dizinlerindeki dosyalar taranıyor...\n")
        
        output_dirs = ["output/network", "output/web", "output/osint", "output/passwords"]
        all_files = []
        
        for dir_path in output_dirs:
            if os.path.exists(dir_path):
                files = os.listdir(dir_path)
                for f in files:
                    all_files.append(os.path.join(dir_path, f))
                    print(f"  {Colors.CYAN}[+]{Colors.END} {os.path.join(dir_path, f)}")
        
        if not all_files:
            print_warning("Hiç tarama sonucu bulunamadı!")
        else:
            print_success(f"\nToplam {len(all_files)} dosya bulundu.")
            
            if confirm("Tüm sonuçlar tek dosyada birleştirilsin mi?"):
                timestamp = get_timestamp()
                merged_file = f"{self.output_dir}/merged_results_{timestamp}.txt"
                
                with open(merged_file, 'w', encoding='utf-8') as outfile:
                    for filepath in all_files:
                        outfile.write(f"\n{'='*60}\n")
                        outfile.write(f"FILE: {filepath}\n")
                        outfile.write(f"{'='*60}\n\n")
                        try:
                            with open(filepath, 'r', encoding='utf-8', errors='ignore') as infile:
                                outfile.write(infile.read())
                        except Exception as e:
                            outfile.write(f"Error reading file: {e}\n")
                
                print_success(f"Birleştirildi: {merged_file}")
        
        input("\nPress Enter to continue...")

    def generate_html(self):
        clear_screen()
        print_banner("=== HTML RAPOR ===\n")
        
        project_name = get_input("Proje adı")
        
        timestamp = get_timestamp()
        html_file = f"{self.output_dir}/report_{project_name}_{timestamp}.html"
        
        html_content = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Güvenlik Raporu - {project_name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #1a1a2e; color: #eee; }}
        .header {{ background: #16213e; padding: 20px; border-radius: 10px; margin-bottom: 20px; }}
        h1 {{ color: #e94560; }}
        h2 {{ color: #0f3460; background: #e94560; padding: 10px; border-radius: 5px; }}
        .finding {{ background: #16213e; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #e94560; }}
        .critical {{ border-left-color: #ff0000; }}
        .high {{ border-left-color: #ff6600; }}
        .medium {{ border-left-color: #ffcc00; }}
        .low {{ border-left-color: #00cc00; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ border: 1px solid #0f3460; padding: 10px; text-align: left; }}
        th {{ background: #0f3460; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔒 Güvenlik Değerlendirme Raporu</h1>
        <p><strong>Proje:</strong> {project_name}</p>
        <p><strong>Tarih:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        <p><strong>Oluşturan:</strong> CyberKit</p>
    </div>
    
    <h2>📊 Yürütücü Özeti</h2>
    <div class="finding">
        <p>[Özet bilgileri buraya ekleyin]</p>
    </div>
    
    <h2>🎯 Kapsam</h2>
    <div class="finding">
        <p>[Kapsam bilgilerini buraya ekleyin]</p>
    </div>
    
    <h2>⚠️ Bulgular</h2>
    
    <div class="finding critical">
        <h3>Kritik</h3>
        <p>[Kritik bulguları buraya ekleyin]</p>
    </div>
    
    <div class="finding high">
        <h3>Yüksek</h3>
        <p>[Yüksek riskli bulguları buraya ekleyin]</p>
    </div>
    
    <div class="finding medium">
        <h3>Orta</h3>
        <p>[Orta riskli bulguları buraya ekleyin]</p>
    </div>
    
    <div class="finding low">
        <h3>Düşük</h3>
        <p>[Düşük riskli bulguları buraya ekleyin]</p>
    </div>
    
    <h2>✅ Öneriler</h2>
    <div class="finding">
        <ul>
            <li>[Öneri 1]</li>
            <li>[Öneri 2]</li>
            <li>[Öneri 3]</li>
        </ul>
    </div>
    
    <h2>📎 Ekler</h2>
    <div class="finding">
        <p>Detaylı tarama sonuçları için output/ dizinine bakınız.</p>
    </div>
    
    <footer style="text-align: center; margin-top: 40px; color: #666;">
        <p>CyberKit ile oluşturuldu | {datetime.now().year}</p>
    </footer>
</body>
</html>"""
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print_success(f"HTML rapor oluşturuldu: {html_file}")
        input("\nPress Enter to continue...")

    def generate_markdown(self):
        clear_screen()
        print_banner("=== MARKDOWN RAPOR ===\n")
        
        project_name = get_input("Proje adı")
        
        timestamp = get_timestamp()
        md_file = f"{self.output_dir}/report_{project_name}_{timestamp}.md"
        
        md_content = f"""# 🔒 Güvenlik Değerlendirme Raporu

**Proje:** {project_name}  
**Tarih:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Oluşturan:** CyberKit

---

## 📊 Yürütücü Özeti

[Özet bilgileri buraya ekleyin]

---

## 🎯 Kapsam

| Target | Tip | Durum |
|-------|-----|-------|
| [IP/Domain] | [Web/Network] | [Tamamlandı] |

---

## ⚠️ Bulgular

### 🔴 Kritik Bulgular

| # | Bulgu | Etki | Öneri |
|---|-------|------|-------|
| 1 | [Açıklama] | [Etki] | [Öneri] |

### 🟠 Yüksek Riskli Bulgular

| # | Bulgu | Etki | Öneri |
|---|-------|------|-------|
| 1 | [Açıklama] | [Etki] | [Öneri] |

### 🟡 Orta Riskli Bulgular

| # | Bulgu | Etki | Öneri |
|---|-------|------|-------|
| 1 | [Açıklama] | [Etki] | [Öneri] |

### 🟢 Düşük Riskli Bulgular

| # | Bulgu | Etki | Öneri |
|---|-------|------|-------|
| 1 | [Açıklama] | [Etki] | [Öneri] |

---

## ✅ Öneriler

1. [Öneri 1]
2. [Öneri 2]
3. [Öneri 3]

---

## 📎 Ekler

- Nmap Scan Resultsı: `output/network/`
- Web Scan Resultsı: `output/web/`
- OSINT Resultsı: `output/osint/`

---

*CyberKit ile oluşturuldu*
"""
        
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print_success(f"Markdown rapor oluşturuldu: {md_file}")
        input("\nPress Enter to continue...")

    def list_reports(self):
        clear_screen()
        print_banner("=== MEVCUT RAPORLAR ===\n")
        
        if os.path.exists(self.output_dir):
            files = os.listdir(self.output_dir)
            if files:
                for f in files:
                    filepath = os.path.join(self.output_dir, f)
                    size = os.path.getsize(filepath)
                    print(f"  {Colors.CYAN}[+]{Colors.END} {f} ({size} bytes)")
            else:
                print_warning("Henüz rapor oluşturulmamış.")
        else:
            print_warning("Rapor dizini bulunamadı.")
        
        input("\nPress Enter to continue...")
