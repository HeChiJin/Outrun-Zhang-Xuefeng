import asyncio


class ZhangXuefeng:
    def __init__(self):
        self.velocity = 8
        self.distance = 0
        self.portal = False

    def shift_velocity(self):
        if self.portal:
            self.velocity = 1

    def reset(self):
        self.velocity = 8
        self.distance = 0
        self.portal = False


class Player:
    def __init__(self):
        self.velocity = 1
        self.distance = 0
        self.chocliz = False
        self.sprite = False

    def purchase_chocliz(self):
        self.chocliz = True

    # Keep the misspelled name usable in case existing code calls it.
    def purchase_choliz(self):
        self.purchase_chocliz()

    def purchase_sprite(self):
        self.sprite = True

    def chase(self):
        self.velocity = 1
        if self.chocliz:
            self.velocity += 1
        if self.sprite:
            self.velocity *= 2
        self.distance += self.velocity*10

    def reset(self):
        self.velocity = 1
        self.distance = 0
        self.chocliz = False
        self.sprite = False
