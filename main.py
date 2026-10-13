import time
import pygame

from src.camera import Camera
from src.hand_tracker import HandTracker
from src.puzzle import Puzzle
from src.ui import PuzzleUI


# ============================================================
# WINDOW
# ============================================================

WIDTH = 1280
HEIGHT = 720


# ============================================================
# TIMINGS
# ============================================================

PINCH_HOLD_TIME = 0.25
COUNTDOWN_SECONDS = 3

FLASH_DURATION = 0.30
BW_TRANSITION_DURATION = 0.70
PHOTO_HOLD_DURATION = 1.0

GRID_DURATION = 0.65
SHUFFLE_DURATION = 1.20
SOLVE_INTRO_DURATION = 0.75

SNAP_EFFECT_DURATION = 0.45
WRONG_EFFECT_DURATION = 0.45

COMPLETE_REVEAL_DURATION = 0.80

FIST_HOLD_DURATION = 0.55
SHATTER_DURATION = 1.15


# ============================================================
# POLISH
# ============================================================

MIN_CAPTURE_WIDTH = 180
MIN_CAPTURE_HEIGHT = 180

TRACKING_GRACE_TIME = 0.20

# Higher = more responsive
# Lower = smoother
DRAG_SMOOTHING = 0.35


# ============================================================
# STATES
# ============================================================

LIVE = "LIVE"
COUNTDOWN = "COUNTDOWN"
FLASH = "FLASH"
BW_TRANSITION = "BW_TRANSITION"
PHOTO_HOLD = "PHOTO_HOLD"
GRID_FORM = "GRID_FORM"
SHUFFLE = "SHUFFLE"
SOLVE_INTRO = "SOLVE_INTRO"
PUZZLE = "PUZZLE"
COMPLETE_REVEAL = "COMPLETE_REVEAL"
FIST_HOLD = "FIST_HOLD"
SHATTER = "SHATTER"


# ============================================================
# SETUP
# ============================================================

camera = Camera()
hand_tracker = HandTracker()
puzzle = Puzzle()
ui = PuzzleUI(WIDTH, HEIGHT)

state = LIVE
state_start_time = time.time()


# ============================================================
# CAPTURE VARIABLES
# ============================================================

pinch_start_time = None

capture_rect_camera = None
capture_rect_screen = None

captured_colour = None
captured_bw = None
final_photo = None


# ============================================================
# PUZZLE FEEDBACK
# ============================================================

snap_effect_start = None
snap_effect_slot = None

wrong_effect_start = None
wrong_effect_slot = None


# ============================================================
# HAND TRACKING / SMOOTHING
# ============================================================

last_hand_seen_time = None

smooth_drag_x = None
smooth_drag_y = None


# ============================================================
# MOUSE CONTROL
# ============================================================

mouse_dragging = False

mouse_x = None
mouse_y = None


# ============================================================
# ENDING
# ============================================================

fist_start_time = None

shatter_particles = []


running = True


# ============================================================
# CHANGE STATE
# ============================================================

def change_state(new_state):

    global state
    global state_start_time

    state = new_state
    state_start_time = time.time()


# ============================================================
# CAMERA RECT -> SCREEN RECT
# ============================================================

def camera_to_screen_rect(rect, frame_shape):

    if rect is None:
        return None

    frame_height, frame_width, _ = frame_shape

    x1, y1, x2, y2 = rect

    scale_x = WIDTH / frame_width
    scale_y = HEIGHT / frame_height

    return (
        int(x1 * scale_x),
        int(y1 * scale_y),
        int(x2 * scale_x),
        int(y2 * scale_y)
    )


# ============================================================
# SCREEN -> PUZZLE COORDINATES
# ============================================================

def screen_to_puzzle(screen_x, screen_y):

    if (
        capture_rect_screen is None
        or puzzle.original_image is None
    ):
        return None

    x1, y1, x2, y2 = capture_rect_screen

    display_width = x2 - x1
    display_height = y2 - y1

    if display_width <= 0 or display_height <= 0:
        return None

    puzzle_height, puzzle_width, _ = (
        puzzle.original_image.shape
    )

    relative_x = screen_x - x1
    relative_y = screen_y - y1

    puzzle_x = (
        relative_x
        / display_width
        * puzzle_width
    )

    puzzle_y = (
        relative_y
        / display_height
        * puzzle_height
    )

    return puzzle_x, puzzle_y


