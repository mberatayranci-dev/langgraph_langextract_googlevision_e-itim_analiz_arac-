"""
PDF islemleri icin yardimci fonksiyonlar
"""

import os
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

try:
    import pdfplumber
except ImportError:
    pdfplumber = None


def pdf_metin_oku(pdf_yolu):
    """
    PDF dosyasindan metin cikarir
    
    pdfplumber kullaniyoruz, daha temiz sonuc veriyor
    PyMuPDF'e gore yavas ama layout'u daha iyi koruyor
    """
    if pdfplumber is None:
        print("pdfplumber yuklu degil")
        return ""
    
    metin = ""
    
    try:
        with pdfplumber.open(pdf_yolu) as pdf:
            for sayfa in pdf.pages:
                sayfa_metni = sayfa.extract_text()
                if sayfa_metni:
                    metin += sayfa_metni + "\n\n"
    except Exception as e:
        print(f"PDF okuma hatasi: {e}")
    
    return metin.strip()


def pdf_gorsel_cikar(pdf_yolu, cikti_klasoru):
    """
    PDF icindeki gorselleri cikarir
    
    PyMuPDF (fitz) kullaniyoruz, embedded resimleri
    cikarmak icin daha iyi
    
    Returns:
        list: cikarilan gorsel yollari ve metadata
    """
    if fitz is None:
        print("PyMuPDF yuklu degil")
        return []
    
    Path(cikti_klasoru).mkdir(parents=True, exist_ok=True)
    
    dosya_adi = Path(pdf_yolu).stem
    bulunan = []
    
    try:
        doc = fitz.open(pdf_yolu)
        
        for sayfa_no in range(len(doc)):
            sayfa = doc[sayfa_no]
            resimler = sayfa.get_images()
            
            for idx, resim in enumerate(resimler):
                try:
                    xref = resim[0]
                    pix = fitz.Pixmap(doc, xref)
                    
                    # CMYK kontrolu
                    if pix.n > 4:
                        pix = fitz.Pixmap(fitz.csRGB, pix)
                    
                    # cok kucukleri atla
                    if pix.width < 60 or pix.height < 60:
                        continue
                    
                    gorsel_adi = f"{dosya_adi}_s{sayfa_no + 1}_g{idx + 1}.png"
                    gorsel_yolu = os.path.join(cikti_klasoru, gorsel_adi)
                    pix.save(gorsel_yolu)
                    
                    bulunan.append({
                        "yol": gorsel_yolu,
                        "sayfa": sayfa_no + 1,
                        "boyut": f"{pix.width}x{pix.height}",
                        "kaynak": pdf_yolu
                    })
                    
                except Exception:
                    # bazi resimler cikarilmiyor, devam
                    pass
        
        doc.close()
        
    except Exception as e:
        print(f"Gorsel cikarma hatasi: {e}")
    
    return bulunan
