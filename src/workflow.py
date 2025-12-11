"""
LangGraph workflow tanimi
"""

from typing import TypedDict, List, Any
from langgraph.graph import StateGraph, START, END

from .nodes import (
    dosya_tara,
    metin_cikar,
    gorsel_cikar,
    metin_analiz,
    gorsel_analiz,
    iliski_bul,
    kaydet
)


class AnalysisState(TypedDict, total=False):
    """
    Workflow boyunca tasinan state
    """
    konu: str
    dosyalar: List[str]
    metinler: List[dict]
    gorseller: List[dict]
    metin_sonuclari: List[dict]
    gorsel_sonuclari: List[dict]
    iliskiler: List[dict]


def create_workflow():
    """
    Analiz workflow'unu olusturur
    
    Akis:
    dosya_tara -> metin_cikar -> gorsel_cikar -> metin_analiz 
               -> gorsel_analiz -> iliski_bul -> kaydet
    """
    
    wf = StateGraph(AnalysisState)
    
    # node'lari ekle
    wf.add_node("dosya_tara", dosya_tara)
    wf.add_node("metin_cikar", metin_cikar)
    wf.add_node("gorsel_cikar", gorsel_cikar)
    wf.add_node("metin_analiz", metin_analiz)
    wf.add_node("gorsel_analiz", gorsel_analiz)
    wf.add_node("iliski_bul", iliski_bul)
    wf.add_node("kaydet", kaydet)
    
    # baglantilari ekle
    wf.add_edge(START, "dosya_tara")
    wf.add_edge("dosya_tara", "metin_cikar")
    wf.add_edge("metin_cikar", "gorsel_cikar")
    wf.add_edge("gorsel_cikar", "metin_analiz")
    wf.add_edge("metin_analiz", "gorsel_analiz")
    wf.add_edge("gorsel_analiz", "iliski_bul")
    wf.add_edge("iliski_bul", "kaydet")
    wf.add_edge("kaydet", END)
    
    return wf.compile()