# ============================================================
# CHECK MARK
# ============================================================

def draw_check_mark(center_x, center_y, size=14):

    yellow = (255, 214, 10)

    pygame.draw.circle(
        ui.screen,
        (15, 15, 15),
        (center_x, center_y),
        size
    )

    pygame.draw.circle(
        ui.screen,
        yellow,
        (center_x, center_y),
        size,
        2
    )

    pygame.draw.line(
        ui.screen,
        yellow,
        (
            center_x - 7,
            center_y
        ),
        (
            center_x - 2,
            center_y + 5
        ),
        3
    )

    pygame.draw.line(
        ui.screen,
        yellow,
        (
            center_x - 2,
            center_y + 5
        ),
        (
            center_x + 8,
            center_y - 7
        ),
        3
    )


# ============================================================
# DRAW INTERACTIVE PUZZLE
# ============================================================

def draw_interactive_puzzle(
    drag_screen_x=None,
    drag_screen_y=None
):

    if (
        capture_rect_screen is None
        or puzzle.original_image is None
    ):
        return

    x1, y1, x2, y2 = capture_rect_screen

    display_width = x2 - x1
    display_height = y2 - y1

    grid_size = puzzle.grid_size

    cell_width = (
        display_width / grid_size
    )

    cell_height = (
        display_height / grid_size
    )

    # ========================================================
    # DRAW GRID PIECES
    # ========================================================

    for slot_index, piece in enumerate(
        puzzle.slots
    ):

        row = (
            slot_index // grid_size
        )

        col = (
            slot_index % grid_size
        )

        draw_x = int(
            x1 + col * cell_width
        )

        draw_y = int(
            y1 + row * cell_height
        )

        cell_rect = (
            draw_x,
            draw_y,
            int(cell_width),
            int(cell_height)
        )

        # ====================================================
        # EMPTY SLOT
        # ====================================================

        if piece is None:

            pygame.draw.rect(
                ui.screen,
                (25, 25, 25),
                cell_rect
            )

            pygame.draw.rect(
                ui.screen,
                (90, 90, 90),
                cell_rect,
                1
            )

            continue

        # ====================================================
        # PIECE
        # ====================================================

        piece_surface = (
            ui.cv_to_surface(
                piece["image"]
            )
        )

        piece_surface = (
            pygame.transform.smoothscale(
                piece_surface,
                (
                    int(cell_width) + 1,
                    int(cell_height) + 1
                )
            )
        )

        ui.screen.blit(
            piece_surface,
            (
                draw_x,
                draw_y
            )
        )

        pygame.draw.rect(
            ui.screen,
            (225, 225, 225),
            cell_rect,
            1
        )

        # ====================================================
        # CORRECT PIECE CHECK
        # ====================================================

        if puzzle.is_piece_correct(
            slot_index,
            piece
        ):

            check_x = int(
                draw_x
                + cell_width
                - 21
            )

            check_y = int(
                draw_y + 20
            )

            draw_check_mark(
                check_x,
                check_y
            )

    # ========================================================
    # DRAGGED PIECE
    # ========================================================

    if (
        puzzle.dragged_piece is not None
        and drag_screen_x is not None
        and drag_screen_y is not None
    ):

        piece = puzzle.dragged_piece

        scale = 1.08

        held_width = int(
            cell_width * scale
        )

        held_height = int(
            cell_height * scale
        )

        held_x = int(
            drag_screen_x
            - held_width / 2
        )

        held_y = int(
            drag_screen_y
            - held_height / 2
        )

        # Shadow
        shadow = pygame.Surface(
            (
                held_width,
                held_height
            ),
            pygame.SRCALPHA
        )

        shadow.fill(
            (
                0,
                0,
                0,
                100
            )
        )

        ui.screen.blit(
            shadow,
            (
                held_x + 10,
                held_y + 10
            )
        )

        # Piece
        held_surface = (
            ui.cv_to_surface(
                piece["image"]
            )
        )

        held_surface = (
            pygame.transform.smoothscale(
                held_surface,
                (
                    held_width,
                    held_height
                )
            )
        )

        ui.screen.blit(
            held_surface,
            (
                held_x,
                held_y
            )
        )

        pygame.draw.rect(
            ui.screen,
            (245, 245, 245),
            (
                held_x,
                held_y,
                held_width,
                held_height
            ),
            3
        )

    # ========================================================
    # CORRECT SNAP EFFECT
    # ========================================================

    if (
        snap_effect_start is not None
        and snap_effect_slot is not None
    ):

        elapsed = (
            time.time()
            - snap_effect_start
        )

        if elapsed < SNAP_EFFECT_DURATION:

            progress = (
                elapsed
                / SNAP_EFFECT_DURATION
            )

            row = (
                snap_effect_slot
                // grid_size
            )

            col = (
                snap_effect_slot
                % grid_size
            )

            pulse_x = int(
                x1
                + col * cell_width
            )

            pulse_y = int(
                y1
                + row * cell_height
            )

            expansion = int(
                18
                * (
                    1.0 - progress
                )
            )

            pygame.draw.rect(
                ui.screen,
                (255, 214, 10),
                (
                    pulse_x - expansion,
                    pulse_y - expansion,
                    int(cell_width)
                    + expansion * 2,
                    int(cell_height)
                    + expansion * 2
                ),
                5
            )

            ui.draw_text(
                "✓",
                (
                    int(
                        pulse_x
                        + cell_width / 2
                    ),
                    int(
                        pulse_y
                        + cell_height / 2
                    )
                ),
                ui.font_large,
                (255, 214, 10),
                center=True
            )

    # ========================================================
    # WRONG DROP EFFECT
    # ========================================================

    if (
        wrong_effect_start is not None
        and wrong_effect_slot is not None
    ):

        elapsed = (
            time.time()
            - wrong_effect_start
        )

        if elapsed < WRONG_EFFECT_DURATION:

            row = (
                wrong_effect_slot
                // grid_size
            )

            col = (
                wrong_effect_slot
                % grid_size
            )

            wrong_x = int(
                x1
                + col * cell_width
            )

            wrong_y = int(
                y1
                + row * cell_height
            )

            center_x = int(
                wrong_x
                + cell_width / 2
            )

            center_y = int(
                wrong_y
                + cell_height / 2
            )

            size = 24

            pygame.draw.line(
                ui.screen,
                (245, 245, 245),
                (
                    center_x - size,
                    center_y - size
                ),
                (
                    center_x + size,
                    center_y + size
                ),
                6
            )

            pygame.draw.line(
                ui.screen,
                (245, 245, 245),
                (
                    center_x + size,
                    center_y - size
                ),
                (
                    center_x - size,
                    center_y + size
                ),
                6
            )


