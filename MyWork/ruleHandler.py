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
            "pressure": {"units": "pa", "max": 3*10e-15}
        }    
    )
    
    i2 = Interface(
        "IF-2",
        {
            "protocol": "MIL-STD-1553B",
            "data structure": "packet structure definition",
            "voltage": {"units": "v", "min": 0, "max": 5},
            "impedance": {"units": "ohm", "min": (78*0.98), "max": (78*1.02)},
            "conducted emissions": "plot",
            "radiated emissions": "plot",
            "thermal conductivity": {"units": "w/k", "max": 200},
            "connector type": "d9f"
        },
        ["gnd", "data+", "data-"]
    )
    
    i3 = Interface(
        "IF-3",
        {
            "voltage": {"units": "v", "min": 22, "max": 28, "normal": 24},
            "impedance": {"units": "mohm", "min": 1},
            "conducted emision": "plot",
            "conducted susceptibility": "plot",
            "thermal conductivity": {"units": "w/k", "max": 200},
            "connector Type": "d9m"
        },
        ["gnd", "gnd", "power"]
    )
    
    i4 = Interface(
        "IF-4",
        {
            "thermal conductivity": {"units": "w/k", "max": 5},
            "contact surface": {"units": "cm2", "min": 2.0, "max": 2.5},
            "footprint": "plot"
        } 
    )

    return [i1, i2, i3, i4]

def populate_signals():
    esf = Signal(
        "Earth Spectral Features",
        {
            "Spectral radiance": "plot",
            "flow type": "continuous", 
            "area": {"units": "deg", "min": 2},
            "distance": {"units": "km", "min": 600, "max": 650}
        }
    )

    command_a = Signal(
        "Command A",
        {
            "message": ["current image", "last image"],
            "flow type": "trigger"
        }
    )

    telemetry = Signal(
        "Telemetry",
        {
            "flow type": {"units": "hz", "min": 1, "max": 1}
        }
    )

    acceleration = Signal(
        "Acceleration",
        {
            "flow type": "continuous",
            "range": {"units": "m/s", "min": 0, "max": 5*9.8}
        }
    )

    image_data = Signal(
        "Image data",
        {
            "flow type": "trigger",
            "FOV": {"units": "deg", "min": 2},
            "resolution": {"units": "unit", "max": 1}
        }
    )

    heat = Signal(
        "Heat",
        {
            "flow type": "continuous",
            "temperature": {"units": "c", "min": -1, "max": 45}
        }
    )

    electrical_power = Signal(
        "Electrical Power",
        {
            "flow type": "continuous",
            "range": {"units": "w", "min": 0, "max": 600}
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
    #"SIGNAL SELECT ALL",
    #"SIGNAL SELECT WHERE name='Earth Spectral Features'",
    #"SIGNAL SELECT WHERE name='Earth Spectral Features', distance>=600",
    #"INTERFACE SELECT ALL",
    #"INTERFACE SELECT WHERE name=IF-2",
    #"INTERFACE SELECT WHERE voltage>=0, 'conducted emissions'=plot",
    #"INTERFACE SELECT WHERE 'proxy port'=gnd",
    #"BLOCK SELECT ALL",
    #"BLOCK SELECT WHERE name='Instrument'",
    #"BLOCK SELECT WHERE INTERFACE.name=IF-1",
    #"BLOCK SELECT WHERE INTERFACE.pressure=*",
    #"BLOCK SELECT WHERE Output.name=IF-1",
    #"BLOCK SELECT WHERE SIGNAL.name=heat",
    "BLOCK SELECT WHERE SIGNAL.'Flow type'=trigger"
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
            print()

if __name__ == "__main__":
    main()
    print("All done")