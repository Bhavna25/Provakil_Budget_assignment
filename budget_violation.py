import csv                                         
import datetime                                    
from dateutil.relativedelta import relativedelta    


class BudgetViolation:
    def __init__(self, budget_file, investment_file):                           
        """Initialization"""
        self.budget_file = budget_file
        self.investment_file = investment_file
        self.rule = {'1.00': {}, '2.00': {}, '3.00': {}, '4.00': {}, '5.00': {}}
        self.time = {"Month": 1, "Quarter": 3, "Year": 12}

    def check_violation_investments(self):                                         
        with open(self.investment_file, 'r') as investments:                       
            read_invests = csv.DictReader(investments)                              
            for invest in read_invests:                                            
                self.check_violation(invest)                                       

    def check_violation(self, invest):                                                                  
        invest_date = datetime.datetime.strptime(invest['Date'], '%d/%m/%Y')                           
        with open(self.budget_file, 'r') as budgets:                                                   
            read_budgets = csv.DictReader(budgets)                                                     
            for budget in read_budgets:
                if budget['Sector'] == '' or invest['Sector'] == budget['Sector']:                                     
                    if float(invest['Amount']) <= float(budget['Amount']):                                              
                        if self.rule[budget['ID']] != {} and invest_date.date() < self.rule[budget['ID']]['to_date']:
                            self.rule[budget['ID']]['Amount'] += float(invest['Amount'])
                            if self.rule[budget['ID']]['Amount'] > float(budget['Amount']):
                                self.rule[budget['ID']]['Amount'] -= float(invest['Amount'])
                                print(int(float(invest['ID'])))                                                        
                                break
                        else:
                            self.rule[budget['ID']]['from_date'] = invest_date.date()
                            self.rule[budget['ID']]['to_date'] = invest_date.date() + relativedelta(
                                months=+ self.time.get(budget['Time Period'], 0))
                            self.rule[budget['ID']]['Amount'] = float(invest['Amount'])
                    else:
                        print(int(float(invest['ID'])))                                                               
                        break


if __name__ == '__main__':
    budget_file = input()                                           
    investment_file = input()                                      
    budget = BudgetViolation(budget_file, investment_file)          
    budget.check_violation_investments()                           