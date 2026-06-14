import pygame
import random
from player import Player

# Configurações da janela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Space Collector 🚀"

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Star:
    """Estrela de fundo para o efeito de parallax simples."""

    def __init__(self):
        self.reset()
        # Começa em posição aleatória
        self.x = random.randint(0, SCREEN_WIDTH)

    def reset(self):
        self.x = SCREEN_WIDTH
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.speed = random.uniform(0.3, 1.5)
        self.radius = random.choice([1, 1, 1, 2])
        self.brightness = random.randint(100, 255)

    def update(self):
        self.x -= self.speed
        if self.x < 0:
            self.reset()

    def draw(self, surface: pygame.Surface):
        color = (self.brightness, self.brightness, self.brightness)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.radius)


class Game:
    """
    Classe principal que gerencia o loop do jogo, eventos e renderização.

    Responsabilidades:
        - Inicializar o PyGame e criar a janela
        - Manter o loop principal (eventos → update → draw)
        - Coordenar os objetos do jogo (player, coletáveis, placar)
    """

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        # Objetos do jogo
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        # Fundo estrelado
        self.stars = [Star() for _ in range(120)]

        # Fonte para HUD simples
        self.font = pygame.font.SysFont("monospace", 18)
        self.font_big = pygame.font.SysFont("monospace", 28, bold=True)

    # ------------------------------------------------------------------
    # Loop principal

    def run(self):
        """Executa o loop principal até o jogador fechar o jogo."""
        while self.running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(FPS)

        pygame.quit()

    # ------------------------------------------------------------------
    # Etapas do loop
    
    def _handle_events(self):
        """Processa eventos do sistema (fechar janela, teclas globais)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def _update(self):
        """Atualiza o estado do jogo a cada frame."""
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys, SCREEN_WIDTH, SCREEN_HEIGHT)

        for star in self.stars:
            star.update()

    def _draw(self):
        """Renderiza todos os elementos na tela."""
        # Fundo
        self.screen.fill((5, 5, 20))  # azul-escuro espacial

        # Estrelas
        for star in self.stars:
            star.draw(self.screen)

        # Jogador
        self.player.draw(self.screen)

        # HUD temporário
        self._draw_hud()

        pygame.display.flip()

    def _draw_hud(self):
        """Desenha a interface com informações do jogador."""
        # Instrução de movimento
        hint = self.font.render("WASD ou setas para mover  |  ESC para sair", True, (120, 120, 150))
        self.screen.blit(hint, (10, SCREEN_HEIGHT - 28))

        # Título no canto superior
        title = self.font_big.render("SPACE COLLECTOR", True, (180, 200, 255))
        self.screen.blit(title, (10, 10))



if __name__ == "__main__":
    game = Game()
    game.run()