import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import drawing_utils, drawing_styles
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[0]
model_path = PROJECT_ROOT / "hand_landmarker.task"

options = vision.HandLandmarkerOptions(
    base_options=python.BaseOptions(model_asset_path=str(model_path)),
    num_hands=2,
    min_hand_detection_confidence=0.7,
    min_hand_presence_confidence=0.7,
    min_tracking_confidence=0.7
)

detector = vision.HandLandmarker.create_from_options(options)

#  Conexões e estilos oficiais do MediaPipe Tasks
connections = vision.HandLandmarksConnections.HAND_CONNECTIONS

landmark_style = drawing_styles.get_default_hand_landmarks_style()
connection_style = drawing_styles.get_default_hand_connections_style()

video = cv2.VideoCapture(0)

while video.isOpened():
    sucess, frame = video.read()

    if not sucess:
        print("Erro ao acessar a câmera")
        continue

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(mp.ImageFormat.SRGB, frame_rgb)

    result = detector.detect(mp_image)

    if result.hand_landmarks:
        for hand_landmarks in result.hand_landmarks:
            drawing_utils.draw_landmarks(
                image=frame_rgb,
                landmark_list=hand_landmarks,
                connections=connections,
                landmark_drawing_spec=landmark_style,
                connection_drawing_spec=connection_style
            )
    
    frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

    cv2.imshow("Reconhecimento das mãos", frame)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
