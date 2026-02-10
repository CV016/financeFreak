class couponBonds:

    def __init__(self,principal,rate,maturity,interest_rate):
        self.principal = principal
        self.rate = rate / 100
        self.maturity = maturity
        self.interest_rate = interest_rate / 100

    # discrete model
    def present_value(self,amount,period):
        return amount / (1+self.interest_rate)**period

    def calculate_price(self):
         
        price = 0
        
        for t in (1,self.maturity+1):
            price = price + self.present_value(self.principal*self.rate,t)

        price = price + self.present_value(self.principal,self.maturity)

        return price

if __name__ == '__main__':

    bond = couponBonds(1000,10,3,4)
    print(bond.calculate_price())
    

    
    