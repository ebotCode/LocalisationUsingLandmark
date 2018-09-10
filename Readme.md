# SimpleLocalisation 

This Repository contains code that implements the particle filter localisation algorithm which is used in Self Driving car technology today. 

Programming langauge : Python 
libraries : matplotlib, numpy

Description:

This implementation uses 4 landmarks.

The robot (autonomous vehicle) is represented as a blue circle, and the particles are represented as red circles, and the land marks are represented as green-circles.


Initially, the mobile robot doesn't know where it is. This is seen by the uniform distribution of the particles over space.

![Alt text](/img/img1.png?raw=true "Initial Particle Distribution")

As the robot moves and takes measurements, the particle filter algorithms uses the measurements to weight each particle, and generates a new set of particles sampled propotional to their weights. The particle weights just represent how likely it is that the measurement taken by the robot was taken at that particle location, and with that particles orientation. 

Here is a converged solution after a few iterations : 

![Alt text](/img/img2.png?raw=true "Initial Particle Distribution")

As you can see above, the particles (red circles) are concentrated around the robot (blue circle). And there you have it, the robot now knows where it is using the information provided by the particle filter. 

One more thing to note is tuning the modeled process noise added. I noticed that if you take out noise from the measuremnent model (beam based model), the algorithm is practically useless. it doesn't do anything. So it needs noise...why?...it is because robot motion and measurement has uncertainty associated with it. This uncertainty can be caused by noise in measurements, noise in motion. modelling this noise in the motion and measurment models allows the robot to perform better. One of my favorite quotes from Sebastian Thrun,CEO Udacity, "a robot that has a sense of its uncertainty would perform better than one that doesn't"...hope it sparks some thinking..lol

Feel free to contact me if you have any contribution or comment or correction.