# ============================================================
# RESET
# ============================================================

def reset():

    global pinch_start_time

    global capture_rect_camera
    global capture_rect_screen

    global captured_colour
    global captured_bw
    global final_photo

    global snap_effect_start
    global snap_effect_slot

    global wrong_effect_start
    global wrong_effect_slot

    global last_hand_seen_time

    global smooth_drag_x
    global smooth_drag_y

    global mouse_dragging
    global mouse_x
    global mouse_y

    global fist_start_time

    global shatter_particles

    # Capture
    pinch_start_time = None

    capture_rect_camera = None
    capture_rect_screen = None

    captured_colour = None
    captured_bw = None
    final_photo = None

    # Puzzle feedback
    snap_effect_start = None
    snap_effect_slot = None

    wrong_effect_start = None
    wrong_effect_slot = None

    # Hand tracking
    last_hand_seen_time = None

    smooth_drag_x = None
    smooth_drag_y = None

    # Mouse
    mouse_dragging = False

    mouse_x = None
    mouse_y = None

    # Ending
    fist_start_time = None

    shatter_particles = []

    # Puzzle data
    puzzle.cancel_drag()

    puzzle.original_image = None
    puzzle.pieces = []
    puzzle.slots = []

    puzzle.completed = False
    puzzle.was_pinching = False

    puzzle.just_snapped_slot = None

    puzzle.last_drop_correct = None
    puzzle.last_drop_slot = None

    change_state(
        LIVE
    )


# ============================================================
# MAIN LOOP
# ============================================================

