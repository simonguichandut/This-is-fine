# Structure of the Particle, Box and Population classes

from random import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.lines import Line2D



class Particle:

    def __init__(self, i, x0, y0, vx0, vy0, q, CT, IT, PST):

        # Basic parameters
        self.i = i          # identifier
        self.network_id = 0  # identifier in network
        self.pos = (x0,y0)  # position tuple
        self.v = (vx0,vy0)  # velocity tuple
        self.a = (0,0)      # acceleration tuple
        self.q = q          # charge
        self.speed_cap = 0.5

        # Boolean epidemic parameters
        self.CT = CT        # on contact tracing network 
        self.H  = True      # Healthy
        self.AS = False     # Infected asymptomatic
        self.S  = False     # Infected symptomatic
        self.I  = False     # Immune
        self.ISO = False    # Isolated

        # Changing from pre-symptomatic to symptomatic
        self.clock = 0      # Infection clock
        self.IT    = IT     # Total infection time
        self.PST   = PST    # A tuple. PST[0]=True if the particle will develop symptom. PST[1] is the pre-symptomatic time if PST[0]=True, else None

    def set_network_id(self, id):
        self.network_id = id
        return self

    def update(self, dt, lims, graph):

        # lims is (xmin,xmax,ymin,ymax)

        self.v = (self.v[0]+self.a[0]*dt, self.v[1]+self.a[1]*dt)

        # Capping speed to stop particles to go away
        if abs(self.v[0]) > self.speed_cap:
            self.v = (np.sign(self.v[0])*self.speed_cap,self.v[1])
        if abs(self.v[1]) > self.speed_cap:
            self.v = (self.v[0], np.sign(self.v[1])*self.speed_cap)

        self.pos = (self.pos[0]+self.v[0]*dt, self.pos[1]+self.v[1]*dt)

        # If exited box, place at wall with opposite velocity (reflection)
        if self.pos[0]<lims[0]:
            self.pos = (lims[0] + 0.01,self.pos[1])
            self.v = (self.v[0]*-1,self.v[1])
        elif self.pos[0]>lims[1]:
            self.pos = (lims[1] - 0.01,self.pos[1])
            self.v = (self.v[0]*-1,self.v[1])

        if self.pos[1]<lims[2]:
            self.pos = (self.pos[0],lims[2] + 0.01)
            self.v = (self.v[0],self.v[1]*-1)
        elif self.pos[0]>lims[3]:
            self.pos = (self.pos[0],lims[3] - 0.01)
            self.v = (self.v[0],self.v[1]*-1)


        if self.H == False: # (if sick)
            self.clock += dt

            if self.ISO is False and self.PST[0] is True and self.clock > self.PST[1]: 
                
                if self.CT:
                    graph.reset( graph.propagate( self.network_id ) )
                    
                # reached end of pre-symptomatic phase and is still in the population
                self.AS = False
                self.S  = True
                self.ISO = True # stays home because symptoms

            if self.clock > self.IT: # finished infection time
                self.H,self.AS,self.S = True,False,False
                self.I = True # now Immune
                self.ISO = False
                self.clock = 0

    def infect(self):
        if self.I == False:
            self.H  = False
            self.AS = True      # asymptomatic when first infected

    def isolate(self):
        self.ISO = True
        self.a = (0, 0)
        self.v = (0, 0)


