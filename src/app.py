import streamlit as st
import cv2
import tempfile
import os
from pytube import YouTube

from config.settings import MODEL_PATH, TEMP_DIR
from analyzers.video_analyzer import VideoAnalyzer
from ui.visualizations import create_shot_chart, create_heatmap, create_stats_comparison

# Sayfa yapılandırması
st.set_page_config(page_title="Basketbol Video Analizi", layout="wide")

# Başlık ve açıklama
st.title("🏀 Basketbol Video Analizi")
st.markdown("""
Bu uygulama, basketbol videolarını analiz ederek detaylı istatistikler çıkarır.
* Oyuncu takibi
* Şut analizi
* Takım istatistikleri
* Pozisyon haritaları
""")

# YouTube URL girişi
youtube_url = st.text_input("YouTube Video URL'sini Girin")

if youtube_url:
    try:
        # Video indirme
        @st.cache_data
        def download_youtube_video(url):
            yt = YouTube(url)
            stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
            if not os.path.exists(TEMP_DIR):
                os.makedirs(TEMP_DIR)
            return stream.download(output_path=TEMP_DIR)

        # Video analizi
        @st.cache_data
        def analyze_video(video_path):
            analyzer = VideoAnalyzer(MODEL_PATH)
            cap = cv2.VideoCapture(video_path)
            
            # Progress bar
            progress_bar = st.progress(0)
            frame_placeholder = st.empty()
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            frame_count = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Her 3 frame'de bir analiz yap
                if frame_count % 3 == 0:
                    annotated_frame = analyzer.analyze_frame(frame)
                    frame_placeholder.image(annotated_frame, channels="BGR")
                    
                    # İlerleme çubuğunu güncelle
                    progress = int((frame_count / total_frames) * 100)
                    progress_bar.progress(progress)
                
                frame_count += 1
            
            cap.release()
            return analyzer.get_stats()
            
        # Video indir ve analiz et
        with st.spinner('Video indiriliyor...'):
            video_path = download_youtube_video(youtube_url)
            
        with st.spinner('Video analiz ediliyor...'):
            stats = analyze_video(video_path)
            
        # Sonuçları göster
        st.header("Analiz Sonuçları")
        
        # Sekmeler oluştur
        tab1, tab2, tab3 = st.tabs(["Takım İstatistikleri", "Şut Haritası", "Pozisyon Analizi"])
        
        with tab1:
            st.plotly_chart(create_stats_comparison(stats['team_stats']))
            
            # Detaylı istatistik tablosu
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Takım A")
                st.table(pd.DataFrame(stats['team_stats']['team_a'], index=[0]).T)
            with col2:
                st.subheader("Takım B")
                st.table(pd.DataFrame(stats['team_stats']['team_b'], index=[0]).T)
        
        with tab2:
            st.plotly_chart(create_shot_chart(stats['shot_locations']))
            
            # Şut istatistikleri
            successful_shots = stats['shot_locations']['successful'].sum()
            total_shots = len(stats['shot_locations'])
            st.metric("Şut Yüzdesi", f"%{(successful_shots/total_shots)*100:.1f}")
        
        with tab3:
            # Heatmap'leri göster
            heatmaps = create_heatmap(analyzer.get_heatmap_data())
            for team, fig in heatmaps.items():
                st.subheader(f"{team} Pozisyon Yoğunluğu")
                st.plotly_chart(fig)
                
    except Exception as e:
        st.error(f"Bir hata oluştu: {str(e)}")
        
# Footer
st.markdown("---")
st.markdown("Basketbol Video Analiz Uygulaması - v1.0") 