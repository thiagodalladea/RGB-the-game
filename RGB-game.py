from cProfile import run
import pygame, sys, random
from pygame.locals import *

run
colors = []
winner_color = []
coords = []

pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((1920,1080))
pygame.display.set_caption('Red, Blue or Green!')
pygame.mouse.set_visible(False)
pygame.font.init()
font_350 = pygame.font.Font('FiraCode-Light.ttf', 350)
font_50 = pygame.font.Font('FiraCode-Light.ttf', 50)
font_25 = pygame.font.Font('FiraCode-Light.ttf', 25)

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
DARK_RED = (35,0,0)
GREEN = (0,255,0)
DARK_GREEN = (0,35,0)
BLUE = (0,0,255)
DARK_BLUE = (0,0,35)

class Square():
  def __init__(self, screen, color, side, startX, startY, speedX, speedY):
    self.screen = screen
    self.color = color
    self.side = side
    self.startX = startX
    self.startY = startY
    self.speedX = speedX
    self.speedY = speedY
    self.rect = pygame.Rect(startX, startY, side, side)

  def draw(self):
    pygame.draw.rect(self.screen, self.color, self.rect, 2)

  def advance(self):
    self.rect.x += self.speedX
    self.rect.y += self.speedY

    if self.rect.right >= self.screen.get_width() or self.rect.left <= 0:
      self.speedX *= -1
    if self.rect.top <= 0 or self.rect.bottom >= self.screen.get_height():
      self.speedY *= -1

  def collision(self, other):
    collision_tolerance = 25
    if self.rect.colliderect(other):
      #VERTICAL COLLISION
      if abs(self.rect.top - other.rect.bottom) < collision_tolerance and self.speedY < 0 and other.speedY > 0:
        self.speedY *= -1
        other.speedY *= -1
      if abs(self.rect.bottom - other.rect.top) < collision_tolerance and self.speedY > 0 and other.speedY < 0:
        self.speedY *= -1
        other.speedY *= -1
      if abs(other.rect.bottom - self.rect.top) < collision_tolerance and self.speedY > 0 and other.speedY > 0:
        other.speedY *= -1
      if abs(other.rect.top - self.rect.bottom) < collision_tolerance and self.speedY < 0 and other.speedY < 0:
        other.speedY *= -1

      #HORIZONTAL COLLISION
      if abs(self.rect.right - other.rect.left) < collision_tolerance and self.speedX > 0 and other.speedX < 0:
        self.speedX *= -1
        other.speedX *= -1
      if abs(self.rect.left - other.rect.right) < collision_tolerance and self.speedX < 0 and other.speedX > 0:
        self.speedX *= -1
        other.speedX *= -1
      if abs(other.rect.left - self.rect.right) < collision_tolerance and self.speedX < 0 and other.speedX < 0:
        other.speedX *= -1
      if abs(other.rect.right - self.rect.left) < collision_tolerance and self.speedX > 0 and other.speedX > 0:
        other.speedX *= -1

      #COLOR CHANGING
      if self.color == GREEN and other.color == RED:
        other.color = GREEN
      if self.color == RED and other.color == BLUE:
        other.color = RED
      if self.color == BLUE and other.color == GREEN:
        other.color = BLUE
      if other.color == GREEN and self.color == RED:
        self.color = GREEN
      if other.color == RED and self.color == BLUE:
        self.color = RED
      if other.color == BLUE and self.color == GREEN:
        self.color = BLUE

