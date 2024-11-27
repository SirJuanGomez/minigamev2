import pygame
from pygame.locals import *
from constants import *
import globals

# Dimensiones del jugador y del hitbox
WIDTH = 100
HEIGHT = 100
HITBOX_WIDTH = 60
HITBOX_HEIGHT = 100

ASSET_SIZE = 48  # Tamaño de cada cuadro en la animación

JUMP_POWER = 12  # Fuerza del salto

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()

        # Configuración inicial de la animación
        self.current_animation = "run"
        self.animations = {}
        self.animation_behaviour = {
            "run": "continuous",  # Animación continua al correr
            "jump": "once",       # Animación que solo se reproduce una vez al saltar
            "doublejump": "once"  # Animación que solo se reproduce una vez en un doble salto
        }

        self.load_assets()  # Carga las animaciones

        # Configuración inicial de la animación
        self.idxAnimation = 0  # Índice del cuadro de la animación
        self.animationSpeed = .15  # Velocidad de la animación
        self.surf = self.animations[self.current_animation][self.idxAnimation]  # Superficie con el cuadro actual
        self.surf = pygame.transform.scale(self.surf, (WIDTH, HEIGHT))  # Escala el sprite
        self.rect = self.surf.get_rect()  # Rectángulo de la imagen para manejar la posición
        self.update_hitbox()  # Actualiza el hitbox
        self.update_mask()  # Actualiza la máscara para colisiones
        self.vel = pygame.math.Vector2(0, 0)  # Velocidad del jugador
        self.pos = pygame.math.Vector2(100, 300)  # Posición inicial
        self.acc = pygame.math.Vector2(0, .022)  # Aceleración (gravedad)

        # Variables de salto y control
        self.jumpCount = 0
        self.canJump = False
        self.doJump = False
        self.wantedToJump = False
        self.wantToJumpTime = -1
        self.lastJumpTime = pygame.time.get_ticks()

        self.timeToHonorJumpAttempt = 100  # Tiempo mínimo entre intentos de salto
        self.dead = False  # Estado de muerte
        self.addScore = 0  # Puntos obtenidos
        self.colliding_with_floor = False  # Si está tocando el suelo
        self.shield = True  # Si el jugador tiene escudo
        self.shieldSurf = pygame.image.load("plataformas/img/shield-big.png")  # Imagen del escudo
        self.shieldSurf = pygame.transform.scale(self.shieldSurf, (WIDTH*1.1, HEIGHT*1.1))  # Escala el escudo
        self.shieldRect = self.shieldSurf.get_rect()  # Rectángulo del escudo

        self.canOnlyJumpGoingDown = False  # Si solo puede saltar al ir hacia abajo

    def load_animation(self, name):
        # Cargar animaciones de los diferentes estados del jugador (correr, saltar, doble salto)
        self.animations[name] = []
        asset = pygame.image.load(f"plataformas/img/2 Punk/Punk_{name}.png").convert_alpha()
        width = asset.get_width()
        idx = 0
        while (idx * ASSET_SIZE < width):  # Extrae cada cuadro de la animación
            frame = pygame.Surface((ASSET_SIZE, ASSET_SIZE), pygame.SRCALPHA)
            frame.blit(asset, asset.get_rect(), Rect(idx * ASSET_SIZE, 0, ASSET_SIZE, ASSET_SIZE))
            self.animations[name].append(frame)
            idx += 1
            
    def load_assets(self):
        # Cargar todas las animaciones del jugador
        self.load_animation("run")
        self.load_animation("jump")
        self.load_animation("doublejump")

    def changeAnimation(self, name):
        # Cambiar la animación actual y reiniciar el índice de la animación
        if self.current_animation != name:
            self.current_animation = name
            self.idxAnimation = 0

    def jump(self):
        # Función para saltar, evitando saltos repetidos de inmediato
        if pygame.time.get_ticks() - self.lastJumpTime < 100:
            return
        self.lastJumpTime = pygame.time.get_ticks()

        # Evitar saltos si se está yendo hacia arriba (con escudo)
        if self.canOnlyJumpGoingDown and self.vel.y < 0:
            return

        # Realizar salto si se puede
        if self.canJump:
            self.doJump = True
            self.wantedToJump = False
            if self.jumpCount == 2:
                self.canJump = False
        else:
            self.wantedToJump = True
            self.wantToJumpTime = pygame.time.get_ticks()

    def cancel_jump(self):
        # Función para cancelar un salto si se va demasiado alto
        if self.vel.y < -3:
            self.vel.y = -3

    def check_collisions_floor(self, spritegroup):
        # Revisar colisión con el suelo
        oldRect = self.rect
        self.rect = self.hitbox
        hits = pygame.sprite.spritecollide(self, spritegroup, False)
        self.rect = oldRect
        self.colliding_with_floor = False

        if hits:
            if self.rect.bottom - hits[0].rect.top < (ASSET_SIZE / 2) and self.vel.y >= 0:
                self.vel.y = 0
                self.jumpCount = 0
                self.canJump = True
                self.pos.y = hits[0].rect.top + 1
                self.changeAnimation("run")
                if self.wantedToJump:
                    self.jump()
                self.colliding_with_floor = True
        else:
            if self.jumpCount == 2:
                self.canJump = False

    def check_collisions_enemies(self, enemies_group):
        # Revisar colisión con enemigos
        hits = pygame.sprite.spritecollide(self, enemies_group, False, pygame.sprite.collide_mask)
        if hits:
            if self.shield:
                self.shield = False
                hits[0].kill()  # Elimina al enemigo
            else:
                self.dead = True  # Si no tiene escudo, muere

    def check_collisions_shields(self, group):
        # Revisar colisión con escudos
        oldRect = self.rect
        self.rect = self.hitbox
        hits = pygame.sprite.spritecollide(self, group, True, pygame.sprite.collide_rect_ratio(1))
        self.rect = oldRect
        if hits:
            for hit in hits:
                self.shield = True  # Obtiene escudo
                self.addScore += 5  # Gana puntos
                hit.kill()  # Elimina el escudo recogido

    def check_collisions_powerups(self, group):
        # Revisar colisión con power-ups (dinero u otros objetos)
        oldRect = self.rect
        self.rect = self.hitbox
        hits = pygame.sprite.spritecollide(self, group, True, pygame.sprite.collide_rect_ratio(1))
        self.rect = oldRect
        if hits:
            for hit in hits:
                self.addScore += 10  # Gana puntos por recoger power-up
                hit.kill()  # Elimina el power-up

    def animate(self, delta_time):
        # Actualizar la animación según el tiempo transcurrido
        self.animationSpeed = .008 * delta_time
        self.idxAnimation += self.animationSpeed
        if int(self.idxAnimation) + 1 >= len(self.animations[self.current_animation]):
            if self.animation_behaviour[self.current_animation] == "continuous":
                self.idxAnimation = 0
            else:
                self.idxAnimation = len(self.animations[self.current_animation]) - 1
        self.surf = self.animations[self.current_animation][int(self.idxAnimation)]
        self.surf = pygame.transform.scale(self.surf, (WIDTH, HEIGHT))
        self.rect = self.surf.get_rect()
        self.update_hitbox()  # Actualiza el hitbox
        self.update_mask()  # Actualiza la máscara para colisiones

    def update(self, delta_time, collision_floor_group, collision_group_powerups, collision_group_enemies, collision_group_shields):
        # Actualiza el jugador (revisar colisiones, animaciones, gravedad, etc.)
        self.check_collisions_floor(collision_floor_group)
        self.check_collisions_powerups(collision_group_powerups)
        self.check_collisions_enemies(collision_group_enemies)
        self.check_collisions_shields(collision_group_shields)

        if self.dead:
            return

        self.animate(delta_time)

        now = pygame.time.get_ticks()
        if self.wantedToJump and now - self.wantToJumpTime > self.timeToHonorJumpAttempt:
            self.wantedToJump = False

        if self.doJump:
            if self.jumpCount == 0 and not self.colliding_with_floor:
                self.jumpCount += 1

            if self.jumpCount == 0:
                self.vel.y = JUMP_POWER * -1
                self.changeAnimation("jump")
            elif self.jumpCount == 1:
                self.vel.y = JUMP_POWER * -1 * .8
                self.changeAnimation("doublejump")
            self.jumpCount += 1
            self.doJump = False

        # Aplicar gravedad
        self.vel += self.acc * delta_time
        self.pos += self.vel

        # Si el jugador cae fuera de la pantalla, muere
        if self.rect.top > alto_ventana:
            if self.shield:
                self.shield = False
                self.pos.y = 50
            else:
                self.dead = True

        self.rect.midbottom = self.pos
        self.update_hitbox()  # Actualiza el hitbox
        self.update_mask()  # Actualiza la máscara
        self.update_shield()  # Actualiza la posición del escudo
        
        if self.canOnlyJumpGoingDown and self.vel.y > 0:
            self.canOnlyJumpGoingDown = False

    def shield_save(self):
        # Usar el escudo para salvarse de la caída
        if self.shield:
            self.shield = False
            self.canOnlyJumpGoingDown = True
            self.vel.y = JUMP_POWER * -1.5  # Mega salto
            self.pos.y -= 20  # Ajustar la posición
            self.jumpCount = 0
            self.canJump = True
            self.changeAnimation("jump")
        else:
            self.dead = True  # Si no tiene escudo, muere

    def update_shield(self):
        # Actualizar la posición del escudo
        self.shieldRect.center = (
            self.rect.center[0] - 20,
            self.rect.center[1] + 10,
        )

    def update_hitbox(self):
        # Actualizar el hitbox del jugador, para las colisiones con el piso, objetos, etc.
        self.hitbox = pygame.Rect(
            self.rect.x * 1 + (.1 * globals.game_speed), self.rect.y,
            HITBOX_WIDTH, HITBOX_HEIGHT
        )
    
    def update_mask(self):
        # Actualizar la máscara para las colisiones con enemigos
        self.maskSurface = self.surf
        self.maskSurface = pygame.transform.scale(self.maskSurface, (WIDTH * .8, HEIGHT * .8))
        self.mask = pygame.mask.from_surface(self.maskSurface)

    def display_hitbox(self):
        # Mostrar el hitbox en la pantalla para depuración
        debugRect = pygame.Surface((self.hitbox.width, self.hitbox.height))
        debugRect.set_alpha(128)
        debugRect.fill((255, 0, 0))
        pygame.display.get_surface().blit(debugRect, (self.hitbox.x, self.hitbox.y))
