# Compiladores 2020-2


class Gramatic:
    struct = dict()
    no_terminals = []
    dollar = '$'
    
    def get_right(self, line):
        begin = 0
        list_product = []
        while begin < len(line):
            end = line.find("|", begin)
            if end != -1:
                list_product.append(line[begin:end - 1].strip())
                begin = end + 1
            else:
                list_product.append(line[begin:].strip())
                begin = len(line)
        return list_product

    def __init__(self, path_text):
        file = open(path_text + ".txt", 'r')
        for line in file:
            half = line.find('::=')
            if line[:half].strip() in self.struct:
                self.struct[line[:half].strip()].extend(self.get_right(line[half + 3:].strip()))
            else:
                self.struct[line[:half].strip()] = self.get_right(line[half + 3:].strip())
        
        for k, _ in self.struct.items():
            self.no_terminals.append(k)

    def get_production(self, left):
        return self.struct[left]

    def get_first(self, product):
        element = None
        firsts =[]
        for prod in self.struct[product]:
            element = (prod[:prod.find(" ")] if prod.find(" ") != -1 else prod)
            firsts.extend(self.get_first(element)) if element in self.no_terminals else firsts.append(element)
        return firsts

    def get_next(self, node):
        nexts = [self.dollar]
        for k, v in self.struct.items():
            for item in v:
                index  = item.find(node)
                if index != -1:
                    if index + len(node) == len(item):
                        if k != node:
                            for j in self.get_next(k):
                                if j not in nexts:
                                    nexts.append(j)
                    elif index + len(node) < len(item) and not item[index + len(node)].isalpha():
                        i = item.find(" ", index + len(node) + 1)
                        temp = (item[index + len(node) + 1:i] if i != -1 else item[index + len(node) + 1:])
                        if temp in self.no_terminals:
                            for item_gotten in self.get_first(temp):
                                if 'lambda' == item_gotten:
                                    for j in self.get_next(temp):
                                        if j not in nexts:
                                            nexts.append(j)
                                elif item_gotten not in nexts:
                                    nexts.append(item_gotten)
                        else:
                            nexts.append(temp)
        return nexts

    def __str__(self):
        return "%s" % self.struct


grammar = Gramatic('sos')
# print(grammar.get_first("F"))
# print(grammar.get_next("F"))
print(grammar.struct)
# print(grammar.no_terminals)
