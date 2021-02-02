import numpy as np
import random as rnd



class Particle:
  def __init__(self,ndim, nhood_size):
    self.fit = self.fitnbest = self.fitbest = 0#my fitness,neighborhood best fitness, best fitness
    self.v	=	np.zeros(ndim,dtype=np.float)#velocity
    self.x	=	np.zeros(ndim,dtype=np.float)#position
    self.xbest	=	np.zeros(ndim,dtype=np.float)#personal best
    self.nxbest	=	np.zeros(ndim,dtype=np.float)#neighborhood best
    self.nset	=	np.zeros(nhood_size,dtype=np.int)#neighbor indexes

''' Particie swarm optimization ''' 
class PSO:
  def __init__(self,indexes,fitness_func, init_func, numvar,weight,xmin=0.05,xmax=1):
    self.c0 = 0.25 # velocity coefficient
    self.c1 = 1.5
    self.c2 = 2.0
    self.alpha = 1.5
    self.weight = weight
    self.fitbest = -np.inf
    self.xmin = xmin
    self.xmax = xmax-(xmin*numvar)
    self.indexes = indexes
    self.fitness_func = fitness_func
    self.init_func = init_func
    self.numvar = numvar

  '''fitness_func should take a particle as input and output a fitness, init_func should initialise a particle's position'''
  def pso_solve(self, popsize,  niter, nhood_size):
    rnd.seed(550)
    self.xsolbest = np.zeros(self.numvar,dtype=np.float)

    # ............................... initialize  
    pop = []
    for i in range(popsize):
      p = Particle(self.numvar,nhood_size) 
      pop.append(p)
    
    for i in range(popsize):
      # initialize positions and velocities 
      pop[i].x = self.init_func(self.numvar)
      for j in range(self.numvar):
        # pop[i].x[j] = rnd.random()*(self.xmax-self.xmin)
        pop[i].v[j] = (rnd.random()-rnd.random())*0.5*(self.xmax-self.xmin)-self.xmin 
        pop[i].xbest[j] = pop[i].x[j]
        pop[i].nxbest[j] = pop[i].x[j]
    
      pop[i].fit = self.fitness_func(self.indexes,self.weight,self.alpha,pop[i].x)
      pop[i].fitbest = pop[i].fit
      #	initialize neighborhood 
      for j in range(nhood_size):
        id = rnd.randrange(popsize)
        while (id in pop[i].nset):
          id = rnd.randrange(popsize)
        else:
          pop[i].nset[j] = id
      print("i::")
      print(pop[i].x)
    #..........-..................-........run the code
    for iter in range(niter) :
      print("............. iter {0} zub {1}".format(iter,self.fitbest))
      #	update all particles
      for i in range(popsize):
        # for each dimension 
        for d in range (self.numvar):
          #	stochastic coefficients
          rho1 = self.c1 * rnd.random()
          rho2 = self.c2 * rnd.random()
          #	update velocity
          pop[i].v[d] = self.c0 * pop[i].v[d] + rho1 * (pop[i].xbest[d] - pop[i].x[d]) + rho2 * (pop[i].nxbest[d] - pop[i].x[d])
          # update position	
          pop[i].x[d] += pop[i].v[d]	

        pop[i].x,pop[i].v = self.fix_pos(pop[i].x,pop[i].v)

        # for d in range (self.numvar):
        #   # clamp position within bounds	
        #   pop[i].x /= np.sum(pop[i].x)  
        #   if (pop[i].x[d] <= self.xmin):	
        #     pop[i].x[d] = self.xmin
        #     pop[i].v[d] = -pop[i].v[d]
        #   elif (pop[i].x[d] >= self.xmax):
        #     pop[i].x[d] = self.xmax
        #     pop[i].v[d] = -pop[i].v[d]
        # print(pop[i].x)



        # pop[i].x /= np.sum(pop[i].x)
        # if (int(np.sum(pop[i].x))>1):
        #   print("b::")
        #   print(pop[i].x)

        #ensure sum is 1

        # update particle fitness
        pop[i].fit = self.fitness_func(self.indexes,self.weight,self.alpha,pop[i].x)
    
        # update personal best position, min
        if (pop[i].fit > pop[i].fitbest):
          pop[i].fitbest = pop[i].fit
          for j in range(self.numvar):
            pop[i].xbest[j] = pop[i].x[j]

        # update neighborhood best
        pop[i].fitnbest = -np.inf#meno?
        for j in range(nhood_size):
          if(pop[pop[i].nset[j]].fit > pop[i].fitnbest):
            pop[i].fitnbest = pop[pop[i].nset[j]].fit
            # copy particle pos to gbest vector 
            for k in range (self.numvar):
              pop[i].nxbest[k] = pop[ pop[i].nset[j]].x[k]
        #	update gbest
        if (pop[i].fit > self.fitbest):#>?
          print(pop[i].fit)
          #	update best fitness 
          self.fitbest = pop[i].fit
          #	copy particle pos to gbest vector
          for j in range(self.numvar):
            self.xsolbest[j] = pop[i].x[j]
        #..........-......................... return result
    #return self.fitbest
    return self.xsolbest  

  def is_pos_ok(self,x):
    for i in range(len(x)):
      # clamp position within bounds	
      if (x[i] < self.xmin or x[i] > self.xmax):	
        return False
    if (int(np.sum(x))>1 or int(np.sum(x))<1 ):
      return False
    return True

  def fix_pos(self,x,v):
    pos_out = np.array([])
    vel_out = np.array([])
    for i in range(len(x)):
      # clamp position within bounds	
      if (x[i] < self.xmin):	
        pos_out= np.append(pos_out,self.xmin)
        vel_out= np.append(vel_out,-v[i])
      elif (x[i] > self.xmax):
        pos_out=np.append(pos_out,self.xmax)
        vel_out=np.append(vel_out,-v[i])
      else:
        pos_out=np.append(pos_out,x[i])
        vel_out=np.append(vel_out,v[i])
      # print(pop[
    pos_out /= np.sum(pos_out)  
    if(self.is_pos_ok(pos_out)):
      return pos_out, vel_out
    else:
      p =self.init_func(self.numvar)
      return p,v

  def ensure_sum_1(self, pos):
    res = np.array([])
    for p in pos: # ensures sum to 1.0
        res = np.append(res, p/sum(pos))
    return res




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

