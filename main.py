from random import seed
from graph import Sparse_Graph
from Objects import Particle,Box,Population,THE_CURVE
from physics import particle_interaction
import shutil
import os


# Simulation parameters

Nparticles = 200        # number of particles in the box
charge = 0.04           # particle charge
wall_factor = 0.1       # wall repulsion strength
action_radius = 0.15    # radius for interaction (infection & coulomb)
boxsize = 3             # size of (square) box

CT_fraction = 0.8         # fraction of population on contact tracing network
I_time = 1.5            # total infection time
prob_symptom = 0.15     # fraction of population that develops symptoms
PS_time = 0.3           # pre-symptomatic time
prob_infect = 0.25      # probability of infection within action radius at each timestep

dt = 0.05               # timestep
Niter = 300             # Number of iterations

seed(2)                 # Fixed random seed. Comment out for pure random


Infection_curve_frames = False



if __name__ == "__main__":

    # Declare square box
    box = Box(boxsize, boxsize)

    # Declare infection curve
    curve = THE_CURVE()

    # Declare maximum Coulomb force
    max_force = charge * charge / 0.01 ** 2

    # Declare population and infect patient zero
    pop = Population(box,Nparticles,charge,CT_fraction,I_time,PS_time,prob_symptom,prob_infect)
    pop.particle_list[0].infect()

    # Declare CT network
    particles_network = [pop.particle_list[i] \
                         for i in range( Nparticles ) if pop.particle_list[i].CT]
    graph = Sparse_Graph([particles_network[i].set_network_id(i) \
                         for i in range( len(particles_network) ) ])

    # Remove previous saved frames
    try: 
        shutil.rmtree('./box/')
    except:
        print('Could not delete folder box')
    os.makedirs('./box/',exist_ok=True)

    # Run simulation
    for i in range(0, Niter):
        print(i)
        particle_interaction(pop, box, graph, action_radius, wall_factor, max_force, dt, i)
        pop.update_pop(dt, graph)
        box.plot_pop(pop, i, graph, dt, show=False)
        curve.update(pop, iteration=i)
        
    # Save infection curve (at every iteration or just last one)
    if Infection_curve_frames:
        try: 
            shutil.rmtree('./curve/')
        except:
            print('Could not delete folder curve')
        os.makedirs('./curve/',exist_ok=True)
        curve.save_frames()
    
    curve.make_curve()







