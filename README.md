# 🧪 Fen Bilimleri Bağlam Temelli Öğretim ve Etkinlik Portalı
### 🇹🇷 Millî Eğitim Bakanlığı (MEB) Türkiye Yüzyılı Maarif Modeli (TYMM) Uyumlu

Bu proje, **MEB Türkiye Yüzyılı Maarif Modeli (TYMM)** fen bilimleri öğretim programına ve pedagojik omurgasına tam uyumlu, 6 modüllü görsel şablonlara sahip, yapay zekâ (Gemini 2.5/3.x) destekli **A4 Çalışma Kâğıdı ve Öğretmen Ölçme-Değerlendirme Rehberi Üretim Sistemidir**.

---

## 🌟 Öne Çıkan Özellikler

- **🏛️ 6 Modüllü Pedagojik Omurga:**
  1. 🔴 **Bağlam:** Günlük yaşam / fen deneyi olay ve problem hikâyesi
  2. 🔵 **Veriyi İncele:** Deney tablosu, ölçüm değişkenleri ve gözlem seti
  3. 🟢 **Keşfet:** Veri setine ve metne dayalı açık uçlu keşif soruları
  4. 🟠 **Açıkla ve Kanıtla:** Bilimsel açıklama ve kanıta dayalı gerekçelendirme
  5. 🟣 **Araştır:** Araştırma yönergesi ve öğrenciler için kesikli çizgili **Deney / Model Çizim Alanı**
  6. 🟢 **Çözüm Üret:** Fen ilkesini günlük yaşam problemine aktarma ve özgün transfer çözümü
- **🎨 4 Farklı Görsel Tasarım Şablonu:**
  - **Şablon 1:** Klasik Canlı TYMM Renkleri
  - **Şablon 2:** Pastel Minimalist ve Modern
  - **Şablon 3:** Biyo-Teknoloji & Bilimsel Gradyan
  - **Şablon 4:** Eğlenceli Çizim & Fırça (Doodle) Tarzı
  - *(Rastgele seçim veya tek tıkla canlı şablon değiştirme desteği)*
- **✨ Özel Bağlam & Senaryo İsteği:** Öğretmenlerin istedikleri özel mekan, karakter veya deney senaryosunu (örn: Uzay istasyonu, lunapark, kış sporları) belirtebilmesi için açılır akıllı form.
- **✏️ Canlı Doğrudan Düzenleme (Inline Editing):** Çalışma kâğıdındaki tüm metinler tıklanarak anında değiştirilebilir, yeni bölümler/sorular eklenebilir veya silinebilir.
- **💾 JSON Dışa / İçe Aktarma:** Hazırlanan çalışma kâğıtlarını JSON olarak kaydetme ve daha sonra tekrar yükleyip düzenleme imkânı.
- **🖨️ A4 Baskı Standartları:** Düzenleme butonları baskıda otomatik gizlenir, tertemiz 2 sayfalık (1. Sayfa Öğrenci Kâğıdı, 2. Sayfa Öğretmen Rehberi & Rubrik) çıktı alınır.

---

## 🚀 Kurulum ve Çalıştırma

### 1. Projeyi Klonlayın
```bash
git clone https://github.com/mahofen/fen-bilimleri-calisma-kagidi-portali.git
cd fen-bilimleri-calisma-kagidi-portali
```

### 2. Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### 3. Çevre Değişkenlerini Ayarlayın
`.env.example` dosyasını `.env` olarak kopyalayın ve Gemini API anahtarınızı ekleyin:
```env
GEMINI_API_KEY=your_gemini_api_key_here
PORT=5000
```

### 4. Sunucuyu Başlatın
```bash
python app.py
```
Tarayıcınızda `http://localhost:5000` adresine giderek kullanmaya başlayabilirsiniz!

---

## 📁 Proje Yapısı
```
├── app.py                      # Flask backend API sunucusu
├── gemini_service.py           # Gemini AI entegrasyonu ve pedagojik motor
├── curriculum_data.py          # 5. Sınıf MEB TYMM müfredat ve kazanım verisi
├── templates/
│   └── index.html              # 6 modüllü, 4 şablon temalı interaktif web arayüzü
├── fen_bilimleri_portali.html  # Bağımsız statik şablon önizleme dosyası
├── ŞABLON/                     # Orijinal görsel şablon referansları (1.png - 4.png)
└── requirements.txt            # Gerekli Python kütüphaneleri
```

---

## 📜 Lisans
Bu proje eğitim amaçlı geliştirilmiştir. MEB Türkiye Yüzyılı Maarif Modeli standartları referans alınmıştır.
