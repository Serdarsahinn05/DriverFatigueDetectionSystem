import math

def euclidean_distance(point1, point2):
    """
    İki nokta (x,y) arasındaki kuş uçuşu mesafeyi hesaplar.
    """
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def calculate_ear(eye_points):
    """
    Verilen 6 göz noktasına göre EAR (Göz Açıklık Oranı) hesaplar.
    Noktalar şu sırada olmalı: [SolKöşe, Üst1, Üst2, SağKöşe, Alt2, Alt1]
    """
    # Dikey çizgilerin uzunluğu (Göz kapakları arası mesafe)
    A = euclidean_distance(eye_points[1], eye_points[5])
    B = euclidean_distance(eye_points[2], eye_points[4])

    # Yatay çizginin uzunluğu (Göz genişliği)
    C = euclidean_distance(eye_points[0], eye_points[3])

    # Olası sıfıra bölünme hatasını önle
    if C == 0:
        return 0.0

    # EAR Formülü
    ear = (A + B) / C
    return ear