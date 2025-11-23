# config.py

# KAMERA AYARI
CAMERA_ID = 0

# EŞİK DEĞERLERİ (Hassasiyet Ayarları)
EAR_THRESHOLD = 0.27  # Göz oranı bunun altına düşerse 'KAPALI' sayılacak
CLOSED_FRAMES = 30    # Kaç kare boyunca kapalı kalırsa alarm çalsın?

# RENKLER (BGR Formatı)
GREEN = (0, 255, 0)
RED = (0, 0, 255)
YELLOW = (0, 255, 255)

# MEDIAPIPE YÜZ NOKTA İNDEKSLERİ (Sabit Değerler)
# Bu numaralar MediaPipe'ın haritasında gözlere denk gelen noktalardır.

# Sol Göz Noktaları (P1, P2, P3, P4, P5, P6)
LEFT_EYE_IDXS = [33, 160, 158, 133, 153, 144]

# Sağ Göz Noktaları
RIGHT_EYE_IDXS = [362, 385, 387, 266, 373, 380]