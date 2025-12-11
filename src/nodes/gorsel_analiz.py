"""
Gemini Vision ile gorsel analizi
"""

import os
import json
import time
from pathlib import Path

try:
    import google.generativeai as genai
except ImportError:
    genai = None


def gorsel_analiz(state: dict) -> dict:
    """
    Gemini Vision kullanarak gorselleri analiz eder
    """
    print("\n[5/7] Gorsel analizi (Gemini Vision)")
    
    gorseller = state.get("gorseller", [])
    
    if not gorseller:
        print("  analiz edilecek gorsel yok")
        return {"gorsel_sonuclari": []}
    
    if genai is None:
        print("  google-generativeai yuklu degil")
        return {"gorsel_sonuclari": []}
    
    api_key = os.getenv("GOOGLE_API_KEY", "")
    if not api_key:
        print("  API key bulunamadi")
        return {"gorsel_sonuclari": []}
    
    genai.configure(api_key=api_key)
    
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
    except Exception as e:
        print(f"  model yuklenemedi: {e}")
        return {"gorsel_sonuclari": []}
    
    # cok fazla gorsel varsa sinirla
    MAX_GORSEL = 12
    islenecek = gorseller[:MAX_GORSEL]
    
    if len(gorseller) > MAX_GORSEL:
        print(f"  (ilk {MAX_GORSEL} gorsel isleniyor)")
    
    sonuclar = []
    
    for i, gorsel in enumerate(islenecek):
        gorsel_yolu = gorsel["yol"]
        gorsel_adi = Path(gorsel_yolu).name
        sayfa = gorsel.get("sayfa", 0)
        
        print(f"  {gorsel_adi}...", end=" ")
        
        try:
            with open(gorsel_yolu, "rb") as f:
                gorsel_bytes = f.read()
            
            prompt = """
            Bu bir egitim materyalinden alinmis gorsel.
            JSON formatinda analiz et:
            {"tur": "diyagram/tablo/grafik/sema/formul/sekil", "kavramlar": ["kavram1", "kavram2"], "aciklama": "kisa aciklama"}
            Sadece JSON yaz.
            """
            
            cevap = model.generate_content([
                prompt,
                {"mime_type": "image/png", "data": gorsel_bytes}
            ])
            
            cevap_metni = cevap.text.strip()
            
            # json parse
            if "{" in cevap_metni:
                json_str = cevap_metni[cevap_metni.find("{"):cevap_metni.rfind("}") + 1]
                analiz = json.loads(json_str)
            else:
                analiz = {"tur": "belirsiz", "kavramlar": [], "aciklama": ""}
            
            sonuclar.append({
                "gorsel": gorsel_yolu,
                "sayfa": sayfa,
                "kaynak": gorsel.get("kaynak", ""),
                "tur": analiz.get("tur", "belirsiz"),
                "kavramlar": analiz.get("kavramlar", []),
                "aciklama": analiz.get("aciklama", "")
            })
            
            print(f"{analiz.get('tur', '?')}, {len(analiz.get('kavramlar', []))} kavram")
            
            # rate limit icin bekle
            if i < len(islenecek) - 1:
                time.sleep(1.5)
            
        except Exception as e:
            hata_mesaj = str(e)
            if "429" in hata_mesaj:
                print("rate limit, bekleniyor...")
                time.sleep(5)
            else:
                print(f"hata: {hata_mesaj[:50]}")
            
            sonuclar.append({
                "gorsel": gorsel_yolu,
                "sayfa": sayfa,
                "tur": "hata",
                "kavramlar": [],
                "aciklama": hata_mesaj[:100]
            })
    
    return {"gorsel_sonuclari": sonuclar}
