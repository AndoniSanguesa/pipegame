from element import Element
import pygame as pg


class WinScreen(Element):
    def __init__(self, surf, font):
        super().__init__("win_screen")
        self.show = False
        self.surf = surf
        self.font = font
        self.no = None
        self.play_again = None

    def draw(self):
        if not self.show:
            return
        fill_surf = pg.Surface((self.surf.get_width(), self.surf.get_height()))
        fill_surf.set_alpha(90)
        fill_surf.fill((255, 255, 255))
        self.surf.blit(fill_surf, (0, 0))
        win_text = self.font.render("You Win!", (255, 255, 255), size=50)
        self.surf.blit(win_text[0], ((self.surf.get_width() / 2) - (win_text[1].w / 2), (self.surf.get_height() / 2) - (win_text[1].h / 2)))

        play_again_text = self.font.render("Play Again?", (255, 255, 255), size=30)
        no_text = self.font.render("No", (255, 255, 255), size=30)

        tot_width = (play_again_text[1].width + 40) * 2 + 40
        y_lvl = (self.surf.get_height() / 2) + (win_text[1].h / 2) + 40
        cur_x = (self.surf.get_width() / 2) - (tot_width / 2)

        play_again_rect = pg.Rect(cur_x, y_lvl, play_again_text[1].width + 40, play_again_text[1].height + 20)
        cur_x += play_again_text[1].width + 80
        no_rect = pg.Rect(cur_x, y_lvl, play_again_text[1].width + 40, play_again_text[1].height + 20)

        self.play_again = play_again_rect
        self.no = no_rect

        pg.draw.rect(self.surf, (0, 0, 0), play_again_rect, border_radius=15)
        pg.draw.rect(self.surf, (255, 255, 255), play_again_rect, width=4, border_radius=15)

        pg.draw.rect(self.surf, (0, 0, 0), no_rect, border_radius=15)
        pg.draw.rect(self.surf, (255, 255, 255), no_rect, width=4, border_radius=15)

        self.surf.blit(play_again_text[0], (play_again_rect.x + 20, play_again_rect.y + 15))
        self.surf.blit(no_text[0], (no_rect.x + no_rect.w/2 - no_text[1].w/2, no_rect.y + 15))

    def event(self, event):
        if self.show:
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.play_again.collidepoint(event.pos):
                    Element.element_dict["graph"].generate_puzzle()
                    self.show = False
                elif self.no.collidepoint(event.pos):
                    self.show = False
