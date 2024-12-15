import cv2
import numpy as np
from ultralytics import YOLO
import pandas as pd
from ..config.settings import STAT_CATEGORIES, COURT_ZONES, CONFIDENCE_THRESHOLD

class VideoAnalyzer:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
        self.stats = {
            'team_a': {cat: 0 for cat in STAT_CATEGORIES},
            'team_b': {cat: 0 for cat in STAT_CATEGORIES}
        }
        self.player_positions = []
        self.shot_locations = []
        
    def analyze_frame(self, frame):
        """Tek bir frame'i analiz eder"""
        results = self.model(frame)
        detections = results[0]
        
        # Oyuncu pozisyonlarını kaydet
        self._track_players(detections)
        
        # Top hareketlerini analiz et
        self._analyze_ball_movement(detections)
        
        return detections.plot()
        
    def _track_players(self, detections):
        """Oyuncuları takip eder ve pozisyonlarını kaydeder"""
        for det in detections.boxes.data:
            if det[4] > CONFIDENCE_THRESHOLD:  # Confidence check
                x, y = det[0], det[1]  # Pozisyon
                class_id = int(det[5])  # Sınıf ID
                
                if class_id == 0:  # Oyuncu sınıfı
                    team = self._determine_team(det)
                    self.player_positions.append({
                        'team': team,
                        'x': float(x),
                        'y': float(y),
                        'frame_number': len(self.player_positions)
                    })
                    
    def _analyze_ball_movement(self, detections):
        """Top hareketlerini analiz eder"""
        for det in detections.boxes.data:
            if det[4] > CONFIDENCE_THRESHOLD and int(det[5]) == 1:  # Top sınıfı
                x, y = det[0], det[1]
                
                # Şut tespiti
                if self._is_shot_attempt(x, y):
                    team = self._determine_shooting_team(x, y)
                    self.shot_locations.append({
                        'team': team,
                        'x': float(x),
                        'y': float(y),
                        'successful': self._is_successful_shot(det)
                    })
                    
    def _determine_team(self, detection):
        """Oyuncunun hangi takımda olduğunu belirler"""
        # Bu fonksiyon renk analizi veya pozisyon bazlı takım belirleme yapabilir
        x = detection[0]
        return 'team_a' if x < 640 else 'team_b'
        
    def _is_shot_attempt(self, x, y):
        """Topun şut girişimi olup olmadığını kontrol eder"""
        # Top yüksekliği ve pozisyonu bazlı şut tespiti
        return y < COURT_ZONES['free_throw_line']['y']
        
    def _is_successful_shot(self, detection):
        """Şutun başarılı olup olmadığını belirler"""
        # Bu kısım hareket analizi ve basket tespiti içerebilir
        return np.random.random() > 0.5  # Şimdilik rastgele
        
    def get_stats(self):
        """Tüm istatistikleri döndürür"""
        return {
            'team_stats': self.stats,
            'shot_locations': pd.DataFrame(self.shot_locations),
            'player_positions': pd.DataFrame(self.player_positions)
        }
        
    def get_heatmap_data(self):
        """Oyuncu pozisyonlarından heatmap verisi oluşturur"""
        positions_df = pd.DataFrame(self.player_positions)
        return positions_df.groupby('team').agg({
            'x': list,
            'y': list
        }).to_dict('index') 