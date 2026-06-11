# Circuit Design

Circuit design & simulation with KiCad/SKiDL/ngspice, AI-assisted via Claude Code & Codex.

## Overview

This repository implements a **programmatic circuit design workflow** using Python-based tools for schematic generation, SPICE simulation, and KiCad format output. The approach treats circuit design as code — enabling version control, parameterization, and AI-assisted design iteration.

## Toolchain

| Tool | Version | Purpose |
|------|---------|---------|
| [SKiDL](https://github.com/devbismuth/skidl) | 2.2.3 | Programmatic schematic generation in Python |
| [ngspice](http://ngspice.sourceforge.net/) | 41 | SPICE circuit simulation |
| [KiCad](https://www.kicad.org/) | — | Schematic/PCB format output |
| [kiutils](https://github.com/mvitous/kiutils) | — | KiCad file manipulation |
| Claude Code | 2.1.118 | AI-assisted circuit design & code generation |
| Codex CLI | 0.135.0 | AI-assisted design exploration |

## Directory Structure

```
circuit-design/
├── schematics/     # SKiDL Python scripts for circuit generation
├── simulations/    # ngspice simulation scripts and results
├── layouts/        # KiCad PCB layout files (.kicad_pcb)
├── gerbers/        # Gerber files for manufacturing
├── lib/            # Custom symbols, footprints, and SPICE models
└── docs/           # Design notes, datasheets, and references
```

## Workflow

1. **Design** — Write SKiDL Python scripts that describe circuits programmatically
2. **Simulate** — Generate ngspice decks from SKiDL and run SPICE simulations
3. **Export** — Output KiCad schematic (`.kicad_sch`) and PCB format files
4. **Manufacture** — Generate Gerber files from KiCad layouts

### Quick Start

```python
# schematics/led_blinker.py
from skidl import *

# Define circuit
vcc = Net('+5V')
gnd = Net('GND')

mcu = Part('MCU_STM32', 'STM32F103C8Tx')
led = Part('Device', 'LED')
r = Part('Device', 'R', value='330')

vcc += mcu.VDD
gnd += mcu.VSS
mcu.PA0 += r[1]
r[2] += led.A
led.K += gnd

generate_netlist()
```

## Environment

Activate the KiCad conda environment:
```bash
conda activate kicad-env
```

## Related

- Part of the [hardware-lab](https://github.com/fennhelloworld/hardware-lab) workspace
- Companion repo: [3d-design](https://github.com/fennhelloworld/3d-design) for enclosure and mechanical design
