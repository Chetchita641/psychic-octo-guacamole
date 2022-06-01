import json

class HoustonDB:
    def __init__(self, blocks=[], interfaces=[], signals=[], rules=[]):
        self.blocks = blocks
        self.interfaces = interfaces
        self.signals = signals
        self.rules = rules

    def get_block(self, name):
        for block in self.blocks:
            if block.name.lower() == name.lower():
                return block
        return None

    def get_interface(self, name):
        for interface in self.interfaces:
            if interface.name.lower() == name.lower():
                return interface
        return None

    def get_signal(self, name):
        for signal in self.signals:
            if signal.name.lower() == name.lower():
                return signal
        return None

    def get_keywords(self, stmt):
        isCat = False
        out = []
        words = [word.lower() for word in stmt.split(' ')]
        for word in words:
            if isCat:
                if word[-1] == "'":
                    buf.append(word[:-1])
                    out.append(' '.join(buf))
                    isCat = False
                else:
                    buf.append(word)

            elif word[0] == "'" and word[-1] == "'":
                out.append(word[1:-1])
            elif word[0] == "'":
                isCat = True
                buf = []
                buf.append(word[1:])
            else:
                out.append(word)

        return out 

    def execute(self, stmt):
        isAttach = False
        isBlock = False
        isInterface = False
        isSignal = False

        words = self.get_keywords(stmt)
        for i in range(len(words)):
            if isAttach:
                if words[i] == 'input' or words[i] == 'output':
                    block_name, interface_name = words[i+1].split('.')
                    block = self.get_block(block_name)
                    interface = self.get_interface(interface_name)
                    signal = self.get_signal(words[i+2])
                    if words[i] == 'input':
                        block.add_input(interface.name, signal)
                    else:
                        block.add_output(interface.name, signal)
                else:
                    block = self.get_block(words[i])
                    interface = self.get_interface(words[i+1])
                    block.add_interface(interface)
                
                return json.dumps({})

            if isBlock:
                if words[i] == 'select':
                    if words[i+1] == '*':
                        return json.dumps([block.to_dict() for block in self.blocks])
                    block = self.get_block(words[i+1])
                    if block:
                        return block.to_json()
                    else:
                        return json.dumps({})
                
            if isInterface:
                if words[i] == 'select':
                    if words[i+1] == '*':
                        return json.dumps([interface.to_dict() for interface in self.interfaces])
                    interface = self.get_interface(words[i+1])
                    if interface:
                        return interface.to_json()
                    else:
                        return json.dumps({})

            if isSignal:
                if words[i] == 'select':
                    if words[i+1] == '*':
                        return json.dumps([signal.to_dict() for signal in self.signals])
                    signal = self.get_signal(words[i+1])
                    if signal:
                        return signal.to_json()
                    else:
                        return json.dumps({})                


            if words[i] == 'attach':
                isAttach = True
            elif words[i] == 'block':
                isBlock = True
            elif words[i] == 'interface':
                isInterface = True
            elif words[i] == 'signal':
                isSignal = True

        return json.dumps({}) 


        



        

    
