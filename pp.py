import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh

def detect_forehead(image, face_mesh):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image_rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            forehead_point = face_landmarks.landmark[10]  # Index 10 approximates the forehead
            h, w, _ = image.shape
            x, y = int(forehead_point.x * w), int(forehead_point.y * h)
            return (x, y)
    return None

def main():
    cap = cv2.VideoCapture(0)
    face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        forehead_coords = detect_forehead(frame, face_mesh)
        if forehead_coords:
            cv2.circle(frame, forehead_coords, 5, (0, 0, 255), -1)

        cv2.imshow('Forehead Tracking', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()