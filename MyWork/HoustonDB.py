import json
from myObjects import *

operators = ['=', '!=', '<', '>', '<=', '>=', '+=', '-=']

class HoustonDB:
    def __init__(self, blocks=[], interfaces=[], signals=[], rules=[]):
        self.blocks = blocks
        self.interfaces = interfaces
        self.signals = signals
        self.rules = rules

    def add_block(self, block):
        if not any(b.name == block.name for b in self.blocks):
            self.blocks.append(block)
            return True
        return False

    def get_block(self, name):
        for block in self.blocks:
            if block.name.lower() == name.lower():
                return block
        return None

    def add_interface(self, interface):
        if not any(i.name == interface.name for i in self.interfaces):
            self.interfaces.append(interface)
            return True
        return False

    def get_interface(self, name):
        for interface in self.interfaces:
            if interface.name.lower() == name.lower():
                return interface
        return None

    def add_signal(self, signal):
        if not any(s.name == signal.name for s in self.signals):
            self.signals.append(signal)
            return True
        return False

    def get_signal(self, name):
        for signal in self.signals:
            if signal.name.lower() == name.lower():
                return signal
        return None

    def execute(self, stmt):
        words = self.__get_keywords(stmt)
        if words[0] == 'attach':
            return json.dumps(self.__execute_attach(words[1:]))

        elif words[0] == 'block':
            return json.dumps(self.__execute_block(words[1:]))
        elif words[0] == 'interface':
            return json.dumps(self.__execute_interface(words[1:]))
        elif words[0] == 'signal':
            return json.dumps(self.__execute_signal(words[1:]))
        else:
            return json.dumps({})

    def __compare(self, lh, op, rh):
        try:
            lh_val = float(lh)
        except ValueError:
            lh_val = lh
        
        try:
            rh_val = float(rh)
        except ValueError:
            rh_val = rh

        if op == '=':
            return lh_val == rh_val
        elif op == '!=':
            return lh_val != rh_val
        elif op == '<':
            return lh_val < rh_val
        elif op == '>':
            return lh_val > rh_val
        elif op == '<=':
            return lh_val <= rh_val
        elif op == '>=':
            return lh_val >= rh_val
        else:
            return False 


    def __get_op(self, s):
        for i in range(len(s)-1):
            if s[i] == '!' and s[i+1] == '=':
                return '!='
            elif s[i] == '<' and s[i+1] == '=':
                return '<='
            elif s[i] == '>' and s[i+1] == '=':
                return '>='
            elif s[i] == '=':
                return '='
            elif s[i] == '<':
                return '<'
            elif s[i] == '>':
                return '>'
            elif s[i] == '+' and s[i+1] == '=':
                return '+='
            elif s[i] == '-' and s[i+1] == '=':
                return '-='
        return None

    def __is_number(self, str):
        try:
            float(str)
            return True
        except ValueError:
            return False
        

    def __get_keywords(self, stmt):
        isCat = False
        out = []
        stmt = stmt.replace(',', '')
        words = [word.lower() for word in stmt.split(' ')]

        buf = []
        for word in words:
            if any(operator in word for operator in operators):
                op = self.__get_op(word)
                lh = word[:word.index(op)]
                rh = word[word.index(op)+len(op):]
                buf.append(lh)
                buf.append(op)
                buf.append(rh)
            else:
                buf.append(word)

        words = buf
        isCat = False
        isDict = False
        isArray = False
        bufStr = ""
        dictStr = ""
        arrayStr = ""
        for word in words:
            if word[0] == "{":
                isDict = True
                word = word.replace("{", "")
                dictStr = "{"
            elif word[0] == "'" and word[-1] == "'":
                word = word.replace("'", "")
            elif word[0] == "'":
                isCat = True
                word = word.replace("'", "")
            elif word[0] == '[':
                isArray = True
                word = word.replace("[", "")
                arrayStr = "["

            if isDict:
                key, val = word.split(':')
                if '}' in val:
                    isEnd = True
                    val = val.replace('}', '')
                else:
                    isEnd = False
                if self.__is_number(val) or (val[0] == "'" and val[-1] == "'"):
                    dictStr += "'" + key + "':" + val
                else:
                    dictStr += "'" + key + "':'" + val + "'"
                if not isEnd:
                    dictStr += ", "
                else:
                    dictStr += '}'
                    out.append(dictStr)
                    dictStr = ""
                    isDict = False
                    isEnd = False
                
            elif isCat:
                if bufStr:
                    bufStr += ' '
                bufStr += word
                if "'" in bufStr:
                    bufStr = bufStr.replace("'", "")
                    out.append(bufStr)
                    bufStr = ""
                    isCat = False
            
            elif isArray:
                if ']' in word:
                    isEnd = True
                    word = word.replace("]", "")
                else:
                    isEnd = False
                if self.__is_number(word):
                    arrayStr += word
                else:
                    arrayStr += "'" + word + "'"
                if not isEnd:
                    arrayStr += ", "
                else:
                    arrayStr += ']'
                    out.append(arrayStr)
                    arrayStr = ""
                    isArray = False
                    isEnd = False
                
            else:
                out.append(word)

        if bufStr:
            out.append(bufStr) 
        return out

    def __execute_attach(self, words):
        resp = False
        if words[0] == 'input' or words[0] == 'output':
            block_name, interface_name = words[1].split('.')
            block = self.get_block(block_name)
            interface = self.get_interface(interface_name)
            signal = self.get_signal(words[2])
            if block and interface and signal:
                if words[0] == 'input':
                    resp = block.add_input(interface.name, signal)
                else:
                    resp = block.add_output(interface.name, signal)
        else:
            block = self.get_block(words[0])
            interface = self.get_interface(words[1])
            if block and interface:
                resp = block.add_interface(interface)
        
        return {'ok': resp}

    def __execute_block(self, words):
        ok = True
        out = []
        if words[0] == 'select':
            if words[1] == 'all':
                out = [block.to_dict() for block in self.blocks]
            elif words[1] == 'where' and len(words) >= 5:
                for block in self.blocks:
                    isInvalid = False
                    for i in range(2, len(words), 3):
                        lh = words[i]
                        op = words[i+1]
                        rh = words[i+2]
                        if lh == 'name' and op == '=':
                            if block.name.lower() != rh:
                                isInvalid = True
                        elif 'interface' in lh:
                            lh = lh.split('.')[1]
                            if ' ' in lh:
                                lh = "'"+lh+"'"
                            stmt = "SELECT WHERE " + lh + op + rh
                            interfaces = self.__execute_interface(self.__get_keywords(stmt))
                            for interface in interfaces:
                                if lh == 'name' and not any(i.name == interface['name'] for i in block.interfaces):
                                    isInvalid = True
                        elif 'input' in lh:
                            lh = lh.split('.')[1]
                            if lh == 'name' and not any(i_name.lower() == rh for i_name in block.inputs.keys()):
                                isInvalid = True
                        elif 'output' in lh:
                            lh = lh.split('.')[1]
                            if lh == 'name' and not any(i_name.lower() == rh for i_name in block.outputs.keys()):
                                isInvalid = True
                        elif 'signal' in lh:
                            lh = lh.split('.')[1]
                            if ' ' in lh:
                                lh = "'"+lh+"'"
                            stmt = "SELECT WHERE " + lh + op + rh
                            signals = self.__execute_signal(self.__get_keywords(stmt))
                            found = False
                            for signal in signals:
                                for i_signals in block.inputs.values():
                                    if any(i_signal.name == signal['name'] for i_signal in i_signals):
                                        found = True
                                for o_signals in block.outputs.values():
                                    if any(o_signal.name == signal['name'] for o_signal in o_signals):
                                        found = True
                            isInvalid = not found
                        
                        if isInvalid:
                            break
                    
                    if not isInvalid:
                        out.append(block.to_dict())

            elif self.get_block(words[1]):
                out.append(self.get_block(words[1]).to_dict())
            else:
                ok = False

        elif words[0] == 'update':
            updateAll = words[1] == 'all'
            if not updateAll:
                name = words[1]

            for block in self.blocks:
                for i in range(2, len(words[1:]), 3):
                    if updateAll or block.name.lower() == name:
                        lh = words[i]
                        op = words[i+1]
                        rh = words[i+2]

                        if lh == 'name':
                            block.name = rh
                        elif lh == 'interfaces':
                            if op == '+=':
                                interface = self.get_interface(rh)
                                ok = block.add_interface(interface)
                            elif op == '=':
                                rh = eval(rh)
                                block.interfaces = [self.get_interface(i_name) for i_name in rh]
                        elif 'inputs' in lh:
                            interface = self.get_interface(lh.split('.')[1])
                            signal = self.get_signal(rh)
                            if interface and signal:
                                block.add_signal('input', interface, signal)
                        

        elif words[0] == 'create':
            block = Block(words[1])
            self.add_block(block)
            for i in range(2, len(words[2:]), 3):
                lh = words[i]
                op = words[i+1]
                rh = words[i+2]

                if lh == 'interfaces':
                    if rh[0] == '[' and rh[-1] == ']':
                        rh = eval(rh)
                        [block.add_interface(self.get_interface(i)) for i in rh]

                    


        
        if ok:
            return {'ok': ok, 'resp': out}
        else:
            return {'ok': ok, 'detail': "Something went wrong"}

    
    

    def __execute_interface(self, words):
        ok = True
        out = []
        if words[0] == 'select':
            if words[1] == 'all':
                out = [interface.to_dict() for interface in self.interfaces]
            elif words[1] == 'where' and len(words) > 3:
                for interface in self.interfaces:
                    isInvalid = False
                    for i in range(2, len(words), 3):
                        lh = words[i]
                        op = words[i+1]
                        rh = words[i+2]
                        if lh == 'name' and op == '=':
                            if interface.name.lower() != rh:
                                isInvalid = True
                                break
                        elif lh == 'proxy port' and op == '=':
                            found = False
                            for port in interface.proxy_ports:
                                if port.lower() == rh:
                                    found = True
                                    break
                            isInvalid = not found
                        else:
                            if lh not in interface.values:
                                isInvalid = True
                                break
                            if op == '=' and rh == '*':
                                continue
                            elif type(interface.values[lh]) == dict:
                                if 'min' in interface.values[lh] and not self.__compare(interface.values[lh]['min'], op, rh):
                                    isInvalid = True
                                elif 'max' in interface.values[lh] and not self.__compare(interface.values[lh]['max'], op, rh):
                                    isInvalid = True
                            elif not self.__compare(interface.values[lh], op, rh):
                                isInvalid = True
                    
                        if isInvalid:
                            break
                
                    if not isInvalid:
                        out.append(interface.to_dict())
        
            elif self.get_interface(words[1]):
                out.append(self.get_interface(words[1]).to_dict())

        elif words[0] == 'update':
            updateAll = words[1] == 'all'
            if not updateAll:
                name = words[1]

            for interface in self.interfaces:
                for i in range(2, len(words[2:]), 3):
                    if updateAll or interface.name.lower() == name:
                        lh = words[i]
                        op = words[i+1]
                        rh = words[i+2]
                        if ('{' in rh and '}' in rh) or ('[' in rh and ']' in rh):
                            rh = eval(rh)
                        elif self.__is_number(rh):
                            rh = float(rh)
                        
                        if lh == 'name':
                            interface.name = rh
                        elif '.' in lh:
                            key1, key2 = lh.split('.')
                            if key1 in interface.values:
                                interface.values[key1][key2] = rh
                        elif lh == 'proxy_ports':
                            if type(rh) == list:
                                interface.proxy_ports = rh
                            else:
                                interface.proxy_ports.append(rh)
                        else:
                            interface.values[lh] = rh
        
        elif words[0] == 'create':
            interface = Interface(words[1])
            for i in range(2, len(words[2:]), 3):
                lh = words[i]
                op = words[i+1]
                rh = words[i+2]

                if rh[0] == '{' and rh[-1] == '}':
                    rh = eval(rh)
                interface.add_value(lh, rh)
                self.add_interface(interface)

        if ok:
            return {'ok': ok, 'resp': out}
        else:
            return {'ok': ok, 'detail': "Unknown command"}
        

    def __execute_signal(self, words):
        if words[0] == 'select':
            out = []
            if words[1] == 'all':
                out = [signal.to_dict() for signal in self.signals]
            elif words[1] == 'where' and len(words) >= 5:
                for signal in self.signals:
                    isInvalid = False
                    for i in range(2, len(words), 3):
                        lh = words[i]
                        op = words[i+1]
                        rh = words[i+2]
                        if lh == 'name' and op == '=':
                            if signal.name.lower() != rh:
                                isInvalid = True
                        else:
                            if lh not in signal.attributes:
                                isInvalid = True
                            if op == '=' and rh == '*':
                                continue
                            elif type(signal.attributes[lh]) == dict:
                                if 'min' in signal.attributes[lh] and not self.__compare(signal.attributes[lh]['min'], op, rh):
                                    isInvalid = True
                                elif 'max' in signal.attributes[lh] and not self.__compare(signal.attributes[lh]['max'], op, rh):
                                    isInvalid = True
                            elif not self.__compare(signal.attributes[lh], op, rh):
                                isInvalid = True
                        
                        if isInvalid:
                            break
                    
                    if not isInvalid:
                        out.append(signal.to_dict())
            return {'ok': True, 'resp':out}

        elif words[0] == 'update':
            updateAll = words[1] == 'all'
            if not updateAll:
                name = words[1]

            for signal in self.signals:
                for i in range(2, len(words[2:]), 3):
                    if updateAll or signal.name.lower() == name:
                        lh = words[i]
                        op = words[i+1]
                        rh = words[i+2]
                        if '{' in rh and '}' in rh:
                            rh = eval(rh)
                        elif self.__is_number(rh):
                            rh = float(rh)
                        
                        if lh == 'name':
                            signal.name = rh
                        elif '.' in lh:
                            key1, key2 = lh.split('.')
                            if key1 in signal.attributes:
                                signal.attributes[key1][key2] = rh
                        else:
                            signal.attributes[lh] = rh 

            return {'ok': True}

        elif self.get_signal(words[1]):
            out.append(self.get_signal(words[1]).to_dict())
            return {'ok': True, 'resp': out}

        return {'ok': False, 'detail': "Unknown command"}



                            

                            


                




        



        

    
