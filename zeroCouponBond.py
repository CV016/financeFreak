class ZeroCouponBond:

    def __init__(self,principal,maturity,interest_rate):

        self.principal = principal
        self.maturity = maturity
        self.interest_rate = interest_rate / 100

    # discrete model
    def present_value(self,amount,period):
        return amount/(1+self.interest_rate)**period

    def calculate_price(self):
        return self.present_value(self.principal,self.maturity)

    
if __name__ == '__main__':

    bond = ZeroCouponBond(1000,2,4)
    print(bond.calculate_price())

    

    