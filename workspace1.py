import matplotlib.pyplot as plt 

import numpy as np 
import random 

from Utils import* 


def plotParticles(particlelist):
	for i in range(len(particlelist)):
		x,y = particlelist[i].getPosition()
		plt.plot(x,y,'ro')

def plotHuman(human):
	x,y = human.getPosition()
	plt.plot(x,y,'bo')

def pltTags():
	for i in range(len(Sensor.sensor_tags)):
		x,y,z = Sensor.sensor_tags[i]
		plt.plot(x,y,'go')

def test():
	a = Sensor(0.1)
	p = Particle(a,(0,5),orientation = 45, height = 1, forward_noise = 2,turn_noise_deg = 2)

	a.measure((1,3),2)

	print(a.getMeasurement())

	print(a.getSensorTags())

	print(p.getPosition())
	print(p.getOrientation())
	print(p.getHeight())

	p.move(0,1)
	print('new position  = ',p.getPosition(), ' new orient = ',p.getOrientation())


def showFilterError(filter_algorithm, iteration):
	# dispalys the error 
	# and 
	avg_pos_error,avg_orient_error  = filter_algorithm.getAverageError()
	true_pos_error,true_orient_error = filter_algorithm.getTrueError()
	print("*"*14," (True Error) ", "*"*10," (Average Error ) ","*"*10)
	print("@ iteration = ",iteration )
	print("%14s %13s %10s %14s"%("pos error", "(%.4f)"%true_pos_error,
											  " ","(%.4f)"%avg_pos_error))
	print("%14s %13s %10s %14s"%("orient error", "(%.4f)"%true_orient_error,
											      " ","(%.4f)"%avg_orient_error))
	print("*"*70)


def showFilterProcess(particles, human):
	plotParticles(particles)
	plotHuman(human)
	pltTags()
	plt.xlim((0,Particle.world_size))
	plt.ylim((0,Particle.world_size))

# Create the Main Particle (Human) 
s1 = Sensor(0.5)
pos1 = (5,5)
orient1 = 3
human = Particle(s1,pos1,orient1,1)
human.setNoise(forward_noise = 1, turn_noise_deg = 1)

#::Create the particle set 
Nparticles = 1000
Particle.world_size = 100
particles = []
for i in range(Nparticles):
	s = Sensor(0.8)
	pos = (random.randrange(0,Particle.world_size),
		   random.randrange(0,Particle.world_size))
	orient = random.randrange(0,360)
	p = Particle(s,pos,orient,1)
	p.setNoise(forward_noise = 2,turn_noise_deg = 3)
	particles.append(p)

#::Create the ParticleFilterAlgorithm 
algorithm = ParticleFilter()
#:: tolerances 
# tolerance for each tag reading:
measurement_tolerance = 1 
avg_pos_error_tolerance = np.sqrt(len(Sensor.sensor_tags) * (measurement_tolerance **2) )
# tolerance for orientation. 
avg_orient_error_tolerance = 2 
#:: Start the filter process. 
showFilterProcess(particles,human)
plt.pause(0.1)
counter = 0 
for i in range(1000):
	plt.clf()
	particles = algorithm.filter(particles,human)
	showFilterError(algorithm,i)
	showFilterProcess(particles, human)
	# Convergence test. 
	avg_pos_error, avg_orient_error = algorithm.getAverageError()
	if ((avg_pos_error < avg_pos_error_tolerance) and 
	   (avg_orient_error < avg_orient_error_tolerance)):
	   print("Convergence Reached")
	   print(" pos_tolerance of (",avg_pos_error_tolerance,") reached ")
	   print(" orient_tolerance of (",avg_orient_error_tolerance,") reached")
	   if counter % 50 == 0: 
	   		input('<enter to continue>')
	   counter += 1 

	plt.pause(0.1)

plt.pause(0)
