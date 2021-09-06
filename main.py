import pygame, sys, random
from settings import *
from level import Level
from level2 import LevelBg
from level_data import *
from overworld import Overworld
import button

class Game:
    def __init__(self):
        self.max_level = 5
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.status = 'overworld'

    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_overworld)
        self.status = 'level'

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)
        self.status = 'overworld'

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()   

class GameLevelBg:
    def __init__(self):
        self.max_level = 5
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.status = 'overworld'

    def create_level(self, current_level):
        self.level = LevelBg(current_level, screen, self.create_overworld)
        self.status = 'level'

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)
        self.status = 'overworld'

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run() 

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Battle')
game = Game()
game2 = GameLevelBg()

current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 90
attack = False
potion = False
potion_effect = 5
clicked = False
game_over = 0

font = pygame.font.SysFont('assets/font/Pixellari.ttf', 26)

red = (255, 0, 0)
green = (0, 255, 0)	

panel_img = pygame.image.load('assets/decoration/icons/panel.png').convert_alpha()
potion_img = pygame.image.load('assets/decoration/icons/potion.png').convert_alpha()

restart_img = pygame.image.load('assets/decoration/icons/restart.png').convert_alpha()

victory_img = pygame.image.load('assets/decoration/icons/victory.png').convert_alpha()
defeat_img = pygame.image.load('assets/decoration/icons/defeat.png').convert_alpha()

hammer_img = pygame.image.load('assets/decoration/icons/hammer.png').convert_alpha()

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def draw_panel():
	screen.blit(panel_img, (0, screen_height - bottom_panel))
	draw_text(f'{viking.name} HP: {viking.hp}', font, red, 50, screen_height - bottom_panel +12)
	for count, i in enumerate(enemy_list):
		draw_text(f'{i.name} HP: {i.hp}', font, red, 450, (screen_height - bottom_panel +12) + count * 60)



