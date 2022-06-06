import json

class Rule:
    def __init__(self, name, text):
        self.name = name
        self.text = text


class Block:
    def __init__(self, name=""):
        self.name = name
        self.interfaces = [] 
        self.inputs = {}
        self.outputs = {}

    def add_interface(self, interface):
        self.interfaces.append(interface)
        return True

    def add_input(self, name, signal):
        if name not in self.inputs:
            self.inputs[name] = []
        self.inputs[name].append(signal)
        return True
        

    def add_output(self, name, signal):
        if name not in self.outputs:
            self.outputs[name] = []
        self.outputs[name].append(signal)
        return True

    def to_dict(self):
        mod_inputs = {}
        for name, signals in self.inputs.items():
            mod_inputs[name] = [signal.to_dict() for signal in signals]
        mod_outputs = {}
        for name, signals in self.outputs.items():
            mod_outputs[name] = [signal.to_dict() for signal in signals]

        return {
            'name': self.name,
            'interfaces': [interface.to_dict() for interface in self.interfaces],
            'inputs': mod_inputs,
            'outputs': mod_outputs
        }

    def to_json(self):
        return json.dumps(self.to_dict())
        

    def print(self):
        print(self.name)
        print("=============")
        print("Interfaces:")
        for i, interface in enumerate(self.interfaces):
            if interface.name in self.inputs:
                print(interface.name + ": ", end=" ")
                print("In:", end=" ")
                for i, signal in enumerate(self.inputs[interface.name]):
                    if i < len(self.inputs[interface.name]) - 1:
                        print(signal.name + ",", end=" ")
                    else:
                        print(signal.name)
            if interface.name in self.outputs:
                print(interface.name + ": ", end=" ")
                print("Out:", end=" ")
                for i, signal in enumerate(self.outputs[interface.name]):
                    if i < len(self.outputs[interface.name]) - 1:
                        print(signal.name + ",", end=" ")
                    else:
                        print(signal.name)
        print()
                

class Interface:
    def __init__(self, name="", values={}, proxy_ports=[]):
        self.name = name
        self.values = values
        self.proxy_ports = proxy_ports

    def to_json(self):
        return json.dumps({
            'name': self.name,
            'values': self.values,
            'proxy_ports': self.proxy_ports
        })

    def to_dict(self):
        return {
            'name': self.name,
            'values': self.values,
            'proxy_ports': self.proxy_ports
        }
        

class Signal:
    def __init__(self, name="", attributes={}):
        self.name = name
        self.attributes = attributes

    def to_json(self):
        return json.dumps({
            'name': self.name,
            'attributes': self.attributes
        })

    def to_dict(self):
        return {
            'name': self.name,
            'attributes': self.attributes
        }
