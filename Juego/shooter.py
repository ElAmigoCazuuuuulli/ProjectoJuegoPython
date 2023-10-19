import pygame, random

#Constantes
WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = ( 255, 255, 255)
RED = (255, 0, 0)

#inicializacion del juego
pygame.init()
pygame.mixer.init()

#inicializacion de la pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("disparoer")
clock = pygame.time.Clock()

def texto_pantalla(surface, text, size, x, y):
	font = pygame.font.SysFont("serif", size)
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surface.blit(text_surface, text_rect)

def vida(surface, x, y, percentage):
	BAR_LENGHT = 100
	BAR_HEIGHT = 10
	fill = (percentage / 100) * BAR_LENGHT
	border = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
	fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
	pygame.draw.rect(surface, RED, fill)
	pygame.draw.rect(surface, WHITE, border, 2)

class personaje(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("assets/player.png").convert()
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH // 2
		self.rect.bottom = HEIGHT - 10
		self.speed_x = 0
		self.shield = 100

	def update(self):
		self.speed_x = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.speed_x = -5
		if keystate[pygame.K_RIGHT]:
			self.speed_x = 5
		self.rect.x += self.speed_x
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0

	def disparo(self):
		bullet = disparo(self.rect.centerx, self.rect.top)
		all_sprites.add(bullet)
		bullets.add(bullet)
		#laser_sound.play()

class asteroide(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = random.choice(imagenes_asteroideo)
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.randrange(-140, -100)
		self.speedy = random.randrange(1, 10)
		self.speedx = random.randrange(-5, 5)

	def update(self):
		self.rect.y += self.speedy
		self.rect.x += self.speedx
		if self.rect.top > HEIGHT + 10 or self.rect.left < -40 or self.rect.right > WIDTH + 40:
			self.rect.x = random.randrange(WIDTH - self.rect.width)
			self.rect.y = random.randrange(-140, - 100)
			self.speedy = random.randrange(1, 10)

class disparo(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.image.load("assets/laser1.png")
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.centerx = x
		self.speedy = -10

	def update(self):
		self.rect.y += self.speedy
		if self.rect.bottom < 0:
			self.kill()

class Explosion(pygame.sprite.Sprite):
	def __init__(self, center):
		super().__init__()
		self.image = animacion_explosion[0]
		self.rect = self.image.get_rect()
		self.rect.center = center 
		self.frame = 0
		self.last_update = pygame.time.get_ticks()
		self.frame_rate = 50 # VELOCIDAD DE LA EXPLOSION

	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > self.frame_rate:
			self.last_update = now
			self.frame += 1
			if self.frame == len(animacion_explosion):
				self.kill()
			else:
				center = self.rect.center
				self.image = animacion_explosion[self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center

def pantalla_muerte():
	screen.blit(background, [0,0])
	texto_pantalla(screen, "Tu nave ha sido destruida", 65, WIDTH // 2, HEIGHT // 4)
	texto_pantalla(screen, "Presines una tecla para continuar", 20, WIDTH // 2, HEIGHT * 3/4)
	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYUP:
				waiting = False
				pantalla_inicio()


def pantalla_inicio():
	screen.blit(background, [0,0])
	texto_pantalla(screen, "Lluvia de Asteroides!!!", 65, WIDTH // 2, HEIGHT // 4)
	texto_pantalla(screen, "Presine una tecla para continuar...", 30, WIDTH // 2, HEIGHT * 3/5)
	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYUP:
				waiting = False


imagenes_asteroideo = []
lista_asteroideo = ["assets/meteorGrey_big1.png", "assets/meteorGrey_big2.png", "assets/meteorGrey_big3.png", "assets/meteorGrey_big4.png",
				"assets/meteorGrey_med1.png", "assets/meteorGrey_med2.png", "assets/meteorGrey_small1.png", "assets/meteorGrey_small2.png",
				"assets/meteorGrey_tiny1.png", "assets/meteorGrey_tiny2.png"]
for img in lista_asteroideo:
	imagenes_asteroideo.append(pygame.image.load(img).convert())


#Animacion Explosion
animacion_explosion = []
for i in range(9):
	file = "assets/regularExplosion0{}.png".format(i)
	img = pygame.image.load(file).convert()
	img.set_colorkey(BLACK)
	img_scale = pygame.transform.scale(img, (70,70))
	animacion_explosion.append(img_scale)

#Cargar background
background = pygame.image.load("assets/background2.png").convert()

# Detectar Game over
game_over = True
running = True
while running:
	if game_over:

		pantalla_inicio()

		game_over = False
		all_sprites = pygame.sprite.Group()
		lista_asteroideo = pygame.sprite.Group()
		bullets = pygame.sprite.Group()

		Personaje = personaje()
		all_sprites.add(Personaje)
		for i in range(8):
			Asteroide = asteroide()
			all_sprites.add(Asteroide)
			lista_asteroideo.add(Asteroide)

		score = 0
	


	clock.tick(60)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				Personaje.disparo()


	all_sprites.update()

	#colisiones - asteroideo - laser
	hits = pygame.sprite.groupcollide(lista_asteroideo, bullets, True, True)
	for hit in hits:
		score += 10
		#explosion_sound.play()
		explosion = Explosion(hit.rect.center)
		all_sprites.add(explosion)
		Asteroide = asteroide()
		all_sprites.add(Asteroide)
		lista_asteroideo.add(Asteroide)

	# Checar colisiones - jugador - asteroideo
	hits = pygame.sprite.spritecollide(Personaje, lista_asteroideo, True)
	for hit in hits:
		Personaje.shield -= 25
		Asteroide = asteroide()
		all_sprites.add(Asteroide)
		lista_asteroideo.add(Asteroide)
		if Personaje.shield <= 0:
			game_over = True
			pantalla_muerte()

	screen.blit(background, [0, 0])

	all_sprites.draw(screen)

	#Marcador
	texto_pantalla(screen, str(score), 25, WIDTH // 2, 10)

	# Escudo.
	vida(screen, 5, 5, Personaje.shield)

	pygame.display.flip()
pygame.quit()