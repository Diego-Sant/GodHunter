import pygame
from support import *
from settings import tile_size, screen_height, screen_width
from tiles import StaticTile
from level_data import levels

class Level:
	def __init__(self, current_level, surface, create_overworld):
		self.display_surface = surface
		self.world_shift = 0
		self.current_x = None

		self.create_overworld = create_overworld
		self.current_level = current_level
		level_data = levels[self.current_level]
		self.new_max_level = level_data['unlock']

		terrain_layout = import_csv_layout(level_data['terrain'])
		self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')

		terrain2_layout = import_csv_layout(level_data['terrain2'])
		self.terrain2_sprites = self.create_tile_group(terrain2_layout,'terrain2')

		cacto1_layout = import_csv_layout(level_data['cacto1'])
		self.cacto1_sprites = self.create_tile_group(cacto1_layout, 'cacto1')
		cacto2_layout = import_csv_layout(level_data['cacto2'])
		self.cacto2_sprites = self.create_tile_group(cacto2_layout, 'cacto2')
		cacto3_layout = import_csv_layout(level_data['cacto3'])
		self.cacto3_sprites = self.create_tile_group(cacto3_layout, 'cacto3')

		stone1_layout = import_csv_layout(level_data['stone1'])
		self.stone1_sprites = self.create_tile_group(stone1_layout, 'stone1')
		stone2_layout = import_csv_layout(level_data['stone2'])
		self.stone2_sprites = self.create_tile_group(stone2_layout, 'stone2')
		stone3_layout = import_csv_layout(level_data['stone3'])
		self.stone3_sprites = self.create_tile_group(stone3_layout, 'stone3')
		stone4_layout = import_csv_layout(level_data['stone4'])
		self.stone4_sprites = self.create_tile_group(stone4_layout, 'stone4')

	def create_tile_group(self,layout,type):
		sprite_group = pygame.sprite.Group()

		for row_index, row in enumerate(layout):
			for col_index,val in enumerate(row):
				if val != '-1':
					x = col_index * tile_size
					y = row_index * tile_size

					if type == 'terrain':
						terrain_tile_list = import_cut_graphics('assets/terrain/Tileset3.png')
						tile_surface = terrain_tile_list[int(val)]
						sprite = StaticTile(tile_size,x,y,tile_surface)

					if type == 'terrain2':
						terrain2_tile_list = import_cut_graphics('assets/terrain/Tileset1.png')
						tile_surface = terrain2_tile_list[int(val)]
						sprite = StaticTile(tile_size,x,y,tile_surface)										

					if type == 'cacto1':
						cacto1_tile_list = import_cut_graphics('assets/decoration/cactos/1/1.png')
						tile_surface = cacto1_tile_list[int(val)]
						sprite = StaticTile(tile_size, x, y, tile_surface)
					if type == 'cacto2':
						cacto2_tile_list = import_cut_graphics('assets/decoration/cactos/2/2.png')
						tile_surface = cacto2_tile_list[int(val)]
						sprite = StaticTile(tile_size, x, y, tile_surface)
					if type == 'cacto3':
						cacto3_tile_list = import_cut_graphics('assets/decoration/cactos/3/3.png')
						tile_surface = cacto3_tile_list[int(val)]
						sprite = StaticTile(tile_size, x, y, tile_surface)

					if type == 'stone1':
						stone1_tile_list = import_cut_graphics('assets/decoration/stone/1/1.png')
						tile_surface = stone1_tile_list[int(val)]
						sprite = StaticTile(tile_size, x, y, tile_surface)
					if type == 'stone2':
						stone2_tile_list = import_cut_graphics('assets/decoration/stone/2/2.png')
						tile_surface = stone2_tile_list[int(val)]
						sprite = StaticTile(tile_size, x, y, tile_surface)
					if type == 'stone3':
						stone3_tile_list = import_cut_graphics('assets/decoration/stone/3/3.png')
						tile_surface = stone3_tile_list[int(val)]
						sprite = StaticTile(tile_size, x, y, tile_surface)																					
					if type == 'stone4':
						stone4_tile_list = import_cut_graphics('assets/decoration/stone/4/4.png')
						tile_surface = stone4_tile_list[int(val)]
						sprite = StaticTile(tile_size, x, y, tile_surface)	

					sprite_group.add(sprite)

		return sprite_group 	

	def run(self):
		self.terrain2_sprites.update(self.world_shift)
		self.terrain2_sprites.draw(self.display_surface)
		self.terrain_sprites.update(self.world_shift)
		self.terrain_sprites.draw(self.display_surface)

		self.stone1_sprites.update(self.world_shift)
		self.stone1_sprites.draw(self.display_surface)
		self.stone2_sprites.update(self.world_shift)
		self.stone2_sprites.draw(self.display_surface)
		self.stone3_sprites.update(self.world_shift)
		self.stone3_sprites.draw(self.display_surface)
		self.stone4_sprites.update(self.world_shift)
		self.stone4_sprites.draw(self.display_surface)			

		self.cacto1_sprites.update(self.world_shift)
		self.cacto1_sprites.draw(self.display_surface)
		self.cacto2_sprites.update(self.world_shift)
		self.cacto2_sprites.draw(self.display_surface)
		self.cacto3_sprites.update(self.world_shift)
		self.cacto3_sprites.draw(self.display_surface)									