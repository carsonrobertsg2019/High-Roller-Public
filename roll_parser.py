import string
import re
from calc import Calc

class Parser:
    def __init__(self, s):
        self.calc = Calc()
        self.s = s
        self.list_of_lists_of_rolled = []
        self.text_channels = [
            "dice-rolls",
            "dice-tray",
            "dicetray",
            "death-saving-throws",
            "box-of-doom"
        ]

    def clear_disallowed_chars(self):
        all_chars = list(chr(i) for i in range(1114111))
        allowed_chars = list(string.digits)
        allowed_chars.extend([
            'd',
            'e',
            '+',
            '-',
            '*',
            '/',
            '(',
            ')'
        ])
        disallowed_chars = [c for c in all_chars if c not in allowed_chars]
        self.s = (self.s[0] + ''.join(i for i in self.s[1:len(self.s)] if not i in disallowed_chars))

    def expect(self, char):
        if self.s[0] == char:
            self.s = self.s[1:len(self.s)]

    def parse_oper(self):
        if(self.s[0] == '+'):
            self.expect('+')
            self.calc.current_oper = '+'
        elif(self.s[0] == '-'):
            self.expect('-')
            self.calc.current_oper = '-'
        elif(self.s[0] == '*'):
            self.expect('*')
            self.calc.current_oper = '*'
        elif(self.s[0] == '/'):
            self.expect('/')
            self.calc.current_oper = '/'

    def parse_roll(self):
        list_of_rolled = []

        if self.calc.editing_main_term:
            if self.calc.just_switched:
                self.calc.past_main = self.calc.parenthetical_total
            else:
                self.calc.past_main = self.calc.main
        else:
            if self.calc.just_switched:
                self.calc.past_parenthetical = 0
            else: 
                self.calc.past_parenthetical = self.calc.parenthetical

        num_rolls = self.calc.calc_num_rolls(self.s)
        if(num_rolls > 101):
            return
        self.s = self.s[self.s.index('d'):len(self.s)]
        self.expect('d')
        num_sides = int(self.s[0:len(re.findall("[\dA-Za-z]*", self.s)[0])])
        self.s = self.s[len(re.findall("[\dA-Za-z]*", self.s)[0]):len(self.s)]

        if self.calc.editing_main_term:
            self.calc.main.term = 0
            self.calc.main.avg = 0
        else:
            self.calc.parenthetical.term = 0
            self.calc.parenthetical.avg = 0

        for i in range(num_rolls):
            num = self.calc.roll_die(num_sides)
            list_of_rolled.append(num)
            if self.calc.editing_main_term:
                self.calc.main.term += num
                self.calc.main.avg += (num_sides + 1) / 2
            else:
                self.calc.parenthetical.term += num
                self.calc.parenthetical.avg += (num_sides + 1) / 2

        if self.calc.editing_main_term:
            self.calc.calc_main_total()
        else:
            self.calc.calc_parenthetical_total()

        self.list_of_lists_of_rolled.append(list_of_rolled)

    def parse_exploding_roll(self):
        list_of_rolled = []
        #self.calc.past_main.term = self.calc.main.term
        #self.calc.past_main.avg = self.calc.main.avg
        num_rolls = self.calc.calc_num_rolls(self.s)
        if(num_rolls > 101):
            return
        self.s = self.s[self.s.index('e'):len(self.s)]
        self.expect('e')
        num_sides = int(self.s[0:len(re.findall("[\dA-Za-z]*", self.s)[0])])
        self.s = self.s[len(re.findall("[\dA-Za-z]*", self.s)[0]):len(self.s)]
        #self.calc.main.term = 0
        #self.calc.main.avg = 0
        for i in range(num_rolls):
            avg_calculated = False
            while(True): #would've preferred a do loop
                num = self.calc.roll_die(num_sides)
                list_of_rolled.append(num)
                #self.calc.main.term += num
                sum_sides = 0
                if not avg_calculated:
                    for side_num in range(num_sides + 1):
                        sum_sides += side_num
                    #self.calc.main.avg += sum_sides/(num_sides - 1)
                    avg_calculated = True
                if(num_sides == 1 or num != num_sides): break
        self.calc.calc_main_total()
        self.list_of_lists_of_rolled.append(list_of_rolled)
    
    def parse_num(self):
        if((self.calc.editing_main_term and self.calc.just_switched) or (not self.calc.editing_main_term and not self.calc.just_switched)):
            self.calc.past_main.term = self.calc.main.term
        else:
            self.calc.past_main.term = self.calc.main.term
            self.calc.past_main.avg = self.calc.main.avg
        
        #self.calc.main.term = int(self.s[0:len(re.findall("[\dA-Za-z]*", self.s)[0])])
        #self.calc.main.avg = self.calc.main.term
        self.s = self.s[len(re.findall("[\dA-Za-z]*", self.s)[0]):len(self.s)]
        self.calc.calc_main_total()

    def parse_expr(self):
        res = len(re.findall("[\dA-Za-z(]*", self.s)[0])
        if('(' in self.s[0:res]):
            self.calc.parenthetical_total.term = 0
            self.calc.parenthetical_total.avg = 0
            self.calc.pre_parenthetical_oper = self.calc.current_oper
            self.calc.editing_main_term = False
            self.calc.just_switched = True
            self.expect('(')
        if 'd' in self.s[0:res]:
            self.parse_roll()
        elif 'e' in self.s[0:res]:
            self.parse_exploding_roll()
        else:
            self.parse_num()
        self.calc.just_switched = False
        if len(self.s[0:res]) != 0 and ')' in self.s[0]:
            self.calc.editing_main_term = True
            self.calc.just_switched = True
            self.expect(')')
            self.calc.update_main_total()
            if len(self.s[0:res]) != 0:
                self.parse_oper()
                self.parse_expr()
        elif len(self.s[0:res]) != 0:
            self.parse_oper()
            self.parse_expr()

    def parse_init(self):
        self.expect('!')
        self.parse_expr()