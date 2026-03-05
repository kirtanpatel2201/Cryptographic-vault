import cv2
import os
import time

FACE_DIR = "data/faces"

if not os.path.exists(FACE_DIR):
    os.makedirs(FACE_DIR)

# Load Haar Cascade
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


# -----------------------------
# FACE REGISTRATION
# -----------------------------
def register_face(username):

    cam = cv2.VideoCapture(0)

    captured = False

    while True:

        ret, frame = cam.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            1.3,
            5
        )

        for (x, y, w, h) in faces:

            face_img = frame[y:y+h, x:x+w]

            path = os.path.join(FACE_DIR, f"{username}.jpg")

            cv2.imwrite(path, face_img)

            captured = True

            break

        if captured:
            break

        time.sleep(0.5)

    cam.release()
    cv2.destroyAllWindows()


# -----------------------------
# FACE AUTHENTICATION
# -----------------------------
def authenticate_face(username):

    path = os.path.join(FACE_DIR, f"{username}.jpg")

    if not os.path.exists(path):
        return False

    stored_face = cv2.imread(path, 0)

    cam = cv2.VideoCapture(0)

    verified = False

    start_time = time.time()

    while True:

        ret, frame = cam.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            1.3,
            5
        )

        for (x, y, w, h) in faces:

            face_img = gray[y:y+h, x:x+w]

            face_img = cv2.resize(face_img, (200, 200))
            stored_resized = cv2.resize(stored_face, (200, 200))

            difference = cv2.absdiff(face_img, stored_resized)

            score = difference.mean()

            if score < 60:
                verified = True
                break

        if verified:
            break

        # stop after 5 seconds
        if time.time() - start_time > 5:
            break

    cam.release()
    cv2.destroyAllWindows()

    return verified