while running:

    # ========================================================
    # EVENTS
    # ========================================================

    for event in pygame.event.get():

        # ====================================================
        # CLOSE
        # ====================================================

        if event.type == pygame.QUIT:

            running = False

        # ====================================================
        # KEYBOARD
        # ====================================================

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_q:

                running = False

            elif event.key == pygame.K_r:

                reset()

        # ====================================================
        # LEFT CLICK -> PICK UP
        # ====================================================

        elif (
            event.type
            == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and state == PUZZLE
            and not mouse_dragging
            and puzzle.dragged_piece is None
        ):

            mouse_x, mouse_y = (
                event.pos
            )

            puzzle_position = (
                screen_to_puzzle(
                    mouse_x,
                    mouse_y
                )
            )

            if puzzle_position is not None:

                puzzle_x, puzzle_y = (
                    puzzle_position
                )

                picked_up = (
                    puzzle.start_drag(
                        puzzle_x,
                        puzzle_y
                    )
                )

                if picked_up:

                    mouse_dragging = True

                    # Mouse directly owns the drag now.
                    puzzle.was_pinching = False

                    smooth_drag_x = (
                        mouse_x
                    )

                    smooth_drag_y = (
                        mouse_y
                    )

        # ====================================================
        # MOUSE MOVE
        # ====================================================

        elif (
            event.type
            == pygame.MOUSEMOTION
            and mouse_dragging
            and state == PUZZLE
        ):

            mouse_x, mouse_y = (
                event.pos
            )

        # ====================================================
        # LEFT RELEASE -> DROP
        # ====================================================

        elif (
            event.type
            == pygame.MOUSEBUTTONUP
            and event.button == 1
            and mouse_dragging
            and state == PUZZLE
        ):

            mouse_x, mouse_y = (
                event.pos
            )

            puzzle_position = (
                screen_to_puzzle(
                    mouse_x,
                    mouse_y
                )
            )

            if puzzle_position is not None:

                puzzle_x, puzzle_y = (
                    puzzle_position
                )

                snapped = (
                    puzzle.release_drag(
                        puzzle_x,
                        puzzle_y
                    )
                )

                # =============================================
                # CORRECT
                # =============================================

                if snapped:

                    snap_effect_start = (
                        time.time()
                    )

                    snap_effect_slot = (
                        puzzle.just_snapped_slot
                    )

                    wrong_effect_start = None
                    wrong_effect_slot = None

                # =============================================
                # WRONG
                # =============================================

                else:

                    if (
                        puzzle.last_drop_slot
                        is not None
                    ):

                        wrong_effect_start = (
                            time.time()
                        )

                        wrong_effect_slot = (
                            puzzle.last_drop_slot
                        )

                    snap_effect_start = None
                    snap_effect_slot = None

            else:

                # Released outside puzzle
                puzzle.cancel_drag()

            mouse_dragging = False

            smooth_drag_x = None
            smooth_drag_y = None

    # ========================================================
    # CAMERA
    # ========================================================

    frame = camera.get_frame()

    if frame is None:
        break

    raw_frame = frame.copy()

    tracked_frame, hands = (
        hand_tracker.detect(
            frame
        )
    )

    # ========================================================
    # BACKGROUND
    # ========================================================

    ui.clear()

    ui.draw_camera(
        raw_frame
    )

    # ========================================================
    # LIVE
    # ========================================================

    if state == LIVE:

        hand_rect = (
            hand_tracker.get_hand_frame(
                hands,
                frame.shape
            )
        )

        screen_rect = (
            camera_to_screen_rect(
                hand_rect,
                frame.shape
            )
        )

        # ====================================================
        # MINIMUM CAPTURE SIZE
        # ====================================================

        capture_large_enough = False

        if hand_rect is not None:

            hx1, hy1, hx2, hy2 = (
                hand_rect
            )

            capture_width = (
                hx2 - hx1
            )

            capture_height = (
                hy2 - hy1
            )

            capture_large_enough = (
                capture_width
                >= MIN_CAPTURE_WIDTH
                and
                capture_height
                >= MIN_CAPTURE_HEIGHT
            )

        # ====================================================
        # BOTH HANDS PINCH
        # ====================================================

        both_pinching = (
            len(hands) == 2
            and hands[0]["pinching"]
            and hands[1]["pinching"]
        )

        pinch_progress = 0.0

        if (
            hand_rect is not None
            and both_pinching
            and capture_large_enough
        ):

            if pinch_start_time is None:

                pinch_start_time = (
                    time.time()
                )

            hold_time = (
                time.time()
                - pinch_start_time
            )

            pinch_progress = min(
                hold_time
                / PINCH_HOLD_TIME,
                1.0
            )

            if (
                hold_time
                >= PINCH_HOLD_TIME
            ):

                capture_rect_camera = (
                    hand_rect
                )

                capture_rect_screen = (
                    screen_rect
                )

                pinch_start_time = None

                change_state(
                    COUNTDOWN
                )

        else:

            pinch_start_time = None

        # ====================================================
        # FRAME
        # ====================================================

        ui.draw_capture_frame(
            screen_rect,
            pinch_progress
        )

        # ====================================================
        # LIVE INSTRUCTIONS
        # ====================================================

        if (
            hand_rect is not None
            and not capture_large_enough
        ):

            ui.draw_text(
                "MOVE HANDS FURTHER APART",
                (
                    WIDTH // 2,
                    HEIGHT - 70
                ),
                ui.font_medium,
                (255, 214, 10),
                center=True
            )

        elif both_pinching:

            ui.draw_text(
                "HOLD IT...",
                (
                    WIDTH // 2,
                    HEIGHT - 78
                ),
                ui.font_medium,
                (255, 214, 10),
                center=True
            )

            ui.draw_hold_bar(
                pinch_progress
            )

        else:

            ui.draw_text(
                "FRAME YOUR PHOTO WITH TWO HANDS",
                (
                    WIDTH // 2,
                    HEIGHT - 80
                ),
                ui.font_medium,
                (245, 245, 245),
                center=True
            )

            ui.draw_text(
                "PINCH BOTH HANDS TO CAPTURE",
                (
                    WIDTH // 2,
                    HEIGHT - 45
                ),
                ui.font_small,
                (255, 214, 10),
                center=True
            )

        ui.draw_header()

    # ========================================================
    # COUNTDOWN
    # ========================================================

    elif state == COUNTDOWN:

        ui.draw_dark_overlay(
            60
        )

        ui.draw_capture_frame(
            capture_rect_screen,
            1.0
        )

        elapsed = (
            time.time()
            - state_start_time
        )

        number = (
            COUNTDOWN_SECONDS
            - int(elapsed)
        )

        phase = (
            elapsed % 1.0
        )

        if number > 0:

            ui.draw_countdown(
                number,
                phase
            )

        else:

            x1, y1, x2, y2 = (
                capture_rect_camera
            )

            captured_colour = (
                raw_frame[
                    y1:y2,
                    x1:x2
                ].copy()
            )

            puzzle.create_puzzle(
                captured_colour
            )

            captured_bw = (
                puzzle.original_image.copy()
            )

            final_photo = (
                captured_bw.copy()
            )

            change_state(
                FLASH
            )

    # ========================================================
    # FLASH
    # ========================================================

    elif state == FLASH:

        elapsed = (
            time.time()
            - state_start_time
        )

        progress = (
            elapsed
            / FLASH_DURATION
        )

        ui.draw_flash(
            1.0 - progress
        )

        if (
            elapsed
            >= FLASH_DURATION
        ):

            change_state(
                BW_TRANSITION
            )

    # ========================================================
    # B&W TRANSITION
    # ========================================================

    elif state == BW_TRANSITION:

        elapsed = (
            time.time()
            - state_start_time
        )

        progress = min(
            elapsed
            / BW_TRANSITION_DURATION,
            1.0
        )

        ui.draw_photo_transition(
            captured_colour,
            captured_bw,
            capture_rect_screen,
            progress
        )

        ui.draw_capture_frame(
            capture_rect_screen,
            1.0
        )

        ui.draw_text(
            "SNAP!",
            (
                WIDTH // 2,
                110
            ),
            ui.font_large,
            (255, 214, 10),
            center=True
        )

        if progress >= 1.0:

            change_state(
                PHOTO_HOLD
            )

    # ========================================================
    # REMEMBER PHOTO
    # ========================================================

    elif state == PHOTO_HOLD:

        ui.draw_photo(
            captured_bw,
            capture_rect_screen
        )

        ui.draw_capture_frame(
            capture_rect_screen,
            1.0
        )

        ui.draw_text(
            "REMEMBER THIS!",
            (
                WIDTH // 2,
                105
            ),
            ui.font_medium,
            (255, 214, 10),
            center=True
        )

        elapsed = (
            time.time()
            - state_start_time
        )

        if (
            elapsed
            >= PHOTO_HOLD_DURATION
        ):

            change_state(
                GRID_FORM
            )

    # ========================================================
    # GRID FORM
    # ========================================================

    elif state == GRID_FORM:

        ui.draw_photo(
            captured_bw,
            capture_rect_screen
        )

        elapsed = (
            time.time()
            - state_start_time
        )

        progress = min(
            elapsed
            / GRID_DURATION,
            1.0
        )

        ui.draw_grid(
            capture_rect_screen,
            progress
        )

        if progress >= 1.0:

            change_state(
                SHUFFLE
            )

    # ========================================================
    # SHUFFLE
    # ========================================================

    elif state == SHUFFLE:

        elapsed = (
            time.time()
            - state_start_time
        )

        progress = min(
            elapsed
            / SHUFFLE_DURATION,
            1.0
        )

        ui.draw_shuffle(
            puzzle,
            capture_rect_screen,
            progress
        )

        ui.draw_text(
            "SHUFFLING...",
            (
                WIDTH // 2,
                105
            ),
            ui.font_medium,
            (255, 214, 10),
            center=True
        )

        if progress >= 1.0:

            puzzle.was_pinching = False

            change_state(
                SOLVE_INTRO
            )

    # ========================================================
    # SOLVE INTRO
    # ========================================================

    elif state == SOLVE_INTRO:

        # Draw completely shuffled puzzle
        ui.draw_shuffle(
            puzzle,
            capture_rect_screen,
            1.0
        )

        elapsed = (
            time.time()
            - state_start_time
        )

        progress = min(
            elapsed
            / SOLVE_INTRO_DURATION,
            1.0
        )

        # ====================================================
        # FADE SOLVE IT
        # ====================================================

        if progress < 0.75:

            text_color = (
                255,
                214,
                10
            )

        else:

            fade = (
                1.0
                - (
                    progress - 0.75
                ) / 0.25
            )

            fade = max(
                0.0,
                min(
                    fade,
                    1.0
                )
            )

            text_color = (
                int(255 * fade),
                int(214 * fade),
                0
            )

        # Center SOLVE IT relative to puzzle frame
        if capture_rect_screen is not None:

            cx1, cy1, cx2, cy2 = (
                capture_rect_screen
            )

            puzzle_center_x = (
                cx1 + cx2
            ) // 2

            puzzle_center_y = (
                cy1 + cy2
            ) // 2

        else:

            puzzle_center_x = (
                WIDTH // 2
            )

            puzzle_center_y = (
                HEIGHT // 2
            )

        ui.draw_text(
            "SOLVE IT!",
            (
                puzzle_center_x,
                puzzle_center_y
            ),
            ui.font_large,
            text_color,
            center=True
        )

        ui.draw_text(
            "0 / 9",
            (
                puzzle_center_x,
                65
            ),
            ui.font_large,
            (255, 214, 10),
            center=True
        )

        if progress >= 1.0:

            puzzle.was_pinching = False

            last_hand_seen_time = None

            smooth_drag_x = None
            smooth_drag_y = None

            mouse_dragging = False

            change_state(
                PUZZLE
            )

    # ========================================================
    # PUZZLE
    # ========================================================

    elif state == PUZZLE:

        # Real fingertip position
        finger_screen_x = None
        finger_screen_y = None

        pinching = False

        # ====================================================
        # HAND CONTROL
        #
        # Mouse gets priority while mouse dragging.
        # ====================================================

        if (
            len(hands) > 0
            and not mouse_dragging
        ):

            last_hand_seen_time = (
                time.time()
            )

            camera_x, camera_y = (
                hands[0]["points"][8]
            )

            frame_height, frame_width, _ = (
                frame.shape
            )

            finger_screen_x = (
                camera_x
                / frame_width
                * WIDTH
            )

            finger_screen_y = (
                camera_y
                / frame_height
                * HEIGHT
            )

            pinching = (
                hands[0]["pinching"]
            )

            # =================================================
            # REAL POSITION FOR GAME LOGIC
            # =================================================

            puzzle_position = (
                screen_to_puzzle(
                    finger_screen_x,
                    finger_screen_y
                )
            )

            if puzzle_position is not None:

                puzzle_x, puzzle_y = (
                    puzzle_position
                )

                was_dragging = (
                    puzzle.dragged_piece
                    is not None
                )

                was_pinching = (
                    puzzle.was_pinching
                )

                snapped = (
                    puzzle.update_drag(
                        puzzle_x,
                        puzzle_y,
                        pinching
                    )
                )

                released_now = (
                    was_dragging
                    and was_pinching
                    and not pinching
                )

                # =============================================
                # HAND RELEASE FEEDBACK
                # =============================================

                if released_now:

                    if snapped:

                        snap_effect_start = (
                            time.time()
                        )

                        snap_effect_slot = (
                            puzzle.just_snapped_slot
                        )

                        wrong_effect_start = None
                        wrong_effect_slot = None

                    else:

                        if (
                            puzzle.last_drop_slot
                            is not None
                        ):

                            wrong_effect_start = (
                                time.time()
                            )

                            wrong_effect_slot = (
                                puzzle.last_drop_slot
                            )

                        snap_effect_start = None
                        snap_effect_slot = None

            # =================================================
            # SMOOTH HAND VISUAL DRAG
            # =================================================

            if (
                puzzle.dragged_piece
                is not None
            ):

                if (
                    smooth_drag_x is None
                    or smooth_drag_y is None
                ):

                    smooth_drag_x = (
                        finger_screen_x
                    )

                    smooth_drag_y = (
                        finger_screen_y
                    )

                else:

                    smooth_drag_x += (
                        finger_screen_x
                        - smooth_drag_x
                    ) * DRAG_SMOOTHING

                    smooth_drag_y += (
                        finger_screen_y
                        - smooth_drag_y
                    ) * DRAG_SMOOTHING

            else:

                smooth_drag_x = (
                    finger_screen_x
                )

                smooth_drag_y = (
                    finger_screen_y
                )

        # ====================================================
        # HAND LOST
        # ====================================================

        elif (
            not mouse_dragging
        ):

            if (
                last_hand_seen_time
                is not None
            ):

                lost_duration = (
                    time.time()
                    - last_hand_seen_time
                )

                if (
                    lost_duration
                    > TRACKING_GRACE_TIME
                ):

                    puzzle.cancel_drag()

                    smooth_drag_x = None
                    smooth_drag_y = None

        # ====================================================
        # MOUSE VISUAL SMOOTHING
        # ====================================================

        if (
            mouse_dragging
            and mouse_x is not None
            and mouse_y is not None
        ):

            if (
                smooth_drag_x is None
                or smooth_drag_y is None
            ):

                smooth_drag_x = (
                    mouse_x
                )

                smooth_drag_y = (
                    mouse_y
                )

            else:

                smooth_drag_x += (
                    mouse_x
                    - smooth_drag_x
                ) * DRAG_SMOOTHING

                smooth_drag_y += (
                    mouse_y
                    - smooth_drag_y
                ) * DRAG_SMOOTHING

        # ====================================================
        # DRAW PUZZLE
        # ====================================================

        draw_interactive_puzzle(
            smooth_drag_x,
            smooth_drag_y
        )

        # ====================================================
        # HAND CURSOR
        # ====================================================

        if (
            not mouse_dragging
            and finger_screen_x is not None
            and finger_screen_y is not None
        ):

            cursor = (
                int(finger_screen_x),
                int(finger_screen_y)
            )

            if pinching:

                pygame.draw.circle(
                    ui.screen,
                    (255, 214, 10),
                    cursor,
                    10
                )

            else:

                pygame.draw.circle(
                    ui.screen,
                    (245, 245, 245),
                    cursor,
                    11,
                    3
                )

        # ====================================================
        # PROGRESS
        # ====================================================

        current_progress = (
            puzzle.get_progress()
        )

        if capture_rect_screen is not None:

            px1, py1, px2, py2 = (
                capture_rect_screen
            )

            puzzle_center_x = (
                px1 + px2
            ) // 2

        else:

            puzzle_center_x = (
                WIDTH // 2
            )

        ui.draw_text(
            f"{current_progress} / 9",
            (
                puzzle_center_x,
                65
            ),
            ui.font_large,
            (255, 214, 10),
            center=True
        )

        # ====================================================
        # INSTRUCTIONS
        # ====================================================

        if (
            puzzle.dragged_piece
            is not None
        ):

            ui.draw_text(
                "WHERE DOES IT BELONG?",
                (
                    WIDTH // 2,
                    HEIGHT - 60
                ),
                ui.font_medium,
                (245, 245, 245),
                center=True
            )

        else:

            ui.draw_text(
                "PINCH OR CLICK • MOVE • RELEASE",
                (
                    WIDTH // 2,
                    HEIGHT - 60
                ),
                ui.font_medium,
                (245, 245, 245),
                center=True
            )

        # ====================================================
        # COMPLETED
        # ====================================================

        if puzzle.completed:

            # Wait for final check animation
            if (
                snap_effect_start is None
                or time.time()
                - snap_effect_start
                >= SNAP_EFFECT_DURATION
            ):

                smooth_drag_x = None
                smooth_drag_y = None

                mouse_dragging = False

                change_state(
                    COMPLETE_REVEAL
                )

    # ========================================================
    # COMPLETE REVEAL
    # ========================================================

    elif state == COMPLETE_REVEAL:

        elapsed = (
            time.time()
            - state_start_time
        )

        progress = min(
            elapsed
            / COMPLETE_REVEAL_DURATION,
            1.0
        )

        ui.draw_completion_reveal(
            final_photo,
            capture_rect_screen,
            progress
        )

        if capture_rect_screen is not None:

            rx1, ry1, rx2, ry2 = (
                capture_rect_screen
            )

            complete_center_x = (
                rx1 + rx2
            ) // 2

        else:

            complete_center_x = (
                WIDTH // 2
            )

        ui.draw_text(
            "PUZZLE COMPLETE!",
            (
                complete_center_x,
                105
            ),
            ui.font_large,
            (255, 214, 10),
            center=True
        )

        if progress >= 1.0:

            fist_start_time = None

            change_state(
                FIST_HOLD
            )

    # ========================================================
    # FIST HOLD
    # ========================================================

    elif state == FIST_HOLD:

        ui.draw_photo(
            final_photo,
            capture_rect_screen
        )

        ui.draw_capture_frame(
            capture_rect_screen,
            1.0
        )

        ui.draw_dark_overlay(
            25
        )

        if capture_rect_screen is not None:

            fx1, fy1, fx2, fy2 = (
                capture_rect_screen
            )

            fist_center_x = (
                fx1 + fx2
            ) // 2

        else:

            fist_center_x = (
                WIDTH // 2
            )

        ui.draw_text(
            "PUZZLE COMPLETE!",
            (
                fist_center_x,
                105
            ),
            ui.font_large,
            (255, 214, 10),
            center=True
        )

        ui.draw_text(
            "MAKE A FIST TO FINISH",
            (
                WIDTH // 2,
                HEIGHT - 90
            ),
            ui.font_medium,
            (245, 245, 245),
            center=True
        )

        # ====================================================
        # FIST DETECTION
        # ====================================================

        fist_detected = any(
            hand["fist"]
            for hand in hands
        )

        fist_progress = 0.0

        if fist_detected:

            if fist_start_time is None:

                fist_start_time = (
                    time.time()
                )

            fist_elapsed = (
                time.time()
                - fist_start_time
            )

            fist_progress = min(
                fist_elapsed
                / FIST_HOLD_DURATION,
                1.0
            )

            ui.draw_text(
                "HOLD...",
                (
                    WIDTH // 2,
                    HEIGHT - 60
                ),
                ui.font_small,
                (255, 214, 10),
                center=True
            )

            if fist_progress >= 1.0:

                shatter_particles = (
                    ui.create_shatter_particles(
                        final_photo,
                        capture_rect_screen,
                        rows=6,
                        cols=6
                    )
                )

                fist_start_time = None

                change_state(
                    SHATTER
                )

        else:

            fist_start_time = None

        ui.draw_hold_bar(
            fist_progress
        )

    # ========================================================
    # SHATTER
    # ========================================================

    elif state == SHATTER:

        elapsed = (
            time.time()
            - state_start_time
        )

        # Dark background so fragments stand out
        ui.draw_dark_overlay(
            70
        )

        ui.draw_shatter(
            shatter_particles,
            elapsed
        )

        # ====================================================
        # AUTOMATIC RESTART
        # ====================================================

        if (
            elapsed
            >= SHATTER_DURATION
        ):

            reset()

    # ========================================================
    # DISPLAY
    # ========================================================

    ui.update()


# ============================================================
# CLEANUP
# ============================================================

camera.release()
hand_tracker.close()
ui.close()