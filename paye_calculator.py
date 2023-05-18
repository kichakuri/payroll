def get_taxable_pay(basic_pay,allowances,taxable_deductions):
    return basic_pay+allowances-taxable_deductions

def get_taxable_deductions(nssf,paye,pension):
    return nssf+paye+pension

def get_paye(taxable_pay):
    band1,band2=24000,32333
    band1rate,band2rate,band3rate = 0.1,0.25,0.3

    if taxable_pay > band2:
        return (taxable_pay-band2)*band3rate+4483.25
    elif taxable_pay > band1:
        return (taxable_pay-band1)*band2rate+2400
    else:
        return taxable_pay*band1rate
def get_net_paye(paye):
    return max(0,paye-2400)
