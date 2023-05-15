import numpy as np
import pandas as pd

class loan:
    def __init__(self, amount, interest, period, excess, lower_rate=False):
        self.amount = amount
        self.interest = interest
        self.period = period
        self.excess = excess
        self.lower_rate = lower_rate
        self.df = pd.DataFrame({'Debt left': [], 'Debt paid': [], 'Capital_part': [], 'Interest_part': [],
                        'Installment': [], 'Excess':[], 'Tot. Payment': [], 'Cost':[], 'Tot. Interest':[]})
        self.df = self.df.append([[] for _ in range(self.period)], ignore_index=True)
        self.df['Debt left'][0] = self.amount

        self.calc_loan()


class fixed_loan(loan):

    def calc_installment(self, amount, interest, period):
        L = ((interest/12)*(1+(interest/12))**period)
        M = ((1+(interest/12))**period - 1)
        installment = amount * (L/M)
        return round(installment, 2)

    def calc_row(self, n):
        if(self.lower_rate):
            installment = self.calc_installment(self.df['Debt left'][n], self.interest, self.period-n)
        else:
            installment = self.calc_installment(self.amount, self.interest, self.period)

        self.df['Installment'][n] = installment
        self.df['Excess'][n] = self.excess[n]
        self.df['Interest_part'][n] = self.interest/12 * self.df['Debt left'][n]
        self.df['Capital_part'][n] = installment - self.df['Interest_part'][n]
        self.df['Debt left'][n+1] = self.df['Debt left'][n] - self.df['Capital_part'][n] - self.excess[n]

        if(self.df['Debt left'][n] < installment + self.excess[n]):
            self.df['Tot. Payment'][n] = self.df['Debt left'][n]
            self.df.drop(self.df.tail(self.period-1-n).index,inplace = True)
            end = True
        else:
            self.df['Tot. Payment'][n] = installment + self.df['Excess'][n]
            end = False

        if n==0:
            self.df['Cost'][n] = self.df['Tot. Payment'][n]
            self.df['Debt paid'][n] = self.df['Capital_part'][n] + self.excess[n]
        else:
            self.df['Cost'][n] = self.df['Cost'][n-1] + self.df['Tot. Payment'][n]
            self.df['Debt paid'][n] = self.df['Debt paid'][n-1] + self.df['Capital_part'][n] + self.excess[n]

        self.df['Tot. Interest'][n] = self.df['Cost'][n] - self.df['Debt paid'][n]
        return end

    def calc_loan(self):
        for n in range(self.period):
            if (self.calc_row(n)) : break

        self.df.index = np.arange(1, len(self.df)+1)
        self.df = self.df.round(2)

class decreasing_loan(loan):

    def calc_installment(self, n):
        installment = (self.amount/self.period) * (1+(self.period-n+1)*(self.interest/12))
        return round(installment, 2)

    def calc_loan(self):
        print(self.calc_installment(1))
        # for n in range(self.period):
        #     if (self.calc_row(n)) : break

        # self.df.index = np.arange(1, len(self.df)+1)
        # self.df = self.df.round(2)