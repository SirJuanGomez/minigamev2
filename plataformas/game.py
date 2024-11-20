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


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode([ancho_ventana, alto_ventana])
        self.clock = pygame.time.Clock()
        self.running = True

        pygame.init()
        pygame.display.set_caption("Plataformas")

        #2 fondos para manejar el paralaje. El detalle puedes leerlo
        #en background.py
        self.background1 = Background(True, .05, "2", 0)
        self.background2 = Background(False, .2, "3", 40)

        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.smaller_font = pygame.font.Font('freesansbold.ttf', 22)

        #Sonidillos
        self.powerup_sound = pygame.mixer.Sound("plataformas/sound/Card_Sound.wav")
        self.powerup_sound.set_volume(.1)
        self.death_sound = pygame.mixer.Sound("plataformas/sound/Dead_Sound.mp3")

        self.initialize()

    def initialize(self):
        self.player = Player()
        self.no_face = False
        self.dead = False

        self.platforms = []

        #La primera plataforma grande
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

        #powerups = el dinero. se llama asi porque segun yo iba a agregar mas pero nunca lo hice
        self.powerups = []
        self.group_powerups = pygame.sprite.Group()
        pygame.time.set_timer(CREATE_NEW_MONEY, 1000)

        self.enemies = []
        self.group_enemies = pygame.sprite.Group()
        pygame.time.set_timer(CREATE_NEW_ENEMY, 15000)

        self.shields = []
        self.group_shields = pygame.sprite.Group()
        pygame.time.set_timer(CREATE_NEW_SHIELD, 10000)

    def update(self, delta_time):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                # Handle spacebar and up arrow key for jumping
                if event.key == K_SPACE or event.key == K_UP:
                    self.player.jump()

            elif event.type == KEYUP:
                if event.key == K_SPACE or event.key == K_UP:
                    self.player.cancel_jump()

            elif event.type == CREATE_NEW_PLATFORM:
                self.platformWillBeCreated = False
                #Basar el tamano en la dificultad
                min = 1
                if self.difficulty <= 3:
                    min = 3
                max = 12 - self.difficulty
                if max < 4:
                    max = 4
                tileNumber = random.randrange(min, max)

                #Basar el espacio entre plataformas en la dificultad
                min_space = 90 + (self.difficulty*2)
                if min_space > 150:
                    min_space = 150
                max_space = 200 + (self.difficulty*2)
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

                #Calculos para ver cuando crear mas dinero, segun la dificultad
                min_time = 4000 - self.difficulty*500
                if min_time < 2000:
                    min_time = 2000
                max_time = 10000 - self.difficulty*500
                if max_time < 4000:
                    max_time = 4000

                pygame.time.set_timer(CREATE_NEW_MONEY, random.randint(3000, 10000))
            elif event.type == CREATE_NEW_ENEMY:
                enemy = Enemy()
                self.enemies.append(enemy)
                self.group_enemies.add(enemy)

                min_time = 4000 - self.difficulty*500
                if min_time < 2000:
                    min_time = 2000
                max_time = 10000 - self.difficulty*500
                if max_time < 4000:
                    max_time = 4000
                pygame.time.set_timer(CREATE_NEW_ENEMY, random.randint(min_time, max_time))
            elif event.type == CREATE_NEW_SHIELD:
                shield = Shield()
                self.shields.append(shield)
                self.group_shields.add(shield)
                min_time = 4000 - self.difficulty*500
                if min_time < 2000:
                    min_time = 2000
                max_time = 10000 - self.difficulty*500
                if max_time < 4000:
                    max_time = 4000

                pygame.time.set_timer(CREATE_NEW_SHIELD, random.randint(10000, 20000))

        if not self.player.dead:
            self.background1.update(delta_time)
            self.background2.update(delta_time)
            self.player.update(delta_time, self.group_platforms, self.group_powerups, self.group_enemies, self.group_shields)
            if self.player.dead or self.player.rect.top > alto_ventana:
                if self.player.shield:
                    #Moriste pero tienes escudo? No morir!
                    self.player.shield_save()
                else:
                    #No tenias escudo. Dead
                    self.dead = True
                    pygame.mixer.Sound.play(self.death_sound)

            if self.player.addScore > 0:
                self.score += (self.player.addScore*1000)
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

            seconds = int( (pygame.time.get_ticks() - self.start_time) / 1000)
            self.difficulty = int( 1+(seconds/10) )
            globals.game_speed = 1 + (self.difficulty*.2)

            self.score += globals.game_speed * delta_time
            self.text_score = self.font.render('Score: ' + str(int(self.score/1000)), True, (255,255,255))
            self.text_score_rect = self.text_score.get_rect()
            self.text_score_rect.y = 10
            self.text_score_rect.x = (ancho_ventana//2) - (self.text_score_rect.width//2)

    def render(self):
        self.screen.fill((92, 89, 92))

        self.background1.render(self.screen)
        self.background2.render(self.screen)

        for platform in self.platforms:
            self.screen.blit(platform.surf, platform.rect)

        self.screen.blit(self.player.surf, self.player.rect)
        if (self.player.shield):
            self.screen.blit(self.player.shieldSurf, self.player.shieldRect)

        for powerup in self.group_powerups:
            self.screen.blit(powerup.surf, powerup.rect)
        for enemy in self.group_enemies.sprites():
            self.screen.blit(enemy.surf, enemy.rect)
        for shield in self.group_shields:
            self.screen.blit(shield.surf, shield.rect)

        if self.text_score is not None:
            self.screen.blit(self.text_score, self.text_score_rect)
            
        if self.dead:
            self.dead = self.font.render('GAME OVER :(', True, (255,255,255), (0,0,0))
            dead_rect = self.dead.get_rect()
            dead_rect.center = (ancho_ventana // 2, alto_ventana// 2)
            self.screen.blit(self.dead, dead_rect)
            self.retry = self.smaller_font.render('Presiona enter para reintentar', True, (200,200,200), (0,0,0))
            retry_rect = self.retry.get_rect()
            retry_rect.center = (ancho_ventana // 2, (alto_ventana // 2) + 40)
            self.screen.blit(self.retry, retry_rect)

        pygame.display.flip()

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