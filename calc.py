import random
from term_avg_pair import TermAvgPair

class Calc:
    def __init__(self):
        self.editing_main_term = True
        self.just_switched = False
        self.cocked_results = []
        self.current_oper = '+'
        self.pre_parenthetical_oper = ''
        self.main = TermAvgPair()
        self.past_main = TermAvgPair()
        self.parenthetical = TermAvgPair()
        self.past_parenthetical = TermAvgPair()
        self.main_total = TermAvgPair()
        self.parenthetical_total = TermAvgPair()
        self.i = 0

    def honor_the_cock(self, sides):
        return "Honor the cock. Roll " + str(self.i) + " would have been " + str(random.randint(1, sides))

    def roll_die(self, sides):
        self.i += 1
        if random.random() < .025:
            self.cocked_results.append(
                self.honor_the_cock(sides)
            )
        result = random.randint(1, sides)
        return result

    def calc_num_rolls(self, s):
        try:
            num_rolls = int(s[0:s.index('d')])
        except: 
            try:
                num_rolls = int(s[0:s.index('e')])
            except: 
                num_rolls = 1
        return num_rolls
    
    def update_main_total(self):
        if self.pre_parenthetical_oper == '+':
            self.main_total.term += self.parenthetical_total.term
            self.main_total.avg += self.parenthetical_total.avg
        if self.pre_parenthetical_oper == '-':
            self.main_total.term -= self.parenthetical_total.term
            self.main_total.avg -= self.parenthetical_total.avg
        if self.pre_parenthetical_oper == '*':
            self.main_total.term *= self.parenthetical_total.term
            self.main_total.avg *= self.parenthetical_total.avg
        if self.pre_parenthetical_oper == '/':
            self.main_total.term /= self.parenthetical_total.term
            self.main_total.avg /= self.parenthetical_total.avg

    def calc_main_total(self):
        if self.current_oper == '+':
            self.main_total.term += self.main.term
            self.main_total.avg += self.main.avg
        elif self.current_oper == '-':
            self.main_total.term -= self.main.term
            self.main_total.avg -= self.main.avg
        elif self.current_oper == '*':
            self.main_total.term += self.past_main.term * self.main.term - self.past_main.term
            self.main_total.avg += self.past_main.avg * self.main.avg - self.past_main.avg
        elif self.current_oper == '/':
            self.main_total.term += int(self.past_main.term / self.main.term) - self.past_main.term
            self.main_total.avg += int(self.past_main.avg / self.main.avg) - self.past_main.avg

    def calc_parenthetical_total(self):
        if self.current_oper == '+':
            self.parenthetical_total.term += self.parenthetical.term
            self.parenthetical_total.avg += self.parenthetical.avg
        elif self.current_oper == '-':
            self.parenthetical_total.term -= self.parenthetical.term
            self.parenthetical_total.avg -= self.parenthetical.avg
        elif self.current_oper == '*':
            self.parenthetical_total.term += self.past_main.term * self.parenthetical.term - self.past_main.term
            self.parenthetical_total.avg += self.past_main.avg * self.parenthetical.avg - self.past_main.avg
        elif self.current_oper == '/':
            self.parenthetical_total.term += int(self.past_main.term / self.parenthetical.term) - self.past_main.term
            self.parenthetical_total.avg += int(self.past_main.avg / self.parenthetical.avg) - self.past_main.avg