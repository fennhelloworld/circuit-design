"""LeoDrone Phoenix - ESP32-S3 Sensor Node Circuit
BME280 (I2C) + ICM-42688-P (SPI) + UART MAVLink + Power Management
Generates SPICE deck for power rail simulation
"""
import os

# ============================================================
# SPICE Simulation: Power Rails
# ============================================================
spice_deck = """* LeoDrone Phoenix - ESP32-S3 Sensor Node Power Rails
* 4S LiPo (14.8V) → 5V/3A BEC → 3.3V LDO → ESP32-S3 + Sensors

* === Power Sources ===
V_BAT  n_bat 0 DC 14.8
V_5V   n_5v  0 DC 5.0
V_3V3  n_3v3 0 DC 3.3

* === BEC: 14.8V → 5V/3A (LM2596 Buck Converter Model) ===
* Simplified as ideal + efficiency loss
X_BEC n_bat n_5v BEC_LM2596

.SUBCKT BEC_LM2596 VIN VOUT
* Simplified buck: Vout = 5V, efficiency ~90%
R_BEC_EFF VIN VOUT 0.1
V_BEC_OUT VOUT 0 DC 5
.ENDS

* === 3.3V LDO: AMS1117-3.3 (5V → 3.3V) ===
X_LDO n_5v n_3v3 LDO_AMS1117

.SUBCKT LDO_AMS1117 VIN VOUT
* Quiescent current ~5mA, dropout ~1.1V
R_LDO VIN VOUT 0.5
V_LDO_OUT VOUT 0 DC 3.3
.ENDS

* === ESP32-S3 Current Draw ===
* Active WiFi: ~240mA, Sleep: ~10uA
R_ESP32 n_3v3 0 R=13.75   ; 3.3V/240mA = 13.75 ohm

* === BME280 (I2C, 3.3V) ===
* Average: 2.7mA in normal mode
R_BME280 n_3v3 0 R=1222   ; 3.3V/2.7mA

* === ICM-42688-P (SPI, 3.3V) ===
* Active: 1.4mA (gyro+accel), Low-power: 7uA
R_ICM42688 n_3v3 0 R=2357   ; 3.3V/1.4mA

* === IMX219 Camera x4 (via RPi5, separate 5V rail) ===
* 4 cameras ~ 4 x 250mA = 1A on 5V
R_CAM n_5v 0 R=5          ; 5V/1A

* === GPS Module (3.3V) ===
* Acquisition: 25mA, Tracking: 20mA
R_GPS n_3v3 0 R=132       ; 3.3V/25mA

* === UART Level Shifter (3.3V) ===
R_UART n_3v3 0 R=10000    ; 0.33mA

* === Analysis ===
.OP
.DC V_BAT 12 16.8 0.1
.PRINT DC V(n_bat) V(n_5v) V(n_3v3) I(R_ESP32) I(R_BME280) I(R_ICM42688)

* Power budget
* 3.3V rail total: 240+2.7+1.4+25+0.33 = 269.4mA
* 5V rail total: 1000mA (cameras)
* BEC output: 269.4*3.3/0.9 + 1000*5/0.9 = 5.55W + 5.56W = 11.1W
* BEC input: 11.1W / 14.8V = 750mA from 4S

.END
"""

