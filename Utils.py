import random 
import numpy as np 

def deg2rad(x):
	return np.pi * x/180.0 

class Sensor:
	# sensor_tags = [(0,3,1.5),(0,6,1.5),(0,9,1.5),
	# 			   (0,3, 3), (0,6,3),(0,9,3),
	# 			   (0,3,3.8),(0,6,3.8),(0,9,3.8)]
	sensor_tags = [(0,0,0), (10,20,0), (30,80,0),(50,50,0),(80,70,0)]
	def __init__(self, sensor_noise = 0.1):
		self.sensor_noise = sensor_noise 
		self.sensor_reading = [0 for i in range(len(Sensor.sensor_tags))]
		
	def measure(self, position,height):
		x,y = position 
		for i in range(len(Sensor.sensor_tags)):
			x1,y1,z1 = Sensor.sensor_tags[i]
			self.sensor_reading[i] = np.sqrt(((x1-x)**2 + (y1 - y)**2) ) # + (z1 - height)**2) 
			self.sensor_reading[i] += random.gauss(0,self.sensor_noise)

	def getSensorTags(self):
		return Sensor.sensor_tags 

	def getMeasurement(self):
		return self.sensor_reading 

	def getNoise(self):
		return self.sensor_noise 

	def setMeasurement(self, measurement ):
		self.sensor_reading  = mesurement

	def setNoise(self, noise):
		self.sensor_noise = noise 




class Particle:
	world_size = 5 
	def __init__(self, sensor,position,orientation = 0, height = 1):
		self.sensor = sensor 
		self.forward_noise = 0 
		self.turn_noise = 0
		self.weight = 1 
		self.setPosition(position)
		self.setHeight(height)
		self.setOrientation(orientation)

	def measure(self):
		self.sensor.measure(self.getPosition(),self.getHeight())

	def setNoise(self,forward_noise = 0.1, turn_noise_deg = 0.1):
		self.forward_noise = forward_noise 
		self.turn_noise = turn_noise_deg 

	def getNoise(self):
		return self.forward_noise, turn_noise_deg 

	def setPosition(self,position):
		self.position = position 

	def setHeight(self,height):
		self.height = height 

	def setOrientation(self,orientation):
		self.orientation = orientation 

	def setWeight(self,weight):
		self.weight = weight 

	def getWeight(self):
		return self.weight 

	def getOrientation(self):
		return self.orientation 

	def getPosition(self):
		return self.position 

	def getHeight(self):
		return self.height 

	def move(self, turn_deg, distance):
		# comput the new orientation 
		x,y = self.getPosition()
		new_orient = (self.getOrientation() + turn_deg + random.gauss(0,self.turn_noise) ) % 360
		# compute the new distance. 
		new_distance = distance + random.gauss(0,self.forward_noise)

		new_x = max([0, (x + new_distance*np.cos(deg2rad(new_orient))) % Particle.world_size ])
		new_y = max([0, (y + new_distance*np.sin(deg2rad(new_orient))) % Particle.world_size ]) 

		self.setPosition((new_x, new_y))
		self.setOrientation(new_orient )

	def clone(self):
		# clone the current particle
		sensor = Sensor(self.sensor.getNoise())
		new_p = Particle( sensor,self.getPosition(),
						orientation = self.getOrientation(), 
						height = self.getHeight())
		new_p.setNoise(self.forward_noise, self.turn_noise)
		return new_p 





