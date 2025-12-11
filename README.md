# Eğitim Dokümanı Analiz Aracı

PDF formatındaki eğitim materyallerinden metin ve görsel çıkarıp, bunları analiz eden ve aralarındaki ilişkileri bulan araç

## Özellikler

- PDF'lerden metin çıkarma
- PDF'lerden görsel çıkarma (diyagram, şema, tablo vb.)
- LangExtract ile metin analizi (kavram, formül, kişi çıkarma)
- Gemini Vision ile görsel analizi
- Metin-görsel ilişki eşleştirme(tam, kısmi ve kelime eşleme olarak 3 kategoride eşleme arar)
- LangGraph tabanlı workflow yönetimi

## Kullanım

```bash
# PDF'leri data/pdfs klasörüne koyun
python src/main.py
```

Sonuçlar `output/` klasöründe oluşturulur.


## Workflow

```
START
  ↓
dosya_tara      → PDF'leri bul
  ↓
metin_cikar     → PDF'lerden metin çıkar
  ↓
gorsel_cikar    → PDF'lerden görsel çıkar
  ↓
metin_analiz    → LangExtract ile kavram çıkar
  ↓
gorsel_analiz   → Gemini Vision ile görsel analiz
  ↓
iliski_bul      → Metin-görsel eşleştirme
  ↓
kaydet          → JSON çıktıları oluştur
  ↓
END
```
## Gereksinimler

- Python 
- Google API Key 

## Lisans

MIT