# ============================================================
# KiCad Netlist (S-expression format)
# ============================================================
kicad_netlist = """(export (version "E")
  (design
    (source "LeoDrone Phoenix Sensor Node")
    (date "2026-06-12")
    (tool "SKiDL + Manual"))
  (components
    (comp (ref U1)
      (value "ESP32-S3-WROOM-1-N16R8")
      (footprint "ESP32-S3:ESP32-S3-WROOM-1")
      (libsource (lib "MCU_Espressif") (part "ESP32-S3")))
    (comp (ref U2)
      (value "BME280")
      (footprint "BME280:BME280")
      (libsource (lib "Sensor") (part "BME280")))
    (comp (ref U3)
      (value "ICM-42688-P")
      (footprint "ICM42688:QFN-16")
      (libsource (lib "Sensor_Motion") (part "ICM-42688-P")))
    (comp (ref U4)
      (value "AMS1117-3.3")
      (footprint "Package_TO_SOT_SMD:SOT-223")
      (libsource (lib "Regulator_Linear") (part "AMS1117-3.3")))
    (comp (ref U5)
      (value "LM2596-5.0")
      (footprint "Package_TO_SOT_SMD:TO-263-5")
      (libsource (lib "Regulator_Switching") (part "LM2596-5.0")))
    (comp (ref J1)
      (value "GH1.25-6P")
      (footprint "Connector_JST:JST_GH_BM06B-GHS-TB_1x06")
      (libsource (lib "Connector") (part "GH1.25-6P")))
    (comp (ref C1) (value "100uF") (footprint "Capacitor_SMD:C_1206"))
    (comp (ref C2) (value "22uF") (footprint "Capacitor_SMD:C_0805"))
    (comp (ref C3) (value "100nF") (footprint "Capacitor_SMD:C_0402"))
    (comp (ref C4) (value "100nF") (footprint "Capacitor_SMD:C_0402"))
    (comp (ref R1) (value "4.7K") (footprint "Resistor_SMD:R_0402"))
    (comp (ref R2) (value "4.7K") (footprint "Resistor_SMD:R_0402"))
    (comp (ref L1) (value "33uH") (footprint "Inductor_SMD:L_12x12mm"))
  )
  (nets
    (net (code 1) (name "VBAT")
      (node (ref U5) (pin 1)) (node (ref J1) (pin 1)) (node (ref C1) (pin 1)))
    (net (code 2) (name "+5V")
      (node (ref U5) (pin 2)) (node (ref U4) (pin 3)) (node (ref C2) (pin 1)))
    (net (code 3) (name "+3V3")
      (node (ref U4) (pin 2)) (node (ref U1) (pin 2)) (node (ref U2) (pin 8))
      (node (ref U3) (pin 1)) (node (ref C3) (pin 1)) (node (ref C4) (pin 1))
      (node (ref R1) (pin 1)) (node (ref R2) (pin 1)))
    (net (code 4) (name "GND")
      (node (ref U1) (pin 1)) (node (ref U2) (pin 1)) (node (ref U3) (pin 7))
      (node (ref U4) (pin 1)) (node (ref U5) (pin 3)) (node (ref C1) (pin 2))
      (node (ref C2) (pin 2)) (node (ref C3) (pin 2)) (node (ref C4) (pin 2))
      (node (ref J1) (pin 6)))
    (net (code 5) (name "I2C_SDA")
      (node (ref U1) (pin 37)) (node (ref U2) (pin 3)) (node (ref R1) (pin 2)))
    (net (code 6) (name "I2C_SCL")
      (node (ref U1) (pin 36)) (node (ref U2) (pin 4)) (node (ref R2) (pin 2)))
    (net (code 7) (name "SPI_MOSI")
      (node (ref U1) (pin 35)) (node (ref U3) (pin 4)))
    (net (code 8) (name "SPI_MISO")
      (node (ref U1) (pin 37)) (node (ref U3) (pin 5)))
    (net (code 9) (name "SPI_CLK")
      (node (ref U1) (pin 38)) (node (ref U3) (pin 3)))
    (net (code 10) (name "SPI_CS0")
      (node (ref U1) (pin 10)) (node (ref U3) (pin 2)))
    (net (code 11) (name "UART_TX")
      (node (ref U1) (pin 43)) (node (ref J1) (pin 2)))
    (net (code 12) (name "UART_RX")
      (node (ref U1) (pin 44)) (node (ref J1) (pin 3)))
  )
)
"""

# ============================================================
# BOM (Bill of Materials)
# ============================================================
bom = """
| Ref | Value | Package | Qty | DigiKey/Mouser | Desc |
|-----|-------|---------|-----|----------------|------|
| U1 | ESP32-S3-WROOM-1-N16R8 | Module | 1 | ESP32-S3 | WiFi+BLE MCU, 16MB Flash, 8MB PSRAM |
| U2 | BME280 | LGA-8 | 1 | BME280 | Temp/Humidity/Pressure sensor |
| U3 | ICM-42688-P | QFN-16 | 1 | ICM-42688-P | 6-axis IMU (gyro+accel) |
| U4 | AMS1117-3.3 | SOT-223 | 1 | AMS1117 | 3.3V LDO, 1A |
| U5 | LM2596-5.0 | TO-263-5 | 1 | LM2596 | 5V buck, 3A |
| J1 | GH1.25-6P | SMD | 2 | JST GH | UART+Power connector |
| C1 | 100uF/25V | 1206 | 1 | MLCC | BEC input cap |
| C2 | 22uF/10V | 0805 | 1 | MLCC | BEC output cap |
| C3 | 100nF | 0402 | 2 | MLCC | Bypass caps |
| C4 | 100nF | 0402 | 2 | MLCC | Bypass caps |
| R1 | 4.7K | 0402 | 1 | Resistor | I2C pull-up SDA |
| R2 | 4.7K | 0402 | 1 | Resistor | I2C pull-up SCL |
| L1 | 33uH | 12x12mm | 1 | Inductor | Buck converter inductor |

Power Budget: 3.3V@269mA + 5V@1A = Total ~11.1W from 4S (750mA@14.8V)
"""

# Write files
base_dir = os.path.dirname(os.path.abspath(__file__))
sim_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'simulations')
net_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'layouts')

os.makedirs(sim_dir, exist_ok=True)
os.makedirs(net_dir, exist_ok=True)

with open(os.path.join(sim_dir, 'phoenix_power_rails.cir'), 'w') as f:
    f.write(spice_deck)
print(f"SPICE: {sim_dir}/phoenix_power_rails.cir")

with open(os.path.join(net_dir, 'phoenix_sensor_node.net'), 'w') as f:
    f.write(kicad_netlist)
print(f"Netlist: {net_dir}/phoenix_sensor_node.net")

with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'BOM_PHOENIX_SENSOR.md'), 'w') as f:
    f.write(bom)
print(f"BOM: BOM_PHOENIX_SENSOR.md")
print("\nS3: Circuit design files generated")
