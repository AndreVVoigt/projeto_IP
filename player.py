import pygame

# Velocidade de movimento do jogador (pixels por frame)
PLAYER_SPEED = 4


class Player:
    """
    Representa o astronauta controlado pelo jogador.

    Atributos:
        x, y   -- posição atual no mundo
        width, height -- dimensões do sprite
        vel_x, vel_y  -- velocidade atual (usada para animação futura)
    """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.vel_x = 0
        self.vel_y = 0
        self.color = (200, 220, 255)   # branco-azulado (traje espacial)
        self.visor_color = (100, 180, 255)

    # ------------------------------------------------------------------
    # Lógica

    def handle_input(self, keys, screen_width: int, screen_height: int):
        """Lê o teclado e atualiza a posição, mantendo o jogador na tela."""
        self.vel_x = 0
        self.vel_y = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = PLAYER_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vel_y = -PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vel_y = PLAYER_SPEED

        self.x += self.vel_x
        self.y += self.vel_y

        # Limita às bordas da tela
        self.x = max(0, min(self.x, screen_width - self.width))
        self.y = max(0, min(self.y, screen_height - self.height))

    def get_rect(self) -> pygame.Rect:
        """Retorna o retângulo de colisão do jogador."""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    # ------------------------------------------------------------------
    # Desenho

    def draw(self, surface: pygame.Surface):
        """Desenha o astronauta como formas geométricas simples."""
        x, y = self.x, self.y
        w, h = self.width, self.height

        # Corpo (retângulo arredondado simulado)
        pygame.draw.rect(surface, self.color, (x + 6, y + 12, w - 12, h - 14), border_radius=6)

        # Capacete (círculo)
        cx, cy = x + w // 2, y + 14
        pygame.draw.circle(surface, self.color, (cx, cy), 14)

        # Visor
        pygame.draw.circle(surface, self.visor_color, (cx, cy), 9)
        pygame.draw.circle(surface, (180, 220, 255), (cx - 3, cy - 3), 3)  # reflexo

        # Mochila propulsora
        pygame.draw.rect(surface, (150, 160, 180), (x + w - 10, y + 16, 8, 14), border_radius=3)

        # Chama da propulsora (só aparece quando se move)
        if self.vel_x != 0 or self.vel_y != 0:
            flame_color = (255, 160, 60)
            pygame.draw.circle(surface, flame_color, (x + w - 6, y + 32), 4)