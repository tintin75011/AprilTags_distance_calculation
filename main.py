import cv2
import numpy as np
from pupil_apriltags import Detector

# --- Paramètres caméra calibration ---
camera_matrix = np.array([[518.08250954, 0., 314.13013755],
                          [0., 588.4995957, 218.58106919],
                          [0., 0., 1.]])
dist_coeffs = np.array([0.00405433, -1.19756207, 0.02470587, 0.04513974, 0.47613094])

# --- Dictionnaire tailles par ID (en mètres) ---
tags_sizes = {
    0: 0.055,  
    1: 0.055,  
    2: 0.055
    # ajoute d'autres si besoin
}

# Détecteur AprilTag
detector = Detector(families='tag25h9')

# Ouvrir webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Détection sans pose
    detections = detector.detect(gray, estimate_tag_pose=False)

    # Stocker les poses détectées
    positions = {}
    rotations = {}
    for det in detections:
        tag_id = det.tag_id
        tag_size = tags_sizes.get(tag_id, 0.01)  # taille par défaut si ID inconnu

        # Points 3D du carré tag dans son repère (z=0 car plan)
        obj_pts = np.array([
            [0, 0, 0],
            [tag_size, 0, 0],
            [tag_size, tag_size, 0],
            [0, tag_size, 0]
        ], dtype=np.float32)

        # Points 2D détectés (corners) convertis en float32
        img_pts = det.corners.astype(np.float32)

        # Estimer la pose avec solvePnP
        success, rvec, tvec = cv2.solvePnP(obj_pts, img_pts, camera_matrix, dist_coeffs)
        if not success:
            continue

        # Stocker la position de chaque tag par ID
        positions[tag_id] = tvec
        rotations[tag_id] = rvec

        # Dessiner contour du tag
        corners = det.corners.reshape((-1, 1, 2)).astype(int)
        cv2.polylines(frame, [corners], True, (0, 255, 0), 2)
    

        # Afficher l’ID
        c_x, c_y = int(det.center[0]), int(det.center[1])
        cv2.putText(frame, f"ID:{tag_id}", (c_x - 10, c_y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Afficher la position (translation)
        tvec_str = f"x={tvec[0][0]:.3f}m y={tvec[1][0]:.3f}m z={tvec[2][0]:.3f}m"
        cv2.putText(frame, tvec_str, (c_x - 50, c_y + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
    # Afficher la distance entre les tags 0 et 1 s'ils sont tous les deux détectés
    if 0 in positions and 1 in positions and 2 in positions:
                # Dessiner une ligne entre les centres des tags 0 et 1
        for det in detections:
            if det.tag_id == 0:
                center0 = tuple(map(int, det.center))
            if det.tag_id == 1:
                center1 = tuple(map(int, det.center))
            if det.tag_id == 2:
                center2 = tuple(map(int, det.center))
        
        cv2.line(frame, center0, center1, (0, 0, 255), 1)  # rouge, épaisseur 1
        cv2.line(frame, center0, center2, (255, 0, 0), 1)  # rouge, épaisseur 1

        tvec0 = positions[0].flatten()
        tvec1 = positions[1].flatten()
        tvec2 = positions[2].flatten()

        dx1 = tvec1[0] - tvec0[0]
        dy1= tvec1[1] - tvec0[1]
        dz1 = tvec1[2] - tvec0[2]
        dist = np.linalg.norm([dx1, dy1, dz1])
        #Calculer l'angle de rotation pour le tag 1
        rvec1 = rotations[1]
        R1, _ = cv2.Rodrigues(rvec1)  # Convertir rvec en matrice de rotation
        angle_z_rad1 = np.arctan2(R1[1, 0], R1[0, 0])  # angle yaw
        angle_z_deg1 = np.degrees(angle_z_rad1)
        
        
        # Affichage des composantes + distance
        cv2.putText(frame, f"dx: {dx1:.3f} m", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        cv2.putText(frame, f"dy: {dy1:.3f} m", (10, 55),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        cv2.putText(frame, f"dz: {dz1:.3f} m", (10, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        cv2.putText(frame, f"Dist: {dist:.3f} m", (10, 105),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        cv2.putText(frame, f"yaw z: {angle_z_deg1:.1f} deg", (10, 130),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
        # Calculer la distance entre le tag 0 et le tag 2
        dx2 = tvec2[0] - tvec0[0]
        dy2= tvec2[1] - tvec0[1]
        dz2 = tvec2[2] - tvec0[2]
        dist = np.linalg.norm([dx2, dy2, dz2])
        #Calculer l'angle de rotation pour le tag 2
        rvec2 = rotations[2]
        R2, _ = cv2.Rodrigues(rvec2)  # Convertir rvec en matrice de rotation
        angle_z_rad2 = np.arctan2(R2[1, 0], R2[0, 0])  # angle yaw
        angle_z_deg2 = np.degrees(angle_z_rad2)

        # Affichage des composantes + distance
        cv2.putText(frame, f"dx: {dx2:.3f} m", (300, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        cv2.putText(frame, f"dy: {dy2:.3f} m", (300, 55),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        cv2.putText(frame, f"dz: {dz2:.3f} m", (300, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        cv2.putText(frame, f"Dist: {dist:.3f} m", (300, 105),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        cv2.putText(frame, f"yaw z: {angle_z_deg2:.1f} deg", (300, 130),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    else:
        cv2.putText(frame, "Tags 0 ou 1 ou 2 non detectes", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)


    cv2.imshow("AprilTags", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC pour quitter
        break

cap.release()
cv2.destroyAllWindows()
