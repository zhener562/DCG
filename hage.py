import pygame
from pygame.locals import *
import sys
import random

ScreenSize = (1370, 600)
void = []

pygame.font.init()
font = pygame.font.Font(None, 20)


class player:
    def __init__(self):
        self.health = 30
        self.mana = 0
        self.MaxMana = 0
        self.hand = []
        self.permanent = []
        self.tomb = []
        self.power = 0
        self.icon = []

    def SortCards():
        global ScreenSize
        global players
        for dex, tem in enumerate(players):
            for index, item in enumerate(tem.hand):
                item.rect.move_ip(item.rect.width * (index + 1) - item.rect.left,
                                  (ScreenSize[1] - item.rect.height) * (1 - dex) - item.rect.top)
                if item.filter != 0:
                    item.filter.rect.move_ip(item.filter.rect.width * (index + 1) - item.filter.rect.left,
                                             (ScreenSize[1] - item.filter.rect.height) * (
                                                     1 - dex) - item.filter.rect.top)
            for index, item in enumerate(tem.permanent):
                item.rect.move_ip(item.rect.width * (index) - item.rect.left,
                                  (ScreenSize[1] - item.rect.height * 2) * (1 - dex / 2) - item.rect.top)
                if item.filter != 0:
                    item.filter.rect.move_ip(item.filter.rect.width * (index) - item.filter.rect.left,
                                             (ScreenSize[1] - item.filter.rect.height * 2) * (
                                                     1 - dex / 2) - item.filter.rect.top)

    def drow():

        hage = random.randint(1, 15)
        if hage <= 8:
            hg = hand("swamp", turn)
        elif hage < 11:
            hg = thinking("swamp", turn)
        elif hage <= 12:
            hg = storm("swamp", turn)
        else:
            hg = Thander("swamp", turn)

    def GetTurn():
        global turn
        global Opponent
        global box
        box = 0
        Opponent = turn
        if turn == p1:
            turn = p2
        else:
            turn = p1
        turn.MaxMana += 1
        turn.mana = turn.MaxMana
        player.drow()
        for index, item in enumerate(turn.permanent):
            item.attacktime = 1

        for index, item in enumerate(Opponent.permanent):
            item.attacktime = 0


p1 = player()
p2 = player()
players = [p1, p2]
turn = p1
Opponent = p2