class Fighter():
	def __init__(self, x, y, name, max_hp, strength, potions):
		self.name = name
		self.max_hp = max_hp
		self.hp = max_hp
		self.strength = strength
		self.start_potions = potions
		self.potions = potions
		self.alive = True
		self.animation_list = []
		self.frame_index = 0
		self.action = 0
		self.update_time = pygame.time.get_ticks()

		temp_list = []
		for i in range(4):
			img = pygame.image.load(f'assets/fighters/{self.name}/idle/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
			temp_list.append(img)
		self.animation_list.append(temp_list)

		temp_list = []
		for i in range(6):
			img = pygame.image.load(f'assets/fighters/{self.name}/attack/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
			temp_list.append(img)
		self.animation_list.append(temp_list)

		temp_list = []
		for i in range(2):
			img = pygame.image.load(f'assets/fighters/{self.name}/hurt/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
			temp_list.append(img)
		self.animation_list.append(temp_list)

		temp_list = []
		for i in range(6):
			img = pygame.image.load(f'assets/fighters/{self.name}/death/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
			temp_list.append(img)
		self.animation_list.append(temp_list)

		self.image = self.animation_list[self.action][self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)

	def update(self):
		animation_cooldown = 100
		self.image = self.animation_list[self.action][self.frame_index]
		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1
		if self.frame_index >= len(self.animation_list[self.action]):
			if self.action == 3:
				self.frame_index = len(self.animation_list[self.action]) - 1
			else:	
				self.idle()

	def idle(self):
		self.action = 0
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()							

	def attack(self, target):
		rand = random.randint(0, 4)
		damage = self.strength + rand
		target.hp -= damage
		target.hurt()

		if target.hp < 1:
			target.hp = 0
			target.alive = False
			target.death()
		damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
		damage_text_group.add(damage_text)	

		self.action = 1
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def hurt(self):
		self.action = 2
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()					

	def death(self):
		self.action = 3
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def reset (self):
		self.alive = True
		self.potions = self.start_potions
		self.hp = self.max_hp
		self.frame_index = 0
		self.action = 0
		self.update_time = pygame.time.get_ticks()		

	def draw(self):
		screen.blit(self.image, self.rect)


	
class HealthBar():
	def __init__(self, x, y, hp, max_hp):
		self.x = x
		self.y = y
		self.hp = hp
		self.max_hp = max_hp

	def draw(self, hp):
		self.hp = hp
		ratio = self.hp / self.max_hp
		pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
		pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))


class DamageText(pygame.sprite.Sprite):
	def __init__(self, x, y, damage, colour):
		pygame.sprite.Sprite.__init__(self)
		self.image = font.render(damage, True, colour)
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)
		self.counter = 0

	def update(self):
		self.rect.y -= 1
		self.counter += 1
		if self.counter > 30:
			self.kill()		

damage_text_group = pygame.sprite.Group()		


viking = Fighter(200, 255, 'Magni', 65, 15, 2)
mummy = Fighter(440, 275, 'Mummy', 25, 5, 0)
anubis = Fighter(580, 255, 'Anubis', 50, 12, 1)

enemy_list = []
enemy_list.append(mummy)
enemy_list.append(anubis)

viking_health_bar = HealthBar(50, screen_height - bottom_panel + 40, viking.hp, viking.max_hp)

mummy_health_bar = HealthBar(450, screen_height - bottom_panel + 40, mummy.hp, mummy.max_hp)
anubis_health_bar = HealthBar(450, screen_height - bottom_panel + 100, anubis.hp, anubis.max_hp)		

potion_button = button.Button(screen, 50, screen_height - bottom_panel + 65, potion_img, 70, 70)
restart_button = button.Button(screen, 330, 120, restart_img, 120, 30)


run = True
while run:

	clock.tick(fps)

	game2.run()

	draw_panel()
	viking_health_bar.draw(viking.hp)
	mummy_health_bar.draw(mummy.hp)
	anubis_health_bar.draw(anubis.hp)

	viking.update()
	viking.draw()
	for enemy in enemy_list:
		enemy.update()
		enemy.draw()		

	damage_text_group.update()
	damage_text_group.draw(screen)	

	attack = False
	potion = False
	target = None


	pygame.mouse.set_visible(True)
	pos = pygame.mouse.get_pos()
	for count, enemy in enumerate(enemy_list):
		if enemy.rect.collidepoint(pos):
			pygame.mouse.set_visible(False)

			screen.blit(hammer_img, pos)
			if clicked == True and enemy.alive == True:
				attack = True
				target = enemy_list[count]

	if potion_button.draw():
		potion = True	

	draw_text(str(viking.potions), font, red, 105, screen_height - bottom_panel + 70)

	game.run()				

	if game_over == 0:

		if viking.alive == True:
			if current_fighter == 1:
				action_cooldown += 1
				if action_cooldown >= action_wait_time:

					if attack == True and target != None:
						viking.attack(target)

						current_fighter += 1
						action_cooldown = 0

					if potion == True:
						if viking.potions > 0:
							if viking.max_hp - viking.hp > potion_effect:
								heal_amount = potion_effect
							else:
								heal_amount = viking.max_hp - viking.hp
							viking.hp += heal_amount
							viking.potions -= 1
							damage_text = DamageText(viking.rect.centerx, viking.rect.y, str(heal_amount), green)
							damage_text_group.add(damage_text)

		else:
			game_over = -1					



		for count, enemy in enumerate(enemy_list):
			if current_fighter == 2 + count:
				if enemy.alive == True:
					action_cooldown += 1
					if action_cooldown >= action_wait_time:
						if (enemy.hp / enemy.max_hp) < 0.5 and enemy.potions > 0:
							if enemy.max_hp - enemy.hp > potion_effect:
								heal_amount = potion_effect
							else:
								heal_amount = enemy.max_hp - enemy.hp
							enemy.hp += heal_amount
							enemy.potions -= 1
							damage_text = DamageText(enemy.rect.centerx, enemy.rect.y, str(heal_amount), green)
							damage_text_group.add(damage_text)
						else:
							enemy.attack(viking)
							current_fighter += 1
							action_cooldown = 0
				else:
					current_fighter += 1

		if current_fighter > total_fighters:
			current_fighter = 1

	alive_enemy = 0
	for enemy in enemy_list:
		if enemy.alive == True:
			alive_enemy += 1
	if alive_enemy == 0:
		game_over = 1

	if game_over != 0:
		if game_over == 1:
			screen.blit(victory_img, (250, 50))
		if game_over == -1:
			screen.blit(defeat_img, (270, 50))

		if restart_button.draw():
			viking.reset()
			for enemy in enemy_list:
				enemy.reset()
			current_fighter = 1
			action_cooldown
			game_over = 0	
					

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			clicked = True
		else:
			clicked = False			

	pygame.display.update()		

pygame.quit()
