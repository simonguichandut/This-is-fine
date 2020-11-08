import numpy as np
import matplotlib.pyplot as plt
from random import seed
from scipy.spatial.distance import *
from graph import Sparse_Graph
from Objects import *
import time
from physics import *


if __name__ == "__main__":
    seed( 2 )
    # Variables
    Nparticles = 200
    q = 0.04
    wall_factor = 0.1
    action_radius = 0.15
    max_force = q * q / 0.01 ** 2
    dt = 0.05
    # Declare box
    box = Box(3, 3)

    # Declare curve
    curve = THE_CURVE()

    # Declare population
    pop = Population(box,Nparticles,charge=q,CT_fraction=0,I_time=1.5,PS_time=0.3,prob_symptom=0,prob_infect=0.15)
    # Declare population
    #pop = Population(box, Nparticules, charge = q, CT_fraction = 0.5, I_time = 1, 
    #                 PS_time = 0.5, prob_symptom = 0.2, prob_infect = 1)
    
    pop.particle_list[0].infect()
    
    particles_network = [pop.particle_list[i] \
                         for i in range( Nparticles ) if pop.particle_list[i].CT]
    graph = Sparse_Graph([particles_network[i].set_network_id(i) \
                         for i in range( len(particles_network) ) ])

    for i in range(0, 300):
        print(i)
        particule_interaction(pop, box, graph, action_radius, wall_factor, max_force, dt,i)
        pop.update_pop(dt, graph)
        box.plot_pop(pop, False, i, graph, dt)
        # print(pop.particle_list[0].clock)
        curve.plot_comp(pop, iteration=i)
        
        # if i % 99 == 0 :
        #     print("Particle 0 position:",pop.particle_list[0].pos)
        #     print("Particle 1 position:",pop.particle_list[1].pos)
        #     print("Particle 0 acceleration:",pop.particle_list[0].a)
        #     print("Particle 1 acceleration:",pop.particle_list[1].a)
            
    #curve.show(show=True)
    #curve.save()
    curve.saveV2()






