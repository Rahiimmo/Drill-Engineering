import math
import matplotlib.pyplot as plt
import numpy as nmpy

#input
Well_depth = 10000                                              #Well depth                                #unit: ft
Dp_OD = 5                                                       #Drill pipe OD                             #unit: in
Dp_ID = 4.276                                                   #Drill pipe ID                             #unit: in
Dp_weight = 19.5                                                #Drill pipe weight                         #unit: lbm/ft
Dc_OD = 5                                                       #Drill collar OD                           #unit: in
Dc_ID = 2.5                                                     #Drill collar ID                           #unit: in
Dc_weight = 147                                                 #Drill collar weight                       #unit: lbm/ft
Casing_shoe = 7000                                              #Casing shoe                               #unit: ft
Casing_OD = 9.75                                                #Casing OD                                 #unit: in
Casing_ID = 8.625                                               #Casing ID                                 #unit: in
Casing_weight = 59.2                                            #Casing weight                             #unit: lbm/ft
WOB = 59000                                                     #Required WOB                              #unit: lbf
Pore_pressure = 6000                                            #Pore pressure                             #unit: psi
Mud_volume = 100                                                #Mud pit and surface facility volume       #unit: bbl
d = 6.5                                                         #Liner ID                                  #unit: in
L = 18                                                          #Stroke length                             #unit: in
P = 3000                                                        #Pump pressure                             #unit: psi
R = 20                                                          #Pump speed                                #unit: SPM
E = 0.8                                                         #Efficiency


#calculation
#assumption:  SF = 1.15   and      rho_s = 65.5 ppg
# P = .52 * MW * TVD            , MW = rho
rho = ( Pore_pressure + 100) / ( Well_depth * .052 )                                                        #unit: ppg
BF = 1 - rho / 65.5
L_dc = ( WOB * 1.15 ) / ( BF * Dc_weight )                                     #Drill collar length         #unit: ft
print('Length of drill collar: ',L_dc, 'ft')

L_dp = Well_depth - L_dc                                                       #Drill pipe length           #unit: ft
Ds_weight = ( L_dp * Dp_weight ) + ( L_dc * Dc_weight )                        #Drill string weight         #unit: lbm
print('Weight of drill string at air: ',Ds_weight, 'lbm')

Well_volume = math.pi * ( Casing_ID ** 2 ) * Well_depth / ( 4 * 5.615 * 144 )                               #unit: bbl
Dp_volume = math.pi * ( Dp_OD ** 2 - Dp_ID ** 2 ) * L_dp / ( 4 * 5.615 * 144 )                              #unit: bbl
Dc_volume = math.pi * ( Dc_OD **2 - Dc_ID ** 2 ) * L_dc / ( 4 * 5.615 * 144 )                               #unit: bbl
Volume_of_required_mud = Well_volume - Dp_volume - Dc_volume + 100                                          #unit: bbl
print('Volume of required mud: ', Volume_of_required_mud , 'bbl')

Weight_of_mud = rho * Volume_of_required_mud * 42                                                           #unit:lbm
print('Weight of desired mud: ', Weight_of_mud,'lbm')
print('Density of desired mud: ',rho,'ppg')

# rho * V = rho_w * V_w + rho_b * V_b    , V_b = V - V_w   , b = barite    w = water
# V * ( rho_b - rho ) = V_w * ( rho_b - rho_w )    rho_b = 35 ppg      rho_w = 8.33
Water_volume = ( 35 - rho ) * Volume_of_required_mud / ( 35 - 8.33 )                                        #unit: bbl
Barite_volume = Volume_of_required_mud - Water_volume                                                       #unit: bbl
Barite_mass = Barite_volume * 1470 / 100                                                                    #unit: sack
print('Volume of fresh water: ', Water_volume, 'bbl')
print('Mass of Brite: ',Barite_mass,'Sack')

P1 = .052 * rho * L_dp                                                                                      #unit: psi
P2 = .052 * rho * Well_depth                                                                                #unit: psi
A1 = math.pi * ( Dp_OD ** 2 - Dp_ID ** 2 ) / 4                                                              #unit: in^2
A2 = math.pi * ( Dc_OD ** 2 - Dc_ID ** 2 ) / 4                                                              #unit: in^2

plt.figure('Mud pressure profile')
TVD = nmpy.arange(0,Well_depth)
pressure = .052 * rho * TVD
plt.plot(TVD,pressure)
plt.xlabel('Depth(ft)')
plt.ylabel('Pressure(psi)')

plt.figure('axial tension')
Dp = nmpy.arange(0,L_dp)
Dc = nmpy.arange(L_dp,Well_depth)
F_dp = Dp_weight * ( L_dp - Dp ) + Dc_weight * L_dc + P1 * ( A2 - A1 ) - P2 * A2
F_dc = Dc_weight * ( Well_depth - Dc ) - P2 * A2
F_neutral_dp = Dp_weight * ( L_dp - L_dp ) + Dc_weight * L_dc + P1 * ( A2 - A1 ) - P2 * A2
F_neutral_dc = Dc_weight * ( Well_depth - L_dp ) - P2 * A2
plt.plot(F_dp,Dp)
plt.plot([ F_neutral_dp , F_neutral_dc ] , [L_dp , L_dp])
plt.plot(F_dc,Dc)
plt.xlabel(' Axial tension (lbf)')
plt.ylabel('Depth (ft) ')

Q = ( d ** 2 ) * L * E * R / 98.03
plt.figure('Volume of pumped mud')
t = nmpy.arange(0,1000)
V = Q * t
plt.plot(t,V,label='f')
plt.xlabel('time (min)')
plt.ylabel('Volume of pumped mud (gal)')
plt.show()







