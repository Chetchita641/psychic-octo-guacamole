class Table:
    def __init__(self):
        pass
        
class Block:
    def __init__(self, name=""):
        self.name = name
        self.interfaces = []
        self.inputs = {}
        self.outputs = {}

    def add_interface(self, interface):
        self.interfaces.append(interface)
                

class Interface:
    def __init__(self, name="", values={}, proxy_ports={}):
        self.name = name
        self.values = values
        self.proxy_ports = proxy_ports

class Signal:
    def __init__(self, name="", attributes={}):
        self.name = name
        self.attributes = attributes


def populate_blocks():
    # pg 17 of paper
    earth = Block("Earth")
    platform = Block("Platform")
    instrument = Block("Instrument")

    i1 = Interface(
        "IF-1",
        {
            "Pressure": {"Units": "Pa", "Min": float('-inf'), "Max": 3*10e-15}
        }    
    )
    earth.add_interface(i1)

    i2 = Interface(
        "IF-2",
        {
            "Protocol": "MIL-STD-1553B",
            "Data structure": "Packet structure definition",
            "Voltage": {"Units": "V", "Min": 0, "Max": 5},
            "Impedance": {"Units": "Ohm", "Min": (78*0.98), "Max": (78*1.02)},
            "Conducted emissions": "Plot",
            "Radiated emissions": "Plot",
            "Thermal conductivity": {"Units": "W/K", "Min": float('-inf'), "Max": 200},
            "Connector type": "D9F"
        },
        {
            "Ports": ["GND", "Data+", "Data-"]
        }
    )
    instrument.add_interface(i2)
    platform.add_interface(i2)

    i3 = Interface(
        "IF-3",
        {
            "Voltage": {"Units": "V", "Min": 22, "Max": 28, "Normal": 24},
            "Impedance": {"Units": "Mohm", "Min": 1, "Max": float('inf')},
            "Conducted emision": "Plot",
            "Conducted susceptibility": "Plot",
            "Thermal conductivity": {"Units": "W/K", "Min": float('-inf'), "Max": 200},
            "Connector Type": "D9M"
        },
        {
            "Ports": ["GND", "GND", "Power"]
        }
    )
    instrument.add_interface(i3)
    platform.add_interface(i3)

    i4 = Interface(
        "IF-4",
        {
            "Thermal conductivity": {"Units": "W/K", "Min": float('-inf'), "Max": 5},
            "Contact surface": {"Units": "Cm2", "Min": 2.0, "Max": 2.5},
            "Footprint": "Plot"
        }, 
        {}
    )
    instrument.add_interface(i4)
    platform.add_interface(i4)

    return [earth, instrument, platform]
blocks = populate_blocks()


def attach_signal(interface_name, signal, from_block, to_block):
    for block in blocks:
        if block.name == to_block:
            for interface in block.interfaces:
                if interface.name == interface_name:
                    if interface_name not in block.inputs:
                        block.inputs[interface_name] = []
                    block.inputs[interface_name].append(signal)
        elif block.name == from_block:
            for interface in block.interfaces:
                if interface.name == interface_name:
                    if interface_name not in block.outputs:
                        block.outputs[interface_name] = []
                    block.outputs[interface_name].append(signal)


def populate_signals():
    esf = Signal(
        "Earth Spectral Features",
        {
            "Spectral radiance": "Plot",
            "Flow type": "Continuous", 
            "Area": {"Units": "Deg", "Min": 2, "Max": float('inf')},
            "Distance": {"Units": "Km", "Min": 600, "Max": 650}
        }
    )
    attach_signal("IF-1", esf, "Earth", "Instrument")

    command_a = Signal(
        "Command A",
        {
            "Message": ["current image", "last image"],
            "Flow type": "Trigger"
        }
    )
    attach_signal("IF-2", command_a, "Platform", "Instrument")

    telemetry = Signal(
        "Telemetry",
        {
            "Flow type": {"Units": "Hz", "Min": 1, "Max": 1}
        }
    )
    attach_signal("IF-2", telemetry, "Instrument", "Platform")

    acceleration = Signal(
        "Acceleration",
        {
            "Flow type": "Continuous",
            "Range": {"Units": "M/S", "Min": 0, "Max": 5*9.8}
        }
    )
    attach_signal("IF-4", acceleration, "Platform", "Instrument")

    image_data = Signal(
        "Image Data",
        {
            "Flow type": "Trigger",
            "FOV": {"Units": "Deg", "Min": 2, "Max": float('inf')},
            "Resolution": {"Units": "Unit", "Min": float('-inf'), "Max": 1}
        }
    )
    attach_signal("IF-2", image_data, "Instrument", "Platform")

    heat = Signal(
        "Heat",
        {
            "Flow type": "Continuous",
            "Temperature": {"Units": "C", "Min": -1, "Max": 45}
        }
    )
    attach_signal("IF-4", heat, "Platform", "Instrument")

    electrical_power = Signal(
        "Electrical Power",
        {
            "Flow type": "Continuous",
            "Range": {"Units": "W", "Min": 0, "Max": 600}
        }
    )
    attach_signal("IF-3", electrical_power, "Platform", "Instrument")
populate_signals()
    
# -----------------------------------------------------------------------------------------------------------

def print_block(block):
    print(block.name)
    print("=============")
    print("Interfaces:")
    for i, interface in enumerate(block.interfaces):
        if interface.name in block.inputs:
            print(interface.name + ": ", end=" ")
            print("In:", end=" ")
            for i, signal in enumerate(block.inputs[interface.name]):
                if i < len(block.inputs[interface.name]) - 1:
                    print(signal.name + ",", end=" ")
                else:
                    print(signal.name)
        if interface.name in block.outputs:
            print(interface.name + ": ", end=" ")
            print("Out:", end=" ")
            for i, signal in enumerate(block.outputs[interface.name]):
                if i < len(block.outputs[interface.name]) - 1:
                    print(signal.name + ",", end=" ")
                else:
                    print(signal.name)
    print()
        


def find_blocks_with_interface(interface_name):
    for block in blocks:
        for interface in block.interfaces:
            if interface.name == interface_name:
                print_block(block)

def main():
    find_blocks_with_interface("IF-2")

    


if __name__ == "__main__":
    main()
    print("All done")