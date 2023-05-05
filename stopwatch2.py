import datetime
import pygame
import sys
from pygame.locals import *

ScreenSize = (1370, 600)

pygame.font.init()
font = pygame.font.Font(None, 80)

owner=[]
def get_now():
    return datetime.datetime.now()


def update_display_status(display, passed_time, lap_list):
    w = display.image.get_width()
    h = display.image.get_height()
    x = ScreenSize[0] / 2 - w / 2
    y = 0
    display.rect = Rect(x, y, w, h)
    display.status = font.render(passed_time, True, (0, 0, 0), (255, 255, 255))
    display.image.blit(display.status, [w / 2 - display.status.get_width() / 2, 40])

    for i, name in enumerate(lap_list):
        lap_time = str((name - start_time))[0:10]
        display.status = font.render(lap_time, True, (0, 0, 0), (255, 255, 255))
        display.image.blit(display.status,
                           [w / 2 - display.status.get_width() / 2, 40 + display.status.get_height() * (i + 1)])


class Card(pygame.sprite.Sprite):
    def __init__(self, name):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.name = name
        self.image = pygame.image.load(name + ".png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 150))
        w = self.image.get_width()
        h = self.image.get_height()
        x = ScreenSize[0] / 2 + w * (len(owner) - 1.5)
        y = ScreenSize[1] - h
        self.rect = Rect(x, y, w, h)
        owner.append(self)


class Display(Card):
    def __init__(self, name):
        super().__init__(name)
        self.image = pygame.image.load(name + ".png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (400, 400))
        w = self.image.get_width()
        h = self.image.get_height()
        x = ScreenSize[0] / 2 - w / 2
        y = 0
        self.rect = Rect(x, y, w, h)

    def update(self):
        global box
        global start_time
        global stop_time
        global lap_list

        now = get_now()
        passed_time = "0:00:00.00"

        if box == 0:
            passed_time = "0:00:00.00"
        elif box == "start":
            passed_time = str((now - start_time))[0:10]
        elif box == "stop":
            passed_time = str((stop_time - start_time))[0:10]

        update_display_status(self, passed_time, lap_list)


def main():
    pygame.init()
    screen = pygame.display.set_mode(ScreenSize)
    group = pygame.sprite.OrderedUpdates()
    Card.containers = group
    group.draw(screen)

    global box
    global start_time
    global stop_time
    global lap_list

    start = Card("start")
    stop = Card("stop")
    lap = Card("lap")
    display = Display("display")

    lap_list = []

    while True:
        now = get_now()
        screen.fill((255, 255, 255))


        group.update()

        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                if box != "start":
                    for l in owner:
                        if l.rect.right > x > l.rect.left and l.rect.top < y < l.rect.bottom:
                            if l.name == "start":
                                box = l.name
                                start_time = get_now()
                                lap_list = []
                            elif l.name == "stop":
                                box = l.name
                            elif l.name == "lap":
                                lap_list.append(get_now())
                                print(lap_list)
                            else:
                                box = l.name
                elif box == "start":
                    for l in owner:
                        if l.rect.right > x > l.rect.left and l.rect.top < y < l.rect.bottom:
                            if l.name == "stop":
                                box = l.name
                                stop_time = get_now()
                            elif l.name == "lap":
                                lap_list.append(get_now())
                                print(lap_list)
                else:
                    print(box)

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        group.draw(screen)
        pygame.display.update()
if __name__ == "main":
    main()