def get_nssf_tier2_value(basicpay):
    basicpay = float(basicpay)
    if basicpay <= 6000:
        return 0
    rate = (basicpay * 0.06 - 360)
    if rate < 720:
        return rate
    return 720


def get_nssf_tier1_value(basicpay):
    tier1amt = float(basicpay) * 0.06
    return min(360, tier1amt)


def get_nhifrates():
    return [
        {'min': 1, 'max': 5999, 'value': 150},
        {'min': 6000, 'max': 7999, 'value': 300},
        {'min': 8000, 'max': 11999, 'value': 400},
        {'min': 12000, 'max': 14999, 'value': 500},
        {'min': 15000, 'max': 19999, 'value': 600},
        {'min': 20000, 'max': 24999, 'value': 750},
        {'min': 25000, 'max': 29999, 'value': 850},
        {'min': 30000, 'max': 34999, 'value': 900},
        {'min': 35000, 'max': 39999, 'value': 1000},
        {'min': 40000, 'max': 44999, 'value': 1100},
        {'min': 45000, 'max': 59999, 'value': 1200},
        {'min': 60000, 'max': 69999, 'value': 1300},
        {'min': 70000, 'max': 79999, 'value': 1400},
        {'min': 80000, 'max': 89999, 'value': 1500},
        {'min': 90000, 'max': 99999, 'value': 1600},
        {'min': 100000, 'max': 9999999, 'value': 1700},

    ]


def get_paye_rates_2021():
    lowest = {'min': 1, 'max': 24000, 'rate': 0.1}
    medium = {'min': 24001, 'max': 32333, 'rate': 0.25}
    highest = {'min': 32334, 'max': 9999999, 'rate': 0.3}

    return lowest, medium, highest


def get_personal_relief_2022(nhif, lifeinsurancepremium=0):
    nhif = int(nhif)
    lifeinsurancepremium = int(lifeinsurancepremium)
    total_relief_on_insurance = 0.15 * (nhif + lifeinsurancepremium)
    allowable_total_relief_on_insurance = min(5000, total_relief_on_insurance)
    personal_income_tax_relief = 2400

    return allowable_total_relief_on_insurance + personal_income_tax_relief


def get_nhif_value(gross_pay):
    rates = get_nhifrates()
    amount = 0
    for rate in rates:
        min_r = rate.get('min')
        max_r = rate.get('max')
        value_r = rate.get('value')
        if min_r and max_r and value_r:
            min_r = int(min_r)
            max_r = int(max_r)
            value_r = int(value_r)
            if max_r >= gross_pay >= min_r:
                amount = value_r
                break

    return amount


def get_allowable_pension(basicpay, pension=0):
    """
    The maximum monthly tax-allowable deduction with respect to contributions to a pension scheme
    is the minimum of:

    1. 30% of pensionable pay (for our case we use basic pay)
    2. actual deduction made
    3. Ksh 20,000

    NSSF is considered a contribution to a pension scheme.

    :param basicpay:
    :param pension:
    :return:
    """
    nssf = get_nssf_tier1_value(basicpay) + get_nssf_tier2_value(basicpay)

    return min(basicpay * 0.3, (nssf + pension), 20000)


def get_taxablepay(basicpay, allowances=0):
    allowablepensiondeduction = get_allowable_pension(basicpay)
    return basicpay + allowances - allowablepensiondeduction


def get_paye(basicpay, allowances=0):
    """
    If taxablepay > 32333 then:
        PAYE = (taxablepay-32333)*0.3 + 8333*0.25 + 24000*0.1
    Elsif taxablepay > 24000 then:
        PAYE = (taxablepay-24000)*0.25 + 24000*0.1
    Else:
        PAYE = taxablepay * 0.1

    :param basicpay:
    :param allowances:
    :return:
    """
    lowest_band, medium_band, highest_band = get_paye_rates_2021()
    taxablepay = get_taxablepay(basicpay, allowances)
    #    lowest_band_min_amount = lowest_band.get('min')
    lowest_band_max_amount = lowest_band.get('max')
    lowest_band_tax_rate = lowest_band.get('rate')
    medium_band_min_amount = medium_band.get('min')
    medium_band_max_amount = medium_band.get('max')
    medium_band_tax_rate = medium_band.get('rate')
    highest_band_min_amount = highest_band.get('min')
    highest_band_max_amount = highest_band.get('max')
    highest_band_tax_rate = highest_band.get('rate')

    if highest_band_min_amount <= taxablepay <= highest_band_max_amount:
        print("WE are using the highest band")
        amount_in_highest_band = taxablepay - highest_band_min_amount
        amount_in_medium_band=medium_band_max_amount-medium_band_min_amount
        return (amount_in_highest_band * highest_band_tax_rate) + \
            (amount_in_medium_band * medium_band_tax_rate) + \
            (lowest_band_max_amount * lowest_band_tax_rate)

    if medium_band_min_amount <= taxablepay <= medium_band_max_amount:
        print(" we are in the medium band")
        amount_in_medium_band = taxablepay - medium_band_min_amount
        return (amount_in_medium_band * medium_band_tax_rate) + \
            (lowest_band_max_amount * lowest_band_tax_rate)

    print("Lowest band")
    return taxablepay * lowest_band_tax_rate


def get_paye_payable(basicpay, allowances, lifeinsurancepremium=0):
    """
    The PAYE payable is the tax to pay after deducting personal relief from the computed PAYE
    :return:
    """
    basicpay = float(basicpay)
    allowances = float(allowances)
    grosspay = basicpay + allowances
    nhif = get_nhif_value(grosspay)
    paye = get_paye(basicpay, allowances)
    personal_relief = get_personal_relief_2022(nhif, lifeinsurancepremium)
    print("Calculated PAYE :", paye)
    print("Relief :", personal_relief)

    return max(0, (paye - personal_relief))


def get_total_deductions(basicpay, allowances, helb=0, pension=0, lifeinsurancepremium=0, otherdeductions=0):
    """

    :return:
    """
    gross_pay = basicpay + allowances
    paye_payable = get_paye_payable(basicpay, allowances, lifeinsurancepremium)
    nssf = get_nssf_tier1_value(basicpay) + get_nssf_tier2_value(basicpay)
    nhif = get_nhif_value(gross_pay)
    print("Gross :", gross_pay)
    print("PAYE :", paye_payable)
    print("NSSF :", nssf)
    print("NHIF :", nhif)
    print('Pension: ',pension)
    print('Ins Prem: ',lifeinsurancepremium)
    print('Other Deds: ',otherdeductions)
    print('HELB: ',helb)

    return paye_payable + nssf + nhif + pension + lifeinsurancepremium + otherdeductions + helb


def get_net_pay(basicpay, allowances, helb=0, pension=0, lifeinsurancepremium=0, otherdeductions=0):
    print('Basic pay: ',basicpay)
    totaldeduction = get_total_deductions(basicpay=basicpay, allowances=allowances, helb=helb, pension=pension,
                                          lifeinsurancepremium=lifeinsurancepremium, otherdeductions=otherdeductions)
    print('Total deductions: ',totaldeduction)
    grosspay = basicpay + allowances
    return grosspay - totaldeduction


def get_pension(basicpay):
    return 0
