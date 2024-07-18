import pygame
from random import *
import sys

WIDTH = 450
HEIGHT = 450
SCALE = 11
IMG_SIZE = 50
TREE_CHANCE = 20
ENEMY_CHANCE = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init() 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
icon = pygame.image.load('img/sl2.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("spore rpg")
TREE_IMG = pygame.image.load('img/derevo.png').convert_alpha()
GRASS_IMG = pygame.image.load('img/grass.png').convert_alpha()
SEA_IMG = pygame.image.load('img/sea.png').convert_alpha()
MAGE_IMG = pygame.image.load('img/mage.png').convert_alpha()

class Mage:
    def __init__(self, hp, sp, xp, lvl, inventory, staff, x, y):
        self.hp = hp
        self.sp = sp
        self.xp = xp
        self.lvl = lvl
        self.staff = staff
        self.x = x
        self.y = y
        self.inventory = inventory

class Game:
    def __init__(self, walk):
        self.walk = walk

    def move(self, dx, dy, mage, map):
        new_x = mage.x + dx
        new_y = mage.y + dy
        if 0 <= new_x < SCALE and 0 <= new_y < SCALE and map[new_y][new_x] != 'T':
            map[mage.y][mage.x] = 'G'
            mage.x = new_x
            mage.y = new_y

    def battle(self, mage, enemy_type, map):
        enemy_hp = 5 * (int(enemy_type[1:]) - 1)
        battle_window = BattleWindow(mage, enemy_hp)
        while mage.hp > 0 and enemy_hp > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        enemy_hp -= 3
                        mage.hp -= 2
                        battle_window.update_stats(mage.hp, enemy_hp)
                        if enemy_hp <= 0:
                            mage.xp += 50
                            map[mage.y][mage.x] = 'G'
                            battle_window.show_results(mage.xp)
                            return True
            battle_window.draw(screen)
            pygame.display.flip()
        if mage.hp <= 0:
            print('You died')
            quit()


class Board:
    def __init__(self):
        self.bg_img = pygame.image.load('img/bg.png').convert_alpha()
        self.font = pygame.font.Font(None, 20)

    def generate_map(self):
        map = [['G' for _ in range(SCALE)] for _ in range(SCALE)]
        for _ in range(SCALE * SCALE * TREE_CHANCE // 100):
            x = randint(0, SCALE - 1)
            y = randint(0, SCALE - 1)
            map[y][x] = 'T'
        for _ in range(SCALE * SCALE * ENEMY_CHANCE // 100):
            x = randint(0, SCALE - 1)
            y = randint(0, SCALE - 1)
            map[y][x] = f'E{randint(2,3)}'
        map[0][0] = 'X'
        return map

    def draw(self, screen, mage, map):
        view = self.get_view(mage, map)
        for y in range(len(view)):
            for x in range(len(view[y])):
                screen.blit(GRASS_IMG, (x * IMG_SIZE, y * IMG_SIZE))
        for y in range(len(view)):
            for x in range(len(view[y])):
                tile = view[y][x]
                if tile == 'T':
                    screen.blit(TREE_IMG, (x * IMG_SIZE, y * IMG_SIZE))
                if tile == 'X':
                    screen.blit(MAGE_IMG, (x * IMG_SIZE, y * IMG_SIZE))
                if tile == 'E1':
                    SLIME_IMG = pygame.image.load(f'img/sl1.png').convert_alpha()
                    screen.blit(SLIME_IMG, (x * IMG_SIZE, y * IMG_SIZE))
                if tile == 'E2':
                    SLIME_IMG = pygame.image.load(f'img/sl2.png').convert_alpha()
                    screen.blit(SLIME_IMG, (x * IMG_SIZE, y * IMG_SIZE))
                if tile == 'E3':
                    SLIME_IMG = pygame.image.load(f'img/sl3.png').convert_alpha()
                    screen.blit(SLIME_IMG, (x * IMG_SIZE, y * IMG_SIZE))
                elif tile == '~':
                    screen.blit(SEA_IMG, (x * IMG_SIZE, y * IMG_SIZE))
        hp_text = self.font.render(f"HP: {mage.hp}/{10*mage.lvl}", True, BLACK)
        sp_text = self.font.render(f"SP: {mage.sp}/{5*mage.lvl}", True, BLACK)
        xp_text = self.font.render(f"XP: {mage.xp}/{100*mage.lvl}", True, BLACK)
        lvl_text = self.font.render(f"LVL: {mage.lvl}", True, BLACK)
        staff_text = self.font.render(f"STAFF: {mage.staff}", True, BLACK)
        screen.blit(hp_text, (20, 20))
        screen.blit(sp_text, (20, 40))
        screen.blit(xp_text, (20, 60))
        screen.blit(lvl_text, (20, 80))
        screen.blit(staff_text, (20, 100))

    def get_view(self, mage, map):
        view = []
        for i in range(mage.y - 4, mage.y + 5):
            row = []
            for j in range(mage.x - 4, mage.x + 5):
                if 0 <= i < SCALE and 0 <= j < SCALE:
                    row.append(map[i][j])
                else:
                    row.append('~')
            view.append(row)
        return view

class BattleWindow:
    def __init__(self, mage, enemy_hp):
        self.font = pygame.font.Font(None, 20)
        self.mage_hp = mage.hp
        self.enemy_hp = enemy_hp

    def update_stats(self, mage_hp, enemy_hp):
        self.mage_hp = mage_hp
        self.enemy_hp = enemy_hp

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 100))
        mage_hp_text = self.font.render(f"Your HP: {self.mage_hp}", True, BLACK)
        enemy_hp_text = self.font.render(f"Enemy HP: {self.enemy_hp}", True, BLACK)
        attack_text = self.font.render("Press space to attack", True, BLACK)
        screen.blit(mage_hp_text, (WIDTH // 2 - 90, HEIGHT // 2 - 40))
        screen.blit(enemy_hp_text, (WIDTH // 2 - 90, HEIGHT // 2 - 20))
        screen.blit(attack_text, (WIDTH // 2 - 90, HEIGHT // 2))

    def show_results(self, xp):
        results_window = ResultsWindow(xp)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
            results_window.draw(screen)
            pygame.display.flip()

    def drawlose(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 100))
        result_text = self.font.render(f"You died! Close the game to restart", True, BLACK)
        screen.blit(result_text, (WIDTH // 2 - 90, HEIGHT // 2 - 20))

class ResultsWindow:
    def __init__(self, xp):
        self.font = pygame.font.Font(None, 20)
        self.xp = xp

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 100))
        result_text = self.font.render(f"You won and got 50 XP! Press escape to exit", True, BLACK)
        screen.blit(result_text, (WIDTH // 2 - 90, HEIGHT // 2 - 20))

def main():
    game = Game(True)
    board = Board()
    mage = Mage(10, 5, 0, 1, [], 'Topaz Staff', 0, 0)
    map = board.generate_map()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move(-1, 0, mage, map)
                elif event.key == pygame.K_RIGHT:
                    game.move(1, 0, mage, map)
                elif event.key == pygame.K_UP:
                    game.move(0, -1, mage, map)
                elif event.key == pygame.K_DOWN:
                    game.move(0, 1, mage, map)
                elif event.key == pygame.K_d:
                    game.move(1, 0, mage, map)
                elif event.key == pygame.K_w:
                    game.move(0, -1, mage, map)
                elif event.key == pygame.K_s:
                    game.move(0, 1, mage, map)
                elif event.key == pygame.K_a:
                    game.move(-1, 0, mage, map)
        if map[mage.y][mage.x] in ['E2', 'E3']:
            enemy_type = map[mage.y][mage.x]
            if game.battle(mage, enemy_type, map):
                map[mage.y][mage.x] = 'G'
        map[mage.y][mage.x] = 'X'
        screen.blit(board.bg_img, (0, 0))
        board.draw(screen, mage, map)
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()