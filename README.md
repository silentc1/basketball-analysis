# Basketbol Video Analiz Uygulaması

Bu uygulama, YouTube'dan basketbol videolarını indirip analiz ederek takım ve oyuncu istatistiklerini çıkaran bir web uygulamasıdır.

## Özellikler

- YouTube video indirme
- Gerçek zamanlı oyuncu ve top takibi
- Takım istatistikleri
- Atış analizi
- Kullanıcı dostu web arayüzü

## Kurulum

1. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

2. YOLO modelini indirin:
```bash
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8x.pt
```

## Kullanım

1. Uygulamayı başlatın:
```bash
streamlit run app.py
```

2. Web tarayıcınızda açılan uygulamaya bir YouTube video URL'si girin
3. Analiz sonuçlarını görüntüleyin

## Gereksinimler

- Python 3.8+
- İnternet bağlantısı
- Modern web tarayıcısı 