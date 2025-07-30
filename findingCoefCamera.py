import cv2
import numpy as np
import os

# Configuration du damier
nb_rows =  6 # coins internes (6 cases → 5 coins)
nb_cols = 8
square_size = 0.025  # taille réelle en mètres (2.5 cm)

# Critères de terminaison pour l'optimisation
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Prépare les points 3D du damier (ex: (0,0,0), (1,0,0), ...)
objp = np.zeros((nb_rows * nb_cols, 3), np.float32)
objp[:, :2] = np.mgrid[0:nb_cols, 0:nb_rows].T.reshape(-1, 2) * square_size

# Listes pour les points 3D et les points 2D détectés
objpoints = []
imgpoints = []

# Capture vidéo
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Impossible d'ouvrir la webcam.")

print("➡️ Appuie sur ESPACE quand le damier est bien visible, ou 'q' pour calibrer.")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Recherche des coins du damier
        found, corners = cv2.findChessboardCorners(gray, (nb_cols, nb_rows), None)

        if found:
            cv2.drawChessboardCorners(frame, (nb_cols, nb_rows), corners, found)

        cv2.imshow('Calibration', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord(' '):  # Espace → sauvegarde une image
            if found:
                objpoints.append(objp)
                corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
                imgpoints.append(corners2)
                print(f"✅ Image ajoutée ({len(objpoints)} total)")
            else:
                print("❌ Damier non détecté")
        elif key == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()

# Calcule les paramètres de calibration
if len(objpoints) >= 10:
    print("📸 Calibration en cours...")
    ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, gray.shape[::-1], None, None
    )

    print("\n🎯 Résultats de calibration :")
    print("Matrice de la caméra (camera_matrix):\n", camera_matrix)
    print("Coefficients de distorsion (dist_coeffs):\n", dist_coeffs.ravel())

    # Sauvegarde
    np.savez("camera_calibration.npz", camera_matrix=camera_matrix, dist_coeffs=dist_coeffs)
    print("\n💾 Fichier 'camera_calibration.npz' sauvegardé.")
else:
    print("❗️ Pas assez d'images pour calibrer. Recommence en ajoutant au moins 10 vues.")

