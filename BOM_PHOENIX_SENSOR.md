
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
