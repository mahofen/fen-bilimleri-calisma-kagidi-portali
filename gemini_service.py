import os
import json
import re
import random
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

# .env dosyasını mutlak yol ile garanti yükle
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(dotenv_path=env_path, override=True)

class GeminiAssessmentService:
    def __init__(self):
        # Tekrar kontrol et
        if not os.getenv("GEMINI_API_KEY"):
            load_dotenv(dotenv_path=env_path, override=True)
        
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY bulunamadı! Lütfen .env dosyanızı kontrol edin.")
        self.client = genai.Client(api_key=self.api_key)
        # Aktif ve yüksek kotalı güncel Flash modelleri
        self.models = [
            "gemini-3.5-flash",
            "gemini-3.5-flash-lite",
            "gemini-3.7-flash",
            "gemini-3.8-flash",
            "gemini-flash-latest",
            "gemini-3.1-flash-lite"
        ]

    def generate_assessment(
        self,
        grade_level: str,
        subject: str,
        learning_area: str,
        learning_outcome: str,
        assessment_tool: str = "A4 Pedagojik Çalışma Kâğıdı",
        difficulty: str = "Orta",
        question_count: int = 1,
        custom_context: str = "",
        template_style: str = "random"
    ) -> dict:
        """
        Antigravity Fen Bilimleri Çalışma Kâğıdı Yapı Standardizasyonu Şartnamesine
        ve 6 modüllü MEB TYMM görsel şablon mimarisine (1. Bağlam, 2. Veriyi İncele, 
        3. Keşfet, 4. Açıkla ve Kanıtla, 5. Araştır, 6. Çözüm Üret) tam uyumlu olarak
        yapılandırılmış JSON formatında materyal üretir.
        """
        system_instruction = """
Sen Millî Eğitim Bakanlığı (MEB) Türkiye Yüzyılı Maarif Modeli (TYMM) 'Antigravity Fen Bilimleri Çalışma Kâğıdı Yapı Standardizasyonu' şartnamesine göre çalışan Başuzman Eğitim Tasarımcısısın.

GÖREVİN VE KESİN KURALLARIN:
1. PEDAGOJİK OMURGA & 6 MODÜLLÜ ŞABLON MİMARİSİ:
   Çalışma kâğıdı tam olarak aşağıdaki 6 ardışık pedagojik bölümü içerecektir:
   - 1. BÖLÜM: 🔴 BAĞLAM (Günlük yaşam, deney veya problem hikâyesi)
   - 2. BÖLÜM: 🔵 VERİYİ İNCELE (Deney tablosu, ölçüm verileri veya gözlem seti)
   - 3. BÖLÜM: 🟢 KEŞFET (Veri tablosuna ve metne dayalı 2 adet açık uçlu keşif sorusu)
   - 4. BÖLÜM: 🟠 AÇIKLA ve KANITLA (1: Bilimsel Açıklama Sorusu, 2: Kanıt ve Gerekçe Sorusu)
   - 5. BÖLÜM: 🟣 ARAŞTIR (Araştırma yönergesi / sorusu ve öğrencilerin şema/çizim yapabileceği deney alanı)
   - 6. BÖLÜM: 🟢 ÇÖZÜM ÜRET (Öğrenilen fen ilkesinin günlük yaşamdaki bir probleme aktarılması ve transfer çözümü)

2. ÖĞRENCİ VE ÖĞRETMEN ALANI AYRIMI:
   Öğrenci Çalışma Kâğıdı (studentWorksheet) içinde KESİNLİKLE kazanım kodu (FB.5.X.X), süreç bileşeni, bilişsel düzey, cevap anahtarı, rubrik veya öğretmen notu YER ALAMAZ. Bu teknik bilgiler SADECE Öğretmen Rehberi (teacherGuide) bölümünde yer alacaktır.

3. 5. SINIF DİL DÜZEYİ VE SORU KÖKÜ YAZIM KURALLARI:
   - 5. sınıf öğrencisinin dil ve okuma düzeyine tam uygun, duru, akıcı ve sade bir Türkçe kullan.
   - Uzun, karmaşık, iç içe geçmiş cümlelerden kaçın.
   - Her soru kökünde tek temel işlem iste.
   - Noktalı cevap alanlarında ('answerSpace') öğrencilerin rahat yazması için en az 2 tam satır noktalı boşluk sağla.

JSON ŞEMASI VE SABİT İSKELET YAPISI:
{
  "studentWorksheet": {
    "header": {
      "title": "FEN BİLİMLERİ DERSİ ÇALIŞMA KÂĞIDI",
      "subject": "Fen Bilimleri",
      "grade": "5. Sınıf",
      "unit": "Ünite Adı",
      "topic": "Konu Başlığı",
      "duration": "40 Dakika",
      "totalScore": 100
    },
    "context": {
      "sectionNumber": 1,
      "title": "1. BAĞLAM",
      "subtitle": "Gerçek Yaşam ve Deney Senaryosu",
      "text": "100-150 kelimelik, günlük yaşam veya fen deneyiyle doğrudan ilişkili, soru çözümünü zorunlu kılan duru metin."
    },
    "dataSet": {
      "sectionNumber": 2,
      "type": "table",
      "title": "2. VERİYİ İNCELE",
      "description": "Deney ölçüm tablosunu inceleyiniz.",
      "headers": ["Deney No", "Değişken 1 (Birim)", "Değişken 2 (Birim)", "Ölçülen Sonuç (Birim)"],
      "rows": [
        ["1", "Değer A", "Değer B", "Sonuç X"],
        ["2", "Değer C", "Değer D", "Sonuç Y"],
        ["3", "Değer E", "Değer F", "Sonuç Z"]
      ]
    },
    "exploreSection": {
      "sectionNumber": 3,
      "title": "3. KEŞFET",
      "tasks": [
        {
          "taskNumber": "1",
          "question": "Tablodaki verilere göre ilk durum ile son durum arasındaki temel farkı belirtiniz.",
          "answerSpace": "Cevabım:\n........................................................................................................................\n........................................................................................................................"
        },
        {
          "taskNumber": "2",
          "question": "Ölçülen sonuçlara göre değişkenler arasındaki ilişkiyi açıklayınız.",
          "answerSpace": "Cevabım:\n........................................................................................................................\n........................................................................................................................"
        }
      ]
    },
    "explainSection": {
      "sectionNumber": 4,
      "title": "4. AÇIKLA ve KANITLA",
      "tasks": [
        {
          "taskNumber": "1",
          "type": "aciklama",
          "title": "1. Bilimsel Açıklamam",
          "question": "Deneyde gözlemlenen durumun bilimsel nedenini açıklayınız.",
          "answerSpace": "Açıklamam:\n........................................................................................................................\n........................................................................................................................"
        },
        {
          "taskNumber": "2",
          "type": "kanit",
          "title": "2. Kanıtım ve Gerekçem",
          "question": "Açıklamanızı tablodaki hangi somut veriye dayandırarak kanıtlarsınız?",
          "answerSpace": "Kanıtım ve Gerekçem:\n........................................................................................................................\n........................................................................................................................"
        }
      ]
    },
    "researchSection": {
      "sectionNumber": 5,
      "title": "5. ARAŞTIR",
      "question": "Bu deneyi farklı bir ortamda veya yeni bir değişkenle tekrarlamak isteseydiniz nasıl bir düzenek kurardınız? Tasarımınızı açıklayıp çiziniz.",
      "answerSpace": "Araştırma Tasarımım:\n........................................................................................................................\n........................................................................................................................",
      "drawingBoxLabel": "Deney Düzeneği / Model Çizim Alanı"
    },
    "solutionSection": {
      "sectionNumber": 6,
      "title": "6. ÇÖZÜM ÜRET",
      "question": "Öğrendiğiniz fen prensibini kullanarak günlük yaşamda karşılaşılan bir soruna yönelik yenilikçi bir çözüm önerisi yazınız.",
      "answerSpace": "Çözüm Önerim ve Bilimsel Gerekçem:\n........................................................................................................................\n........................................................................................................................\n........................................................................................................................"
    }
  },
  "teacherGuide": {
    "learningOutcome": "FB.5.X.X. Kazanım tam metni",
    "processComponents": [
      "a) Verileri analiz edebilme ve örüntü keşfedebilme",
      "b) Kanıta dayalı bilimsel açıklama ve gerekçelendirme yapabilme",
      "c) Bilimsel bilgiyi günlük yaşam problemlerine transfer edebilme"
    ],
    "cognitiveLevel": "Bilişsel Düzey (Uygulama / Analiz / Değerlendirme)",
    "measuredSkills": ["Tümevarımsal Akıl Yürütme", "Veri Okuryazarlığı", "Bilimsel Sorgulama", "Model Oluşturma", "Problem Çözme"],
    "answerKey": [
      {
        "section": "3. Keşfet - Soru 1",
        "expectedAnswer": "Beklenen doğru cevap ve kavram",
        "scientificExplanation": "Kavramsal açıklama"
      },
      {
        "section": "3. Keşfet - Soru 2",
        "expectedAnswer": "Beklenen ilişki ve çıkarım",
        "scientificExplanation": "Veri temelli gerekçe"
      },
      {
        "section": "4. Açıkla ve Kanıtla - Açıklama",
        "expectedAnswer": "Doğru bilimsel açıklama",
        "scientificExplanation": "Bilimsel prensip"
      },
      {
        "section": "4. Açıkla ve Kanıtla - Kanıt",
        "expectedAnswer": "Tablodaki veriye dayalı kanıt",
        "scientificExplanation": "Veri göstergesi"
      },
      {
        "section": "5. Araştır",
        "expectedAnswer": "Geçerli araştırma hipotezi ve modelleme",
        "scientificExplanation": "Değişken kontrolü"
      },
      {
        "section": "6. Çözüm Üret",
        "expectedAnswer": "Uygulanabilir fen tabanlı çözüm önerisi",
        "scientificExplanation": "Günlük yaşama transfer ve bilimsel gerekçe"
      }
    ],
    "rubric": {
      "criteria": [
        {
          "criterion": "Veri İnceleme & Keşfetme (3. Bölüm)",
          "needsImprovement": "Verileri eksik veya yanlış yorumlar (0-5 P)",
          "acceptable": "Veriler arasındaki ilişkiyi kısmen kurar (10 P)",
          "proficient": "Veri örüntüsünü eksiksiz ve doğru açıklar (15 P)"
        },
        {
          "criterion": "Bilimsel Açıklama ve Kanıtlama (4. Bölüm)",
          "needsImprovement": "Açıklamasını veriyle destekleyemez (0-10 P)",
          "acceptable": "Doğru açıklar ancak kanıtı yetersizdir (15 P)",
          "proficient": "Tablodaki verilerle eksiksiz ve güçlü kanıt sunar (25 P)"
        },
        {
          "criterion": "Araştırma ve Modelleme (5. Bölüm)",
          "needsImprovement": "Araştırma tasarımı oluşturamaz (0-5 P)",
          "acceptable": "Basit bir düzenek tasarlar ancak değişkenleri netleştirmez (10 P)",
          "proficient": "Değişkenleri kontrollü, özgün ve net bir araştırma tasarlar/çizer (20 P)"
        },
        {
          "criterion": "Günlük Yaşama Transfer & Çözüm Üretme (6. Bölüm)",
          "needsImprovement": "Problemle fen kavramı arasında bağ kuramaz (0-5 P)",
          "acceptable": "Çözüm önerir fakat bilimsel temelini zayıf bırakır (15 P)",
          "proficient": "Fen ilkesini kullanarak uygulanabilir ve özgün çözüm üretir (25 P)"
        }
      ]
    },
    "teacherNote": "Öğretmen için uygulama, yaygın kavram yanılgıları ve süre önerisi notu."
  }
}

ÇIKTI KURALI:
Yalnızca ve yalnızca yukarıdaki JSON formatında çıktı ver. Markdown kod bloğu (```json ... ```) veya saf JSON formatında yaz. JSON dışında hiçbir selamlama veya açıklama yazma.
"""

        custom_context_instruction = ""
        if custom_context and custom_context.strip():
            custom_context_instruction = f"""
ÖNEMLİ - KULLANICININ ÖZEL BAĞLAM VE SENARYO İSTEĞİ:
"{custom_context.strip()}"

DİKKAT: 1. Bağlam metnini (`context.text`), 2. Veri tablosunu (`dataSet`), 3. Keşfet, 4. Açıkla-Kanıtla, 5. Araştır ve 6. Çözüm Üret görevlerini KESİNLİKLE kullanıcının bu özel isteğine, karakterlerine, mekanına veya hikayesine tam olarak uyarlayarak kurgula. Ancak öğrenme çıktısının bilimsel derinliğini ve 6 bölümlü şablon iskeletini eksiksiz koru.
"""

        prompt = f"""
Aşağıdaki parametrelere göre 6 Modüllü MEB TYMM Şablon formatında tam bir çalışma kâğıdı üret:

- Sınıf Seviyesi: {grade_level}
- Ders: {subject}
- Öğrenme Alanı / Ünite: {learning_area}
- Öğrenme Çıktısı: {learning_outcome}
- Zorluk Seviyesi: {difficulty}
{custom_context_instruction}

Lütfen 6 modüllü şablon iskeletini bozmadan, öğrenci ve öğretmen bölümlerini eksiksiz içeren JSON nesnesini döndür.
"""

        # Rastgele şablon stili belirle (1: Klasik TYMM, 2: Pastel Minimal, 3: Teknoloji & Bilim, 4: Doodle / Fırça)
        if template_style == "random" or not template_style:
            chosen_template_id = random.choice([1, 2, 3, 4])
        else:
            try:
                chosen_template_id = int(template_style)
            except ValueError:
                chosen_template_id = random.choice([1, 2, 3, 4])

        last_error = ""
        for model in self.models:
            try:
                response = self.client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.7,
                        response_mime_type="application/json"
                    )
                )
                if response and response.text:
                    raw_text = response.text.strip()
                    # Markdown json bloğunu temizle
                    if raw_text.startswith("```"):
                        raw_text = re.sub(r"^```(?:json)?\n?", "", raw_text)
                        raw_text = re.sub(r"\n?```$", "", raw_text)

                    # JSON nesnesini sınırlarından ayıkla
                    json_match = re.search(r"\{[\s\S]*\}", raw_text)
                    if json_match:
                        raw_text = json_match.group(0)
                    
                    try:
                        data = json.loads(raw_text, strict=False)
                    except json.JSONDecodeError:
                        clean_text = re.sub(r"[\x00-\x1f\x7f-\x9f]", " ", raw_text)
                        data = json.loads(clean_text, strict=False)

                    if isinstance(data, dict):
                        data["templateStyleId"] = chosen_template_id

                    return data
            except Exception as e:
                error_msg = str(e)
                last_error = error_msg
                continue

        return {"error": f"Gemini API Çağrısı Sırasında Hata Oluştu: {last_error}"}

if __name__ == "__main__":
    service = GeminiAssessmentService()
    print("Service initialized with 6-Module Template Schema.")
