import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

RISK_FREE_RATE = 0.05
MONTHS_IN_YEAR = 12

class CAPM:

    def __init__(self,stocks,start_date,end_date):
        
        self.data = None
        self.stocks = stocks
        self.start_date = start_date
        self.end_date = end_date

    def download_data(self):

        ticker = yf.download(
            self.stocks,
            start=self.start_date,
            end=self.end_date,
            auto_adjust=True
        )

        data = ticker['Close'] #Adj Close has now been adjusted to Close

        return data

    def initialize(self):

        stock_data = self.download_data()
        stock_data = stock_data.resample('ME').last()

        self.data = pd.DataFrame({'s_adjclose':stock_data[self.stocks[0]],'m_adjclose':stock_data[self.stocks[1]]})
        self.data[['s_return','m_return']] = np.log(self.data[['s_adjclose','m_adjclose']]/self.data[['s_adjclose','m_adjclose']].shift(1))

        self.data = self.data[1:]
        # print(self.data)

    def calculate_beta(self):

        covariance_matrix = np.cov(self.data['s_return'],self.data['m_return'])
        beta = covariance_matrix[0,1]/covariance_matrix[1,1]
        print('Beta from the Covariance Matrix:',beta)

    def regression(self):

        beta,alpha = np.polyfit(self.data['m_return'],self.data['s_return'],deg=1)
        print('Beta from regression:',beta)

        expected_return = RISK_FREE_RATE + beta*(self.data['m_return'].mean()*MONTHS_IN_YEAR - RISK_FREE_RATE)
        print('Expected return:',expected_return)

        # self.plot_regression(alpha,beta)

    # def plot_regression(self,alpha,beta): , also need to check if the returns are normally distributed can use np.hist() to plot histogram of logarithimic returns to check for it

if __name__ == '__main__':

    capm = CAPM(['IBM','^GSPC'],'2010-01-01','2020-01-01')
    capm.initialize()
    capm.calculate_beta()
    capm.regression()