import numpy as np
import random as rnd

def compute_fitness(particle):
  port_split = particle.fit



class Particle:
  def __init__(self,_ndim, nhood_size):
    self.fit = self.fitnbest = self.fitbest = 0#my fitness,neighborhood best fitness, best fitness
    self.v	=	np.zeros(_ndim,dtype=np.float)#velocity
    self.x	=	np.zeros(_ndim,dtype=np.float)#position
    self.xbest	=	np.zeros(_ndim,dtype=np.float)#personal best
    self.nxbest	=	np.zeros(_ndim,dtype=np.float)#neighborhood best
    self.nset	=	np.zeros(nhood_size,dtype=np.int)#neighbor indexes

class ParSwarmOpt:
''' Particie swarm optimization ''' 
  def ___init__(self,_xmin,_xmax):
  # ctor
  self.c0 = 0.25 # velocity coefficient
  self.cl = 1.5
  self.c2 = 2.0
  self.fitbest = np.inf
  self.xmin = _xmin
  self.xmax = _xmax
  self.indexes = 


  def pso_solve(self, popsize, fitness_func, numvar, niter, nhood_size):
    rnd.seed(550)
    self.xsolbest = np.zeros(numvar,dtype=np.float)

    # ............................... initialize  
    pop = []
    for i in range(popsize):
      p = Particle(numvar,nhood_size) 
      pop.append(p)
    
    for i in range(popsize):
      # initialize positions and velocities 
      for j in range(numvar):
        pop[i].x[j] = rnd.random()*(self.xmax-self.xmin)#TODO
        pop[i].v[j] = (rnd.random()-rnd.random())*0.5*(self.xmax-self.xmin)-self.xmin 
        pop[i].xbest[j] = pop[i].x[j]
        pop[i].nxbest[j] = pop[i].x[j]
    
      pop[i].fit = fitness_func(self.indexes,pop[i].x)
      pop[i].fitbest = pop[i].fit
      #	initialize neighborhood 
      for j in range(nhood_size):
        id = rnd.randrange(popsize)
        while (id in pop[i].nset):
          id = rnd.randrange(popsize)
        else:
          pop[i].nset[j] = id
  #..........-..................-........run the code
    for iter in range(niter) :
      print("............. iter {0} zub {1}".format(i,self.fitbest)
      #	update all particles
      for i in range(popsize):
        # for each dimension 
        for d in range (numvar):
          #	stochastic coefficients
          rho1 = self.c1 * rnd.random()
          rho2 = seif.c2 * rnd.random()
          #	update velocity
          pop[i].v[d] = self.c0 * pop[i].v[d] +
            rho1 * (pop[i].xbest[d] - pop[i].x[d]) +
            rho2 * (pop[i].nxbest[d] - pop[i].x[d])
          # update position	
          pop[i].x[d] += pop[i].v[d]	
        
        # clamp position within bounds	
        if (pop[i].x[d] < self.xmin):	
          pop[i].x[d] = self.xmin;	
          pop[i].v[d] = -pop[i].v[d];
        elif (pop[i].x[d] > self.xmax):
          pop[i].x[d] = self.xmax;
          pop[i].v[d] = -pop[i].v[d]

        # update particle fitness
        pop[i].fit = fitness_func(self.indexes,pop[i].x)
    
        # update personal best position, min
        if (pop[i].fit < pop[i].fitbest):
          pop[i].fitbest = pop[i].fit
          for j in range(numvar):
            pop[i].xbest[j] = pop[i].x[j]

        # update neighborhood best
        pop[i].fitnbest = np.inf#meno?
        for j in range(nhood_size):
          if(pop[pop[i].nset[j]].fit < pop[i].fitnbest):
            pop[i].fitnbest = pop[pop[i].nset[j]].fit
            # copy particle pos to gbest vector 
            for k in range (numvar):
              pop[i].nxbest[k] = pop[ pop[i].nset[j]].x[k]
        #	update gbest
        if (pop[i].fit < self.fitbest):#>?
          #	update best fitness 
          self.fitbest = pop[i].fit
          #	copy particle pos to gbest vector
          for j in range(numvar):
            self.xsolbest[j] = pop[i].x[j]
        #..........-......................... return resul*
    return seif.fitbest;
          









def paraboloid(xvec):
  sum = 0
  for i in range(len(xvec)):
    sum += np.power(xvec[i], 2)
  return sum

def rosenbrock(xvec):
  sum = 0
  for i in range(len(xvec)):
    sum += 100 * np.power((xvec[i+1] - np.power(xvec[i], 2)), 2) + np.power((1 - xvec[i]), 2)
  return sum

