import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import *
from Objects import *
import time

def particule_interaction(population, box, graph, action_radius, wall_factor, max_force, dt, iteration):
    coord_list = [p.pos for p in population.particle_list]
    # F = k * (q1* q2) / r^2
    #for particule in particule_list:
        #coord_list.append(particule.pos)

    # dm = cdist(XA, XB, lambda
    dist_array = cdist(coord_list, coord_list, 'euclidean')

    for i in range(len(dist_array)):
        local_force_x = [0.]
        local_force_y = [0.]
        for j in range(len(dist_array)):

            # If the distance is shorter than the action radius
            if dist_array[i, j] < action_radius and not i == j and population.particle_list[i].ISO == False and population.particle_list[j].ISO == False:

                if ( population.particle_list[i].CT and ( not population.particle_list[i].ISO) and population.particle_list[j].CT) and ( not population.particle_list[j].ISO) and iteration > 70:
                    graph.connec(population.particle_list[i].network_id, population.particle_list[j].network_id )
                    
                # Propagate infection
                infect(population.particle_list[i], population.particle_list[j], population.prob_infect)

                if (population.particle_list[i].pos[0] - population.particle_list[j].pos[0]) != 0:
                    force_x = (population.particle_list[i].pos[0] - population.particle_list[j].pos[0]) * population.particle_list[i].q * population.particle_list[j].q / np.abs((population.particle_list[i].pos[0] - population.particle_list[j].pos[0]) ** 3)

                    local_force_x.append(np.sign(force_x) * min(abs(force_x), max_force))

                if (population.particle_list[i].pos[1] - population.particle_list[j].pos[1]) != 0:
                    force_y = (population.particle_list[i].pos[1] - population.particle_list[j].pos[1]) * population.particle_list[i].q * population.particle_list[j].q / np.abs((population.particle_list[i].pos[1] - population.particle_list[j].pos[1]) ** 3)
                    local_force_y.append(np.sign(force_y) * min(abs(force_y), max_force))
        
        if population.particle_list[i].pos[0] < -0.95 / 2 * box.w:
            wall_forcex = 1 / (box.w / 2 + population.particle_list[i].pos[0]) * wall_factor
            local_force_x.append(wall_forcex)

        elif population.particle_list[i].pos[0] > 0.95 / 2 * box.w:
            wall_forcex = 1 / (population.particle_list[i].pos[0] - box.w / 2) * wall_factor
            local_force_x.append(wall_forcex)

        else:
            wall_forcex = 0


        if population.particle_list[i].pos[1] < -0.95 / 2 * box.h:
            wall_forcey = 1 / (box.h / 2 + population.particle_list[i].pos[1]) * wall_factor
            local_force_y.append(wall_forcey)

        elif population.particle_list[i].pos[1] > 0.95 / 2 * box.h:
            wall_forcey = 1 / (population.particle_list[i].pos[1] - box.h / 2) * wall_factor
            local_force_y.append(wall_forcey)

        else:
            wall_forcey = 0

            # Update acceleration -- F = ma
            # population.particle_list[i].a = (sum(local_force_x) + population.particle_list[i].a[0], sum(local_force_y) + population.particle_list[i].a[1])
        population.particle_list[i].a = (sum(local_force_x), sum(local_force_y))

        # Checked if flipped sign
        vxold, vyold = population.particle_list[i].v
        ax, ay = population.particle_list[i].a
        vxnew, vynew = vxold + ax*dt, vyold + ay*dt

        if vxold+vxnew < vxold:  # different sign
            population.particle_list[i].v = (vxnew, population.particle_list[i].v[1])
            population.particle_list[i].a = (0, population.particle_list[i].a[1])
        if vyold+vynew < vyold:
            population.particle_list[i].v = (population.particle_list[i].v[0], vynew)
            population.particle_list[i].a = (population.particle_list[i].a[0], 0)

        local_force_x.append(wall_forcex)
        local_force_y.append(wall_forcey)

        # wall_forcex = (4/3)*(1/(box.w/2 + population.particle_list[i].pos[0])+1/(population.particle_list[i].pos[0]-box.w/2)) * wall_factor
        # wall_forcey = (4/3)*(1/(box.h/2 + population.particle_list[i].pos[1])+1/(population.particle_list[i].pos[1]-box.h/2)) * wall_factor
        # local_force_x.append(wall_forcex)
        # local_force_y.append(wall_forcey)


        # Update acceleration -- F = ma
        #population.particle_list[i].a = (sum(local_force_x) + population.particle_list[i].a[0], sum(local_force_y) + population.particle_list[i].a[1])
        population.particle_list[i].a = (sum(local_force_x), sum(local_force_y))

    return

def infect(particle1, particle2, infection_probability):
    if particle1.H == False: # this guy is sick
        if random() < infection_probability:
            particle2.infect()
        return

if __name__ == "__main__":
    # Variables
    Nparticules = 1000
    q = 0.1
    wall_factor = 0.1
    action_radius = 0
    dt = 0.1
    # Declare box
    box = Box(3, 3)

    # Declare population
    pop = Population(box, Nparticules, q, 0.5, 10, 2, 0.5)
    t = time.time()
    particule_accel(pop, box, action_radius, wall_factor)
    print("Time normal", time.time()-t)










