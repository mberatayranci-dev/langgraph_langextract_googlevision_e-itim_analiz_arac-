"""
Metin ve gorsel analiz sonuclari arasindaki iliskileri bulur
"""

from pathlib import Path


def iliski_bul(state: dict) -> dict:
    """
    Metin ve gorsel analizlerini karsilastirir, eslesen kavramlari bulur
    """
    print("\n[6/7] Metin-gorsel iliskileri bulunuyor")
    
    metin_sonuclari = state.get("metin_sonuclari", [])
    gorsel_sonuclari = state.get("gorsel_sonuclari", [])
    
    if not metin_sonuclari or not gorsel_sonuclari:
        print("  yeterli veri yok")
        return {"iliskiler": []}
    
    # metinlerden tum kavramlari topla
    metin_kavramlari = {}
    
    for sonuc in metin_sonuclari:
        dosya = sonuc.get("dosya", "")
        
        # kavramlar listesini al
        for kavram in sonuc.get("kavramlar", []):
            if kavram and len(kavram) > 2:
                key = kavram.lower().strip()
                if key not in metin_kavramlari:
                    metin_kavramlari[key] = {
                        "orijinal": kavram,
                        "dosya": dosya
                    }
        
        # formulleri de ekle
        for formul in sonuc.get("formuller", []):
            if formul:
                key = formul.lower().strip()
                metin_kavramlari[key] = {
                    "orijinal": formul,
                    "dosya": dosya,
                    "tip": "formul"
                }
        
        # kisileri de ekle
        for kisi in sonuc.get("kisiler", []):
            if kisi:
                key = kisi.lower().strip()
                metin_kavramlari[key] = {
                    "orijinal": kisi,
                    "dosya": dosya,
                    "tip": "kisi"
                }
    
    print(f"  metinden {len(metin_kavramlari)} kavram cikarildi")
    
    if not metin_kavramlari:
        print("  metin analizi bos, iliski kurulamiyor")
        return {"iliskiler": []}
    
    # eslestirmeleri bul
    iliskiler = []
    eslesen_gorseller = set()
    
    for gorsel in gorsel_sonuclari:
        gorsel_yolu = gorsel.get("gorsel", "")
        gorsel_kavramlari = gorsel.get("kavramlar", [])
        
        if not gorsel_kavramlari:
            continue
        
        for g_kavram in gorsel_kavramlari:
            if not g_kavram or len(g_kavram) < 2:
                continue
                
            g_key = g_kavram.lower().strip()
            
            # 1. tam eslesme
            if g_key in metin_kavramlari:
                iliskiler.append({
                    "metin_kavram": metin_kavramlari[g_key]["orijinal"],
                    "gorsel_kavram": g_kavram,
                    "gorsel": gorsel_yolu,
                    "sayfa": gorsel.get("sayfa", 0),
                    "esleme_tipi": "tam",
                    "guc": 1.0
                })
                eslesen_gorseller.add(gorsel_yolu)
                continue
            
            # 2. kismi eslesme (biri digerini iceriyor)
            for m_key, m_info in metin_kavramlari.items():
                if len(g_key) < 3 or len(m_key) < 3:
                    continue
                    
                if g_key in m_key or m_key in g_key:
                    iliskiler.append({
                        "metin_kavram": m_info["orijinal"],
                        "gorsel_kavram": g_kavram,
                        "gorsel": gorsel_yolu,
                        "sayfa": gorsel.get("sayfa", 0),
                        "esleme_tipi": "kismi",
                        "guc": 0.7
                    })
                    eslesen_gorseller.add(gorsel_yolu)
                    break
            
            # 3. kelime eslesmesi
            g_kelimeler = set(g_key.split())
            if len(g_kelimeler) < 1:
                continue
                
            for m_key, m_info in metin_kavramlari.items():
                m_kelimeler = set(m_key.split())
                ortak = g_kelimeler & m_kelimeler
                ortak = {k for k in ortak if len(k) > 3}
                
                if ortak:
                    iliskiler.append({
                        "metin_kavram": m_info["orijinal"],
                        "gorsel_kavram": g_kavram,
                        "gorsel": gorsel_yolu,
                        "sayfa": gorsel.get("sayfa", 0),
                        "esleme_tipi": "kelime",
                        "guc": 0.5
                    })
                    eslesen_gorseller.add(gorsel_yolu)
                    break
    
    # tekrarlari kaldir
    gorulen = set()
    benzersiz = []
    
    for ili in iliskiler:
        key = (ili["metin_kavram"].lower(), ili["gorsel"])
        if key not in gorulen:
            gorulen.add(key)
            benzersiz.append(ili)
    
    # gucu yuksek olanlari onde sirala
    benzersiz.sort(key=lambda x: x["guc"], reverse=True)
    
    print(f"  {len(benzersiz)} iliski bulundu ({len(eslesen_gorseller)} gorsel eslestirildi)")
    
    if benzersiz:
        print("  ornekler:")
        for ili in benzersiz[:3]:
            gorsel_adi = Path(ili["gorsel"]).name
            print(f"    {ili['metin_kavram']} <-> {gorsel_adi}")
    
    return {"iliskiler": benzersiz}