import math
import random

# V_oc = voltage at OC, v_oc = adjusted V_oc (for calculation of ff)
# I -> intensity, i -> current
# stc -> standard testing conditions, sc -> short circuit, oc -> open circuit
num = int(input("How many materials would you like to compare?"))
materialeff = []
timetorecovercost = []

if num > 0:
    for x in range (0, num):
        T_amb = float(input("What is the ambient temp. of operation of PV cell? (in Celcius) "))
        NOCT  = float(input("What is the NOCT of the given cell? (in Celcius) "))
        nu = float(input("What is the short-circuit temperature coefficient of the PV cell material? "))
        i_stc = float(input("What is the PV cell's short-circuit current under STC? "))
        V_stc = float(input("What is the PV cell's open-circuit volatage, under STC? "))
        latitude_deg = float(input("What is your location's latitude? "))

        I_0 = 1360.00
        k = 0.768
        AM = 1.5
        latitude_rad = latitude_deg * (math.pi / 180)

        I_1 = (k ** (1/math.cos(latitude_rad))) * (math.cos(latitude_rad)/k) * I_0

        I_final = 1.1 * I_1 * (0.7 ** (AM ** 0.678))
 
        T_m = T_amb + ((NOCT - 20)*(I_final / 800))
        i_sc = (I_final / 1000) * (i_stc + (nu * (T_m - 25))) #found this one on the net - https://ac.els-cdn.com/S1876610217347628/1-s2.0-S1876610217347628-main.pdf?_tid=6defd94c-4f6e-437a-aad8-a683dae33239&acdnat=1541625522_124dfad1c893e5c6f62aeff0ed916469
        V_oc = (V_stc / 298.15) * (T_m + 273.15)
        x = ((25.7 * 10 ** -3) / 298.15) * (T_m + 273.15) # just the conversion factor, easier than writing it in one go
        v_oc = V_oc / x
        ff = (v_oc - math.log(v_oc + 0.72)) / (v_oc + 1)

        eff_init = (V_oc * i_sc * ff) / I_final
        eff_dust = 0.93 * eff_init
        print ("Efficiency accounting for avg. effect of dust is: ")
        print (eff_dust)

        costPerPanel = float(input("What is the cost per panel for this system?($) "))
        panelArea= float(input("What is the area of each panel?(m^2) "))
        wattProduced = panelArea*I_final*eff_dust
        perWattElectricityCost = 0.1908/wattProduced
        print (f"The cost of Electricity per Watt is {perWattElectricityCost}.")
        hoursToRecover = costPerPanel/perWattElectricityCost/3600
        print (f"Solar panel will be recover its cost in {hoursToRecover} hours.")

        materialeff.append(eff_dust)
        timetorecovercost.append(hoursToRecover)
        print("\n\n")
        
    maxeff = max(materialeff)
    mintime = min(timetorecovercost)
    bestmaterial = materialeff.index(maxeff)
    besttime = timetorecovercost.index(mintime)

    print (f"The most efficient material has efficiency {maxeff}. This is material {bestmaterial + 1}.")
    print (f"The most cost effective material will recover cost in {mintime} hours. This is material {besttime + 1})
           
else:
    print("Alright. See you later!")