class ParticleFilter:
	def __init__(self,motion_list = [(10,10),(10,10),(15,10)]):
		self.motion_list = motion_list 
		self.counter = 0 
		self.mean_particle = None # stores the aprticle that has the mean value 
		self.true_pos_error = 1000
		self.true_orient_error = 1000 
		self.avg_pos_error = 1000 
		self.avg_orient_error = 1000 

	def filter(self,particles,main_particle):
		particles = self.move(particles,main_particle)
		weights = self.computeWeight(particles,main_particle)
		particles = self.resample(weights,particles)
		# compute the errors for the filtering process. 
		self.updateMeanParticle(particles, main_particle) 
		self.computeTrueError(main_particle)
		self.computeAverageError(main_particle)
		return particles 

	def move(self,particle_list, main_particle):
		turn, distance = self.motion_list[self.counter]
		self.counter = (self.counter + 1) % len(self.motion_list)

		main_particle.move(turn,distance)
		main_particle.measure()

		for i in range(len(particle_list)):
			particle_list[i].move(turn,distance)
			particle_list[i].measure()

		return particle_list 

	def gauss(self,x,mu,sigma):
		return (1/np.sqrt(2 * np.pi * (sigma**2))) * np.exp(-0.5*(float(x - mu)/sigma)**2)

	def computeWeight(self,particles,main_particle):
		main_measurement = main_particle.sensor.getMeasurement()
		# //print('max main measurement = ',max(main_measurement))
		# //print('min main measurement = ',min(main_measurement))
		weights = []
		for i in range(len(particles)):
			w = 1
			p_measurement = particles[i].sensor.getMeasurement() 
			#print( 'max particle measurement = ',max(p_measurement))
			#print( 'min particle measurement = ',min(p_measurement))
			for j in range(len(Sensor.sensor_tags)):
				# print('testing x = ',p_measurement[j])
				# print(' mu = ',main_measurement[j])
				# print(' sigma = ',particles[i].sensor.getNoise())

				k= self.gauss(p_measurement[j],main_measurement[j],particles[i].sensor.getNoise())
				# print('this gave k = ',k)
				w*=k 
				# print('computing w = ',w)
				# input('<en/ter to continue>')

			particles[i].setWeight(w)
			weights.append(w)
		# print("max w seen is ",max(weights))
		return weights 


	def resample(self,weights_unorm, particles): 
		# print("*****************************")
		# print(">> weight values >>> ")
		# print(" max(w) = ",max(weights_unorm))
		# print(" min(w) = ",min(weights_unorm))
		# print(" sum(w) = ",sum(weights_unorm))
		# print("*****************************")

		N = len(particles)
		index = int(random.random() * N)
		beta = 0.0 
		ksum = np.sum(weights_unorm)
		epsilon = 1e-100
		if ksum < epsilon: # if the sum is close to zero, return the particles. 
			return particles 
		weights = np.array(weights_unorm)/sum(weights_unorm)
		# print('normal weights max = ',np.max(weights))
		# print('normal weights min = ',np.min(weights))
		# print('normal weights avg = ',np.mean(weights))

		mw = np.max(weights)
		new_particles = []
		for i in range(N):
			beta += random.random() * 2 * mw 
			while beta > weights[index]:
				beta -= weights[index]
				index = (index + 1) % N
			new_particles.append(particles[index].clone())

		return new_particles 

	def updateMeanParticle(self,particles,main_particle):
		""" updates the mean_particle's position and orientation. """
		# clone mean particle from one of the particles. 
		self.mean_particle = particles[0].clone()
		# comute the mean position position and orientation 
		mean_x,mean_y = 0,0
		mean_orient = 0 
		N = len(particles) 
		for i in range(N):
			x,y = particles[i].getPosition()
			mean_x += x 
			mean_y += y 
			mean_orient += particles[i].getOrientation() 

		mean_x = mean_x / N 
		mean_y = mean_y / N 
		mean_orient = mean_orient / N 
		# set the mean values as the position and orientation of mean_particle 
		self.mean_particle.setPosition((mean_x, mean_y))
		self.mean_particle.setOrientation(mean_orient)

	def computeTrueError(self,main_particle):
		""" computes true error: which is the difference between the position and 
			orientation of the updated mean_particle and main_particle.
			Note: this error is usually not available in practice... """
		mean_pos = self.mean_particle.getPosition()
		mean_orient = self.mean_particle.getOrientation()

		act_pos = main_particle.getPosition()
		act_orient = main_particle.getOrientation()
		# position error is computed as the distance between the mean position and the 
		# actual position of the particle. 
		pos_error = np.sqrt((act_pos[0] - mean_pos[0])**2 + (act_pos[1] - mean_pos[1])**2 )
		orient_error = abs(mean_orient - act_orient)

		self.setTrueError(pos_error,orient_error)

	def computeAverageError(self, main_particle):
		""" computest the Average error by comparing the current measurement of main_particle 
		  with the measurement of the mean_particle (positioned at the mean position of all 
		  particles, and the mean orientation of the particles ) """
		# measure
		self.mean_particle.measure()
		# compare the measurement of both
		mean_mes = self.mean_particle.sensor.getMeasurement()
		act_mes  = main_particle.sensor.getMeasurement()
		# the position error is represented as a measure of the difference in measurement. 
		pos_error = np.sqrt(np.sum([(mean_mes[i] - act_mes[i])**2 for i in range(len(mean_mes))]) )
		# orientation error remains the same abs(mean - actual)
		orient_error = abs(self.mean_particle.getOrientation() - main_particle.getOrientation())

		self.setAverageError(pos_error, orient_error)


	def setTrueError(self, pos_error, orient_error):
		self.true_pos_error = pos_error 
		self.true_orient_error = orient_error 

	def setAverageError(self, pos_error, orient_error):
		self.avg_pos_error = pos_error 
		self.avg_orient_error = orient_error 

	def getTrueError(self):
		return (self.true_pos_error, self.true_orient_error)

	def getAverageError(self):
		return (self.avg_pos_error, self.avg_orient_error)