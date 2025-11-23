import cv2
import mediapipe as mp


class FaceMeshDetector:
    # Yüz tarama modülünü başlatır ve yüz mesh ağını bulur.
    # Parametreler:
    # static_mode: Statik görüntüler için True, video için False.
    # max_faces: Algılanacak maksimum yüz sayısı.
    # refine_landmarks: Göz bebekleri için daha hassas mod.
    # min_detection_con: Minimum algılama güveni (0.0 - 1.0).
    # min_track_con: Minimum takip güveni (0.0 - 1.0).
    def __init__(self, static_mode=False, max_faces=1, refine_landmarks=True, min_detection_con=0.5, min_track_con=0.5):
        """
        Yüz tarama modülünü başlatır.
        """
        self.static_mode = static_mode
        self.max_faces = max_faces
        self.refine_landmarks = refine_landmarks
        self.min_detection_con = min_detection_con
        self.min_track_con = min_track_con

        # MediaPipe araçlarını yükle
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_face_mesh = mp.solutions.face_mesh

        # Yüz Mesh modelini oluştur
        # refine_landmarks parametresi göz bebekleri için daha hassas bir model sağlar
        # bu, göz takibi uygulamalarında faydalı olabilir
        # min_detection_con ve min_track_con parametreleri
        # modelin algılama ve takip güvenini ayarlar

        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=self.static_mode,
            max_num_faces=self.max_faces,
            refine_landmarks=self.refine_landmarks,  # Göz bebekleri için daha hassas mod
            min_detection_confidence=self.min_detection_con,
            min_tracking_confidence=self.min_track_con
        )

        # Çizim ayarları (Yeşil renk, ince çizgi)
        # draw_spec, yüz mesh noktalarının ve bağlantılarının nasıl çizileceğini belirler
        # burada çizgi kalınlığı 1, daire yarıçapı 1 ve renk yeşil olarak ayarlanmıştır
        # bu, yüz mesh'in görsel olarak belirgin olmasını sağlar
        # çizim için kullanılan renk BGR formatındadır
        # yeşil renk (0, 255, 0) olarak ayarlanmıştır
        self.draw_spec = self.mp_draw.DrawingSpec(thickness=1, circle_radius=1, color=(0, 255, 0))

    def find_face_mesh(self, img, draw=True):
        """
        Görüntüdeki yüzü bulur ve mesh ağını çizer.
        """
        # MediaPipe RGB ister, OpenCV BGR kullanır. Dönüşüm yapıyoruz:
        self.img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.face_mesh.process(self.img_rgb)

        faces = []

        #açıkla
        # Eğer yüz mesh algılandıysa, her yüz için noktaları al ve çiz
        # results.multi_face_landmarks, algılanan yüzlerin mesh noktalarını içerir
        # her yüz için ayrı ayrı işlem yapıyoruz
        # draw parametresi True ise, yüz mesh noktalarını ve bağlantılarını görüntüye çiziyoruz
        # yüz mesh noktalarını listeye çeviriyoruz ve faces listesine ekliyoruz
        # her yüz için ayrı bir liste oluşturuluyor
        # yüz mesh noktaları normalize edilmiş koordinatlar (0-1 arası) olarak gelir
        # bu yüzden görüntü boyutları ile çarparak piksel koordinatlarına dönüştürüyoruz
        # her nokta için x ve y koordinatlarını hesaplıyoruz
        # ve face listesine ekliyoruz
        # sonunda img ve faces listesini döndürüyoruz
        # faces listesi, her yüz için ayrı bir liste içerir
        # her yüz listesi ise o yüzün tüm mesh noktalarını içerir
        # böylece yüz mesh verilerini kolayca kullanabiliriz
        # örneğin, göz takibi veya yüz ifadesi analizi için
        # yüz mesh verileri, çeşitli uygulamalarda kullanılabilir
        # yüz mesh noktaları, yüzün 3D yapısını temsil eder
        # bu veriler, artırılmış gerçeklik uygulamalarında da faydalıdır

        if self.results.multi_face_landmarks:
            for face_landmarks in self.results.multi_face_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(
                        image=img,
                        landmark_list=face_landmarks,
                        connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                        landmark_drawing_spec=self.draw_spec,
                        connection_drawing_spec=self.draw_spec
                    )

                # Yüzdeki noktaları listeye çevir
                face = []
                for id, lm in enumerate(face_landmarks.landmark):
                    ih, iw, ic = img.shape
                    x, y = int(lm.x * iw), int(lm.y * ih)
                    face.append([x, y])
                faces.append(face)

        return img, faces


# Test bloğu: Bu dosya tek başına çalıştırılırsa kamera açılır
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    detector = FaceMeshDetector()

    while True:
        success, img = cap.read()
        if not success: break

        img, faces = detector.find_face_mesh(img)

        if len(faces) > 0:
            print(f"Yüz algılandı! Nokta sayısı: {len(faces[0])}")

        cv2.imshow("Test Modu", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()