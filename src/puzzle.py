import cv2
import numpy as np
import random

class Puzzle:
    def __init__(self, grid_size=3):
        self.grid_size = grid_size
        self.original_image = None
        self.pieces = []
        self.slots = []
        self.dragged_piece = None
        self.drag_origin_slot = None
        self.was_pinching = False
        self.completed = False

        # Correct-drop feedback
        self.just_snapped_slot = None

        # Last release result
        self.last_drop_correct = None
        self.last_drop_slot = None

    # ========================================================
    # PHOTO EFFECT
    # ========================================================
    def apply_photo_effect(self, image):

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        gray = cv2.cvtColor(
            gray,
            cv2.COLOR_GRAY2BGR
        )

        effect = cv2.convertScaleAbs(
            gray,
            alpha=1.3,
            beta=10
        )

        noise = np.random.normal(
            0,
            15,
            effect.shape
        ).astype(np.int16)

        effect = np.clip(
            effect.astype(np.int16) + noise,
            0,
            255
        ).astype(np.uint8)

        return effect

    # ========================================================
    # CREATE PUZZLE
    # ========================================================
    def create_puzzle(self, image):

        self.original_image = (self.apply_photo_effect(image))
        height, width, _ = (self.original_image.shape )

        # Make dimensions divisible by grid size
        new_width = ( width - width % self.grid_size)
        new_height = ( height - height % self.grid_size)

        self.original_image = cv2.resize(
            self.original_image,
            (new_width,new_height)
        )

        height, width, _ = (self.original_image.shape)
        piece_width = (width // self.grid_size)
        piece_height = (height // self.grid_size)
        self.pieces = []
        piece_id = 0

        # ====================================================
        # CUT PHOTO INTO 3 x 3
        # ====================================================
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x1 = (col * piece_width)
                y1 = (row * piece_height)
                x2 = (x1 + piece_width)
                y2 = (y1 + piece_height)
                piece_image = (self.original_image[y1:y2,x1:x2].copy())
                piece = {
                    "id": piece_id,
                    "image": piece_image,
                    "correct_row": row,
                    "correct_col": col
                }
                self.pieces.append(piece)
                piece_id += 1

        # ====================================================
        # SHUFFLE
        #
        # Important:
        # keep shuffling until ZERO pieces are already correct.
        #
        # Every new game therefore starts at 0 / 9.
        # ====================================================

        self.slots = (self.pieces.copy())

        while True:
            random.shuffle(self.slots)
            if self.get_progress() == 0:
                break

        # ====================================================
        # RESET GAME STATE
        # ====================================================
        self.dragged_piece = None
        self.drag_origin_slot = None
        self.was_pinching = False
        self.completed = False
        self.just_snapped_slot = None
        self.last_drop_correct = None
        self.last_drop_slot = None

    # ========================================================
    # CHECK WHETHER PIECE IS CORRECT
    # ========================================================

    def is_piece_correct(self,slot_index,piece):

        if piece is None:
            return False

        row = (slot_index // self.grid_size)

        col = (slot_index % self.grid_size)

        return (
            piece["correct_row"] == row
            and
            piece["correct_col"] == col
        )

    # ========================================================
    # GET CURRENT PROGRESS
    # ========================================================
    def get_progress(self):
        if not self.slots:
            return 0
        correct = 0

        for slot_index, piece in enumerate( self.slots):

            if self.is_piece_correct(
                slot_index,
                piece
            ):

                correct += 1

        return correct

    # ========================================================
    # GET CORRECT SLOT OF A PIECE
    # ========================================================
    def get_correct_slot(
        self,
        piece
    ):

        return (
            piece["correct_row"]
            * self.grid_size
            + piece["correct_col"]
        )

    # ========================================================
    # START DRAG
    # ========================================================

    def start_drag(
        self,
        finger_x,
        finger_y
    ):

        if self.completed:
            return False

        if self.original_image is None:
            return False

        height, width, _ = (
            self.original_image.shape
        )

        # Finger must be inside puzzle
        if not (
            0 <= finger_x < width
            and
            0 <= finger_y < height
        ):
            return False

        piece_width = (
            width // self.grid_size
        )

        piece_height = (
            height // self.grid_size
        )

        col = int(
            finger_x // piece_width
        )

        row = int(
            finger_y // piece_height
        )

        slot_index = (
            row
            * self.grid_size
            + col
        )

        piece = (
            self.slots[
                slot_index
            ]
        )

        if piece is None:
            return False

        # ====================================================
        # CORRECT PIECES ARE LOCKED
        # ====================================================

        if self.is_piece_correct(
            slot_index,
            piece
        ):

            return False

        # Pick it up
        self.dragged_piece = piece

        self.drag_origin_slot = (
            slot_index
        )

        # Leave temporary empty slot
        self.slots[
            slot_index
        ] = None

        return True

    # ========================================================
    # RELEASE DRAG
    # ========================================================

    def release_drag(
        self,
        finger_x,
        finger_y
    ):

        if self.dragged_piece is None:
            return False

        height, width, _ = (
            self.original_image.shape
        )

        piece_width = (
            width // self.grid_size
        )

        piece_height = (
            height // self.grid_size
        )

        piece = (
            self.dragged_piece
        )

        placed_correctly = False

        self.last_drop_correct = False
        self.last_drop_slot = None

        # ====================================================
        # CHECK RELEASE POSITION
        # ====================================================

        inside = (
            0 <= finger_x < width
            and
            0 <= finger_y < height
        )

        if inside:

            target_col = int(
                finger_x // piece_width
            )

            target_row = int(
                finger_y // piece_height
            )

            target_slot = (
                target_row
                * self.grid_size
                + target_col
            )

            self.last_drop_slot = (
                target_slot
            )

            correct_slot = (
                self.get_correct_slot(
                    piece
                )
            )

            # =================================================
            # CORRECT RELEASE
            # =================================================

            if target_slot == correct_slot:

                displaced_piece = (
                    self.slots[
                        correct_slot
                    ]
                )

                # Put selected piece into
                # its correct position
                self.slots[
                    correct_slot
                ] = piece

                # If another unsolved piece was there,
                # move it to the slot we picked up from.
                if displaced_piece is not None:

                    self.slots[
                        self.drag_origin_slot
                    ] = displaced_piece

                self.just_snapped_slot = (
                    correct_slot
                )

                self.last_drop_correct = (
                    True
                )

                placed_correctly = (
                    True
                )

        # ====================================================
        # WRONG RELEASE
        # ====================================================

        if not placed_correctly:

            # Return piece to where it came from
            self.slots[
                self.drag_origin_slot
            ] = piece

        # ====================================================
        # FINISH DRAG
        # ====================================================

        self.dragged_piece = None
        self.drag_origin_slot = None

        total = (
            self.grid_size
            * self.grid_size
        )

        if self.get_progress() == total:

            self.completed = True

        return placed_correctly

    # ========================================================
    # UPDATE PINCH STATE
    # ========================================================

    def update_drag(
        self,
        finger_x,
        finger_y,
        pinching
    ):

        snapped = False

        # ====================================================
        # OPEN -> PINCH
        #
        # Start grabbing
        # ====================================================

        if (
            pinching
            and not self.was_pinching
        ):

            self.start_drag(
                finger_x,
                finger_y
            )

        # ====================================================
        # PINCH -> OPEN
        #
        # Release
        # ====================================================

        elif (
            not pinching
            and self.was_pinching
        ):

            snapped = (
                self.release_drag(
                    finger_x,
                    finger_y
                )
            )

        self.was_pinching = (
            pinching
        )

        return snapped

    # ========================================================
    # CANCEL DRAG
    # ========================================================

    def cancel_drag(self):

        if (
            self.dragged_piece is not None
            and
            self.drag_origin_slot is not None
        ):

            self.slots[
                self.drag_origin_slot
            ] = self.dragged_piece

        self.dragged_piece = None
        self.drag_origin_slot = None

        self.was_pinching = False

    # ========================================================
    # GET BASIC PUZZLE IMAGE
    # ========================================================

    def get_puzzle_image(self):

        if self.original_image is None:
            return None

        height, width, _ = (
            self.original_image.shape
        )

        piece_width = (
            width // self.grid_size
        )

        piece_height = (
            height // self.grid_size
        )

        output = np.zeros_like(
            self.original_image
        )

        for slot_index, piece in enumerate(
            self.slots
        ):

            if piece is None:
                continue

            row = (
                slot_index
                // self.grid_size
            )

            col = (
                slot_index
                % self.grid_size
            )

            x1 = (
                col * piece_width
            )

            y1 = (
                row * piece_height
            )

            x2 = (
                x1 + piece_width
            )

            y2 = (
                y1 + piece_height
            )

            output[
                y1:y2,
                x1:x2
            ] = piece["image"]

        return output