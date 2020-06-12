import pygame
from pygame.locals import *
import random
import comprobadorcolisiones
import neat 
import os
pygame.font.init()
"""-----------------------------------------------------"""

STAT_FONT = pygame.font.SysFont("comicsans", 50)

class Pajaro:
	def __init__ (self,pos_y):
		self.pos_x = 100
		self.pos_y = pos_y
		self.radious = 20
		self.score = 1
		self.jumping = False
		self.vel = 0
		self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
	def update(self):
		self.pos_y -= int(self.vel)
	def draw(self,canvas):
		pygame.draw.circle(canvas,self.color,(self.pos_x,self.pos_y),self.radious)

class tubo():
	def __init__(self,pos_x,pos_y):
		self.pos_x = pos_x
		self.pos_y = pos_y
	def actualizar(self,movimiento):
		self.pos_x -= movimiento
		self.x_rect1 = self.pos_x
		self.y_rect1 = 0
		self.width_rect1 = 50
		self.height_rect1 = self.pos_y - 80 
		self.x_rect2 = self.pos_x - 10
		self.y_rect2 = self.height_rect1
		self.width_rect2 = 70
		self.height_rect2 = 10
		#tubo de abajo 
		self.x_rect3 = self.pos_x
		self.y_rect3 = self.pos_y + 80 
		self.width_rect3 = 50
		self.height_rect3 = 500 - self.y_rect3
		self.x_rect4 = self.pos_x - 10
		self.y_rect4 = self.y_rect3 - 10
		self.width_rect4 = 70
		self.height_rect4 = 10
	def dibujar(self,canvas):
		pygame.draw.rect(canvas,(255,0,0),(self.x_rect1,self.y_rect1,self.width_rect1,self.height_rect1))
		pygame.draw.rect(canvas,(255,0,0),(self.x_rect2,self.y_rect2,self.width_rect2,self.height_rect2))
		pygame.draw.rect(canvas,(255,0,0),(self.x_rect3,self.y_rect3,self.width_rect3,self.height_rect3))
		pygame.draw.rect(canvas,(255,0,0),(self.x_rect4,self.y_rect4,self.width_rect4,self.height_rect4))

def main(genomes, config):
	nets = []
	ge = []
	birds = []
	
	for genome_id, genome in genomes:
		genome.fitness = 0
		net = neat.nn.FeedForwardNetwork.create(genome, config)
		nets.append(net)
		birds.append(Pajaro(250))
		ge.append(genome)


	canvas = pygame.display.set_mode((1000,500))
	pygame.init()
	runnig = True

	tubos = []
	alive = True
	
	for i in range(5):
		tubos.append(tubo(400 + (230*i),random.randint(100,400)))
	

	while runnig and len(birds) > 0 :
		if len(birds) <= 0:
			runnig = False
			break

		pygame.time.delay(20)
		canvas.fill([142,213,222])
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				runnig = False
				pygame.quit()
		for bird in birds :
			x = birds.index(bird)
			if comprobadorcolisiones.comprobar_colisiones(bird,tubos[0]):
				ge[x].fitness -= 1
				nets.pop(x)
				ge.pop(x)
				birds.pop(x)
			else:
				bird.vel -= 7
				output = nets[x].activate((bird.pos_y,bird.pos_y - tubos[0].pos_y, tubos[0].pos_x - bird.pos_x))
				if output[0] > 0.5:
					bird.jumping = True
				if bird.jumping :
					bird.vel = 20
					bird.jumping = False
				ge[x].fitness = bird.score
				bird.update()
				bird.draw(canvas)

		

		for i in tubos:
			i.actualizar(10)
			i.dibujar(canvas)
		if tubos[0].pos_x <= 40 :
			tubos.pop(0)
			tubos.append(tubo(1190,random.randint(100,400)))
		try:	
			score_label = STAT_FONT.render("Score: " + str(birds[0].score),1,(255,255,255))
			canvas.blit(score_label, (1000 - 300 - 15, 10))
		except:
			pass
		pygame.display.update()



def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    
    p = neat.Population(config)


    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
 
    winner = p.run(main, 50)

    print('\nBest genome:\n{!s}'.format(winner))



if __name__ == "__main__":
	local_dir = os.path.dirname(__file__)
	config_path = os.path.join(local_dir, "config-feedforward.txt")
	run(config_path)