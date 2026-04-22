import pygame

class Menu:
    def __init__(self):
        cx, cy = 400, 300 
        button_w, button_h = 240, 50

        self.start_btn = pygame.Rect(cx - button_w//2, cy - 120, button_w, button_h)
        self.data_btn  = pygame.Rect(cx - button_w//2, cy - 50,  button_w, button_h)
        self.sound_btn = pygame.Rect(cx - button_w//2, cy + 20,  button_w, button_h)
        self.exit_btn  = pygame.Rect(cx - button_w//2, cy + 90,  button_w, button_h)

        self.font = pygame.font.SysFont("Arial", 30, bold=True)

    def draw(self, screen):
        m_pos = pygame.mouse.get_pos()

        self.draw_styled_button(screen, "START FESTIVAL", self.start_btn, m_pos)
        self.draw_styled_button(screen, "VIEW DATA", self.data_btn, m_pos)
        self.draw_styled_button(screen, "ADJUST SONG", self.sound_btn, m_pos)
        self.draw_styled_button(screen, "EXIT GAME", self.exit_btn, m_pos)

    def draw_styled_button(self, screen, text, rect, m_pos):
        is_hovered = rect.collidepoint(m_pos)
        bg_color = (60, 100, 200) if is_hovered else (45, 45, 60)
        border_color = (255, 255, 255) if is_hovered else (100, 100, 100)

        pygame.draw.rect(screen, bg_color, rect, border_radius=10)
        pygame.draw.rect(screen, border_color, rect, 3, border_radius=10)

        text_surf = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)