from pygame import *
from random import randint
from time import sleep
#music
mixer.init()
#mixer.music.load('music.wav')
#mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
#Font
font.init()
f1 = font.Font(None, 30)
win_font = font.Font(None,200) 
win_text = win_font.render('You win', False , (200,200,255))
lose_text = win_font.render('You lose', False , ( 200,200,255))
#переменные
game = True
finish = False
score = 0
goal = 15
lost = 0
max_losts = 3
cooldown = 60

#FPS
clock = time.Clock()

#classes
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, size_x, size_y, x, y, speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    def reset(self):
        scn.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 595:
            self.rect.x += self.speed
    def fire(self):
        global bullets
        bullet = Bullet(img_bullet, 16, 32, self.rect.x + 50, self.rect.y , 8)
        bullets.add(bullet)
        fire_sound.play()

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > screen_height-40:
            self.rect.x = randint(5,615)
            self.rect.y = 0
            lost += 1

class Rock(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > screen_height-40:
            self.rect.x = randint(5,615)
            self.rect.y = 0

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()
#pictures
img_hero = 'rocket.png'
img_bg = 'cosmos-1845140_1920.jpg'
img_enemy = 'ufo.png'
img_bullet = 'bullet.png'
img_rock = 'asteroid.png'

#screen
screen_width = 700
screen_height = 500
scn = display.set_mode((screen_width, screen_height))
display.set_caption("shooter")
background = transform.scale(image.load(img_bg), (screen_width, screen_height))

player = Player(img_hero,100,100,300,400,7)
enemys = sprite.Group()
bullets = sprite.Group()
rocks = sprite.Group()

for i in range(0,6):
    enemy = Enemy(img_enemy, 80 , 80 , randint(5,screen_width - 80), -20 , randint(1,2))
    enemys.add(enemy)
for i in range(0,2):
    rock = Rock(img_rock, 60,60, randint(5,screen_width - 60), -20, 3)
    rocks.add(rock)
#game cycle
while game:
    #init 
    clock.tick(60)
    #выстрел
    if cooldown != 60:
        cooldown += 1
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN and e.key == K_SPACE:
            if cooldown == 60:
                player.fire()
                cooldown = 0
    if not finish:
        #update
        scn.blit(background,(0, 0))
        player.update()
        player.reset()

        bullets.update()
        bullets.draw(scn)

        enemys.draw(scn)
        enemys.update()

        rocks.draw(scn)
        rocks.update()
        #check finish
        if score == goal:
            scn.blit(win_text, (80, 150))
            finish = True
        elif lost >= max_losts:
            scn.blit(lose_text, (60, 150))
            finish = True
        #check collide
        if sprite.spritecollide(player, enemys, True):
            lost += 1
        elif sprite.spritecollide(player, rocks, True):
            lost = 3
        hits_enemys = sprite.groupcollide(enemys , bullets , True , True)
        #check shoot
        for h in hits_enemys:
            enemy = Enemy(img_enemy, 80 , 80 , randint(5,screen_width - 80), -20 , randint(1,2))
            enemys.add(enemy)
            score += 1
    else:
        sleep(1)
        game = False
    #score and losts text
    score_text = f1.render('Score - '+ str(score)+'/'+str(goal), False , (200,200,255))
    losts_text = f1.render('Losts - '+ str(lost)+'/'+str(max_losts), True, (200,200,255))
    scn.blit(score_text, (20, 20))
    scn.blit(losts_text, (20, 50)) 
    display.update()