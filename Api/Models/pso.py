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