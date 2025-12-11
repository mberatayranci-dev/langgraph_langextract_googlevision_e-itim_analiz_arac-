"""
Sonuclari JSON olarak kaydeder
"""

import json
from pathlib import Path


def kaydet(state: dict) -> dict:
    """
    Tum analiz sonuclarini JSON dosyalarina kaydeder
    """
    print("\n[7/7] Sonuclar kaydediliyor")
    
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # metin analizi
    metin_sonuclari = state.get("metin_sonuclari", [])
    with open(output_dir / "metin_analizi.json", "w", encoding="utf-8") as f:
        json.dump(metin_sonuclari, f, ensure_ascii=False, indent=2)
    
    # gorsel analizi
    gorsel_sonuclari = state.get("gorsel_sonuclari", [])
    with open(output_dir / "gorsel_analizi.json", "w", encoding="utf-8") as f:
        json.dump(gorsel_sonuclari, f, ensure_ascii=False, indent=2)
    
    # iliskiler
    iliskiler = state.get("iliskiler", [])
    with open(output_dir / "iliskiler.json", "w", encoding="utf-8") as f:
        json.dump(iliskiler, f, ensure_ascii=False, indent=2)
    
    # ozet
    ozet = {
        "dosya_sayisi": len(state.get("dosyalar", [])),
        "metin_sayisi": len(state.get("metinler", [])),
        "gorsel_sayisi": len(state.get("gorseller", [])),
        "kavram_sayisi": sum(len(s.get("kavramlar", [])) for s in metin_sonuclari),
        "iliski_sayisi": len(iliskiler)
    }
    
    with open(output_dir / "ozet.json", "w", encoding="utf-8") as f:
        json.dump(ozet, f, ensure_ascii=False, indent=2)
    
    print("  output/ klasorune kaydedildi")
    
    return {}
