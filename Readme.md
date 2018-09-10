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

Feel free to contact me if you have any contribution or comment or correction.