class Box:

    def __init__(self, w, h):
        self.w = w
        self.h = h

        # Init box plot
        plt.style.use('dark_background')
        self.fig = plt.figure(figsize=(8, 6)) 
        gs = gridspec.GridSpec(1, 2, width_ratios=[4, 1], wspace=0) 
        self.ax1 = plt.subplot(gs[0])
        self.ax2 = plt.subplot(gs[1])
        self.ax1.title.set_text('Normal Population')
        self.ax2.title.set_text('Isolated')
        self.ax1.set_xlim([-self.w/2,self.w/2])
        self.ax1.set_ylim([-self.h/2,self.h/2])
        for ax in (self.ax1,self.ax2):
            ax.xaxis.set_ticklabels([])
            ax.xaxis.set_ticks([])
            ax.yaxis.set_ticklabels([])
            ax.yaxis.set_ticks([])
            
        legend_elements = [Line2D([0], [0], marker='o', color='w', label='Healthy', markerfacecolor='w', markersize=10, lw=0),
                           Line2D([0], [0], marker='o', color='r', label='Infected', markerfacecolor='r', markersize=10, lw=0),
                           Line2D([0], [0], marker='o', color='g', label='Immune', markerfacecolor='g', markersize=10, lw=0),
                           Line2D([0], [0], marker='v', color='w', label='Healthy, on CT network', markerfacecolor='w', markersize=10, lw=0),
                           Line2D([0], [0], marker='v', color='r', label='Infected, on CT network', markerfacecolor='r', markersize=10, lw=0),
                           Line2D([0], [0], marker='v', color='g', label='Immune, on CT network', markerfacecolor='g', markersize=10, lw=0)]

        self.ax1.legend(handles=legend_elements, ncol=2, bbox_to_anchor=(1,0.01),bbox_transform=self.ax1.transAxes, frameon=False)


    def random_pos_vel(self,v):
        x,y = random()*self.w - self.w/2 , random()*self.h - self.h/2
        theta = 2*np.pi*random()
        vx,vy = v*np.cos(theta), v*np.sin(theta)
        return x,y,vx,vy

    def plot_pop(self,pop, iteration, graph, dt, show):

        self.ax2.set_xlim([0,5])
        self.ax2.set_ylim([0,pop.Nparticles/4+1])
        iso_x,iso_y = 1,pop.Nparticles/4

        time_string = ('t = ' + ('%d'%(iteration+1)).ljust(4) + (' (%.2f IT)'%((iteration+1)*dt/pop.I_time)))
        time_text = self.ax1.text(-1.4,1.4,time_string,ha='left',va='center',transform=self.ax1.transData)

        points = []
        for p in pop.particle_list:

            if p.H is True and p.I is False:
                col = 'w'
            elif p.AS is True or p.S is True:
                col = 'r'
            elif p.I is True:
                col = 'g'

            marker = 'o' if p.CT == False else 'v'

            if p.ISO is False:
                points.append(self.ax1.plot(p.pos[0],p.pos[1],marker=marker,markerfacecolor=col,ms=5,markeredgecolor=col))
            else:
                points.append(self.ax2.plot(iso_x,iso_y,marker=marker,markerfacecolor=col,ms=5,markeredgecolor=col))
                iso_x += 1
                if iso_x == 5:
                    iso_x = 1
                    iso_y -= 1

        if not graph.E == 0:
            graph.plot(self.ax1, plot_nodes = False, linecolor = 'w')
            
            
        if show==True:
            plt.show()
        else:
            self.fig.savefig('box/%06d.png'%iteration, bbox_inches='tight', dpi=300)

        for point in points:
            point.pop(0).remove()

        time_text.remove()
            
        if not graph.E == 0:
            for line in graph.lines:
                 line.pop(0).remove()
            graph.lines = []
                 




class Population:

    def __init__(self, box, Nparticles, charge, CT_fraction, I_time, PS_time, prob_symptom, prob_infect):
        
        self.Nparticles = Nparticles
        self.box = box
        self.I_time = I_time

        self.prob_infect = prob_infect

        self.particle_list = []
        for i in range(Nparticles):
            x0,y0,vx0,vy0 = box.random_pos_vel(0.2)

            CT = True if random()<=CT_fraction else False
            PST = (True,PS_time) if random()<=prob_symptom else (False,)


            self.particle_list.append(Particle(i,x0,y0,vx0,vy0,charge,CT,I_time,PST))

    def update_pop(self, dt, graph):
        for p in self.particle_list:
            p.update(dt,lims=(-self.box.w/2,self.box.w/2,-self.box.h/2,self.box.h/2), graph=graph)



