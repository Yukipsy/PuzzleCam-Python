import cv2


class Camera:
    def __init__(self, camera_id=0):
        self.camera = cv2.VideoCapture(camera_id)

        if not self.camera.isOpened():
            raise RuntimeError("Could not open webcam.")

        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    def get_frame(self):
        success, frame = self.camera.read()

        if not success:
            return None

        # Mirror camera
        frame = cv2.flip(frame, 1)

        return frame

    def release(self):
        self.camera.release()