import pygame
import sys
import random
from pygame.locals import *

pygame.init()
pygame.font.init()
pygame.mixer.init()

koko = (500,500) #fortti on hyvä peli
ruutu = pygame.display.set_mode(koko)

#lataus
vihollinen = pygame.image.load("uufo.png")
pelaaja =  pygame.image.load("ukkeli.png")
tausta = pygame.image.load("tie.png")

vihollinen = pygame.transform.scale(vihollinen,(42,42))
pelaaja = pygame.transform.scale(pelaaja, (64,64))
tausta = pygame.transform.scale(tausta, koko)

# MUSA
pygame.mixer.music.load("hyvä musa.mp3")
pygame.mixer.music.play(-1)
haviamis = pygame.mixer.Sound("häviämis musa.mp3")
voittomusa = pygame.mixer.Sound("voitto musa.mp3")
#tekstit
pelifontti = pygame.font.SysFont("Impact", 30)
loppufontti = pelifontti
pelivari = (207, 207, 207)
loppuvari = (255, 0, 0)
voittoväri = (0, 38, 255)

#muuttujat
pelx = 200-30
pely = 400
pelnopeus = 5
vihunnopeus = 4
hp = 6
on_tehty = False
ennatys = 0.0

vihut = [
   [100,100],
   [200,200],
   [250,250],
]

# Ennätysksen lukemia
with open ("ennatys","r") as tiedosto: 
   luettu =  tiedosto.read()
   ennatys = int(luettu)

   # Aika jutut
kello = pygame.time.Clock()
FPS = 65
alkuaika = pygame.time.get_ticks()

# käsittelee tapahtumia
def  kasittelia():
   tapahtumat = pygame.event.get()
   for tapahtuma in tapahtumat:
      if tapahtuma.type == pygame.QUIT:
         pygame.quit()
         sys.exit()

def pelilogiikka():
   global pelx 
   global pely
   global hp
   global ennatys
   global vihunnopeus
   aika = pygame.time.get_ticks()

   # Pelaajan liikkuminen
   napit = pygame.key.get_pressed()
   if napit[pygame.K_d]:
      pelx += 5
   if napit[pygame.K_a]:
      pelx -= 5

# PYSÄYTÄ PELAAJA LAITAAN
   if pelx < 0:
      pelx = 0
   if pelx >500-64:
      pelx = 500-64

   
   # Vihollisten kiihdytys
   if (aika//1000) % 10 == 0: # onko jako jäännös nolla? tapahtuu joka 5 sekunttia
      vihunnopeus += 0.1
   
   #VIHOLLISEN liikkuminen
   for vihu in vihut:
      vihu[1]+=vihunnopeus
      if vihu[1] > 500:
         #heittää vihollisen ylös
         vihu[1] = -100
         vihu[0] = random.randint(10, 500-42-10)

#koskevatko viholliset pelaajaan
   for vihu in vihut:
      if vihu[1]+42 > pely and vihu[1] < pely+64:
         if vihu[0]+42 > pelx and vihu[0] < pelx+64:
      #koskee
            hp -= 1
            vihu[1] = -100
            vihu[0] = random.randint(10, 500-42-10)

   aika = pygame.time.get_ticks()-alkuaika
   if aika > ennatys:
      ennatys = aika

def piirtaja():
   ruutu.fill((255,255,255))
   ruutu.blit(tausta, (0,0))
   ruutu.blit(pelaaja, (pelx,pely))

   #vihollisin piirto
   for vihu in vihut:
       ruutu.blit(vihollinen, vihu)

   # Tekstin Piirto
   hpteksti = pelifontti.render("Elämät: "+str (hp), True, pelivari)
   ruutu.blit(hpteksti, (30,30))

   aika = pygame.time.get_ticks()-alkuaika
   aikateksti = pelifontti.render("Aika: "+str (aika/1000), True, pelivari)
   ruutu.blit(aikateksti, (30,70))

   ennatysteksti = pelifontti.render("Ennatys: "+str (ennatys/1000), True, pelivari)
   ruutu.blit(ennatysteksti, (30,120))




def gameover():
   global on_tehty


   if not on_tehty:
      on_tehty = True
      on_tehty = pygame.mixer.music.stop()
      haviamis.play()
      with open ("ennatys","w") as tiedosto:
         tiedosto.write(str(ennatys))

   ruutu.fill(loppuvari)

   teksti = loppufontti.render("HÄVISIT",True, pelivari)
   ruutu.blit(teksti, (30,30))

   ennatysteksti = pelifontti.render("Ennatys: "+str (ennatys/1000), True, pelivari)
   ruutu.blit(ennatysteksti, (30,120))

def voitto():
   global on_tehty


   if not on_tehty:
      on_tehty = True
      on_tehty = pygame.mixer.music.stop()
      voittomusa.play()
      with open ("ennatys","w") as tiedosto:
         tiedosto.write(str(ennatys))

   ruutu.fill(voittoväri)

   teksti = loppufontti.render("voitit",True, pelivari)
   ruutu.blit(teksti, (30,30))

   ennatysteksti = pelifontti.render("Ennatys: "+str (ennatys/1000), True, pelivari)
   ruutu.blit(ennatysteksti, (30,120))


#pelin silmukka
while True:
   kasittelia()
   aika = pygame.time.get_ticks()- alkuaika

   if hp <= 0:
      gameover()
   elif aika > 14000:
      voitto()
   else:
      pelilogiikka()
      piirtaja()


   pygame.display.flip()
   kello.tick(FPS)
