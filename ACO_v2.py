import numpy as np

from Graph import Graph
from Solution import Solution

SOURCE = 0


class ACO(object):
    def __init__(self, q0, beta, rho, phi, K, data):
        self.parameter_q0 = q0
        self.parameter_beta = beta
        self.parameter_rho = rho
        self.parameter_phi = phi
        self.parameter_K = K

        self.graph = Graph(data)
        self.best = Solution(self.graph)
        self.best.cost = 99999999999999
        self.pheromone_init = np.ones((self.graph.N, self.graph.N))
        f = open(data + '_init', 'r')
        self.pheromone_init *= float(f.readline())
        self.pheromone = np.ones((self.graph.N, self.graph.N))

    def get_next_city(self, sol):
        # generate random q distributed in [0:1]
        q = np.random.rand()
        # beta - relative importance of pheromone vs distance 
        b = self.parameter_beta
        
        if sol.visited: source = sol.visited(len(sol.visited))
        else : source = 0
        
        if len(sol.not_visited) > 1:
              if q < self.parameter_q0:
                     nv = np.array(sol.not_visited)            # not visited
                     nv = np.delete(nv, np.where(nv==0))
                     t = self.pheromone[source][nv]            # pheromone associated to each edge
                     c = self.graph.costs[source][nv]          # cost 
                     next_city = np.argmax(t/np.power(c, b)) 
                     # print next_city
                     return nv[next_city]
              else:
                     nv = np.array(sol.not_visited)       
                     nv = np.delete(nv, np.where(nv==0))
                     t = self.pheromone[source][nv]                 # pheromone
                     c = np.power(self.graph.costs[source][nv], b)  # cost 
                     sm = np.sum(t/c) 
                     prob = np.divide(np.divide(t, c), sm)
                     prob = np.append(0, prob)
                     # print prob
                     # print np.random.choice(nv, 1, p=prob[nv])
                     return np.random.choice(nv, 1, p=prob[nv])                       
        return 0 # next city is 0
             

    def heuristic2opt(self, sol):
       new_sol = Solution(sol)
       for i in range(-1, len(sol.visited)-1):
              for k in range(-1, len(sol.visited)-1):
                     new_sol.inverser_ville(i, k)
                     new_sol.cost = new_sol.get_cost(0)
                     if new_sol.cost < sol.cost:
                            sol.visited = new_sol.visited
                            sol.cost = new_sol.cost
       

    def global_update(self, sol):
        # calcule difference to update 
        self.best = Solution(sol)
        L_gb = self.best.cost()
        
        for i in range(0,self.pheromone.shape[0]):
            for j in range(0, self.pheromone.shape[1]):
                self.pheromone[i][j] = (1 -self.parameter_rho)
                for visited_best in range(0, len(self.best.visited)): 
                        if (((i == visited_best) and (j == sol.visited[visited_best+1]))or ((j == visited_best )and i == (sol.visited[visited_best+1]))):  
                            self.pheromone[i][j] = self.pheromone[i][j] + 1/ L_gb 
                            
    def local_update(self, sol):
        index_last_visited = sol.shape[0]-1 
        i = sol.visited[index_last_visited]
        j = index_last_visited -1 
        self.pheromone[i][j] = (1 - self.parameter_phi)*self.pheromone[i][j]+ self.parameter_phi*self.pheromone_init[i][j]*self.pheromone[i][j]
        self.pheromone[j][i] = (1 - self.parameter_phi)*self.pheromone[j][i]+ self.parameter_phi*self.pheromone_init[j][i]*self.pheromone[j][i]
        

    def runACO(self, maxiteration):
        raise NotImplementedError()

# if __name__ == '__main__':
#     aco = ACO(0.9, 2, 0.1, 0.1, 10, 'N12.data')
#     aco.runACO(50)
