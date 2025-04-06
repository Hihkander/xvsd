from pygame import *
from random import randint
 
class GameSprite(sprite.Sprite): #Основной класс спрайта
    def __init__(self, player_image, player_x, player_y, player_speed, size_x=65, size_y=65):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y)) 
 
 
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
 
class Enemy(GameSprite): # Класс для врага
    def update(self):
        global lost
        self.rect.y += self.speed 
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(0, 600)
            self.speed = randint(1, 2)
            lost+=1
 
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
 
 
lost = 0 # Счётчик пропущенных врагов
score = 0
font.init()
font1 = font.Font(None, 36)
text_lose = font1.render(
    'Пропущено: ' + str(lost), 1, (255, 255, 255)
    )
 
win_width = 700
win_height = 500
 
window = display.set_mode((win_width, win_height))
display.set_caption('shooter_game')
background = transform.scale(image.load('lyz.png'), (win_width, win_height))
 
 
player = Player('pudg-Photoroom.png', 325, 400, 10)
monsters = sprite.Group()
bullets = sprite.Group()
for i in range(5):
    monsters.add(Enemy('krip-Photoroom.png', randint(0,600), randint(-200, 0), randint(1,2)))
clock = time.Clock()
FPS = 60
game = True
finish = False
while game:
 
    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish == False:
        window.blit(background, (0,0))
        player.update()
        player.reset()
        monsters.update()
        monsters.draw(window)
        if key.get_pressed()[K_SPACE]:
            bullets.add(Bullet("bullet.png", player.rect.centerx - 7, player.rect.top, 2, 15, 30))
        bullets.update()
        bullets.draw(window)  
 
        if sprite.spritecollide(player, monsters, False) or lost == 3:
            lose = font1.render('Вы проиграли :(', 1, (255, 255, 255))
            window.blit(lose, (200,200))
            finish = True
        
        if sprite.spritecollide(player, monsters, False) or lost == 3:
            lose = font1.render('Вы выйграли :(', 1, (255, 255, 255))
            window.blit(lose, (200,200))
            finish = True

        
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monsters.add(Enemy("krip-Photoroom.png", randint(80, win_width - 80), -40, randint(1, 5)))
 
 
 
        text_lose = font1.render(
        'Пропущено:' + str(lost), 1, (255, 255, 255)
        )
        window.blit(text_lose, (0,20))
 
        text_score = font1.render(
            'Счёт:' + str(score), 1, (255, 255, 255)
            )
        window.blit(text_score, (0,60))
 
    display.update()
    clock.tick(FPS)