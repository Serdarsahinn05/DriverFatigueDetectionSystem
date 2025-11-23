import cv2
import time
import winsound  # Windows'un kendi ses sistemi (playsound yerine)
import config  # Ayarlar dosyamız
from src.face_mesh import FaceMeshDetector
from src import utils


def main():
    # 1. DONANIM VE ARAÇLARI HAZIRLA
    # ---------------------------------------------------------
    cap = cv2.VideoCapture(config.CAMERA_ID)

    # Senin yazdığın sınıfı çağırıyoruz
    detector = FaceMeshDetector(max_faces=1)

    # Değişkenler
    pTime = 0  # FPS hesabı için önceki zaman
    blink_counter = 0  # Gözün kaç kare kapalı kaldığını sayacak sayaç

    print("Sistem Başlatılıyor... Çıkmak için 'q' tuşuna basınız.")

    # 2. SONSUZ DÖNGÜ (GÖRÜNTÜ İŞLEME AKIŞI)
    # ---------------------------------------------------------
    while True:
        success, img = cap.read()
        if not success:
            print("Kamera görüntüsü alınamadı!")
            break

        # A) Yüzü Bul (Senin yazdığın modül çalışıyor)
        # img: Üzerine çizim yapılmış resim
        # faces: Yüz koordinatlarının listesi (örn: [[x,y], [x,y]...])
        img, faces = detector.find_face_mesh(img, draw=True)

        # B) Eğer Yüz Varsa Analize Başla
        if faces:
            face = faces[0]  # İlk tespit edilen yüzü al (Sadece sürücü)

            # --- VERİ ÇIKARMA (DATA EXTRACTION) ---
            # Config dosyasındaki indeksleri kullanarak sadece göz koordinatlarını çek
            left_eye_coords = [face[i] for i in config.LEFT_EYE_IDXS]
            right_eye_coords = [face[i] for i in config.RIGHT_EYE_IDXS]

            # --- MATEMATİKSEL HESAP (EAR) ---
            # utils.py dosyasındaki fonksiyonunu kullan
            left_ear = utils.calculate_ear(left_eye_coords)
            right_ear = utils.calculate_ear(right_eye_coords)

            # İki gözün ortalamasını al (Daha kararlı sonuç verir)
            avg_ear = (left_ear + right_ear) / 2.0

            # --- KARAR MEKANİZMASI (LOGIC) ---
            # Eğer göz oranı eşik değerin (0.15) altındaysa -> KAPALI
            if avg_ear < config.EAR_THRESHOLD:
                blink_counter += 1

                # Görsel Uyarı (Ekrana Yaz)
                cv2.putText(img, f"GOZ KAPALI: {blink_counter}", (10, 100),
                            cv2.FONT_HERSHEY_DUPLEX, 1, config.RED, 2)

                # C) ALARM TETİKLEME
                # Eğer göz 'config.CLOSED_FRAMES' kadar süre kapalı kaldıysa
                if blink_counter > config.CLOSED_FRAMES:
                    cv2.putText(img, "UYARI! UYANIYOR MUSUN?", (1, 300),
                                cv2.FONT_HERSHEY_DUPLEX, 1.5, config.RED, 3)

                    # BİİİP sesi (Frekans: 2500Hz, Süre: 200ms)
                    # Kodun donmaması için kısa bip tercih ettik
                    winsound.Beep(2500, 200)

            else:
                # Göz açıldığı anda sayacı sıfırla
                blink_counter = 0
                cv2.putText(img, "DURUM: NORMAL", (10, 100),
                            cv2.FONT_HERSHEY_DUPLEX, 1, config.GREEN, 2)

            # --- BİLGİ EKRANI (DEBUGGING) ---
            # EAR değerini ekranda görmek ayar yapmak için hayati önem taşır
            cv2.putText(img, f"EAR Degeri: {round(avg_ear, 2)}", (10, 60),
                        cv2.FONT_HERSHEY_DUPLEX, 0.7, config.YELLOW, 1)

        # 3. FPS HESABI VE GÖSTERİM
        # ---------------------------------------------------------
        cTime = time.time()
        fps = 1 / (cTime - pTime) if (cTime - pTime) > 0 else 0
        pTime = cTime

        cv2.putText(img, f"FPS: {int(fps)}", (10, 30),
                    cv2.FONT_HERSHEY_PLAIN, 2, config.GREEN, 2)

        cv2.imshow("Surucu Yorgunluk Tespiti", img)

        # 'q' tuşuna basınca çık
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()