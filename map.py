import pygame, csv


TILE_SIZE = 32
MAP_FILES = ["map1/map_Tile Layer 1.csv", "map1/map_Extra.csv", "map1/map_Collide.csv"]
TILE_SHEET_FILE = "tiles/forest_tiles.png"
TILE_COLUMNS = 16


tile_sheet = pygame.image.load(TILE_SHEET_FILE)


def load_tiles(sheet, tile_size, columns):
    tiles = []
    sheet_width, sheet_height = sheet.get_size()
    rows = sheet_height // tile_size

    for y in range(rows):
        for x in range(columns):
            rect = pygame.Rect(x*tile_size, y*tile_size, tile_size, tile_size)
            tiles.append(sheet.subsurface(rect))

    return tiles


tiles = load_tiles(tile_sheet, TILE_SIZE, TILE_COLUMNS)

def load_csv_map():
    pass