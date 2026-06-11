"""LED Driver Circuit - Generates SPICE deck for ngspice simulation"""
import os

spice_deck = """* LED Driver Circuit - ngspice simulation
* MOSFET + LED driver with PWM control

V1 n1 0 DC 5
V2 ctrl 0 PULSE(0 5 0 1n 1n 10m 20m)

R1 n1 ctrl 10k
R2 n1 n2 220
D1 n2 n3 LED1
M1 n3 ctrl 0 0 NMOS1

* Models
.MODEL NMOS1 NMOS(VTO=2 KP=2)
.MODEL LED1 D(IS=1E-14 N=2 BV=5 CJO=50PF)

* Analysis
.TRAN 0.1m 40m
.PRINT TRAN V(ctrl) V(n3) I(R2)

.END
"""

sim_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'simulations')
os.makedirs(sim_dir, exist_ok=True)
out_path = os.path.join(sim_dir, 'led_driver.cir')

with open(out_path, 'w') as f:
    f.write(spice_deck)

print(f"SPICE deck generated: {out_path}")