class THE_CURVE:
    def __init__(self):
        # Init compile plot
        self.fig, self.ax = plt.subplots()
        self.ax.set(xlabel='Time', ylabel='Population')
        self.not_infected = []
        self.infected = []
        self.immune = []
        self.iteration = []

    def update(self, pop, iteration=0):

        count_not_infected = 0
        count_infected = 0
        count_immune = 0

        self.iteration.append(iteration)

        for p in pop.particle_list:
            if p.H is True and p.I is False:
                count_not_infected += 1
            elif p.AS is True or p.S is True:
                count_infected += 1
            elif p.I is True:
                count_immune += 1

        self.not_infected.append(count_not_infected)
        self.infected.append(count_infected)
        self.immune.append(count_immune)

    def make_curve(self,show=False):
        self.iteration = np.array(self.iteration)
        self.infected = np.array(self.infected)
        self.immune = np.array(self.immune)
        self.not_infected = np.array(self.not_infected)

        self.ax.set_xlim([0,len(self.iteration)-1])
        self.ax.set_ylim([0,self.infected[0]+self.not_infected[0]+self.immune[0]])

        self.ax.fill_between(self.iteration, self.infected+self.not_infected, self.infected+self.not_infected+self.immune, color='g')
        self.ax.fill_between(self.iteration, self.infected, self.infected+self.not_infected, color='w')
        self.ax.fill_between(self.iteration, 0, self.infected, color='r')

        if show:
            plt.show()
        else:
            self.fig.savefig('curve.png', bbox_inches='tight', dpi=300)

    #### besoin de ce saveV1?
    # def save(self):

    #     self.fig2, self.ax = plt.subplots()
    #     self.ax.set(xlabel='Time', ylabel='Population')

    #     self.iteration = np.array(self.iteration)
    #     self.infected = np.array(self.infected)
    #     self.immune = np.array(self.immune)
    #     self.not_infected = np.array(self.not_infected)

    #     self.ax.set_xlim([0,len(self.iteration)-1])
    #     self.ax.set_ylim([0,self.infected[0]+self.not_infected[0]+self.immune[0]])

    #     for i in range(len(self.iteration)):

    #         self.ax.fill_between(self.iteration, self.infected + self.not_infected,self.infected + self.not_infected + self.immune, color='g')
    #         self.ax.fill_between(self.iteration, self.infected, self.infected + self.not_infected, color='w')
    #         self.ax.fill_between(self.iteration, 0, self.infected, color='r')
    #         line = self.ax.plot([self.iteration[i],self.iteration[i]],[0,self.infected[0]+self.not_infected[0]+self.immune[0]], color = 'b')

    #         self.fig2.savefig('curve/%06d.png'%i, bbox_inches='tight', dpi=300)

    #         line.remove(self.ax.lines.pop(-1))

    def save_frames(self):

        self.fig2, self.ax = plt.subplots()
        self.ax.set(xlabel='Time', ylabel='Population')

        self.iteration = np.array(self.iteration)
        self.infected = np.array(self.infected)
        self.immune = np.array(self.immune)
        self.not_infected = np.array(self.not_infected)

        self.ax.set_xlim([0,len(self.iteration)-1])
        self.ax.set_ylim([0,self.infected[0]+self.not_infected[0]+self.immune[0]])

        for i in range(len(self.iteration)):
            j= i+1

            self.ax.fill_between(self.iteration[0:j], self.infected[0:j] + self.not_infected[0:j],self.infected[0:j] + self.not_infected[0:j] + self.immune[0:j], color='g')
            self.ax.fill_between(self.iteration[0:j], self.infected[0:j], self.infected[0:j] + self.not_infected[0:j], color='w')
            self.ax.fill_between(self.iteration[0:j], 0, self.infected[0:j], color='r')

            self.fig.savefig('curve/%06d.png'%i, bbox_inches='tight', dpi=300)


