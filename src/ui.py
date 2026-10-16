import cv2
import pygame
import numpy as np
import random

from src.animations import (
    clamp,
    lerp,
    ease_out_cubic,
    ease_out_back
)

BLACK = (10, 10, 10)
WHITE = (245, 245, 245)
YELLOW = (255, 214, 10)
GREY = (160, 160, 160)
DARK_GREY = (45, 45, 45)

class PuzzleUI:
    def __init__(
        self,
        width=1280,
        height=720
    ):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode(
            (width, height)
        )
        pygame.display.set_caption(
            "PuzzleCam"
        )
        self.clock = pygame.time.Clock()
        self.font_small = pygame.font.SysFont(
            "arial",
            20
        )
        self.font_medium = pygame.font.SysFont(
            "arial",
            30,
            bold=True
        )
        self.font_large = pygame.font.SysFont(
            "arial",
            64,
            bold=True
        )
        self.font_huge = pygame.font.SysFont(
            "arial",
            150,
            bold=True
        )

    # ========================================================
    # BASIC
    # ========================================================
    def clear(self):
        self.screen.fill(
            BLACK
        )
    def update(self):
        pygame.display.flip()
        self.clock.tick(
            60
        )
    def close(self):
        pygame.quit()

    # ========================================================
    # OPENCV -> PYGAME
    # ========================================================
    def cv_to_surface(
        self,
        frame
    ):
        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )
        rgb = np.ascontiguousarray(
            rgb
        )
        return pygame.image.frombuffer(
            rgb.tobytes(),
            (
                rgb.shape[1],
                rgb.shape[0]
            ),
            "RGB"
        ).copy()

    # ========================================================
    # TEXT
    # ========================================================
    def draw_text(
        self,
        text,
        position,
        font=None,
        color=WHITE,
        center=False
    ):
        if font is None:
            font = self.font_small
        surface = font.render(
            text,
            True,
            color
        )
        rect = surface.get_rect()
        if center:
            rect.center = position
        else:
            rect.topleft = position
        self.screen.blit(
            surface,
            rect
        )

    # ========================================================
    # CAMERA
    # ========================================================
    def draw_camera(
        self,
        frame
    ):
        surface = (
            self.cv_to_surface(
                frame
            )
        )
        surface = (
            pygame.transform.smoothscale(
                surface,
                (
                    self.width,
                    self.height
                )
            )
        )
        self.screen.blit(
            surface,
            (0, 0)
        )

    # ========================================================
    # DARK OVERLAY
    # ========================================================
    def draw_dark_overlay(
        self,
        alpha=80
    ):
        overlay = pygame.Surface(
            (
                self.width,
                self.height
            ),
            pygame.SRCALPHA
        )
        overlay.fill(
            (
                0,
                0,
                0,
                alpha
            )
        )
        self.screen.blit(
            overlay,
            (0, 0)
        )

    # ========================================================
    # HEADER
    # ========================================================
    def draw_header(self):
        panel = pygame.Surface(
            (
                self.width,
                90
            ),
            pygame.SRCALPHA
        )
        panel.fill(
            (
                0,
                0,
                0,
                125
            )
        )
        self.screen.blit(
            panel,
            (0, 0)
        )
        self.draw_text(
            "PUZZLECAM",
            (32, 20),
            self.font_medium,
            YELLOW
        )
        self.draw_text(
            "HAND GESTURE PHOTO PUZZLE",
            (32, 57),
            self.font_small,
            WHITE
        )
        pygame.draw.circle(
            self.screen,
            YELLOW,
            (
                self.width - 94,
                35
            ),
            6
        )
        self.draw_text(
            "LIVE",
            (
                self.width - 76,
                23
            ),
            self.font_small,
            WHITE
        )

    # ========================================================
    # CAPTURE FRAME
    # ========================================================
    def draw_capture_frame(
        self,
        rect,
        pinch_progress=0.0
    ):
        if rect is None:
            return
        x1, y1, x2, y2 = rect
        pinch_progress = clamp(
            pinch_progress
        )
        thickness = int(
            lerp(
                3,
                8,
                pinch_progress
            )
        )
        pygame.draw.rect(
            self.screen,
            YELLOW,
            (
                x1,
                y1,
                x2 - x1,
                y2 - y1
            ),
            thickness,
            border_radius=8
        )
        corner_length = 30
        corners = [
            (
                (x1, y1),
                (
                    x1 + corner_length,
                    y1
                )
            ),
            (
                (x1, y1),
                (
                    x1,
                    y1 + corner_length
                )
            ),
            (
                (x2, y1),
                (
                    x2 - corner_length,
                    y1
                )
            ),
            (
                (x2, y1),
                (
                    x2,
                    y1 + corner_length
                )
            ),
            (
                (x1, y2),
                (
                    x1 + corner_length,
                    y2
                )
            ),
            (
                (x1, y2),
                (
                    x1,
                    y2 - corner_length
                )
            ),
            (
                (x2, y2),
                (
                    x2 - corner_length,
                    y2
                )
            ),
            (
                (x2, y2),
                (
                    x2,
                    y2 - corner_length
                )
            )
        ]
        for start, end in corners:
            pygame.draw.line(
                self.screen,
                WHITE,
                start,
                end,
                4
            )

    # ========================================================
    # HOLD BAR
    # ========================================================
    def draw_hold_bar(
        self,
        progress
    ):
        progress = clamp(
            progress
        )
        width = 320
        height = 12
        x = (
            self.width // 2
            - width // 2
        )
        y = (
            self.height - 45
        )
        pygame.draw.rect(
            self.screen,
            DARK_GREY,
            (
                x,
                y,
                width,
                height
            ),
            border_radius=6
        )
        fill_width = int(
            width * progress
        )
        if fill_width > 0:
            pygame.draw.rect(
                self.screen,
                YELLOW,
                (
                    x,
                    y,
                    fill_width,
                    height
                ),
                border_radius=6
            )

    # ========================================================
    # COUNTDOWN
    # ========================================================
    def draw_countdown(
        self,
        number,
        phase
    ):
        phase = clamp(
            phase
        )
        animation = (
            ease_out_back(
                phase
            )
        )
        scale = lerp(
            1.5,
            1.0,
            animation
        )
        text_surface = (
            self.font_huge.render(
                str(number),
                True,
                YELLOW
            )
        )
        new_width = max(
            1,
            int(
                text_surface.get_width()
                * scale
            )
        )
        new_height = max(
            1,
            int(
                text_surface.get_height()
                * scale
            )
        )
        text_surface = (
            pygame.transform.smoothscale(
                text_surface,
                (
                    new_width,
                    new_height
                )
            )
        )
        rect = (
            text_surface.get_rect(
                center=(
                    self.width // 2,
                    self.height // 2
                )
            )
        )
        self.screen.blit(
            text_surface,
            rect
        )

    # ========================================================
    # FLASH
    # ========================================================
    def draw_flash(
        self,
        strength
    ):
        strength = clamp(
            strength
        )
        overlay = pygame.Surface(
            (
                self.width,
                self.height
            ),
            pygame.SRCALPHA
        )
        overlay.fill(
            (
                255,
                255,
                255,
                int(
                    255 * strength
                )
            )
        )
        self.screen.blit(
            overlay,
            (0, 0)
        )

    # ========================================================
    # PHOTO
    # ========================================================
    def draw_photo(
        self,
        image,
        rect
    ):
        if (
            image is None
            or
            rect is None
        ):
            return
        x1, y1, x2, y2 = rect
        surface = (
            self.cv_to_surface(
                image
            )
        )
        surface = (
            pygame.transform.smoothscale(
                surface,
                (
                    x2 - x1,
                    y2 - y1
                )
            )
        )
        self.screen.blit(
            surface,
            (
                x1,
                y1
            )
        )

    # ========================================================
    # PHOTO TRANSITION
    # ========================================================
    def draw_photo_transition(
        self,
        colour_image,
        bw_image,
        rect,
        progress
    ):
        if (
            colour_image is None
            or
            bw_image is None
            or
            rect is None
        ):
            return
        progress = clamp(
            progress
        )
        x1, y1, x2, y2 = rect
        width = x2 - x1
        height = y2 - y1
        colour_surface = (
            self.cv_to_surface(
                colour_image
            )
        )
        bw_surface = (
            self.cv_to_surface(
                bw_image
            )
        )
        colour_surface = (
            pygame.transform.smoothscale(
                colour_surface,
                (
                    width,
                    height
                )
            )
        )
        bw_surface = (
            pygame.transform.smoothscale(
                bw_surface,
                (
                    width,
                    height
                )
            )
        )
        self.screen.blit(
            colour_surface,
            (
                x1,
                y1
            )
        )
        bw_surface.set_alpha(
            int(
                255 * progress
            )
        )
        self.screen.blit(
            bw_surface,
            (
                x1,
                y1
            )
        )

    # ========================================================
    # GRID
    # ========================================================
    def draw_grid(
        self,
        rect,
        progress
    ):
        if rect is None:
            return
        progress = (
            ease_out_cubic(
                clamp(
                    progress
                )
            )
        )
        x1, y1, x2, y2 = rect
        width = x2 - x1
        height = y2 - y1
        for i in range(
            1,
            3
        ):
            x = int(
                x1
                + width * i / 3
            )
            line_height = int(
                height * progress
            )
            pygame.draw.line(
                self.screen,
                WHITE,
                (
                    x,
                    y1
                ),
                (
                    x,
                    y1 + line_height
                ),
                3
            )
        for i in range(
            1,
            3
        ):
            y = int(
                y1
                + height * i / 3
            )
            line_width = int(
                width * progress
            )
            pygame.draw.line(
                self.screen,
                WHITE,
                (
                    x1,
                    y
                ),
                (
                    x1 + line_width,
                    y
                ),
                3
            )
        pygame.draw.rect(
            self.screen,
            YELLOW,
            (
                x1,
                y1,
                width,
                height
            ),
            3,
            border_radius=5
        )

    # ========================================================
    # SHUFFLE
    # ========================================================
    def draw_shuffle(
        self,
        puzzle,
        rect,
        progress
    ):
        if (
            puzzle.original_image is None
            or
            rect is None
        ):
            return
        progress = (
            ease_out_cubic(
                clamp(
                    progress
                )
            )
        )
        x1, y1, x2, y2 = rect
        display_width = x2 - x1
        display_height = y2 - y1
        cell_width = (
            display_width / 3
        )
        cell_height = (
            display_height / 3
        )
        for final_slot, piece in enumerate(
            puzzle.slots
        ):
            if piece is None:
                continue
            original_row = (
                piece["correct_row"]
            )
            original_col = (
                piece["correct_col"]
            )
            final_row = (
                final_slot // 3
            )
            final_col = (
                final_slot % 3
            )
            start_x = (
                x1
                + original_col
                * cell_width
            )
            start_y = (
                y1
                + original_row
                * cell_height
            )
            end_x = (
                x1
                + final_col
                * cell_width
            )
            end_y = (
                y1
                + final_row
                * cell_height
            )
            current_x = lerp(
                start_x,
                end_x,
                progress
            )
            current_y = lerp(
                start_y,
                end_y,
                progress
            )
            piece_surface = (
                self.cv_to_surface(
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
            self.screen.blit(
                piece_surface,
                (
                    int(current_x),
                    int(current_y)
                )
            )
            pygame.draw.rect(
                self.screen,
                WHITE,
                (
                    int(current_x),
                    int(current_y),
                    int(cell_width),
                    int(cell_height)
                ),
                2
            )

    # ========================================================
    # COMPLETION REVEAL
    # ========================================================
    def draw_completion_reveal(
        self,
        image,
        rect,
        progress
    ):
        if (
            image is None
            or
            rect is None
        ):
            return
        progress = clamp(
            progress
        )
        x1, y1, x2, y2 = rect
        width = (
            x2 - x1
        )
        height = (
            y2 - y1
        )
        # Photo
        self.draw_photo(
            image,
            rect
        )
        # Grid fades away
        grid_alpha = int(
            255
            * (
                1.0 - progress
            )
        )
        if grid_alpha > 0:
            grid_surface = pygame.Surface(
                (
                    width,
                    height
                ),
                pygame.SRCALPHA
            )
            for i in range(
                1,
                3
            ):
                gx = int(
                    width * i / 3
                )
                pygame.draw.line(
                    grid_surface,
                    (
                        255,
                        255,
                        255,
                        grid_alpha
                    ),
                    (
                        gx,
                        0
                    ),
                    (
                        gx,
                        height
                    ),
                    3
                )
            for i in range(
                1,
                3
            ):
                gy = int(
                    height * i / 3
                )
                pygame.draw.line(
                    grid_surface,
                    (
                        255,
                        255,
                        255,
                        grid_alpha
                    ),
                    (
                        0,
                        gy
                    ),
                    (
                        width,
                        gy
                    ),
                    3
                )
            self.screen.blit(
                grid_surface,
                (
                    x1,
                    y1
                )
            )
        # Yellow border settles around full photo
        border_width = int(
            lerp(
                8,
                3,
                progress
            )
        )
        pygame.draw.rect(
            self.screen,
            YELLOW,
            (
                x1,
                y1,
                width,
                height
            ),
            border_width,
            border_radius=6
        )

    # ========================================================
    # CREATE SHATTER PARTICLES
    # ========================================================
    def create_shatter_particles(
        self,
        image,
        rect,
        rows=6,
        cols=6
    ):
        particles = []
        if (
            image is None
            or
            rect is None
        ):
            return particles
        x1, y1, x2, y2 = rect
        display_width = (
            x2 - x1
        )
        display_height = (
            y2 - y1
        )
        image_height, image_width, _ = (
            image.shape
        )
        source_piece_width = (
            image_width // cols
        )
        source_piece_height = (
            image_height // rows
        )
        display_piece_width = (
            display_width / cols
        )
        display_piece_height = (
            display_height / rows
        )
        center_x = (
            x1
            + display_width / 2
        )
        center_y = (
            y1
            + display_height / 2
        )
        for row in range(
            rows
        ):
            for col in range(
                cols
            ):
                sx1 = (
                    col
                    * source_piece_width
                )
                sy1 = (
                    row
                    * source_piece_height
                )
                if col == cols - 1:
                    sx2 = (
                        image_width
                    )
                else:
                    sx2 = (
                        sx1
                        + source_piece_width
                    )
                if row == rows - 1:
                    sy2 = (
                        image_height
                    )
                else:
                    sy2 = (
                        sy1
                        + source_piece_height
                    )
                fragment_image = (
                    image[
                        sy1:sy2,
                        sx1:sx2
                    ].copy()
                )
                surface = (
                    self.cv_to_surface(
                        fragment_image
                    )
                )
                surface = (
                    pygame.transform.smoothscale(
                        surface,
                        (
                            max(
                                1,
                                int(
                                    display_piece_width
                                )
                            ),
                            max(
                                1,
                                int(
                                    display_piece_height
                                )
                            )
                        )
                    )
                )
                start_x = (
                    x1
                    + col
                    * display_piece_width
                )
                start_y = (
                    y1
                    + row
                    * display_piece_height
                )
                fragment_center_x = (
                    start_x
                    + display_piece_width / 2
                )
                fragment_center_y = (
                    start_y
                    + display_piece_height / 2
                )
                dx = (
                    fragment_center_x
                    - center_x
                )
                dy = (
                    fragment_center_y
                    - center_y
                )
                distance = max(
                    (
                        dx * dx
                        + dy * dy
                    ) ** 0.5,
                    1.0
                )
                direction_x = (
                    dx / distance
                )
                direction_y = (
                    dy / distance
                )
                speed = random.uniform(
                    230,
                    440
                )
                velocity_x = (
                    direction_x
                    * speed
                    + random.uniform(
                        -100,
                        100
                    )
                )
                velocity_y = (
                    direction_y
                    * speed
                    + random.uniform(
                        -170,
                        20
                    )
                )
                particles.append(
                    {
                        "surface": surface,
                        "x": start_x,
                        "y": start_y,
                        "vx": velocity_x,
                        "vy": velocity_y,
                        "angle": 0.0,
                        "angular_velocity":
                            random.uniform(
                                -220,
                                220
                            )
                    }
                )
        return particles

    # ========================================================
    # DRAW SHATTER
    # ========================================================
    def draw_shatter(
        self,
        particles,
        elapsed
    ):
        gravity = 700.0
        for particle in particles:
            x = (
                particle["x"]
                + particle["vx"]
                * elapsed
            )
            y = (
                particle["y"]
                + particle["vy"]
                * elapsed
                + 0.5
                * gravity
                * elapsed
                * elapsed
            )
            angle = (
                particle["angle"]
                + particle[
                    "angular_velocity"
                ]
                * elapsed
            )
            rotated = (
                pygame.transform.rotate(
                    particle["surface"],
                    angle
                )
            )
            rect = (
                rotated.get_rect(
                    center=(
                        int(
                            x
                            + particle[
                                "surface"
                            ].get_width()
                            / 2
                        ),
                        int(
                            y
                            + particle[
                                "surface"
                            ].get_height()
                            / 2
                        )
                    )
                )
            )
            self.screen.blit(
                rotated,
                rect
            )
