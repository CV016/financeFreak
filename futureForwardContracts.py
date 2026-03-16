import numpy as np

class ForwardFutureContract:

    def __init__(self,spot_price,risk_free_rate,maturity,position="long",delivery_price=None):

        self.S = spot_price
        self.r = risk_free_rate
        self.T = maturity
        self.position = position.lower()
        self.K = delivery_price

    # forward price = futures price , when there are no dividends or storage costs

    def forward_price(self):
        return self.S*np.exp(self.r*self.T)

    # futures and forwards are linear instrument so short = -(long)
    def contract_value(self):

        if self.K is None:
            raise ValueError('Delivery Price K is not defined')

        V = self.S - self.K*np.exp(-self.r*self.T) # using a simplied formula and not simulating random walk for the current time variable t.

        if self.position == 'short':
            V = -V 

        return V


contract = ForwardFutureContract(
    spot_price = 100,
    risk_free_rate = 0.05,
    maturity = 1,
    position = 'long',
    delivery_price = 105
)

print(f"Futures price: ${contract.forward_price():.2f}")
print(f"Contract price: ${contract.contract_value():.2f}")