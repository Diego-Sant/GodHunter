import pygame
from support import *
from settings import tile_size, screen_height, screen_width
from tiles import StaticTile
from level_data import levels

class LevelBg:
	def __init__(self, current_level, surface, create_overworld):
		self.display_surface = surface
		self.world_shift = 0
		self.current_x = None

		self.create_overworld = create_overworld
		self.current_level = current_level
		level_data = levels[self.current_level]
		self.new_max_level = level_data['unlock']

		bg1_layout = import_csv_layout(level_data['bg1'])
		self.bg1_sprites = self.create_tile_group(bg1_layout,'bg1')

		bg4_layout = import_csv_layout(level_data['bg4'])
		self.bg4_sprites = self.create_tile_group(bg4_layout,'bg4')	

	def create_tile_group(self,layout,type):
		sprite_group = pygame.sprite.Group()

		for row_index, row in enumerate(layout):
			for col_index,val in enumerate(row):
				if val != '-1':
					x = col_index * tile_size
					y = row_index * tile_size
					
					if type == 'bg1':
						bg1_tile_list = import_cut_graphics('assets/terrain/background.png')
						tile_surface = bg1_tile_list[int(val)]
						sprite = StaticTile(tile_size,x,y,tile_surface)	
						
					if type == 'bg4':
						bg4_tile_list = import_cut_graphics('assets/terrain/background4.png')
						tile_surface = bg4_tile_list[int(val)]
						sprite = StaticTile(tile_size,x,y,tile_surface)
						
					sprite_group.add(sprite)

		return sprite_group	

	def run(self):
		self.bg1_sprites.update(self.world_shift)
		self.bg1_sprites.draw(self.display_surface)
		self.bg4_sprites.update(self.world_shift)
		self.bg4_sprites.draw(self.display_surface)						