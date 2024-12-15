import streamlit as st
import cv2
import numpy as np
from pytube import YouTube
import tempfile
import os
from ultralytics import YOLO
import plotly.express as px
import pandas as pd

# Sayfa yapılandırması
st.set_page_config(page_title="Basketbol Video Analizi", layout="wide")

# Başlık
st.title("🏀 Basketbol Video Analizi")

# YouTube URL girişi
youtube_url = st.text_input("YouTube Video URL'sini Girin")

if youtube_url:
    try:
        # Video indirme
        @st.cache_data
        def download_youtube_video(url):
            yt = YouTube(url)
            stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
            temp_dir = tempfile.mkdtemp()
            return stream.download(output_path=temp_dir)

        # Video işleme ve analiz
        @st.cache_data
        def process_video(video_path):
            # YOLO modelini yükle
            model = YOLO('yolov8x.pt')
            
            cap = cv2.VideoCapture(video_path)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # İstatistikler için veri yapıları
            player_stats = {
                'team_a': {'shots': 0, 'successful_shots': 0},
                'team_b': {'shots': 0, 'successful_shots': 0}
            }
            
            progress_bar = st.progress(0)
            frame_placeholder = st.empty()
            
            frame_count = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                    
                # Her 3 karede bir işlem yap (performans için)
                if frame_count % 3 == 0:
                    # YOLO ile nesne tespiti
                    results = model(frame)
                    
                    # Tespit edilen nesneleri çiz
                    annotated_frame = results[0].plot()
                    
                    # Frame'i göster
                    frame_placeholder.image(annotated_frame, channels="BGR")
                    
                    # İlerleme çubuğunu güncelle
                    progress = int((frame_count / total_frames) * 100)
                    progress_bar.progress(progress)
                
                frame_count += 1
                
            cap.release()
            return player_stats
            
        with st.spinner('Video indiriliyor...'):
            video_path = download_youtube_video(youtube_url)
            
        with st.spinner('Video analiz ediliyor...'):
            stats = process_video(video_path)
            
        # İstatistikleri göster
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Takım A İstatistikleri")
            st.write(f"Atış Sayısı: {stats['team_a']['shots']}")
            st.write(f"Başarılı Atış: {stats['team_a']['successful_shots']}")
            
        with col2:
            st.subheader("Takım B İstatistikleri")
            st.write(f"Atış Sayısı: {stats['team_b']['shots']}")
            st.write(f"Başarılı Atış: {stats['team_b']['successful_shots']}")
            
    except Exception as e:
        st.error(f"Bir hata oluştu: {str(e)}")
        
# Footer
st.markdown("---")
st.markdown("Basketbol Video Analiz Uygulaması - v1.0") 