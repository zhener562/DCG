import datetime
import pygame
from pygame.locals import *
import sys
ScreenSize = (1370, 600)

pygame.font.init()
font = pygame.font.Font(None, 80)
def getNow():
    return datetime.datetime.now()
dt_now = datetime.datetime.now()
owner=[]
print(dt_now)
box =0
start_time=getNow()
stop_time=getNow()
lapList=[]
class cards(pygame.sprite.Sprite):
    def __init__(self, name):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.name = name
        self.image = pygame.image.load(name + ".png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 150))
        w = self.image.get_width()
        h = self.image.get_height()
        x = ScreenSize[0]/2 +w* (len(owner)-1.5 )
        y = ScreenSize[1] - h
        self.rect = Rect(x, y, w, h)
        owner.append(self)

class DP(cards):
    def __init__(self, name):
        cards.__init__(self, name)
        self.image = pygame.image.load(name + ".png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (400, 400))
        w = self.image.get_width()
        h = self.image.get_height()
        x = ScreenSize[0]/2 -w/2
        y = 0
        self.rect = Rect(x, y, w, h)

    def update(self):
        global box
        global start_time
        global stop_time
        global lapList
        now = getNow()
        passedTime="0:00:00.00"
        if box==0:
            passedTime = "0:00:00.00"
            #print(1)
        elif box=="start":
            passedTime = str((now-start_time))[0:10]
        elif box=="stop":
            passedTime =str((stop_time - start_time))[0:10]
        self.image = pygame.image.load(self.name + ".png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (400, 400))
        w = self.image.get_width()
        h = self.image.get_height()
        x = ScreenSize[0] / 2 - w / 2
        y = 0
        self.rect = Rect(x, y, w, h)
        self.status = font.render(passedTime , True, (0, 0, 0), (255, 255, 255))
        self.image.blit(self.status, [w/2-self.status.get_width()/2, 40])
        for i,name in enumerate(lapList):
            lapTime = str((name - start_time))[0:10]
            self.status = font.render(lapTime, True, (0, 0, 0), (255, 255, 255))
            self.image.blit(self.status, [w/2-self.status.get_width()/2,40+self.status.get_height()*(i+1)])


def main():
    pygame.init()  # Pygameの初期化
    screen = pygame.display.set_mode(ScreenSize)
    group = pygame.sprite.OrderedUpdates()
    cards.containers = group
    group.draw(screen)

    global box
    global start_time
    global stop_time
    global lapList
    start = cards("start")
    stop = cards("stop")
    lap = cards("lap")
    #increase = cards("increase")
    #decrease = cards("decrease")
    display = DP("display")
    while (1):
        now=getNow()
        screen.fill((255, 255, 255))
        group.update()
        # スプライトを描画


        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                if box != "start":
                    for l in owner:
                        if l.rect.right > x > l.rect.left and l.rect.top < y < l.rect.bottom :

                            if l.name == "start":
                                box = l.name
                                start_time=getNow()
                                lapList = []
                            elif l.name == "stop":
                                box = l.name
                            elif l.name == "lap":
                                lapList.append(getNow())
                                print(lapList)

                                box = l.name
                            elif l.name == "increase":
                                box = l.name
                            elif l.name == "decrease":
                                box = l.name
                            else:
                                box = l.name

                elif box=="start":
                    for l in owner:
                        if l.rect.right > x > l.rect.left and l.rect.top < y < l.rect.bottom:
                            if l.name == "stop":
                                box = l.name
                                stop_time=getNow()

                            elif l.name == "lap":
                                lapList.append(getNow())
                                print(lapList)
                else:
                    print(box)



            if event.type == QUIT:  # 閉じるボタンが押されたとき
                pygame.quit()
                sys.exit()

        group.draw(screen)
        pygame.display.update()


if __name__ == "__main__":
    main()