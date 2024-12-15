import os

# Yollar
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(BASE_DIR, 'static', 'models', 'yolov8x.pt')
TEMP_DIR = os.path.join(BASE_DIR, 'static', 'temp')

# Video işleme ayarları
PROCESS_EVERY_N_FRAMES = 3
CONFIDENCE_THRESHOLD = 0.5

# Analiz ayarları
COURT_ZONES = {
    'three_point_line': {'x': (0, 1280), 'y': (0, 720)},
    'paint_area': {'x': (400, 880), 'y': (100, 620)},
    'free_throw_line': {'y': 150}
}

# Takım renkleri
TEAM_COLORS = {
    'team_a': '#FF0000',  # Kırmızı
    'team_b': '#0000FF'   # Mavi
}

# İstatistik kategorileri
STAT_CATEGORIES = [
    'shots_attempted',
    'shots_made',
    'three_pointers_attempted',
    'three_pointers_made',
    'free_throws_attempted',
    'free_throws_made',
    'rebounds',
    'assists',
    'steals',
    'blocks',
    'turnovers',
    'fouls'
] 