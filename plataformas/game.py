import pygame
from pygame.locals import *
import random
from player import Player
from constants import *
from fondo import Background
from events import *
from gameplatform import GamePlatform
from money import Money
from enemy import Enemy
from shield import Shield
import globals
import json

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode([ancho_ventana, alto_ventana])
        self.clock = pygame.time.Clock()
        self.running = True

        self.dead_sound_played = False  # Cambié dead_sound a dead_sound_played

        pygame.init()
        pygame.display.set_caption("Plataformas")

        # Backgrounds for parallax effect
        self.background1 = Background(True, .2, "2", 0)
        self.background2 = Background(True, .2, "3", 0)

        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.smaller_font = pygame.font.Font('freesansbold.ttf', 22)

        # Sounds
        self.powerup_sound = pygame.mixer.Sound("plataformas/sound/Card_Sound.wav")
        self.powerup_sound.set_volume(.1)
        self.death_sound = pygame.mixer.Sound("plataformas/sound/Dead_Sound.mp3")

        self.initialize()

    def initialize(self):
        """Initialize all game elements."""
        self.player = Player()
        self.no_face = False
        self.dead = False
        self.dead_sound_played = False

        self.platforms = []
        # First platform
        platform = GamePlatform(20, 0)
        self.platforms.append(platform)
        self.difficulty = 1
        self.group_platforms = pygame.sprite.Group()
        self.group_platforms.add(platform)
        self.platformWillBeCreated = False

        self.start_time = pygame.time.get_ticks()
        self.last_frame_time = -1

        self.score = 0
        self.text_score = None
        self.text_score_rect = None

        # Power-ups: money
        self.powerups = []
        self.group_powerups = pygame.sprite.Group()
        pygame.time.set_timer(CREATE_NEW_MONEY, 1000)

        self.enemies = []
        self.group_enemies = pygame.sprite.Group()
        pygame.time.set_timer(CREATE_NEW_ENEMY, 15000)

        self.shields = []
        self.group_shields = pygame.sprite.Group()
        pygame.time.set_timer(CREATE_NEW_SHIELD, 10000)

    def restart(self):
        """Reset the game state for a full restart."""
        # Reset the game elements
        self.player = Player()
        self.dead_sound_played = False
        self.no_face = False
        self.dead = False
        self.platforms.clear()
        self.group_platforms.empty()
        self.powerups.clear()
        self.group_powerups.empty()
        self.enemies.clear()
        self.group_enemies.empty()
        self.shields.clear()
        self.group_shields.empty()

        # Recreate the first platform and reset difficulty and score
        platform = GamePlatform(20, 0)
        self.platforms.append(platform)
        self.group_platforms.add(platform)

        self.difficulty = 1
        self.score = 0
        self.start_time = pygame.time.get_ticks()
        self.text_score = None
        self.text_score_rect = None

        pygame.time.set_timer(CREATE_NEW_MONEY, 1000)
        pygame.time.set_timer(CREATE_NEW_ENEMY, 15000)
        pygame.time.set_timer(CREATE_NEW_SHIELD, 10000)

    def update(self, delta_time):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                if event.key == K_SPACE or event.key == K_UP:
                    self.player.jump()

                # Check for R key to restart
                if event.key == K_r and self.dead:
                    self.restart()

            elif event.type == KEYUP:
                if event.key == K_SPACE or event.key == K_UP:
                    self.player.cancel_jump()

            elif event.type == CREATE_NEW_PLATFORM:
                self.platformWillBeCreated = False
                min = 1
                if self.difficulty <= 3:
                    min = 3
                max = 12 - self.difficulty
                if max < 4:
                    max = 4
                tileNumber = random.randrange(min, max)

                min_space = 90 + (self.difficulty * 2)
                if min_space > 150:
                    min_space = 150
                max_space = 200 + (self.difficulty * 2)
                if max_space > 350:
                    max_space = 350

                space = random.randrange(min_space, max_space)

                platform = GamePlatform(tileNumber, ancho_ventana + space)
                self.platforms.append(platform)
                self.group_platforms.add(platform)

            elif event.type == CREATE_NEW_MONEY:
                money = Money()
                self.powerups.append(money)
                self.group_powerups.add(money)

                min_time = 4000 - self.difficulty * 500
                if min_time < 2000:
                    min_time = 2000
                max_time = 10000 - self.difficulty * 500
                if max_time < 4000:
                    max_time = 4000

                pygame.time.set_timer(CREATE_NEW_MONEY, random.randint(3000, 10000))

            elif event.type == CREATE_NEW_ENEMY:
                enemy = Enemy()
                self.enemies.append(enemy)
                self.group_enemies.add(enemy)

                min_time = 4000 - self.difficulty * 500
                if min_time < 2000:
                    min_time = 2000
                max_time = 10000 - self.difficulty * 500
                if max_time < 4000:
                    max_time = 4000

                pygame.time.set_timer(CREATE_NEW_ENEMY, random.randint(min_time, max_time))

            elif event.type == CREATE_NEW_SHIELD:
                shield = Shield()
                self.shields.append(shield)
                self.group_shields.add(shield)

                min_time = 4000 - self.difficulty * 500
                if min_time < 2000:
                    min_time = 2000
                max_time = 10000 - self.difficulty * 500
                if max_time < 4000:
                    max_time = 4000

                pygame.time.set_timer(CREATE_NEW_SHIELD, random.randint(10000, 20000))

        if not self.player.dead:
            self.background1.update(delta_time)
            self.background2.update(delta_time)
            self.player.update(delta_time, self.group_platforms, self.group_powerups, self.group_enemies, self.group_shields)
            if self.player.dead or self.player.rect.top > alto_ventana:
                if self.player.shield:
                    # If dead but with a shield, save the player
                    self.player.shield_save()
                else:
                    # Dead, stop the game
                    self.dead = True
                    if not self.dead_sound_played:  # Reproducir el sonido solo una vez
                        pygame.mixer.Sound.play(self.death_sound)
                        self.dead_sound_played = True  # Marcar que el sonido ya se reprodujo

                    # Llamar a guardar la puntuación solo una vez cuando el juego termina
                    if self.dead and not getattr(self, 'puntuacion_guardada', False):
                        self.guardar_puntuacion()
                        self.puntuacion_guardada = True  # Evitar que se guarde varias veces

            if self.player.addScore > 0:
                self.score += (self.player.addScore * 1000)
                self.player.addScore = 0
                pygame.mixer.Sound.play(self.powerup_sound)

            for platform in self.platforms:
                platform.update(delta_time)

            self.group_powerups.update(delta_time)
            self.group_enemies.update(delta_time)
            self.group_shields.update(delta_time)

            if (ancho_ventana - self.platforms[-1].rect.right > 0) and not self.platformWillBeCreated:
                self.platformWillBeCreated = True
                pygame.event.post(pygame.event.Event(CREATE_NEW_PLATFORM))

            seconds = int((pygame.time.get_ticks() - self.start_time) / 1000)
            self.difficulty = int(1 + (seconds / 10))
            globals.game_speed = 1 + (self.difficulty * .2)

            # Only update score if not dead
            if not self.dead:
                self.score += globals.game_speed * delta_time

            self.text_score = self.font.render('Puntuacion: ' + str(int(self.score / 1000)), True, (255, 255, 255))
            self.text_score_rect = self.text_score.get_rect()
            self.text_score_rect.y = 10
            self.text_score_rect.x = (ancho_ventana // 2) - (self.text_score_rect.width // 2)

    def render(self):
        self.screen.fill((92, 89, 92))

        self.background1.render(self.screen)
        self.background2.render(self.screen)

        for platform in self.platforms:
            self.screen.blit(platform.surf, platform.rect)

        self.screen.blit(self.player.surf, self.player.rect)
        if self.player.shield:
            self.screen.blit(self.player.shieldSurf, self.player.shieldRect)

        for powerup in self.group_powerups:
            self.screen.blit(powerup.surf, powerup.rect)

        for enemy in self.group_enemies.sprites():
            self.screen.blit(enemy.surf, enemy.rect)

        for shield in self.group_shields:
            self.screen.blit(shield.surf, shield.rect)

        if self.text_score:
            self.screen.blit(self.text_score, self.text_score_rect)

        if self.dead:
            self.guardar_puntuacion()
            self.dead = self.font.render('HAS PERDIDO', True, (255, 255, 255), (0, 0, 0))
            dead_rect = self.dead.get_rect()
            dead_rect.center = (ancho_ventana // 2, alto_ventana // 2)
            self.screen.blit(self.dead, dead_rect)

            self.retry = self.smaller_font.render('Presiona R para intentar de nuevo ', True, (200, 200, 200), (0, 0, 0))
            retry_rect = self.retry.get_rect()
            retry_rect.center = (ancho_ventana // 2, (alto_ventana // 2) + 40)
            self.screen.blit(self.retry, retry_rect)
            
            self.mostrar_puntuaciones_altas()

        pygame.display.flip()

    def guardar_puntuacion(self):
        # Obtener la puntuación final
        puntuacion_final = int(self.score)  # Guardamos la puntuación completa sin dividirla por 1000

        # Intentar cargar el archivo JSON existente (si existe)
        try:
            with open('plataformas/puntuaciones_plataformas.json', 'r') as file:
                puntuaciones = json.load(file)  # Cargar las puntuaciones existentes
        except (FileNotFoundError, json.JSONDecodeError):
            puntuaciones = []  # Si no existe el archivo o hay un error, comenzamos con una lista vacía
        
        # Agregar la nueva puntuación a la lista
        puntuaciones.append(puntuacion_final)

        # Ordenar las puntuaciones de mayor a menor
        puntuaciones.sort(reverse=True)

        # Asegurarse de que haya un máximo de 20 puntuaciones
        if len(puntuaciones) > 2:
            puntuaciones = puntuaciones[:2]  # Limitar a las 20 mejores puntuaciones

        # Guardar las puntuaciones actualizadas en el archivo
        with open('plataformas/puntuaciones_plataformas.json', 'w') as file:
            json.dump(puntuaciones, file)

    def mostrar_puntuaciones_altas(self):
    # Intentamos cargar las puntuaciones
        try:
            with open('plataformas/puntuaciones_plataformas.json', 'r') as file:
                puntuaciones = json.load(file)  # Cargar las puntuaciones del archivo
        except (FileNotFoundError, json.JSONDecodeError):
            puntuaciones = []  # Si no existe el archivo o hay un error, comenzamos con una lista vacía

        # Cargar la fuente de Intensamente (suponiendo que tienes el archivo 'intensamente.ttf')
        try:
            self.font = pygame.font.Font('intensamente.ttf', 24)  # Fuente para las puntuaciones
            self.font_bold = pygame.font.Font('intensamente.ttf', 30)  # Fuente para el título con mayor tamaño
        except:
            # Si no se puede cargar la fuente, utilizamos la fuente predeterminada
            self.font = pygame.font.SysFont('Arial', 24)
            self.font_bold = pygame.font.SysFont('Arial', 30)

        # Configuración del área para las puntuaciones
        puntuaciones_width = 300  # Ancho del fondo
        puntuaciones_height = 160  # Alto del fondo (un poco más grande para incluir el título)
        puntuaciones_rect = pygame.Rect((ancho_ventana // 2 - puntuaciones_width // 2, 120), (puntuaciones_width, puntuaciones_height))
        
        # Dibujar el fondo negro con borde blanco
        pygame.draw.rect(self.screen, (0, 0, 0), puntuaciones_rect)  # Fondo negro
        pygame.draw.rect(self.screen, (255, 255, 255), puntuaciones_rect, 3)  # Borde blanco

        # Renderizar el texto de "Mejores Puntuaciones" dentro del fondo
        titulo_texto = self.font_bold.render('Mejores Puntuaciones', True, (255, 255, 255))
        titulo_rect = titulo_texto.get_rect()
        titulo_rect.centerx = puntuaciones_rect.centerx  # Centrar horizontalmente dentro del rectángulo
        titulo_rect.top = puntuaciones_rect.top + 10  # Ubicarlo un poco más cerca de la parte superior
        self.screen.blit(titulo_texto, titulo_rect)

        # Mostrar las 3 primeras puntuaciones
        y_offset = 40  # Reducir el espacio entre el título y las puntuaciones
        for i, puntuacion in enumerate(puntuaciones[:3]):  # Mostramos solo las 3 mejores
            high_score_text = self.font.render(f'{i + 1}. {puntuacion // 1000} puntos', True, (255, 255, 255))  # Dividir la puntuación por 1000 al mostrarla
            high_score_rect = high_score_text.get_rect()
            high_score_rect.centerx = puntuaciones_rect.centerx  # Alinear al centro del rectángulo
            high_score_rect.top = puntuaciones_rect.top + y_offset + i * 30  # Posición vertical ajustada
            self.screen.blit(high_score_text, high_score_rect)
    def loop(self):
        while self.running:
            time = pygame.time.get_ticks()
            if self.last_frame_time == -1:
                delta_time = 1
            else:
                delta_time = time - self.last_frame_time

            self.last_frame_time = time
            self.update(delta_time)
            self.render()
            self.clock.tick(60)
        pygame.quit()
