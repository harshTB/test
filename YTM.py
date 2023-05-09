import pandas as pd
from scipy import optimize
import numpy_financial as npf
from datetime import date

def bondPrice(faceValue,coupon,daysUntilMaturity,daysBetweenCoupon,ytm):
    pv=(faceValue+coupon)/((1+ytm)**(daysUntilMaturity/365))
    daysUntilMaturity-=daysBetweenCoupon
    while daysUntilMaturity>0:
        pv+=coupon/((1+ytm)**(daysUntilMaturity/365))
        daysUntilMaturity-=daysBetweenCoupon
    return(pv)

file= pd.read_excel("Debt_TB2.xlsx", sheet_name=1)
todayDate=file.iloc[1,4]
debtPortfolio = file.iloc[4:,2:]
debtPortfolio.columns = ['S.No.','ISIN','SecurityName','InstrumentType','Maturity','Price','Yield','ModifiedDuration','Rating','RatingChange','ValuationTriggered','TriggerDate','FaceValue','MacaulayDuration','Period']
ytms=[]
for index, row in debtPortfolio.iterrows():
    price=row['Price']
    yld=row['Yield']
    period=row['Period']
    par=row['FaceValue']
    timeToMaturity=(row['Maturity']-todayDate).days
    print(timeToMaturity)
    get_yield= lambda int_rate: bondPrice(par,yld*par*period*30/365,timeToMaturity,period*30,int_rate) - price
    ytm=optimize.newton(get_yield, yld)
    ytms.append(ytm)
debtPortfolio['ytm']=ytms
print(debtPortfolio)
print(ytms)
debtPortfolio.to_csv("YTM.csv")