class cards(pygame.sprite.Sprite):
    def __init__(self, name, owner=p1, position=void, original="None"):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.ActivateFilter = 0
        self.filter = 0
        self.owner = owner
        self.name = name
        self.image = pygame.image.load(name + ".png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (108, 150))
        w = self.image.get_width()
        h = self.image.get_height()
        self.status = random.randint(1, 5)
        self.power = self.status
        self.health = self.status
        self.ManaCost = self.status
        print(original)
        if original != "None":
            print("created by" + original.name)
            self.power = original.power
            self.health = original.health
            self.ManaCost = original.ManaCost
        self.attacktime = 0
        self.objective = 0
        self.angle = 0
        self.status = font.render(str(self.power) + "/" + str(self.health), True, (0, 0, 0), (255, 255, 255))
        self.image.blit(self.status, [w - self.status.get_width(), h - self.status.get_height()])
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.status = font.render(str(self.ManaCost), True, (0, 0, 0), (255, 255, 255))
        self.image.blit(self.status, [w - self.status.get_width(), 0])
        self.position = None

    def update(self):
        w = self.image.get_width()
        h = self.image.get_height()
        self.image = pygame.image.load(self.name + ".png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (108, 150))
        self.status = font.render(str(self.power) + "/" + str(self.health), True, (0, 0, 0), (255, 255, 255))
        self.image.blit(self.status, [w - self.status.get_width(), h - self.status.get_height()])
        player.SortCards()

    def mirror(self):
        if self.owner == p2:
            self.rect.move_ip(0, abs(450 - self.rect.top) - self.rect.top)


class ColorFilter(pygame.sprite.Sprite):
    def __init__(self, color, size, position, parent):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = Rect(position[0], position[1], size[0], size[1])
        self.position = "filter"
        self.parent = parent

    def update(self):
        if self.parent.ActivateFilter == 0:
            self.kill()


class hand(cards):
    def __init__(self, name, owner=p1, position=void):
        super().__init__(name, owner, position)

        w = self.image.get_width()
        h = self.image.get_height()
        x = w * (len(self.owner.hand) + 1)
        y = ScreenSize[1] - h
        self.rect = Rect(x, y, w, h)
        self.owner.hand.append(self)
        self.position = self.owner.hand
        self.image.set_alpha(200)
        if self.owner == p2:
            self.rect.move_ip(0, abs(450 - self.rect.top) - self.rect.top)
            # self.filter=ColorFilter((0,0,0),(w,h),(self.rect.left,self.rect.top),self)
            # self.ActivateFilter=1

    def update(self):
        self.image.set_alpha(200)
        if self.ManaCost <= self.owner.mana:
            self.BlueFilter = permanent.GetBlueFilter(self)
        elif self.filter != 0:
            self.filter.kill()


class Thander(hand):
    def __init__(self, name, owner=p1, position=void):
        super().__init__(name, owner, position)
        self.image = pygame.image.load(name + ".png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (108, 150))
        w = self.image.get_width()
        h = self.image.get_height()
        self.status = font.render("deal " + str(self.ManaCost + 1) + "damage", True, (0, 0, 0), (255, 255, 255))
        self.image.blit(self.status, [10, 100])
        hage = font.get_height()
        self.status = font.render("to any target", True, (0, 0, 0), (255, 255, 255))
        self.image.blit(self.status, [10, 100 + hage])
        self.position = "Thander"
        self.status = font.render(str(self.ManaCost), True, (0, 0, 0), (255, 255, 255))
        self.image.blit(self.status, [w - self.status.get_width(), 0])

    def update(self):
        self.image.set_alpha(200)
        if self.ManaCost <= self.owner.mana:
            self.BlueFilter = permanent.GetBlueFilter(self)
        elif self.filter != 0:
            self.filter.kill()


class storm(hand):
    def __init__(self, name, owner=p1, position=void):
        super().__init__(name, owner, position)
        self.image = pygame.image.load(name + ".png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (108, 150))
        w = self.image.get_width()
        h = self.image.get_height()
        self.status = font.render("deal " + str(self.ManaCost) + "damage", True, (0, 0, 0), (255, 255, 255))
        self.image.blit(self.status, [10, 100])
        hage = font.get_height()
        self.status = font.render("to all creature", True, (0, 0, 0), (255, 255, 255))
        self.image.blit(self.status, [10, 100 + hage])
        self.position = "storm"
        self.status = font.render(str(self.ManaCost), True, (0, 0, 0), (255, 255, 255))
        self.image.blit(self.status, [w - self.status.get_width(), 0])

    def update(self):
        self.image.set_alpha(200)
        if self.ManaCost <= self.owner.mana:
            self.BlueFilter = permanent.GetBlueFilter(self)
        elif self.filter != 0:
            self.filter.kill()


class thinking(hand):
    def __init__(self, name, owner=p1, position=void):
        super().__init__(name, owner, position)
        self.image = pygame.image.load(name + ".png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (108, 150))
        w = self.image.get_width()
        h = self.image.get_height()
        self.ManaCost = random.randint(3, 5)
        self.status = font.render("drow " + str(self.ManaCost - 1) + "cards", True, (0, 0, 0), (255, 255, 255))
        self.image.blit(self.status, [10, 100])
        hage = font.get_height()
        self.position = "thinking"
        self.status = font.render(str(self.ManaCost), True, (0, 0, 0), (255, 255, 255))
        self.image.blit(self.status, [w - self.status.get_width(), 0])

    def update(self):
        self.image.set_alpha(200)
        if self.ManaCost <= self.owner.mana:
            self.BlueFilter = permanent.GetBlueFilter(self)
        elif self.filter != 0:
            self.filter.kill()


class coin(hand):
    def __init__(self, name, owner=p1, position=void):
        super().__init__(name, owner, position)
        self.image = pygame.image.load(name + ".png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (108, 150))
        w = self.image.get_width()
        h = self.image.get_height()
        self.status = font.render("gain a mana ", True, (0, 0, 0), (255, 255, 255))
        self.image.blit(self.status, [10, 100])
        hage = font.get_height()
        self.position = "coin"
        self.ManaCost = 0
        self.status = font.render(str(self.ManaCost), True, (0, 0, 0), (255, 255, 255))
        self.image.blit(self.status, [w - self.status.get_width(), 0])

    def update(self):
        self.image.set_alpha(200)
        if self.ManaCost <= self.owner.mana:
            self.BlueFilter = permanent.GetBlueFilter(self)
        elif self.filter != 0:
            self.filter.kill()


class icon(cards):
    def __init__(self, name, owner=p1, position=void):
        cards.__init__(self, name, owner, position)
        self.owner = owner
        self.owner.icon.append(self)
        w = self.image.get_width()
        h = self.image.get_height()
        x = 0
        y = ScreenSize[1] - h
        self.rect = Rect(x, y, w, h)
        self.power = 0
        self.health = self.owner.health
        self.ManaStatus = font.render(str(self.owner.mana) + "/" + str(self.owner.MaxMana), True, (0, 0, 0),
                                      (255, 255, 255))
        self.image.blit(self.ManaStatus, [0, 80])
        cards.mirror(self)

    def update(self):
        self.image = pygame.image.load(self.name + ".png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (108, 150))
        self.ManaStatus = font.render(str(self.owner.mana) + "/" + str(self.owner.MaxMana), True, (0, 0, 0),
                                      (255, 255, 255))
        self.image.blit(self.ManaStatus, [0, 80])
        w = self.image.get_width()
        h = self.image.get_height()

        self.status = font.render(str(self.power) + "/" + str(self.health), True, (0, 0, 0), (255, 255, 255))
        self.image.blit(self.status, [w - self.status.get_width(), h - self.status.get_height()])
        if self.objective == 1:
            self.GreenFilter = permanent.GetGreenFilter(self)
        elif self.filter != 0:
            self.filter.kill()


class permanent(cards):
    def __init__(self, name, original, position=void, owner=p1):
        cards.__init__(self, name, owner, position, original)
        self.owner = owner
        w = self.image.get_width()
        h = self.image.get_height()
        x = w * (len(self.owner.permanent))
        y = ScreenSize[1] - h * 2
        self.original = original
        self.rect = Rect(x, y, w, h)
        self.owner.permanent.append(self)

        self.position = self.owner.permanent
        self.image.set_alpha(255)
        cards.mirror(self)

    def FiltersClear(self):
        if self.ActivateFilter == 1:
            self.ActivateFilter = 0
            ColorFilter.update(self.filter)

    def GetGreenFilter(self):
        permanent.FiltersClear(self)
        self.filter = ColorFilter((0, 255, 0), (self.rect.width, self.rect.height), (self.rect.left, self.rect.top),
                                  self)
        self.ActivateFilter = 1
        self.filter.image.set_alpha(100)

    def GetBlueFilter(self):
        permanent.FiltersClear(self)
        self.filter = ColorFilter((0, 0, 255), (self.rect.width, self.rect.height), (self.rect.left, self.rect.top),
                                  self)
        self.ActivateFilter = 1
        self.filter.image.set_alpha(100)

    def GetRedFilter(self):
        permanent.FiltersClear(self)
        self.filter = ColorFilter((255, 0, 0), (self.rect.width, self.rect.height), (self.rect.left, self.rect.top),
                                  self)
        self.ActivateFilter = 1
        self.filter.image.set_alpha(100)

    def attack(self, target):
        self.health -= target.power
        target.health -= self.power
        print("combat end")

    def update(self):
        cards.update(self)
        if self.health <= 0:
            self.kill()
            self.position.remove(self)
            self.ActivateFilter = 0
            if self.filter != 0:
                self.filter.kill()

        if self.attacktime == 1:
            self.BlueFilter = permanent.GetBlueFilter(self)
        elif self.filter:
            self.filter.kill()
        if box == self:
            self.RedFilter = permanent.GetRedFilter(self)
        else:
            if self.filter != 0 and self.attacktime == 0:
                self.filter.kill()
        if self.objective == 1:
            self.GreenFilter = permanent.GetGreenFilter(self)


box = 0


def main():
    global Opponent
    global turn
    pygame.init()  # Pygameの初期化
    screen = pygame.display.set_mode(ScreenSize)
    global box
    group = pygame.sprite.OrderedUpdates()
    cards.containers = group
    ColorFilter.containers = group
    catherin = icon("swamp")
    ardan = icon("swamp", p2)

    for i in players:
        for j in range(3):
            hage = random.randint(1, 10)
            if hage <= 7:
                hg = hand("swamp", i)
            else:
                hg = Thander("swamp", i)
    hg = coin("swamp", p1)
    hg = coin("swamp", p1)

    group.draw(screen)
    box = 0
    while (1):
        screen.fill((255, 255, 255))
        # スプライトを描画
        if ardan.health <= 0:
            font = pygame.font.Font(None, 200)
            hage = font.render("you win", True, (0, 0, 0), (255, 255, 255))
            screen.blit(hage, [200, 200])
            pygame.display.update()
            pygame.time.wait(5000)

        elif catherin.health <= 0:
            font = pygame.font.Font(None, 200)
            hage = font.render("you lose", True, (0, 0, 0), (255, 255, 255))
            screen.blit(hage, [200, 200])
            pygame.display.update()
            pygame.time.wait(5000)

        group.update()
        # スプライトを描画
        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:

                if box == 0:
                    for l in turn.hand:
                        if l.rect.right > x > l.rect.left and l.rect.top < y < l.rect.bottom and turn.mana >= l.ManaCost:
                            l.kill()
                            l.owner.mana -= l.ManaCost
                            turn.hand.remove(l)
                            l.ActivateFilter = 0
                            if l.position == "Thander":
                                box = l
                                Opponent = (players.index(turn) + 1) % 2
                                Opponent = players[Opponent]
                                for index, item in enumerate(Opponent.permanent):
                                    item.objective = 1
                                Opponent.icon[0].objective = 1
                            elif l.position == "coin":
                                l.owner.mana += 1
                            elif l.position == "storm":
                                for i in turn.permanent:
                                    i.health -= l.ManaCost
                                for i in Opponent.permanent:
                                    i.health -= l.ManaCost
                            elif l.position == "thinking":
                                for i in range(l.ManaCost - 1):
                                    player.drow()

                            else:
                                l = permanent(l.name, l, owner=l.owner, )

                    for l in turn.permanent:
                        if l.rect.right > x > l.rect.left and l.rect.top < y < l.rect.bottom and l.attacktime:
                            box = l
                            Opponent = (players.index(turn) + 1) % 2
                            Opponent = players[Opponent]

                            for index, item in enumerate(Opponent.permanent):
                                item.objective = 1
                            Opponent.icon[0].objective = 1
                else:
                    print(box.name)
                    for l in Opponent.permanent:
                        if l.rect.right > x > l.rect.left and l.rect.top < y < l.rect.bottom:
                            if box.position == "Thander":
                                l.health -= box.ManaCost + 1
                            else:
                                permanent.attack(box, l)
                                box.attacktime = 0
                            for index, item in enumerate(Opponent.permanent):
                                item.objective = 0
                            Opponent.icon[0].objective = 0
                            box = 0
                    l = Opponent.icon[0]
                    if l.rect.right > x > l.rect.left and l.rect.top < y < l.rect.bottom:
                        if box.position == "Thander":
                            l.health -= box.ManaCost + 1
                        else:
                            permanent.attack(box, l)
                            box.attacktime = 0
                        for index, item in enumerate(Opponent.permanent):
                            item.objective = 0
                        Opponent.icon[0].objective = 0
                        box = 0

            if event.type == KEYDOWN:
                if event.key == K_a:
                    hage = hand("swamp")
                if event.key == K_c:
                    player.SortCards()
                if event.key == K_b:
                    player.GetTurn()

            if event.type == QUIT:  # 閉じるボタンが押されたとき
                pygame.quit()
                sys.exit()
        for l in group:
            if l.rect.right > x > l.rect.left and l.rect.top < y < l.rect.bottom:
                if l.position == p1.hand:
                    l.image.set_alpha(255)

        group.draw(screen)
        pygame.display.update()


if __name__ == "__main__":
    main()
