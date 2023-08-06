import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import datetime as dt
slash = '/'
#path = os.getcwd()
class TaxTools():
    def get_csv_for_dataframe(tax_name,tax_year='2021/2022'):
        '''options for UK tax_name
                'income tax'
                'employee ni'
                'corporate ni'
                'dividend rates'
                'student loans'
                'corporation tax'
                'employee ni bands'
                'corporate ni bands'
                'high income threshold'
                'dividend tax free allowance'
            options for tax_year
                '2021/2022'
                '2022/2023'
        '''
        path = os.path.dirname(__file__)
        log_folder = path + '\\UK Tax Tables'
        tax_table_log = pd.read_csv(log_folder + '\\tax_name_log.csv')
        year = tax_table_log.loc[tax_table_log['tax name'] == tax_name, tax_year].item()
        tax = tax_table_log.loc[tax_table_log['tax name'] == tax_name, 'filename'].item()
        file_path = log_folder + year + tax
        a = pd.read_csv(file_path)
        return a

    #Universal Tax Tools LEVEL 0
    def create_table(tax_rates:pd.DataFrame):
        a = tax_rates.copy()
        a['threshold max'] = a['threshold min'].shift(-1)
        a = a[['threshold min','threshold max','rate']]
        a = a.fillna(np.inf)
        return a

    def marginal(cash,tax_table:pd.DataFrame):
        a = tax_table.copy()
        a.loc[-1] = [cash,cash,np.NaN]
        a.index = a.index + 1
        a = a.sort_index()
        a = a.sort_values(by=['threshold min'])
        a['threshold max'] = a['threshold max'].sort_values().values
        a = a.reset_index(drop=True)
        cut = a.index[a['threshold max'] == cash].tolist()
        cut = cut[0]
        a = a[a.index <= cut].copy()
        a['tax'] = (a['threshold max'] - a['threshold min']) * a['rate']
        a_total = a['tax'].sum()
        return a_total

    def marginalise(cash,table:pd.DataFrame):
        a = TaxTools.create_table(table)
        b = TaxTools.marginal(cash,a)
        return(b)

    def replace_threshold_rates(threshold_table:pd.DataFrame,rates:pd.DataFrame):
        a = threshold_table.copy()
        b = rates.copy()
        a['rate'] = b['rate']
        return a

    def interpret_single_df_value(df:pd.DataFrame):
        return int(df['value'])

    def optimal_iterations(input_value):
        x_min = 5
        x_max = input_value/2
        d = {}

        for i in range(int(x_min),int(x_max)+1):
            key = i
            value = int((input_value/i) + i)
            d[key] = value + int(input_value/i)

        min_value = min(d.values())
        min_key = min([k for k, v in d.items() if v == min_value])
        return min_value

    #UK Tax Tools LEVEL 1
    def interpret_tax_code_allowance(tax_code):
        a = ''.join([i for i in tax_code if i.isdigit()])
        a = int(a)
        a = a * 10
        return a

    def interpret_tax_code_ni_band(tax_code):
        a = ''.join([i for i in tax_code if not i.isdigit()])
        return a

    def adjust_allowance(salary,tax_allowance,tax_table:pd.DataFrame,tax_year):
        a = tax_table
        allowance_reduction = a.loc[1,'threshold min'] - tax_allowance
        a.loc[1,'threshold min'] = a.loc[1,'threshold min'] - allowance_reduction
        a.loc[2,'threshold min'] = a.loc[2,'threshold min'] - allowance_reduction
        b = TaxTools.get_csv_for_dataframe('high income threshold',tax_year)
        c = TaxTools.interpret_single_df_value(b)
        if salary > c:
            change_range = c + 2 * tax_allowance
            d = {'numbers': list(range(c,change_range + 1,2))}
            change_df = pd.DataFrame(data=d)
            change_df = change_df[change_df['numbers'] <= salary]
            allowance_chg = change_df.index[-1]
        else:
            allowance_chg = 0 
        a.loc[1,'threshold min'] = a.loc[1,'threshold min'] - allowance_chg
        a.loc[2,'threshold min'] = a.loc[2,'threshold min'] - allowance_chg
        return a

    def adjust_ni_band(tax_table:pd.DataFrame,ni_band_table:pd.DataFrame,ni_band):
        a = ni_band_table.copy()
        a = a[a['category'] == ni_band]
        a = a.transpose()
        a.columns = ['rate']
        a = a.reset_index(drop=True)
        a.drop([0], axis=0, inplace=True)
        a = a.reset_index(drop=True)
        b = tax_table.copy()
        b['rate'] = a['rate']
        return b

    def create_dividend_table(salary,tax_free_amount,tax_table:pd.DataFrame):
        a = tax_table.copy()
        a.loc[-1] = [(salary + tax_free_amount),np.NaN]
        a = a.sort_values(by=['threshold min'])
        a = a.reset_index(drop=True)
        a = a.fillna(method='ffill')
        cut = a.index[a['threshold min'] == salary + tax_free_amount].tolist()
        cut = cut[0]
        a = a[a.index >= cut]
        return a

    def create_student_loan_table(table:pd.DataFrame,plan):
        a = table.copy()
        a = a[a['category'] == plan]
        a = a[['threshold min','rate']]
        return a

    #UK Tax Laws LEVEL 2
    def employee_ni(salary,tax_code,tax_year):
        a = TaxTools.get_csv_for_dataframe('employee ni',tax_year)
        b = TaxTools.interpret_tax_code_ni_band(tax_code)
        c = TaxTools.get_csv_for_dataframe('employee ni bands',tax_year)
        d = TaxTools.adjust_ni_band(a,c,b)
        e = TaxTools.marginalise(salary,d)
        return e

    def income_tax(salary,tax_code,tax_year):
        a = TaxTools.get_csv_for_dataframe('income tax',tax_year)
        b = TaxTools.interpret_tax_code_allowance(tax_code)
        c = TaxTools.adjust_allowance(salary,b,a,tax_year)
        d = TaxTools.marginalise(salary,c)
        return d

    def corporate_ni(salary,tax_code,tax_year):
        a = TaxTools.get_csv_for_dataframe('corporate ni',tax_year)
        b = TaxTools.get_csv_for_dataframe('corporate ni bands',tax_year)
        c = TaxTools.interpret_tax_code_ni_band(tax_code)
        d = TaxTools.adjust_ni_band(a,b,c)
        e = TaxTools.marginalise(salary,d)
        return e

    def corporation_tax(gross_profit,tax_year):
        a = TaxTools.get_csv_for_dataframe('corporation tax',tax_year)
        b = TaxTools.marginalise(gross_profit,a)
        return b

    def dividend_tax(salary,dividend,tax_code,tax_year):
        a = TaxTools.get_csv_for_dataframe('income tax',tax_year)
        b = TaxTools.interpret_tax_code_allowance(tax_code)
        c = TaxTools.adjust_allowance(salary,b,a,tax_year)
        d = TaxTools.get_csv_for_dataframe('dividend rates',tax_year)
        e = TaxTools.replace_threshold_rates(c,d)
        f = TaxTools.get_csv_for_dataframe('dividend tax free allowance',tax_year)
        g = TaxTools.interpret_single_df_value(f)
        h = TaxTools.create_dividend_table(salary,g,e)
        take = salary + dividend
        i = TaxTools.marginalise(take,h)
        return i

    def student_loans(cash,plan,tax_year):
        a = TaxTools.get_csv_for_dataframe('student loans',tax_year)
        b = TaxTools.create_student_loan_table(a,plan)
        c = TaxTools.marginalise(cash,b)
        return c

    #UK Tax Calculation LEVEL 3
    def salary_taxes(salary,tax_code,student_loan_plan,tax_year,student_loan_second_plan='plan 0'):
        a = TaxTools.employee_ni(salary,tax_code,tax_year)
        b = TaxTools.income_tax(salary,tax_code,tax_year)
        c = TaxTools.corporate_ni(salary,tax_code,tax_year)
        d = TaxTools.student_loans(salary,student_loan_plan,tax_year)
        e = TaxTools.student_loans(salary,student_loan_second_plan,tax_year)
        total_student_loans = d + e
        salary_take = salary - a - b - total_student_loans
        employee_cost = salary + c
        d = {'Salary':[salary],
            'Employee National Insurance':[a],
            'Income Tax':[b],
            'Employer National Insurance':[c],
            'Student Loans':[total_student_loans],
            'Salary Takehome':[salary_take],
            'Total Employee Cost':[employee_cost]
            }
        return pd.DataFrame(data=d)

    #UK Tax Corporate Calculation LEVEL 4
    def ltd_owner_full_take(turnover,salary,expenses,tax_code,tax_year='2021/2022',student_loan_plan='plan 0',student_loan_second_plan='plan 0'):
        a = TaxTools.salary_taxes(salary,tax_code,'plan 0',tax_year).copy()
        turnover_deduct_expenses = turnover - expenses
        gross_profit = turnover - (expenses + salary)
        c = TaxTools.corporation_tax(gross_profit,tax_year)
        net_profit = gross_profit - c
        gross_take = salary + net_profit
        d = TaxTools.dividend_tax(salary,net_profit,tax_code,tax_year)
        div_take = net_profit - d
        e = TaxTools.student_loans(gross_take,student_loan_plan,tax_year)
        f = TaxTools.student_loans(gross_take,student_loan_second_plan,tax_year)
        total_student_loans = e + f
        a['Student Loans'] = total_student_loans
        total_take = int(a['Salary Takehome']) + div_take - total_student_loans
        percentage = total_take/turnover * 100
        i = {'Usable Funds':[turnover_deduct_expenses],
            'Corporation Tax':[c],
            'Dividend':[net_profit],
            'Dividend Tax':[d],
            'Dividend Takehome':[div_take],
            'Gross Take':[gross_take],
            'Total Takehome':[total_take],
            'Percentage Take':[percentage]
            }
        j = pd.DataFrame(i)
        a = a.join(j)
        return a

    #UK Tax Corporate Scenario Iteration LEVEL 5
    def iterate_salaries_ltd_take(turnover,min_salary,max_salary,expenses,iteration_step=1,tax_code='1257A',tax_year='2021/2022',student_loan_plan='plan 0',student_loan_second_plan='plan 0'):
        a = pd.DataFrame()
        for i in range(min_salary,max_salary + 1,iteration_step):
            b = TaxTools.ltd_owner_full_take(turnover,i,expenses,tax_code)
            a = pd.concat([a,b])
        a = a.reset_index(drop=True)
        return a

    def iterate_ltd_owner_full_take(turnover,expenses,tax_code='1257A',tax_year='2021/2022',student_loan_plan='plan 0',student_loan_second_plan='plan 0'):
        turnover_deduct_expenses = turnover - expenses
        a = TaxTools.iterate_salaries_ltd_take(turnover,0,turnover_deduct_expenses,expenses,1,tax_code,tax_year,student_loan_plan,student_loan_second_plan)
        return a

    #UK Tax Corporate Optimisation LEVEL 6
    def optimal_take(options:pd.DataFrame):
        a = options.copy()
        b = a[a['Total Takehome'] == a['Total Takehome'].max()]
        return b

    def optimise_ltd_owner_full_take(turnover,expenses,tax_code,tax_year='2021/2022',student_loan_plan='plan 0',student_loan_second_plan='plan 0'):
        a = TaxTools.iterate_ltd_owner_full_take(turnover,expenses,tax_code,tax_year,student_loan_plan)
        b = TaxTools.optimal_take(a)
        return(b)

    def optimise_lite_ltd_owner_full_take(turnover,expenses,tax_code,tax_year='2021/2022',student_loan_plan='plan 0',student_loan_second_plan='plan 0'):
        turnover_deduct_expenses = turnover - expenses
        iteration_step = TaxTools.optimal_iterations(turnover_deduct_expenses)
        a = TaxTools.iterate_salaries_ltd_take(turnover,0,turnover_deduct_expenses,expenses,iteration_step,tax_code,tax_year,student_loan_plan,student_loan_second_plan)
        optimal_row = a.index[a['Total Takehome'] == a['Total Takehome'].max()].tolist()
        optimal_range = [*range(optimal_row[0]-1,optimal_row[0]+2)]
        optimal_options = a.iloc[optimal_range]
        minn = int(optimal_options.iloc[[0]]['Salary'])
        maxx = int(optimal_options.iloc[[2]]['Salary'])
        b = TaxTools.iterate_salaries_ltd_take(turnover,minn,maxx,expenses,1,tax_code,tax_year,student_loan_plan,student_loan_second_plan)
        c = TaxTools.optimal_take(b)
        return c