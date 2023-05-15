import matplotlib
import matplotlib.pyplot as plt
import loan as ln
import numpy as np

LOAN_AMOUNT = 430_000
WINOR = 5.75/100
MARGIN = 2.3/100
INTEREST2 = 2.0/100 + MARGIN
INTERESTWINOR = WINOR + MARGIN
PERIOD_Y = 20
PERIOD_M = PERIOD_Y * 12
EXCESS = 1000
LOWER_INST = True
SHORTER_LOAN = False

excess_0 = np.zeros(PERIOD_M)
excess_1500 = np.empty(PERIOD_M)
excess_1500.fill(1500)
excess_2000_after_10_y = np.zeros(PERIOD_M)
excess_2000_after_10_y[120:] = 3000

def plotLoan(loan, ax, color):
    df = loan.df
    last_month = df.index[-1]
    total_cost = df['Cost'][last_month]
    last_installment = df['Tot. Payment'][last_month-1]
    first_installment = df['Tot. Payment'][1]

    minExcess = int(df['Excess'].min())
    maxExcess = int(df['Excess'].max())

    ax[0].plot(df.index, df['Cost'], color=color, label=f'Rata stała {loan.interest*100}%, nadpłata {minExcess}-{maxExcess} PLN')
    ax[1].plot(df.index[:-1], df['Tot. Payment'][:-1], color=color)

    ax[0].vlines(x=last_month, ymin=0, ymax=total_cost, colors=color,linestyles='dashed', linewidth=1, alpha=0.5)
    ax[1].vlines(x=df.index[-2], ymin=0, ymax=last_installment, colors=color,linestyles='dashed', linewidth=1, alpha=0.5)

    ax[0].text(last_month, total_cost+50000, f'{total_cost} PLN', color=color, bbox=dict(facecolor='none', edgecolor=color), weight='bold')
    ax[1].text(last_month, last_installment+500, f'{last_installment} PLN', color=color, bbox=dict(facecolor='none', edgecolor=color), weight='bold')
    if(loan.lower_rate):
        ax[1].text(5, first_installment+500, f'{first_installment} PLN', color=color, bbox=dict(facecolor='none', edgecolor=color), weight='bold')

    x_ticks = np.append(ax[0].get_xticks(), last_month)
    ax[0].set_xticks(x_ticks)

fig, ax = plt.subplots(2, 1, figsize=(14,8))
ax[0].set_xticks([])
ax[0].hlines(y=LOAN_AMOUNT, xmin=0, xmax=260, colors='black',linestyles='dashed', linewidth=1, alpha=0.5)
ax[0].text(24, LOAN_AMOUNT+30000, f'{LOAN_AMOUNT} PLN', color='black', bbox=dict(facecolor='none', edgecolor='black'))
fig.suptitle(f'Kredyt {LOAN_AMOUNT} PLN na {PERIOD_Y} lat', fontsize=15)
ax[0].set_xlabel('Miesiące', fontsize=10)
ax[1].set_xlabel('Miesiące', fontsize=10)
ax[0].set_ylabel('Całkowity koszt [PLN]', fontsize=10)
ax[1].set_ylabel('Całkowita rata [PLN]', fontsize=10)
ax[0].set_xlim([1, 260])
ax[1].set_xlim([1, 260])

loans = []
loans.append(ln.fixed_loan(LOAN_AMOUNT, INTEREST2, PERIOD_M, excess_0, SHORTER_LOAN))
loans.append(ln.fixed_loan(LOAN_AMOUNT, INTEREST2, PERIOD_M, excess_2000_after_10_y, SHORTER_LOAN))
loans.append(ln.fixed_loan(LOAN_AMOUNT, INTERESTWINOR, PERIOD_M, excess_0, SHORTER_LOAN))
loans.append(ln.fixed_loan(LOAN_AMOUNT, INTERESTWINOR, PERIOD_M, excess_1500, SHORTER_LOAN))

print(loans[0].df[110:130])

for idx, loan in enumerate(loans):
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["red","green","blue"], N=len(loans))
    plotLoan(loan, ax, cmap(idx))

max_cost = 0
max_installment = 0

for loan in loans:

    total_cost = loan.df['Cost'].iloc[-1]
    installment = loan.df['Tot. Payment'].iloc[0]

    if installment > max_installment:
        max_installment = installment

    if total_cost > max_cost:
        max_cost = total_cost

ax[1].set_ylim([0, max_installment+2000])
ax[0].set_ylim([0, total_cost+500000])
fig.legend()
plt.show()