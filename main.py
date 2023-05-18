# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from paye_calculator import *


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    basic = 30000
    allowance = 5000
    deductions = 200
    taxable_pay = get_taxable_pay(basic_pay=basic, allowances=allowance, taxable_deductions=deductions)
    paye=get_paye(taxable_pay)
    net_paye=get_net_paye(paye)
    print(f'You Taxable income is, {taxable_pay}')  # Press Ctrl+F8 to toggle the breakpoint.
    print(f'Your PAYE is, {get_net_paye(paye)}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
