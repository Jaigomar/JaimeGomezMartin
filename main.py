import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from boiler import boiler
from pump import pump
from steamTurbine import steamTurbine

from numpy_financial import pmt, ipmt, ppmt, npv, irr

def loan(quantity, interest, years):
    """Compute annual payment of a loan. Inputs:
    quantity [monetary units] == investment which will be funded
    interest [as fraction of unity] == annual interest
    years == number of yeras to return the loan."""

    assert quantity > 0
    assert interest >= 0 and interest <= 1
    assert years > 1

    loan_payment = pmt(interest, years, quantity)
    loan_interest = ipmt(interest, np.arange(years) + 1, years, quantity)
    loan_principal = ppmt(interest, np.arange(years) + 1, years, quantity)

    return loan_payment, loan_interest, loan_principal


def depreciation(annual_percent, capex, residual_value=0):
    """Compute annual depreciation of investment. Inputs:
    annual_percent [as fraction of unity] == annual percent of depreciation.
    capex [monetary units] == capital expenditure
    residual_value[monetary units] == plant value at the end of its life."""

    assert annual_percent >= 0 and annual_percent <= 1

    annual_depreciation = []
    prev = 1

    while True:
        if prev < annual_percent:
            annual_depreciation.append(prev)
            break
        annual_depreciation.append(annual_percent)
        prev = prev - annual_percent

    depreciation_array = -1 * np.array(annual_depreciation) * (capex - residual_value)

    return depreciation_array

def calculate_capex(*correlations):
    """
    Add all the correlations to calculate capex
    """
    return np.sum(correlations)


def calculate_financial_model(capex, years, dep_array):
    """
    Return a dataframe with the finacial model and the cash flow
    """
    investment = np.array([-capex * 0.4] + [0 for i in range(years - 1)])
    depreciation = np.hstack(([0], dep_array, [0 for i in range(years - 1 - len(dep_array))]))
    loan_prin = np.hstack(([0], principal, [0 for i in range(years - 1 - len(principal))]))
    loan_int = np.hstack(([0], interest, [0 for i in range(years - 1 - len(interest))]))

    sales_array = np.zeros(years)
    water_array = np.zeros(years)
    salaries_array = np.zeros(years)

    for i in range(years):
        if i == 0:
            sales_array[i] = 0
            water_array[i] = 0
            salaries_array[i] = 0
        elif i == 1:
            sales_array[i] = sales
            water_array[i] = -1 * water
            salaries_array[i] = -1 * salaries
        else:
            sales_array[i] = sales_array[i - 1] * 1.03
            water_array[i] = water_array[i - 1] * 1.03
            salaries_array[i] = salaries_array[i - 1] * 1.02

    ebt = np.vstack((investment, depreciation, loan_int, sales_array, water_array, salaries_array)).sum(axis=0)
    taxes = ebt * -0.3
    for i in range(len(taxes)):
        if taxes[i] > 0:
            taxes[i] = 0
    eat = ebt - taxes
    cash_flow = eat - depreciation + loan_prin
    cumulative_cash_flow = np.cumsum(cash_flow)

    data = np.vstack((investment, sales_array, depreciation, loan_prin, loan_int, salaries_array, water_array, ebt,
                      taxes, eat, cash_flow, cumulative_cash_flow))
    df = pd.DataFrame(data,
                      index=['Investment', 'Sales', 'Depreciation', 'Loan principal', 'Loan interest', 'Salaries',
                             'Water', 'EBT', 'Taxes', 'EAT', 'Cash Flow', 'Cumulative Cash Flow'],
                      columns=[i for i in range(years)])

    return cash_flow, df

def calculate_payback(cash_flow):
    """
    Return payback period
    """
    df = pd.DataFrame(cash_flow, columns=['CashFlow'])
    df['CumulativeCashFlow'] = np.cumsum(df['CashFlow'])
    final_year = df[df.CumulativeCashFlow < 0].index.values.max()
    fraction_year = -df.CumulativeCashFlow[final_year] / df.CashFlow[final_year + 1]
    payback_period = final_year + fraction_year
    return payback_period

def graph(df):
    """
    Shows a graph showing Investment, Sales, Cash Flow and Cumulative Cash Flow
    """
    dfp = df.loc[["Investment","Sales", "Cash Flow", "Cumulative Cash Flow"],:]
    dfp.T.plot()
    plt.title('Financial Model Results', fontsize=20)
    plt.xlabel('Year', fontsize=18)
    plt.show()

def excel(df):
    """
    Prints dataframe to a excel file
    """
    df.to_csv("financial_model.xlsx", index=True, sep=',')

if __name__ == '__main__':

    data_factors = np.array([[0.3, 0.5, 0.6],
                             [0.8, 0.6, 0.2],
                             [0.3, 0.3, 0.2],
                             [0.2, 0.2, 0.15],
                             [0.3, 0.3, 0.2],
                             [0.2, 0.2, 0.1],
                             [0.1, 0.1, 0.05],
                             [0.3, 0.4, 0.4],
                             [0.35, 0.25, 0.2],
                             [0.1, 0.1, 0.1]])

    Capital_factors = pd.DataFrame(data_factors,
                                   index=["fer", "fp", "fi", "fel", "fc", "fs", "fl", "OS", "D&E", "X"],
                                   columns=["Fluids", "Fluids-Solids", "Solids"])

    # Calculating capital costs (CAPEX)
    fm = 1
    installed = True

    boiler = boiler(10000, 70, fm, installed).calculate_cost_boiler(Capital_factors)
    turbine = steamTurbine(1500, fm, installed).calculate_cost_turbine(Capital_factors)
    pump = pump(2.84, fm , installed).calculate_cost_pump(Capital_factors)
    condenser = 400000 * (10000 / 15000) ** 0.8

    capex = calculate_capex([boiler, turbine, condenser, pump])

    # Calculating operational costs (OPEX)
    capacity_factor = 0.9

    water = 1.29 * 10 * 8760 * capacity_factor
    salaries = 4 * 3 * 30000

    # Calculating loan
    quantity = 0.6 * capex
    _, interest, principal = loan(quantity, 0.04, 10)

    # Calculating depreciation
    dep_array = depreciation(0.07, capex)

    # Calculating sales
    sales = 1500 * 0.05 * 8760 * capacity_factor

    # Calculating financial model
    years = 20

    cash_flow, df = calculate_financial_model(capex, years, dep_array)

    # Calculating financial metrics
    discount_rate = 0.053

    npv = npv(discount_rate, cash_flow)
    irr = irr(cash_flow)

    # Calculate payback period
    payback = calculate_payback(cash_flow)

    # Printing results
    print(df)
    print(
        f"The project has a net present value of {'{:,.2f}'.format(npv)}€ and an internal rate of return of {round(irr * 100, 2)}%")
    print(f"The payback period is {round(payback, 2)}")

    # Print to excel
    excel(df)
    graph(df)

