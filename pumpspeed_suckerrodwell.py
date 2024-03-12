import numpy as np
import matplotlib.pyplot as plt
import math

# The values should be change according the requirements. This part can be also changed in the equations below and deleted.
a = 1
b = 2
c = 3
d = 4
e = 5
f = 6
g = 7

tubing_head = 100
bubble_point = 100
plunger_diameter = 1.25
tubing_OD = 2.375
tubing_ID = 2
bo = 1.1
bw = 1.03
sg_water = 1.05
fs = 1.35
steel_density = 490
em = 3*10**7
gl = 0.5
volumetric_efficiency = 0.75
perforation_depth = 3000+f*100
reservoir_pressure = perforation_depth*0.38
productivity_index = 1.20+e*0.05
API = 15+e*2
water_cut = 10+f*5
X = 300+g*20
L = perforation_depth-X

rod_number = 76
first_rod_diameter = 7/8
second_rod_diameter = 6/8

area_first_rod = math.pi*(first_rod_diameter/2)**2
area_second_rod = math.pi*(second_rod_diameter/2)**2
rod_fraction = 0.5
length_first_rod = L*rod_fraction
length_second_rod = L*(1-rod_fraction)

# Pumping unit size is C-114D-133-54 
peak_torque=114000
peak_polished = 13300
max_stroke_length = 54
c_list = [24,20,16]
D1 = 64
D2 = 72
Cs = 330
h = 74.5

sg_oil = 141.5/(131.5+API)
sg_fluid = sg_oil*(1-water_cut/100)+sg_water*water_cut/100
tubing_area = math.pi*(tubing_OD**2-tubing_ID**2)/4
plunger_area = math.pi*plunger_diameter**2*0.25
Wr = (steel_density/144)*(length_first_rod*area_first_rod+length_second_rod*area_second_rod)
Wf = (62.4*sg_fluid)*(L*plunger_area/144)
B = (62.4*sg_fluid)*(Wr/steel_density)

peak_polished_rod = [[] for i in range(3)]
peak_torque_list = [[] for i in range(3)]
stress_top_rod = [[] for i in range(3)]
pump_displacement_rate = [[] for i in range(3)]
oil_production_rate = [[] for i in range(3)]
pumping_speed = [[] for i in range(3)]
optimum_spm = [[] for i in range(3)]
speed_list = []
optimum_production_rate = [[] for i in range(3)]

for i in range(len(c_list)):
    c = c_list[i]
    S = 2*c*D2/D1
    N_limit = (70471*gl/(S*(1-c/h)))**0.5
    speed_list.append(N_limit)
    counter = 1
    j = 1
    
    for N in np.arange(3,N_limit+6,0.01):
        diff = 1
        D_guess = 200
        while diff > 0.1:
            max_acc = (S*N**2/70471)*(1+c/h)
            Wmax = Wf+Wr+Wr*max_acc - B
            min_acc = (S*N**2/70471)*(1-c/h)
            Wmin = Wr-Wr*min_acc-B
            counter_balance = (Wmax+Wmin)*0.5
            Tp = 0.5*S*(Wmax-counter_balance+Cs)
            max_stress = Wmax/area_first_rod
            M = 1+c/h
            ep = 40.8*L**2*max_acc/em
            et = 5.2*sg_fluid*D_guess*plunger_area*L/em/tubing_area
            er = (5.2*sg_fluid*D_guess*plunger_area/em)*(length_first_rod/area_first_rod + length_second_rod/area_second_rod)
            Sp = S+ep-(et+er)
            Qpd = 0.1484*plunger_area*Sp*N*volumetric_efficiency
            qo = Qpd/(bo+bw*(water_cut*0.01/(1-water_cut*0.01)))
            bottom_hole = reservoir_pressure-(Qpd/productivity_index)
            H = bottom_hole/(0.433*sg_fluid)
            D_new = perforation_depth-H
            diff = abs(D_new-D_guess)
            D_guess = D_new
        pumping_speed[i].append(N)
        peak_polished_rod[i].append(Wmax)
        peak_torque_list[i].append(Tp)
        stress_top_rod[i].append(max_stress)
        pump_displacement_rate[i].append(Qpd)
        oil_production_rate[i].append(qo)
        
        if Tp>peak_torque or Wmax>peak_polished:
            if counter == 1:
                optimum_spm[i] = pumping_speed[i][j-1]
                counter = 0
        elif N == N_limit or counter:
            optimum_spm[i] = N_limit
                       
        optimum_production_rate[i]=oil_production_rate[i][j-1]
        j = j+1
        
for i in range(len(optimum_production_rate)):
    if max(optimum_production_rate) == optimum_production_rate[i]:
        index = i

# Graphs
dashed_list = [speed_list[index] for i in range(len(peak_torque_list[index]))]
        
plt.plot(pumping_speed[index], peak_torque_list[index])
plt.plot(dashed_list, peak_torque_list[index], linestyle="-." )
plt.xlabel("Pump Speed (SPM)")
plt.ylabel("Peak Torque (in*lbs)")
plt.title("Pump Speed vs Peak Torque")
plt.show()

plt.plot(pumping_speed[index], peak_polished_rod[index])
plt.plot(dashed_list, peak_polished_rod[index], linestyle="-." )
plt.xlabel("Pump Speed (SPM)")
plt.ylabel("Peak Polished Rod (lbs)")
plt.title("Pump Speed vs Peak Polished Rod")
plt.show()

plt.plot(pumping_speed[index], stress_top_rod[index])
plt.plot(dashed_list, stress_top_rod[index], linestyle="-." )
plt.xlabel("Pump Speed (SPM)")
plt.ylabel("Stress at Rod Top (psi)")
plt.title("Pump Speed vs Stress at Rod Top")
plt.show()

plt.plot(pumping_speed[index], pump_displacement_rate[index])
plt.plot(dashed_list, pump_displacement_rate[index], linestyle="-." )
plt.xlabel("Pump Speed (SPM)")
plt.ylabel("Pump Displacement Rate (STB/day)")
plt.title("Pump Speed vs Pump Displacement Rate")
plt.show()

plt.plot(pumping_speed[index], oil_production_rate[index])
plt.plot(dashed_list, oil_production_rate[index], linestyle="-." )
plt.xlabel("Pump Speed (SPM)")
plt.ylabel("Oil Production Rate (STB/day)")
plt.title("Pump Speed vs Oil Production Rate")
plt.show()
