import pygame
import random
import math
from pygame import mixer

# Inicializar pygame / Initiating pygame
pygame.init()

# Crear la pantalla / Creating the Screen
pantalla = pygame.display.set_mode((800, 600))

# Titulo e Icono / Tittle and Icon
pygame.display.set_caption("Ivasion Espacial")
icono = pygame.image.load("images/ovni-alienigena.png")
pygame.display.set_icon(icono)
background = pygame.image.load('images/background.png')

# Adding sound / Agregando sonido
mixer.music.load('musics/MusicaFondo.mp3')
mixer.music.set_volume(0.3)
mixer.music.play(-1)

# Variables del Jugador / Player Variables
img_jugador = pygame.image.load('images/astronave.png')
jugador_x = 368 # Position of the player / Posicion del jugador
jugador_y = 520 # Position of the player / Posicion del jugador
jugador_x_cambio = 0 #Variable for the player movement / Variable para el movimiento del jugador

# Variables del enemigo / Enemy Variables
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load('images/nave-extraterrestre.png'))
    enemigo_x.append(random.randint(0,736)) # Position of the Enemy / Posicion del enemigo
    enemigo_y.append(random.randint(50,200)) # Position of the Enemy / Posicion del enemigo
    enemigo_x_cambio.append(2.5) #Variable for the Enemy movement / Variable para el movimiento del enemigo
    enemigo_y_cambio.append(50) #Variable for the Enemy movement / Variable para el movimiento del enemigo


# Variables de la bala / bullet Variables
balas = []
img_bala = pygame.image.load('images/bala.png')
bala_x = 0 # Position of the bullet / Posicion de la bala
bala_y = 500 # Position of the bullet / Posicion del bala
bala_x_cambio = 0 #Variable for the bullet movement / Variable para el movimiento del bala
bala_y_cambio = 10 #Variable for the bullet movement / Variable para el movimiento del bala
bala_visible = False #Variable to know if the bullet is visible / Variable para saber si la bala es visible

# Score / Puntaje
score = 0
fuente = pygame.font.Font('freesansbold.ttf', 32)
texto_x = 10
texto_y = 10


# final text game / texto final del juego
fuente_final = pygame.font.Font('freesansbold.ttf', 40)

def texto_final():
    mi_fuente_final = fuente_final.render('GAME OVER', True, (255, 255, 255))
    pantalla.blit(mi_fuente_final, (60, 200))

# Function to show the score / Funcion para mostrar el puntaje
def mostrar_puntaje(x,y):
    texto = fuente.render(f'Score: {score}', True, (255, 255, 255)) 
    pantalla.blit(texto, (x, y))

# Player Function / Funcion del jugador
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))
    

# Enemy Function / Funcion del enemigo
def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))

# shoot bullet Function / Funcion disparar bala
def disparar_bala(x,y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 10))
    
# Function which de detects collision / Funcion que detecta colision
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_2 - y_1, 2))
    
    if distancia < 27:
        return True
    else:
        return False


# Loop del juego y Definicion de los eventos del juego / Game Loop and Gane Events Definitions
se_ejecuta = True

while se_ejecuta:
    
    # background / imagen de fondo
    pantalla.blit(background, (0, 0))
    
    # Iterar eventos / Iterating Events
    for evento in pygame.event.get():
        
        
        # Se define el evento de cerrar la pantalla / Defining the event of closing the screen
        if evento.type == pygame.QUIT:
            se_ejecuta = False
        
        # Event of pressing a key / Evento de presionar una tecla
        if evento.type == pygame.KEYDOWN:
            
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -2
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 2
            if evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound('musics/disparo.mp3')
                sonido_bala.play()
                nueva_bala = {
                    "x": jugador_x,
                    "y": jugador_y,
                    "velocidad": -5
                }
                balas.append(nueva_bala)
                
                if not bala_visible:
                    bala_x = jugador_x
                    disparar_bala(bala_x, bala_y)
        
        # Event Of Releasing a key / Evento de soltar una tecla
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or pygame.K_RIGHT:
                jugador_x_cambio = 0
        
    # Player location / Ubicacion del jugador
    jugador_x += jugador_x_cambio
    
    # Keeping the player within the Screen limits / Mantener al jugador dentro de los limites de la pantalla
    if jugador_x <= 0:
        jugador_x = 0
    
    elif jugador_x >= 736:
        jugador_x = 736

    # Enemy location / Ubicacion del enemigo
    for e in range(cantidad_enemigos):
        
        # Game Over / Fin del juego
        if enemigo_y[e] > 500:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break
        enemigo_x[e] += enemigo_x_cambio[e]
    
    # Keeping the enemy within the Screen limits / Mantener al enemigo dentro de los limites de la pantalla
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 2.5
            enemigo_y[e] += enemigo_y_cambio[e]
        
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -2.5
            enemigo_y[e] += enemigo_y_cambio[e]
        
        # Collision / Colision
        for bala in balas:
            colision_bala_enemigo = hay_colision(enemigo_x[e], enemigo_y[e],
                                                 bala['x'], bala['y'])
            if colision_bala_enemigo:
                sonido_colision = mixer.Sound('musics/Golpe.mp3')
                sonido_colision.play()
                balas.remove(bala)
                score += 1
                enemigo_x[e] = random.randint(0, 736)
                enemigo_y[e] = random.randint(20, 200)
                break
            
            
         #   enemigo_x[e] = random.randint(0,736) # Position of the Enemy / Posicion del enemigo
          #  enemigo_y[e] = random.randint(50,200) # Position of the Enemy / Posicion del enemigo
        
        enemigo(enemigo_x[e], enemigo_y[e], e)
    
    # Bullet movement / Movimiento de la bala
    for bala in balas:
        bala['y'] += bala['velocidad']
        pantalla.blit(img_bala, (bala['x'] + 16, bala['y'] + 10))
        if bala['y'] < 0:
            balas.remove(bala)
 
    jugador(jugador_x, jugador_y)
    mostrar_puntaje(texto_x, texto_y)
    
    # Updating the screen / Actualizando la pantalla
    pygame.display.update() # Actualizar la pantalla / Updating the Screen
    