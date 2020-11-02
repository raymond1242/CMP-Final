# Compiladores 2020-2

operation_assign = ['=', '+', '-', '*', '/']

parenthesis = ['(', ')', '[', ']', '{', '}']

comparison_op = ['!=', '==', '<', '>', '<=', '>=']

reserved_word = ['Frame', 'Video', 'Audio', 'int']

conditional_statement = ['for', 'while', 'if']

function_statement = ['cargar', 'append', 'front', 'getNumberFrames', 'printf', 'setNumberFrames', 'join']


class Token:
    item = None
    type = None
    line = None
    column = None

    def __init__(self, it, ty, ln, col): 
        self.item = it.strip()
        self.line = ln
        self.column = col
        if ty == 'OTHER':
            if self.item in operation_assign:
                self.type = 'OP_ASSIGN'
            elif self.item in parenthesis:
                self.type = 'AGRUP'
            elif self.item in comparison_op:
                self.type = 'OP_COMPARE'

        elif ty == 'STREAM':
            if self.item in reserved_word:
                self.type = 'TYPE'
            elif self.item in conditional_statement:
                self.type = 'CONDITION'
            elif self.item in function_statement:
                self.type = 'FUNCTION'
            else:
                self.type = 'VARIABLE'
        else:
            self.type = ty

    def __str__(self):
        return "<%s, %s, %d, %d>" % (self.item, self.type, self.line, self.column)

    def __repr__(self):
        return "<%s,%s,%d, %d>" % (self.item, self.type, self.line, self.column)


class Tokenizer:
    tokens = []

    def __init__(self, path_text):
        file = open(path_text + ".txt", 'r')
        num_line = 1
        for line in file:
            self.tokenizerLine(line, num_line)
            num_line += 1

    def tokenizerLine(self, line, n_line):
        idx = 0
        while idx < len(line):
            if line[idx].isdigit():
                token,idx = self.checkNumber(line, n_line, idx)
                self.tokens.append(token)
            elif line[idx].isalpha():
                token,idx = self.checkVariable(line, n_line, idx)
                self.tokens.append(token)
            elif line[idx] == ' ' or line[idx] == '\n':
                idx += 1
            elif line[idx] == '.':
                token = Token(line[idx:idx+1], "DOT", n_line, idx)
                self.tokens.append(token)
                idx += 1
            elif line[idx] == '\'':
                next = line.find('\'', idx+1)
                token = Token(line[idx:next+1], "STRING", n_line, idx)
                self.tokens.append(token)
                idx = next+1
            elif line[idx] == ';':
                token = Token(line[idx:idx+1], "END_STATEMENT", n_line, idx)
                self.tokens.append(token)
                idx += 1
            else:
                if line[idx:idx+2] in comparison_op:
                    token = Token(line[idx:idx+2], "OP_COMPARE", n_line, idx)
                    self.tokens.append(token)
                    idx += 2
                else:
                    token = Token(line[idx:idx+1], "OTHER", n_line, idx)
                    self.tokens.append(token)
                    idx += 1

    def checkNumber(self, string, n_line, index):
        begin = index
        while (index < len(string)) and string[index].isdigit():
            index += 1
        temp = Token(string[begin:index], "NUMBER", n_line, begin)
        return temp, index

    def checkVariable(self, string, n_line, index):
        begin = index
        while (index < len(string)) and string[index].isalpha():
            index += 1
        temp = Token(string[begin:index], "STREAM", n_line, begin)
        return temp, index

'''
temp = '('
print(temp.isdigit())
print(temp.isalpha())
temp = '+'
print(temp.isdigit())
print(temp.isalpha())
temp = '!='
print(temp.isdigit())
print(temp.isalpha())
temp = ' '
print(temp.isdigit())
print(temp.isalpha())
'''
# temp = ';'
# print(temp.isdigit())

enter = Tokenizer('input')
print(enter.tokens)