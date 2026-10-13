from pathlib import Path
import cv2
import math
import mediapipe as mp


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "hand_landmarker.task"
)


# ============================================================
# MEDIAPIPE LANDMARK NUMBERS
# ============================================================

WRIST = 0

THUMB_TIP = 4

INDEX_MCP = 5
INDEX_TIP = 8

MIDDLE_MCP = 9
MIDDLE_TIP = 12

RING_MCP = 13
RING_TIP = 16

PINKY_MCP = 17
PINKY_TIP = 20


# ============================================================
# HAND SKELETON
# ============================================================

HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),

    (0, 5),
    (5, 6), (6, 7), (7, 8),

    (5, 9),
    (9, 10), (10, 11), (11, 12),

    (9, 13),
    (13, 14), (14, 15), (15, 16),

    (13, 17),
    (17, 18), (18, 19), (19, 20),

    (0, 17)
]


class HandTracker:

    def __init__(
        self,
        model_path=None
    ):

        if model_path is None:
            model_path = DEFAULT_MODEL_PATH

        model_path = str(model_path)

        BaseOptions = mp.tasks.BaseOptions
        HandLandmarker = mp.tasks.vision.HandLandmarker
        HandLandmarkerOptions = (
            mp.tasks.vision.HandLandmarkerOptions
        )
        RunningMode = mp.tasks.vision.RunningMode

        options = HandLandmarkerOptions(
            base_options=BaseOptions(
                model_asset_path=model_path
            ),
            running_mode=RunningMode.IMAGE,
            num_hands=2,
            min_hand_detection_confidence=0.6,
            min_hand_presence_confidence=0.6,
            min_tracking_confidence=0.6
        )

        self.detector = (
            HandLandmarker.create_from_options(
                options
            )
        )

        # Pinch state for each detected hand
        self.pinch_states = [
            False,
            False
        ]

        # Hysteresis thresholds
        self.PINCH_ON = 0.050
        self.PINCH_OFF = 0.070

    # ========================================================
    # DISTANCE
    # ========================================================

    def distance(
        self,
        point_a,
        point_b
    ):

        dx = point_a.x - point_b.x
        dy = point_a.y - point_b.y

        return math.sqrt(
            dx * dx + dy * dy
        )

    # ========================================================
    # STABLE PINCH
    # ========================================================

    def is_pinching(
        self,
        landmarks,
        hand_index
    ):

        thumb = landmarks[THUMB_TIP]
        index = landmarks[INDEX_TIP]

        distance = self.distance(
            thumb,
            index
        )

        previous_state = (
            self.pinch_states[hand_index]
        )

        # Currently OPEN
        if not previous_state:

            if distance < self.PINCH_ON:
                new_state = True
            else:
                new_state = False

        # Currently PINCHING
        else:

            if distance > self.PINCH_OFF:
                new_state = False
            else:
                new_state = True

        self.pinch_states[hand_index] = (
            new_state
        )

        return new_state

    # ========================================================
    # FIST DETECTION
    # ========================================================

    def is_fist(self, landmarks):

        wrist = landmarks[WRIST]

        fingers = [
            (INDEX_TIP, INDEX_MCP),
            (MIDDLE_TIP, MIDDLE_MCP),
            (RING_TIP, RING_MCP),
            (PINKY_TIP, PINKY_MCP)
        ]

        curled = 0

        for tip_index, mcp_index in fingers:

            tip_distance = self.distance(
                landmarks[tip_index],
                wrist
            )

            mcp_distance = self.distance(
                landmarks[mcp_index],
                wrist
            )

            # Tip closer to wrist than MCP
            if tip_distance < mcp_distance:
                curled += 1

        return curled >= 4

    # ========================================================
    # DRAW HAND
    # ========================================================

    def draw_hand(
        self,
        frame,
        landmarks
    ):

        height, width, _ = frame.shape

        points = []

        for landmark in landmarks:

            x = int(
                landmark.x * width
            )

            y = int(
                landmark.y * height
            )

            points.append(
                (x, y)
            )

        # Skeleton lines
        for start, end in HAND_CONNECTIONS:

            cv2.line(
                frame,
                points[start],
                points[end],
                (255, 255, 255),
                2
            )

        # Landmark dots
        for point in points:

            cv2.circle(
                frame,
                point,
                4,
                (255, 255, 255),
                -1
            )

        return points

    # ========================================================
    # DETECT
    # ========================================================

    def detect(self, frame):

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        result = self.detector.detect(
            mp_image
        )

        hands = []

        if result.hand_landmarks:

            for hand_index, landmarks in enumerate(
                result.hand_landmarks
            ):

                points = self.draw_hand(
                    frame,
                    landmarks
                )

                pinching = self.is_pinching(
                    landmarks,
                    hand_index
                )

                fist = self.is_fist(
                    landmarks
                )

                hands.append({
                    "landmarks": landmarks,
                    "points": points,
                    "pinching": pinching,
                    "fist": fist
                })

        # Reset unused pinch states
        for i in range(
            len(hands),
            len(self.pinch_states)
        ):
            self.pinch_states[i] = False

        return frame, hands

    # ========================================================
    # TWO-HAND PHOTO FRAME
    # ========================================================

    def get_hand_frame(
        self,
        hands,
        frame_shape,
        padding=28
    ):

        if len(hands) != 2:
            return None

        height, width, _ = frame_shape

        point_a = (
            hands[0]["points"][INDEX_TIP]
        )

        point_b = (
            hands[1]["points"][INDEX_TIP]
        )

        x1 = (
            min(point_a[0], point_b[0])
            - padding
        )

        y1 = (
            min(point_a[1], point_b[1])
            - padding
        )

        x2 = (
            max(point_a[0], point_b[0])
            + padding
        )

        y2 = (
            max(point_a[1], point_b[1])
            + padding
        )

        x1 = max(0, x1)
        y1 = max(0, y1)

        x2 = min(width, x2)
        y2 = min(height, y2)

        return (
            x1,
            y1,
            x2,
            y2
        )

    # ========================================================

    def close(self):
        self.detector.close()