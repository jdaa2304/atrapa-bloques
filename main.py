import pygame
import sys
import random

pygame.init()
pygame.mixer.init()

ANCHO, ALTO = 800, 600
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Atrapa los Bloques")
clock = pygame.time.Clock()
FPS = 60

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (50, 150, 255)
VERDE = (50, 220, 100)
ROJO = (220, 60, 60)
AMARILLO = (255, 220, 50)
GRIS = (40, 40, 40)

fuente_grande = pygame.font.SysFont("Arial", 48, bold=True)
fuente_media = pygame.font.SysFont("Arial", 32, bold=True)
fuente_peq = pygame.font.SysFont("Arial", 24)

jugador_ancho = 80
jugador_alto = 20
jugador_x = ANCHO // 2 - jugador_ancho // 2
jugador_y = ALTO - 50
jugador_vel = 8

bloques = []
bombas = []

puntuacion = 0
vidas = 3
velocidad_caida = 4
tiempo_spawn = 0
intervalo_spawn = 45
estado = "menu"


def reiniciar_juego():
    global bloques, bombas, puntuacion, vidas
    global velocidad_caida, tiempo_spawn, estado
    bloques = []
    bombas = []
    puntuacion = 0
    vidas = 3
    velocidad_caida = 4
    tiempo_spawn = 0
    estado = "jugando"


def crear_objeto():
    x = random.randint(0, ANCHO - 40)
    if random.random() < 0.75:
        rect = pygame.Rect(x, -30, 40, 40)
        bloques.append({"rect": rect, "vel": velocidad_caida})
    else:
        rect = pygame.Rect(x, -30, 40, 40)
        bombas.append({"rect": rect, "vel": velocidad_caida})


def dibujar_texto(texto, fuente, color, x, y, centrado=True):
    sup = fuente.render(texto, True, color)
    rect = sup.get_rect()
    if centrado:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(sup, rect)


ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                if estado == "menu" or estado == "gameover":
                    reiniciar_juego()
            if evento.key == pygame.K_ESCAPE:
                ejecutando = False

    if estado == "jugando":
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and jugador_x > 0:
            jugador_x -= jugador_vel
        if teclas[pygame.K_RIGHT] and jugador_x < ANCHO - jugador_ancho:
            jugador_x += jugador_vel

        tiempo_spawn += 1
        if tiempo_spawn >= intervalo_spawn:
            crear_objeto()
            tiempo_spawn = 0

        jrect = pygame.Rect(jugador_x, jugador_y,
                            jugador_ancho, jugador_alto)

        for bloque in bloques[:]:
            bloque["rect"].y += bloque["vel"]
            if bloque["rect"].colliderect(jrect):
                bloques.remove(bloque)
                puntuacion += 10
                if puntuacion % 50 == 0:
                    velocidad_caida += 0.5
            elif bloque["rect"].y > ALTO:
                bloques.remove(bloque)
                vidas -= 1

        for bomba in bombas[:]:
            bomba["rect"].y += bomba["vel"]
            if bomba["rect"].colliderect(jrect):
                bombas.remove(bomba)
                vidas -= 1
            elif bomba["rect"].y > ALTO:
                bombas.remove(bomba)

        if vidas <= 0:
            estado = "gameover"

    screen.fill(NEGRO)

    if estado == "menu":
        dibujar_texto("ATRAPA LOS BLOQUES", fuente_grande,
                      AMARILLO, ANCHO // 2, 180)
        dibujar_texto("Usa las flechas para moverte",
                      fuente_peq, BLANCO, ANCHO // 2, 260)
        dibujar_texto("Atrapa verdes (+10)",
                      fuente_peq, BLANCO, ANCHO // 2, 300)
        dibujar_texto("Esquiva rojas (-1 vida)",
                      fuente_peq, BLANCO, ANCHO // 2, 330)
        dibujar_texto("Pulsa ESPACIO para empezar",
                      fuente_media, VERDE, ANCHO // 2, 420)
        dibujar_texto("ESC para salir",
                      fuente_peq, GRIS, ANCHO // 2, 520)

    elif estado == "jugando":
        pygame.draw.rect(screen, AZUL,
                         (jugador_x, jugador_y,
                          jugador_ancho, jugador_alto))
        for bloque in bloques:
            pygame.draw.rect(screen, VERDE, bloque["rect"])
        for bomba in bombas:
            pygame.draw.rect(screen, ROJO, bomba["rect"])
        dibujar_texto(f"Puntos: {puntuacion}", fuente_peq,
                      BLANCO, 20, 20, centrado=False)
        dibujar_texto(f"Vidas: {vidas}", fuente_peq,
                      BLANCO, ANCHO - 120, 20, centrado=False)

    elif estado == "gameover":
        dibujar_texto("GAME OVER", fuente_grande, ROJO,
                      ANCHO // 2, 200)
        dibujar_texto(f"Puntos: {puntuacion}", fuente_media,
                      BLANCO, ANCHO // 2, 300)
        dibujar_texto("ESPACIO para reiniciar", fuente_media,
                      VERDE, ANCHO // 2, 400)
        dibujar_texto("ESC para salir", fuente_peq, GRIS,
                      ANCHO // 2, 500)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()