class Simulation():
  def __init__(self, nsquare, side):
    self.nsquare = nsquare
    self.side = side
    self.square = [self.init_square() for i in range(self.nsquare)]

  def init_square(self):
    x, y = random.randint(100,1820), random.randint(100,980)
    coords.append((x,y))
    sx, sy = random.choice([-2,2]), random.choice([-2,2])
    return Square(screen=window, color=BLACK, side=self.side, startX=x, startY=y, speedX=sx, speedY=sy)

  def advance(self):
    for square in self.square:
      square.advance()
      square.draw()

    for i in range(self.nsquare):
      pi = self.square[i]
      for j in range(i+1, self.nsquare):
        pj = self.square[j]
        pi.collision(pj)

  def colorize(self, nsquare):
    self.nsquare = nsquare
    qtd = self.nsquare / 3
    for i in range(self.nsquare):
      if i >= 0 and i <= qtd:
        self.square[i].color = GREEN
      elif i > qtd and i <= self.nsquare - qtd:
        self.square[i].color = RED
      else:
        self.square[i].color = BLUE

  def endgame(self):
    for i in range(self.nsquare):
      colors.append(self.square[i].color)
    result = all(element == colors[0] for element in colors)
    if (result):
      winner_color.append(colors[0])
      if winner_color[0] == RED:
        for i in range(self.nsquare):
          self.square[i].color = DARK_RED
      if winner_color[0] == GREEN:
        for i in range(self.nsquare):
          self.square[i].color = DARK_GREEN
      if winner_color[0] == BLUE:
        for i in range(self.nsquare):
          self.square[i].color = DARK_BLUE
      colors.clear()
      return False
    else:
      colors.clear()
      return True

  def winner(self):
    pygame.time.delay(1000)
    pygame.draw.rect(window, winner_color[0], pygame.Rect(785, 100, 350, 350), 4)
    if winner_color[0] == RED:
      winner = font_50.render('Red Wins!', True, WHITE)
      winner_rect = winner.get_rect(center=(1920 / 2, 620))
      window.blit(winner, winner_rect)
    elif winner_color[0] == GREEN:
      winner = font_50.render('Green Wins!', True, WHITE)
      winner_rect = winner.get_rect(center=(1920 / 2, 620))
      window.blit(winner, winner_rect)
    else:
      winner = font_50.render('Blue Wins!', True, WHITE)
      winner_rect = winner.get_rect(center=(1920 / 2, 620))
      window.blit(winner, winner_rect)

    enter = font_25.render('Press ENTER to restart', True, WHITE)
    enter_rect = enter.get_rect(center=(1920 / 4,1025))
    escape = font_25.render('Press ESC to quit', True, WHITE)
    escape_rect = escape.get_rect(center=((1920 / 4 + 1920 / 2),1025))
    window.blit(enter, enter_rect)
    window.blit(escape, escape_rect)

    pygame.display.update()

def randomSquares():
  nsquare = 60
  sim = Simulation(nsquare=nsquare, side=50)
  sim.colorize(nsquare=nsquare)

  winner_color.clear()
  run = True

  while run:
    for event in pygame.event.get():
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          run = False
          pygame.quit()
          sys.exit()
      elif event.type == QUIT:
        run = False
        pygame.exit()
        sys.exit()

    run = sim.endgame()
    window.fill(BLACK)
    sim.advance()
    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)
  
  sim.winner()

def start():
  run = True

  title_R = font_350.render('R', True, RED)
  title_G = font_350.render('G', True, GREEN)
  title_B = font_350.render('B', True, BLUE)
  subtitle = font_50.render('The Game', True, WHITE)
  wins_1 = font_25.render('Wins', True, WHITE)
  wins_2 = font_25.render('Wins', True, WHITE)
  wins_3 = font_25.render('Wins', True, WHITE)
  escape = font_25.render('Press ESC to quit', True, WHITE)
  enter = font_25.render('Press ENTER to start', True, WHITE)

  
  enter_rect = enter.get_rect(center=(1920 / 4,1025))
  escape_rect = escape.get_rect(center=((1920 / 4 + 1920 / 2),1025))
  title_rect = title_G.get_rect(center=(1920 / 2,168))
  subtitle_rect = subtitle.get_rect(center=(1920 / 2,335))
  wins_1_rect = wins_2.get_rect(center=(1920 / 2, 520))
  wins_2_rect = wins_2.get_rect(center=(1920 / 2, 670))
  wins_3_rect = wins_2.get_rect(center=(1920 / 2, 820))

  window.blit(title_R, (650,-50))
  window.blit(title_G, title_rect)
  window.blit(title_B, (1050,-50))
  window.blit(subtitle, subtitle_rect)
  window.blit(enter, enter_rect)
  window.blit(wins_1, wins_1_rect)
  window.blit(wins_2, wins_2_rect)
  window.blit(wins_3, wins_3_rect)
  window.blit(enter, enter_rect)
  window.blit(escape, escape_rect)

  pygame.draw.rect(window, RED, pygame.Rect(820, 485, 70, 70), 2)
  pygame.draw.rect(window, BLUE, pygame.Rect(1030, 485, 70, 70), 2)
  pygame.draw.rect(window, BLUE, pygame.Rect(820, 635, 70, 70), 2)
  pygame.draw.rect(window, GREEN, pygame.Rect(1030, 635, 70, 70), 2)
  pygame.draw.rect(window, GREEN, pygame.Rect(820, 785, 70, 70), 2)
  pygame.draw.rect(window, RED, pygame.Rect(1030, 785, 70, 70), 2)

  pygame.display.flip()

  while run:
    for event in pygame.event.get():
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          run = False
          pygame.quit()
          sys.exit()
        if event.key == K_RETURN:
          randomSquares()
      elif event.type == QUIT:
        run = False
        pygame.quit()
        sys.exit()

start()