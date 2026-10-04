import json
from gemini_service import GeminiAssessmentService

service = GeminiAssessmentService()

print("--- STANDARDIZASYON TESTİ BAŞLATILIYOR ---")
result = service.generate_assessment(
    grade_level="5. Sınıf",
    subject="Fen Bilimleri",
    learning_area="2. ÜNİTE: KUVVETİ TANIYALIM",
    learning_outcome="FB.5.2.4. Sürtünme kuvvetinin çeşitli ortamlardaki etkilerine yönelik tümevarımsal akıl yürütebilme",
    difficulty="Orta"
)

# Test 1: JSON Geçerliliği
assert isinstance(result, dict), "Hata: Sonuç bir JSON nesnesi değil!"
assert "studentWorksheet" in result, "Hata: 'studentWorksheet' anahtarı bulunamadı!"
assert "teacherGuide" in result, "Hata: 'teacherGuide' anahtarı bulunamadı!"

sw = result["studentWorksheet"]
tg = result["teacherGuide"]

# Test 2: Öğrenci Tarafı İskelet Kontrolü
assert "header" in sw, "Hata: Öğrenci başlığı eksik!"
assert "context" in sw, "Hata: Bağlam eksik!"
assert "dataSet" in sw, "Hata: Veri tablosu eksik!"
assert "sections" in sw, "Hata: Bölümler eksik!"
assert len(sw["sections"]) >= 5, f"Hata: En az 5 bölüm olmalı, ancak {len(sw['sections'])} bölüm üretildi!"
assert "reflection" in sw, "Hata: Yansıtma/öz değerlendirme eksik!"

# Test 3: Öğretmen Tarafı Rubrik ve Cevap Kontrolü
assert "answerKey" in tg, "Hata: Cevap anahtarı eksik!"
assert "rubric" in tg, "Hata: Rubrik eksik!"

print("\n[OK] TUM STANDART KONTROLLER BASARIYLA GECTI!")
print(f"Baslik: {sw['header']['title']}")
print(f"Baglam: {sw['context']['title']}")
print(f"Gorev Sayisi: {len(sw['sections'])} Bolum")
print(f"Cevap Anahtari: {len(tg['answerKey'])} Gorev Cevabi")
print(f"Rubrik Kriterleri: {len(tg['rubric']['criteria'])} Olcut")
