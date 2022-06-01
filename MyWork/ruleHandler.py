from myObjects import *
from HoustonDB import HoustonDB

import json

# ------------------------------------------------------------

def populate_blocks():
    # pg 17 of paper
    earth = Block("Earth")
    platform = Block("Platform")
    instrument = Block("Instrument")

    return [earth, instrument, platform]

def populate_interfaces():
    i1 = Interface(
        "IF-1",
        {
            "Pressure": {"Units": "Pa", "Max": 3*10e-15}
        }    
    )
    
    i2 = Interface(
        "IF-2",
        {
            "Protocol": "MIL-STD-1553B",
            "Data structure": "Packet structure definition",
            "Voltage": {"Units": "V", "Min": 0, "Max": 5},
            "Impedance": {"Units": "Ohm", "Min": (78*0.98), "Max": (78*1.02)},
            "Conducted emissions": "Plot",
            "Radiated emissions": "Plot",
            "Thermal conductivity": {"Units": "W/K", "Max": 200},
            "Connector type": "D9F"
        },
        ["GND", "Data+", "Data-"]
    )
    
    i3 = Interface(
        "IF-3",
        {
            "Voltage": {"Units": "V", "Min": 22, "Max": 28, "Normal": 24},
            "Impedance": {"Units": "Mohm", "Min": 1},
            "Conducted emision": "Plot",
            "Conducted susceptibility": "Plot",
            "Thermal conductivity": {"Units": "W/K", "Max": 200},
            "Connector Type": "D9M"
        },
        ["GND", "GND", "Power"]
    )
    
    i4 = Interface(
        "IF-4",
        {
            "Thermal conductivity": {"Units": "W/K", "Max": 5},
            "Contact surface": {"Units": "Cm2", "Min": 2.0, "Max": 2.5},
            "Footprint": "Plot"
        } 
    )

    return [i1, i2, i3, i4]

def populate_signals():
    esf = Signal(
        "Earth Spectral Features",
        {
            "Spectral radiance": "Plot",
            "Flow type": "Continuous", 
            "Area": {"Units": "Deg", "Min": 2},
            "Distance": {"Units": "Km", "Min": 600, "Max": 650}
        }
    )

    command_a = Signal(
        "Command A",
        {
            "Message": ["current image", "last image"],
            "Flow type": "Trigger"
        }
    )

    telemetry = Signal(
        "Telemetry",
        {
            "Flow type": {"Units": "Hz", "Min": 1, "Max": 1}
        }
    )

    acceleration = Signal(
        "Acceleration",
        {
            "Flow type": "Continuous",
            "Range": {"Units": "M/S", "Min": 0, "Max": 5*9.8}
        }
    )

    image_data = Signal(
        "Image Data",
        {
            "Flow type": "Trigger",
            "FOV": {"Units": "Deg", "Min": 2},
            "Resolution": {"Units": "Unit", "Max": 1}
        }
    )

    heat = Signal(
        "Heat",
        {
            "Flow type": "Continuous",
            "Temperature": {"Units": "C", "Min": -1, "Max": 45}
        }
    )

    electrical_power = Signal(
        "Electrical Power",
        {
            "Flow type": "Continuous",
            "Range": {"Units": "W", "Min": 0, "Max": 600}
        }
    )

    return [esf, command_a, telemetry, acceleration, image_data, heat, electrical_power]

def populate_rules():
    # TODO
    return []

# -----------------------------------------------------------------------------------------------------------

setup_stmts = [
    "ATTACH Earth IF-1",
    "ATTACH Instrument IF-1",
    "ATTACH Instrument IF-2",
    "ATTACH Instrument IF-3",
    "ATTACH Instrument IF-4",
    "ATTACH Platform IF-2",
    "ATTACH Platform IF-3",
    "ATTACH Platform IF-4",

    "ATTACH INPUT Instrument.IF-1 'Earth Spectral Features'",
    "ATTACH OUTPUT Earth.IF-1 'Earth Spectral Features'",

    "ATTACH INPUT Instrument.IF-2 'Command A'",
    "ATTACH OUTPUT Platform.IF-2 'Command A'",

    "ATTACH INPUT Platform.IF-2 'Image data'",
    "ATTACH OUTPUT Instrument.IF-2 'Image data'",

    "ATTACH INPUT Platform.IF-2 'Telemetry'",
    "ATTACH OUTPUT Instrument.IF-2 Telemetry",

    "ATTACH INPUT Instrument.IF-3 'Electrical power'",
    "ATTACH OUTPUT Platform.IF-3 'Electrical power'",

    "ATTACH INPUT Instrument.IF-4 Heat",
    "ATTACH OUTPUT Platform.IF-4 Heat",

    "ATTACH INPUT Instrument.IF-4 Acceleration",
    "ATTACH OUTPUT Platform.IF-4 Acceleration",
]

query_statements = [
    "BLOCK SELECT *"
]

def main():
    blocks = populate_blocks()
    interfaces = populate_interfaces()
    signals = populate_signals()
    rules = populate_rules()

    db = HoustonDB(blocks, interfaces, signals, rules)    
    for stmt in setup_stmts:
        db.execute(stmt)

    for stmt in query_statements:
        resp = db.execute(stmt)
        if resp:
            print(resp)

if __name__ == "__main__":
    main()
    print("All done")