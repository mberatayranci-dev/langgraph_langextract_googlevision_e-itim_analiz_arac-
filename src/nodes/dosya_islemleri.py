"""
Dosya tarama, metin ve gorsel cikarma adimlari
"""

from pathlib import Path
from ..utils import pdf_metin_oku, pdf_gorsel_cikar


def dosya_tara(state: dict) -> dict:
    """
    data/pdfs klasorundeki PDF dosyalarini bulur
    """
    print("\n[1/7] Dosyalar taraniyor")
    
    pdf_klasoru = Path("data/pdfs")
    
    if not pdf_klasoru.exists():
        pdf_klasoru.mkdir(parents=True)
        print("  pdfs klasoru olusturuldu, PDF ekleyip tekrar calistir")
        return {"dosyalar": []}
    
    dosyalar = list(pdf_klasoru.glob("*.pdf"))
    
    print(f"  {len(dosyalar)} PDF bulundu")
    for d in dosyalar:
        print(f"  - {d.name}")
    
    return {"dosyalar": [str(d) for d in dosyalar]}


def metin_cikar(state: dict) -> dict:
    """
    PDF'lerden metin cikarir
    """
    print("\n[2/7] Metinler cikariliyor")
    
    dosyalar = state.get("dosyalar", [])
    metinler = []
    
    for dosya in dosyalar:
        dosya_adi = Path(dosya).name
        metin = pdf_metin_oku(dosya)
        
        if metin:
            metinler.append({
                "dosya": dosya,
                "icerik": metin,
                "uzunluk": len(metin)
            })
            print(f"  {dosya_adi}: {len(metin)} karakter")
        else:
            print(f"  {dosya_adi}: okunamadi")
    
    return {"metinler": metinler}


def gorsel_cikar(state: dict) -> dict:
    """
    PDF'lerden gorselleri cikarir
    """
    print("\n[3/7] Gorseller cikariliyor")
    
    dosyalar = state.get("dosyalar", [])
    tum_gorseller = []
    
    cikti_klasoru = "output/images"
    
    for dosya in dosyalar:
        dosya_adi = Path(dosya).name
        gorseller = pdf_gorsel_cikar(dosya, cikti_klasoru)
        tum_gorseller.extend(gorseller)
        print(f"  {dosya_adi}: {len(gorseller)} gorsel")
    
    print(f"  toplam {len(tum_gorseller)} gorsel cikarildi")
    
    return {"gorseller": tum_gorseller}
