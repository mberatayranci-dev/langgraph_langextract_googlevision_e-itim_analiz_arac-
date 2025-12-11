"""
Egitim Dokumani Analiz Araci

PDF'lerden metin ve gorsel cikarip, LangExtract ve Gemini Vision
ile analiz eden, aralarindaki iliskileri bulan bir arac.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# proje kok dizinini ayarla
ROOT_DIR = Path(__file__).parent.parent
os.chdir(ROOT_DIR)
sys.path.insert(0, str(ROOT_DIR))

# .env yukle
load_dotenv()

from src.workflow import create_workflow


def main():
    print()
    print("Egitim Dokumani Analiz Araci")
    print("Metin: LangExtract | Gorsel: Gemini Vision | Workflow: LangGraph")
    print()
    
    # api key kontrol
    api_key = os.getenv("GOOGLE_API_KEY", "")
    if api_key:
        print(f"API Key: {api_key[:8]}...")
    else:
        print("UYARI: GOOGLE_API_KEY bulunamadi")
        print("       .env dosyasini kontrol edin")
    
    # workflow olustur ve calistir
    app = create_workflow()
    
    initial_state = {
        "konu": "Fizik ve Biyoloji"
    }
    
    result = app.invoke(initial_state)
    
    # ozet
    print()
    print("Bitti!")
    print()
    
    dosya_sayisi = len(result.get("dosyalar", []))
    gorsel_sayisi = len(result.get("gorseller", []))
    iliski_sayisi = len(result.get("iliskiler", []))
    
    print(f"Islenen dosya: {dosya_sayisi}")
    print(f"Cikartilan gorsel: {gorsel_sayisi}")
    print(f"Bulunan iliski: {iliski_sayisi}")
    print()
    print("Sonuclar output/ klasorunde")


if __name__ == "__main__":
    main()
