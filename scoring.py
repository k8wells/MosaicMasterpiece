# by Timothy Downs, inputbox written for my map editor

# This program needs a little cleaning up
# It ignores the shift key
# And, for reasons of my own, this program converts "-" to "_"

# A program to get user input, allowing backspace etc
# shown in a box in the middle of the screen
# Called by:
# import inputbox
# answer = inputbox.ask(screen, "Your name")
#
# Only near the center of the screen is blitted to

#Modified by Mary Thompson, to be used for viewing colors

import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *

import math
import json
import fileinput

query_color = []
pos = {}

def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      return event.key
    else:
      pass

def display_box(screen, message):

  fontobject = pygame.font.Font(None,18)
  pygame.draw.rect(screen, (0,0,0), (50, 100,150,20), 0)
  pygame.draw.rect(screen, (255,255,255), (100, 100,100,20), 1)

  if len(message) != 0:
    screen.blit(fontobject.render(message, 1, (255,255,255)), (50,100))
  pygame.display.flip()

def show_color(screen,color,pos):
  pygame.draw.circle(screen, color, pos, 20)

def ask(screen,colors):

  pygame.font.init()
  current_string = []
  display_box(screen,"R, G, B:    " + string.join(current_string,""))
  while 1:
    inkey = get_key()
    if inkey == K_BACKSPACE:
      current_string = current_string[0:-1]
    elif inkey == K_ESCAPE:
      return
    elif inkey == K_RETURN:
      screen.fill([0,0,0])
      all_colors(screen,colors)
      query_color = parse_string(current_string)
      show_color(screen, query_color, (250,110))
      find_closest(screen,query_color,colors)
    elif inkey == K_MINUS:
      current_string.append("_")
    elif inkey <= 127:
      current_string.append(chr(inkey))  
    display_box(screen, "R, G, B:    " + string.join(current_string,""))
  
  return string.join(current_string,"")

def parse_string(string):
  getcolor = []
  val = ""
  for char in string:
    if char != ',':
      val += char
    else:
      getcolor.append(int(val))
      val = ""
  getcolor.append(int(val))
  return getcolor

        
def read_data():
    for line in fileinput.input():
        yield json.loads(line)

def colordict(data):
  dictionary = {}
  for thing in data:
      if 'color' not in thing:
          continue
      dictionary[thing['id']] = thing['color']
  return dictionary

def all_colors(screen,colors):
  x = 100
  y = 200
  count = 0
  for color in colors:
    show_color(screen, colors[color], (x,y))
    pos[color] = [x,y]
    count += 1
    if count != 9:
      x += 50
    else:
      x = 100
      y += 50
    
def find_closest(screen,q,colors):
  diff = []
  previous = 999.999
  current = 999.999
  closest = ""
  for color in colors:
    diff = [pow((a-b),2) for a,b in zip(q,colors[color])]
    current = math.sqrt(sum(diff))
    if current <= previous:
	previous = current
        closest = color
        
  pygame.draw.circle(screen, (255,255,255) , pos[closest], 20, 3)
  

#3  265
#10 291

def main():
  colordata = read_data()
  colors = colordict(colordata)

  screen = pygame.display.set_mode((640,640))

  #This must be called before ask(screen)... 'Cause I said so
  all_colors(screen,colors) 

  ask(screen,colors)

if __name__ == '__main__': main()
