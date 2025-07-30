import cv2
import numpy as np
from pupil_apriltags import Detector

# Initialisation de la capture vidéo
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Erreur : Impossible d'ouvrir la webcam.")

# Création du détecteur AprilTag
detector = Detector(
    families='tag36h11',
    nthreads=1,
    quad_decimate=1.0,
    quad_sigma=0.0,
    refine_edges=True,
    decode_sharpening=0.25,
    debug=False
)

window_name = 'Détection AprilTag'
cv2.namedWindow(window_name)

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erreur de lecture vidéo.")
            break

        # Conversion en niveau de gris
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Détection des tags
        detections = detector.detect(gray)

        # Dessin des tags détectés
        for detection in detections:
            tag_id = detection.tag_id
            center = tuple(map(int, detection.center))
            corners = np.int32(detection.corners)

            # Dessine les coins (rectangle)
            cv2.polylines(frame, [corners], isClosed=True, color=(0, 255, 0), thickness=2)

            # Dessine le centre
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

            # Affiche l'ID du tag
            cv2.putText(frame, f"ID: {tag_id}", (center[0] + 10, center[1]), cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, (255, 0, 0), 2)

        # Affiche le résultat
        cv2.imshow(window_name, frame)

        # Quitte si la fenêtre est fermée ou si 'q' est pressé
        if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
