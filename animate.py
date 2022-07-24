import pygame
import os

path = "images/Celebrate"

pic_name = []
happy_animate = []
for i in range(0, 81):
    pic_name.append(str(i) + ".png")

    temp = pygame.image.load(os.path.join(path, pic_name[i]))
    w = temp.get_width()
    h = temp.get_height()
    scale = 0.7
    temp = pygame.transform.scale(temp, (int(w * scale), int(h * scale)))
    happy_animate.append(temp)


if __name__ == "__main__":
    print(pic_name)
