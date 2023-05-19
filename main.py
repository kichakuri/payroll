# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from paye_calculator import *
from constants import get_net_pay


def calculator():
    # Use a breakpoint in the code line below to debug your script.
    basic = float(input("Provide basic pay: "))
    allowance = float(input("Provide allowances: "))
    helb = float(input("Provide the HELB deduction: "))
    deductions = float(input("Provide the other deductions amount: "))
    life_insurance = float(input("Provide the lite insurance premiums paid: "))

    pension =0# (float(basic) * 0.075)
    net_pay = get_net_pay(basicpay=basic, allowances=allowance, helb=helb, pension=pension,
                          lifeinsurancepremium=life_insurance, otherdeductions=deductions)
    print(f'Your net pay is, {net_pay}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    calculator()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
