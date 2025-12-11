"""
LangExtract ile metin analizi
"""

import os
from pathlib import Path

try:
    import langextract as lx
except ImportError:
    lx = None


def metin_analiz(state: dict) -> dict:
    """
    LangExtract kullanarak metinlerden kavram, formul ve kisi cikarir
    """
    print("\n[4/7] Metin analizi (LangExtract)")
    
    metinler = state.get("metinler", [])
    konu = state.get("konu", "egitim icerigi")
    
    if not metinler:
        print("  analiz edilecek metin yok")
        return {"metin_sonuclari": []}
    
    if lx is None:
        print("  langextract yuklu degil, atlaniyor")
        return {"metin_sonuclari": []}
    
    api_key = os.getenv("GOOGLE_API_KEY", "")
    if not api_key:
        print("  API key bulunamadi, atlaniyor")
        return {"metin_sonuclari": []}
    
    # ornek veri
    ornek = lx.data.ExampleData(
        text="Newton'un ikinci yasasi F=ma formuluyle ifade edilir. Isaac Newton bu yasayi 1687'de yayinladi.",
        extractions=[
            lx.data.Extraction(
                extraction_class="kavram",
                extraction_text="Newton'un ikinci yasasi",
                attributes={"tur": "fizik yasasi"}
            ),
            lx.data.Extraction(
                extraction_class="formul",
                extraction_text="F=ma",
                attributes={"aciklama": "kuvvet = kutle x ivme"}
            ),
            lx.data.Extraction(
                extraction_class="kisi",
                extraction_text="Isaac Newton",
                attributes={"katki": "hareket yasalari"}
            ),
        ]
    )
    
    sonuclar = []
    
    for metin_obj in metinler:
        dosya = metin_obj["dosya"]
        icerik = metin_obj["icerik"]
        dosya_adi = Path(dosya).name
        
        # metin cok uzunsa kisalt
        MAX_UZUNLUK = 10000
        if len(icerik) > MAX_UZUNLUK:
            icerik = icerik[:MAX_UZUNLUK]
        
        try:
            sonuc = lx.extract(
                text_or_documents=icerik,
                prompt_description=f"""
                Bu bir {konu} dokumani.
                Cikarilacak bilgiler:
                - kavram: onemli terim ve kavramlar
                - formul: matematiksel ifadeler  
                - kisi: bilim insanlari
                Her entity icin extraction_class ve extraction_text belirt.
                """,
                examples=[ornek],
                model_id="gemini-2.0-flash",
                api_key=api_key
            )
            
            cikarilan = {
                "kavramlar": [],
                "formuller": [],
                "kisiler": []
            }
            
            # sonuc bir liste (AnnotatedDocument listesi)
            if isinstance(sonuc, list):
                for doc in sonuc:
                    if hasattr(doc, "extractions"):
                        for ext in doc.extractions:
                            sinif = getattr(ext, "extraction_class", "").lower()
                            metin = getattr(ext, "extraction_text", "")
                            
                            if not metin:
                                continue
                            
                            if "formul" in sinif or "=" in metin:
                                cikarilan["formuller"].append(metin)
                            elif "kisi" in sinif or "person" in sinif:
                                cikarilan["kisiler"].append(metin)
                            else:
                                cikarilan["kavramlar"].append(metin)
            
            # sonuc tek bir AnnotatedDocument olabilir
            elif hasattr(sonuc, "extractions"):
                for ext in sonuc.extractions:
                    sinif = getattr(ext, "extraction_class", "").lower()
                    metin = getattr(ext, "extraction_text", "")
                    
                    if not metin:
                        continue
                    
                    if "formul" in sinif or "=" in metin:
                        cikarilan["formuller"].append(metin)
                    elif "kisi" in sinif or "person" in sinif:
                        cikarilan["kisiler"].append(metin)
                    else:
                        cikarilan["kavramlar"].append(metin)
            
            # tekrarlari kaldir
            cikarilan["kavramlar"] = list(set(cikarilan["kavramlar"]))
            cikarilan["formuller"] = list(set(cikarilan["formuller"]))
            cikarilan["kisiler"] = list(set(cikarilan["kisiler"]))
            
            sonuclar.append({
                "dosya": dosya,
                "kavramlar": cikarilan["kavramlar"],
                "formuller": cikarilan["formuller"],
                "kisiler": cikarilan["kisiler"]
            })
            
            print(f"  {dosya_adi}: {len(cikarilan['kavramlar'])} kavram, {len(cikarilan['formuller'])} formul")
            
        except Exception as e:
            print(f"  {dosya_adi}: hata - {str(e)[:50]}")
            sonuclar.append({
                "dosya": dosya,
                "kavramlar": [],
                "formuller": [],
                "kisiler": [],
                "hata": str(e)
            })
    
    return {"metin_sonuclari": sonuclar}