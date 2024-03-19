import numpy as np
import matplotlib.pyplot as plt
import math

# Constants and input parameters, should be cahnged acccording to the requirements
tubing_head = 100  # ft
bubble_point = 100  # psi
plunger_diameter = 1.25  # inches
tubing_OD = 2.375  # inches
tubing_ID = 2  # inches
bo = 1.1
bw = 1.03
sg_water = 1.05
fs = 1.35
steel_density = 490  # lbs/ft^3
em = 3 * 10 ** 7  # psi
gl = 0.5
volumetric_efficiency = 0.75
perforation_depth = 3600  # ft
reservoir_pressure = perforation_depth * 0.38  # psi
productivity_index = 1.45
API = 25
water_cut = 40  # %
X = 440
L = perforation_depth - X

# Rod parameters
rod_number = 76
first_rod_diameter = 7 / 8  # inches
second_rod_diameter = 6 / 8  # inches
area_first_rod = math.pi * (first_rod_diameter / 2) ** 2
area_second_rod = math.pi * (second_rod_diameter / 2) ** 2
rod_fraction = 0.5
length_first_rod = L * rod_fraction
length_second_rod = L * (1 - rod_fraction)

# Pumping unit size C-114D-133-54
peak_torque = 114000  # in-lbs
peak_polished = 13300  # lbs
max_stroke_length = 54  # inches
c_list = [24, 20, 16]
D1 = 64  # inches
D2 = 72  # inches
Cs = 330
h = 74.5  # ft

# Fluid properties
sg_oil = 141.5 / (131.5 + API)
sg_fluid = sg_oil * (1 - water_cut / 100) + sg_water * water_cut / 100
tubing_area = math.pi * (tubing_OD ** 2 - tubing_ID ** 2) / 4
plunger_area = math.pi * plunger_diameter ** 2 * 0.25
Wr = (steel_density / 144) * (length_first_rod * area_first_rod + length_second_rod * area_second_rod)
Wf = (62.4 * sg_fluid) * (L * plunger_area / 144)
B = (62.4 * sg_fluid) * (Wr / steel_density)

# Calculation and data storage arrays
peak_polished_rod = [[] for i in range(3)]
peak_torque_list = [[] for i in range(3)]
stress_top_rod = [[] for i in range(3)]
pump_displacement_rate = [[] for i in range(3)]
oil_production_rate = [[] for i in range(3)]
pumping_speed = [[] for i in range(3)]
optimum_spm = [[] for i in range(3)]
speed_list = []
optimum_production_rate = [[] for i in range(3)]

# Loop over different C values
for i in range(len(c_list)):
    c = c_list[i]
    S = 2 * c * D2 / D1
    N_limit = (70471 * gl / (S * (1 - c / h))) ** 0.5
    speed_list.append(N_limit)
    counter = 1
    j = 1

    # Iterate over pump speeds
    for N in np.arange(3, N_limit + 6, 0.01):
        diff = 1
        D_guess = 200

        # Iteratively solve for parameters
        while diff > 0.1:
            max_acc = (S * N ** 2 / 70471) * (1 + c / h)
            Wmax = Wf + Wr + Wr * max_acc - B
            min_acc = (S * N ** 2 / 70471) * (1 - c / h)
            Wmin = Wr - Wr * min_acc - B
            counter_balance = (Wmax + Wmin) * 0.5
            Tp = 0.5 * S * (Wmax - counter_balance + Cs)
            max_stress = Wmax / area_first_rod
            M = 1 + c / h
            ep = 40.8 * L ** 2 * max_acc / em
            et = 5.2 * sg_fluid * D_guess * plunger_area * L / em / tubing_area
            er = (5.2 * sg_fluid * D_guess * plunger_area / em) * (
                        length_first_rod / area_first_rod + length_second_rod / area_second_rod)
            Sp = S + ep - (et + er)
            Qpd = 0.1484 * plunger_area * Sp * N * volumetric_efficiency
            qo = Qpd / (bo + bw * (water_cut * 0.01 / (1 - water_cut * 0.01)))
            bottom_hole = reservoir_pressure - (Qpd / productivity_index)
            H = bottom_hole / (0.433 * sg_fluid)
            D_new = perforation_depth - H
            diff = abs(D_new - D_guess)
            D_guess = D_new

        # Store results
        pumping_speed[i].append(N)
        peak_polished_rod[i].append(Wmax)
        peak_torque_list[i].append(Tp)
        stress_top_rod[i].append(max_stress)
        pump_displacement_rate[i].append(Qpd)
        oil_production_rate[i].append(qo)

        # Determine optimum speed and production rate
        if Tp > peak_torque or Wmax > peak_polished:
            if counter == 1:
                optimum_spm[i] = pumping_speed[i][j - 1]
                counter = 0
        elif N == N_limit or counter:
            optimum_spm[i] = N_limit

        optimum_production_rate[i] = oil_production_rate[i][j - 1]
        j = j + 1

# Find the index of the array with maximum production rate
for i in range(len(optimum_production_rate)):
    if max(optimum_production_rate) == optimum_production_rate[i]:
        index = i

# Generate dashed list for dashed line plotting
dashed_list = [speed_list[index] for i in range(len(peak_torque_list[index]))]

# Plotting
plt.plot(pumping_speed[index], peak_torque_list[index])
plt.plot(dashed_list, peak_torque_list[index], linestyle="-.")
plt.xlabel("Pump Speed (SPM)")
plt.ylabel("Peak Torque (in*lbs)")
plt.title("Pump Speed vs Peak Torque")
plt.show()

plt.plot(pumping_speed[index], peak_polished_rod[index])
plt.plot(dashed_list, peak_polished_rod[index], linestyle="-.")
plt.xlabel("Pump Speed (SPM)")
plt.ylabel("Peak Polished Rod (lbs)")
plt.title("Pump Speed vs Peak Polished Rod")
plt.show()

plt.plot(pumping_speed[index], stress_top_rod[index])
plt.plot(dashed_list, stress_top_rod[index], linestyle="-.")
plt.xlabel("Pump Speed (SPM)")
plt.ylabel("Stress at Rod Top (psi)")
plt.title("Pump Speed vs Stress at Rod Top")
plt.show()

plt.plot(pumping_speed[index], pump_displacement_rate[index])
plt.plot(dashed_list, pump_displacement_rate[index], linestyle="-.")
plt.xlabel("Pump Speed (SPM)")
plt.ylabel("Pump Displacement Rate (STB/day)")
plt.title("Pump Speed vs Pump Displacement Rate")
plt.show()

plt.plot(pumping_speed[index], oil_production_rate[index])
plt.plot(dashed_list, oil_production_rate[index], linestyle="-.")
plt.xlabel("Pump Speed (SPM)")
plt.ylabel("Oil Production Rate (STB/day)")
plt.title("Pump Speed vs Oil Production Rate")
plt.show()
