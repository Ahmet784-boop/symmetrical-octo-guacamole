from pygame import * # pygame kütüphanesinden her şeyi al

# ----- OYUN PENCERESİ VE ARKAPLAN -----
window = display.set_mode((700,500)) # arkaplan boyutu
display.set_caption("Labirent") # Başlık
# Arkaplan resmini al:
background = transform.scale(image.load("background.jpg"),(700, 500))
# Arkaplan resmini pencereye oturt:
window.blit(background,(0, 0))

# ----- MÜZİK -----
mixer.init() # initialize (başlat)


lose_sfx = mixer.Sound("kick.ogg") # kaybetme ses efekti
win_sfx = mixer.Sound("money.ogg") # kazanma ses efekti

# ----- YAZI -----
font.init()
font = font.Font(None, 70)
win_txt = font.render("YOU WIN!", True, (0,255,0))
lose_txt = font.render("YOU LOSE!", True, (255,0,0))
# ----- GAMESPRITE SINIFI -----
class GameSprite(sprite.Sprite): # üst sınıf: Sprite, alt sınıf: GameSprite
    def __init__(self, player_image, player_speed, player_x, player_y): # özellikler listesi
        super().__init__() # üst sınıfın özelliklerini devral
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# ----- PLAYER SINIFI -----
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 635:
            self.rect.x += self.speed
        if keys[K_DOWN] and self.rect.y < 435:
            self.rect.y += self.speed
        if keys[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
# ----- ENEMY SINIFI -----
class Enemy(GameSprite):
    direction = "left" # yön
    def update(self):
        if self.rect.x <= 470:
            self.direction = "right"
        if self.rect.x >= 640:
            self.direction = "left"
        
        if self.direction == "left":
            self.rect.x -= self.speed
        if self.direction == "right":
            self.rect.x += self.speed

# ----- WALL SINIFI -----
class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1,color_2,color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
#
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# ----- SPRITE TANIMLAMA -----
player = Player("hero.png", 5, 40, 400)
enemy = Enemy("cyborg.png", 2, 550, 270)
finish = GameSprite("treasure.png", 0, 550, 400)
w1 = Wall(0,0,0,200,0,20,100) # duvarlar (renk1, renk2, renk3, konum x, konum y, genişlik, uzunluk)
w2 = Wall(0,0,0,400,0,20,100) # ÖDEV (boyut ve konum ayarlama)
w3 = Wall(0,0,0,600,0,20,100)
avoid_list = [enemy, w1, w2, w3] # kaçmamız gereken şeylerin listesi (düşman, duvar)
# ----- OYUN DÖNGÜSÜ -----
game = True # döngü değişkeni (çarpıya basınca oyun kapansın)
clock = time.Clock() # saat objesi oluştur
end = False # döngü değişkeni (oyunu kazanınca oyun kapansın)
while game: # oyun döngüsü
    for e in event.get(): # oyundaki olayları tara
        if e.type == QUIT: # oyundan çık olayı varsa:
            game = False # döngüyü durdur
    if end == False: # eğer oyunu kazanmadıysa yine güncelle
        if sprite.collide_rect(player, finish): # kazanma durumu
            window.blit(win_txt, (200,200))
            end = True
            win_sfx.play()


        for item in avoid_list: # kaybetme durumu
            if sprite.collide_rect(player, item):
                window.blit(lose_txt, (200,200))
                end = True
                lose_sfx.play()
        window.blit(background,(0,0)) # arkaplanı güncelle
        player.update() # yeni hareket metodları
        enemy.update()
        player.reset() # eskiden yazılmış konum metodları
        enemy.reset()
        finish.reset()
        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
    display.update() # görüntü güncelle
    clock.tick(60) # saniyeyi 60'a böl (60 FPS)