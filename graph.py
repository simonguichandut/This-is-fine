import matplotlib.pyplot as plt
from collections import deque 

class Point(object):
    
    def __init__(self, x, y, H):
        self.pos = (x, y)
        self.H = H
        
        
        

class Sparse_Graph(object):
    
    def __init__(self, nodes):
        self.nodes = nodes
        self.V = len( nodes )
        self.E = 0
        self.neighbors = [ set() for i in range( self.V ) ]
        self.circles = []
        self.lines = []
       
        
       
    def connec(self, idx1, idx2):
        if ( idx2 in self.neighbors[idx1] ):
            return
        self.neighbors[idx1].add(idx2)
        self.neighbors[idx2].add(idx1)
        self.E += 1
        
        
        
    def deconnec(self, idx1, idx2):
        if ( not idx2 in self.neighbors[idx1] ):
            return
        self.neighbors[idx1].discard(idx2)
        self.neighbors[idx2].discard(idx1)
        self.E -= 1
       
       
       
    def reset(self, idxs_to_reset):
        for i in idxs_to_reset:
            for n in self.neighbors[i].copy():
                self.deconnec(i, n)
                
                
                
    def plot(self, ax, plot_nodes = True, radius = 0.1, linecolor = 'k'):
        c = [[1, 0.5, 0], [0, 0.75, 1]]
        self.circles = []
        
        for i in range( self.V ):
                
            for j in self.neighbors[i]:
                
                # plot a semi line between the points
                self.lines.append( ax.plot([self.nodes[i].pos[0], 
                         ( self.nodes[i].pos[0] + self.nodes[j].pos[0] ) / 2],
                        [self.nodes[i].pos[1], 
                         ( self.nodes[i].pos[1] + self.nodes[j].pos[1] ) / 2], 
                                                f'--{linecolor}', alpha = 0.3) )
         # plot the node
            if plot_nodes:
                self.circles.append(plt.Circle( 
                             (self.nodes[i].pos[0], self.nodes[i].pos[1]), radius, 
                                                 color = c[self.nodes[i].H], linewidth = 3) )
                ax.add_artist( self.circles[-1] )
                ax.text(self.nodes[i].pos[0], self.nodes[i].pos[1], 
                           str(i), va = 'center', ha = 'center', fontsize = 20)  
                               

                    
    def propagate(self, origin_idx):
        status = [0] * self.V  # 0 unseen, 1 tocheck, checked
        
        go_home = []
        to_check = deque()
        to_check.append( origin_idx )
        
        while to_check:
            node_idx = to_check.popleft()
            
            # Skip healthy people
            if not self.nodes[ node_idx ].H:
                go_home.append( node_idx )
                self.nodes[ node_idx ].isolate()
                for neighbor_idx in self.neighbors[ node_idx ]:
                    if status[ neighbor_idx ] == 0:
                        status[ neighbor_idx ] = 1
                        to_check.append( neighbor_idx )
            
            status[ node_idx ] = 2
            
        return go_home
    
    
    
    def propagate_plot(self, origin_idx):
        status = [0] * self.V  # 0 unseen, 1 tocheck, checked
        count = 0
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(1, 1 ,1)
        self.plot(ax)
        self.circles[ origin_idx ].set_linestyle('-')
        self.circles[ origin_idx ].set_edgecolor('k')
        fig.savefig(f"images/step{ count }.png")
        count += 1
        
        go_home = []
        to_check = deque()
        to_check.append( origin_idx )
        
        while to_check:
            node_idx = to_check.popleft()
            
            # Skip healthy people
            if not self.nodes[ node_idx ].H:
                go_home.append( node_idx )
                for neighbor_idx in self.neighbors[ node_idx ]:
                    if status[ neighbor_idx ] == 0:
                        status[ neighbor_idx ] = 1
                        to_check.append( neighbor_idx )
                        
                        self.circles[ neighbor_idx ].set_linestyle('-.')
                        self.circles[ neighbor_idx ].set_edgecolor('k')
            
            status[ node_idx ] = 2
            self.circles[ node_idx ].set_linestyle('-')
            fig.savefig(f"images/step{ count }.png")
            count += 1
            
            
        return go_home
            
        

if __name__ == "__main__":
    pt1 = Point(0, 0, 0)
    pt2 = Point(1, 0, 0)
    pt3 = Point(2, 0, 0)
    pt4 = Point(0, 1, 0)
    pt5 = Point(1, 1, 0)
    pt6 = Point(2, 1, 1)
    pt7 = Point(0, 2, 1)
    pt8 = Point(1, 2, 1)
    pt9 = Point(2, 2, 1)
    graph = Sparse_Graph([pt1, pt2, pt3, pt4, pt5, pt6, pt7, pt8, pt9])
    graph.connec(0, 1)
    graph.connec(1, 4)
    graph.connec(0, 3)
    graph.connec(3, 6)
    graph.connec(3, 7)
    graph.connec(6, 8)
    graph.connec(7, 8)
    graph.connec(7, 5)
    graph.connec(5, 2)
    
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1,1 ,1)
    graph.plot(ax)
    graph.reset( graph.propagate_plot(0) )
    
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1,1 ,1)
    graph.plot(ax)
    