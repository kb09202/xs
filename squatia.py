# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 20:27:22 2024

@author: pc
"""

import cv2
import mediapipe as mp
import numpy as np
import pyttsx3

# Initialisation de Mediapipe et du synthétiseur vocal
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

engine = pyttsx3.init()

# Variables pour le comptage des squats
squat_count = 0
stage = None  # Peut être "descente" ou "remontée"

def speak(text):
    """Synthèse vocale."""
    engine.say(text)
    engine.runAndWait()

def calculate_angle(a, b, c):
    """Calcule l'angle entre trois points."""
    a = np.array(a)  # Premier point
    b = np.array(b)  # Deuxième point
    c = np.array(c)  # Troisième point

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle

    return angle

# Ouvrir la webcam
cap = cv2.VideoCapture(0)

speak("Commencez vos squats")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir l'image en RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False

    # Détection des points clés avec Mediapipe
    results = pose.process(image)

    # Convertir l'image en BGR pour affichage
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Extraire les points clés si disponibles
    try:
        landmarks = results.pose_landmarks.landmark

        # Points nécessaires pour détecter les squats
        hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
               landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

        # Calculer l'angle entre la hanche, le genou et la cheville
        angle = calculate_angle(hip, knee, ankle)

        # Détecter la position du squat
        if angle < 90:  # Descente
            stage = "descente"
        if angle > 160 and stage == "descente":  # Remontée
            stage = "remontée"
            squat_count += 1
            speak(str(squat_count))  # Compter à voix haute

        # Afficher l'angle et le comptage sur la vidéo
        cv2.putText(image, f"Angle: {int(angle)}", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(image, f"Squats: {squat_count}", (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    except Exception as e:
        pass

    # Affichage des points clés
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Afficher l'image
    cv2.imshow("Squat Counter", image)

    # Quitter avec la touche 'q'
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
