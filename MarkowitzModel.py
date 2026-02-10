import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import scipy.optimize as optimization
import yfinance as yf

NUM_TRADING_DAYS = 252
NUM_PORTFOLIOS = 10000
stocks = ['AAPL','WMT','TSLA','AMZN','GE']

start_date = '2020-01-01'
end_date = '2025-01-01'

def downloadData():

    stock_data = {}

    for stock in stocks:

        ticker = yf.Ticker(stock)
        stock_data[stock] = ticker.history(start=start_date,end=end_date)['Close']

    return pd.DataFrame(stock_data)

def show_data(data):
    
    data.plot(figsize = (10,5))
    plt.show()

def calculate_return(data):

    log_return = np.log(data/data.shift(1)) # [s(t)/s(t-1)]
    return log_return[1:]

def show_statistics(returns):
    
    print(returns.mean()*NUM_TRADING_DAYS)
    print(returns.cov()*NUM_TRADING_DAYS)

def show_mean_variance(returns,weights):

    # These are the annual return and volatility 
    portfolio_return = np.sum(returns.mean()*weights)*NUM_TRADING_DAYS
    portfolio_volatility = np.sqrt(np.dot(weights.T,np.dot(returns.cov()*NUM_TRADING_DAYS,weights)))

    print(portfolio_return)
    print(portfolio_volatility)

def show_portfolios(returns,volatilites):
    plt.figure(figsize=(10,6))
    plt.scatter(volatilites,returns,c=returns/volatilites,marker='o')
    plt.grid(True)
    plt.xlabel('Expected Volatility')
    plt.ylabel('Expected Return')
    plt.colorbar(label='Sharpe Ratio')
    plt.show()

def generate_portfolio(returns):

    portfolio_means = []
    portfolio_risks = []
    portfolio_weights = []

    for _ in range(NUM_PORTFOLIOS):
        w = np.random.random(len(stocks))
        w /= np.sum(w)
        portfolio_weights.append(w)
        portfolio_means.append(np.sum(returns.mean()*w)*NUM_TRADING_DAYS)
        portfolio_risks.append(np.sqrt(np.dot(w.T,np.dot(returns.cov()*NUM_TRADING_DAYS,w))))

    return np.array(portfolio_weights), np.array(portfolio_means), np.array(portfolio_risks)

def statistics(weights,returns):
    
    portfolio_return = np.sum(returns.mean()*weights)*NUM_TRADING_DAYS
    portfolio_volatility = np.sqrt(np.dot(weights.T,np.dot(returns.cov()*NUM_TRADING_DAYS,weights)))

    # Assuming risk free investments will have zero returns
    return np.array([portfolio_return,portfolio_volatility,portfolio_return/portfolio_volatility])

def min_function_sharpe(weights,returns):
    return -statistics(weights,returns)[2]

def optimize_portfolio(weights,returns):

    constraints = {'type':'eq','fun':lambda x: np.sum(x)-1}
    bounds = tuple((0,1) for _ in range(len(stocks)))
    return optimization.minimize(fun=min_function_sharpe,x0=weights[0],args=returns,method='SLSQP',bounds=bounds,constraints=constraints)

def print_optimal_portfolio(optimum, returns):

    opt_weights = optimum['x']
    for i, stock in enumerate(stocks):
        print(f"{stock}: {opt_weights[i]:.4f} ({opt_weights[i]*100:.2f}%)")
    
    stats = statistics(opt_weights, returns)
    print(f"Expected Annual Return: {stats[0]:.4f}")
    print(f"Expected Volatility:    {stats[1]:.4f}")
    print(f"Sharpe Ratio:           {stats[2]:.4f}")

def show_portfolios(p_means, p_risks, returns, optimum):
    plt.figure(figsize=(10,6))
    
    plt.scatter(p_risks, p_means, c=p_means/p_risks, marker='o', cmap='viridis')
    plt.colorbar(label='Sharpe Ratio')
    
    opt_stats = statistics(optimum['x'], returns)
    
    plt.plot(opt_stats[1], opt_stats[0], 'g*', markersize=20.0, markeredgecolor='black', label='Max Sharpe Ratio')
    
    plt.grid(True)
    plt.xlabel('Expected Volatility')
    plt.ylabel('Expected Return')
    plt.title('Efficient Frontier & Optimal Portfolio')
    plt.legend()
    plt.show()

if __name__ == '__main__':

    dataset = downloadData()

    print("\n--- Individual Stock Performance ---")
    print(dataset.pct_change().mean() * NUM_TRADING_DAYS)

    print("\n--- Correlation Matrix ---")
    print(dataset.pct_change().corr())

    log_daily_returns = calculate_return(dataset)

    pweights, means, risks = generate_portfolio(log_daily_returns)
    optimum = optimize_portfolio(pweights, log_daily_returns)
    print_optimal_portfolio(optimum, log_daily_returns)
    show_portfolios(means, risks, log_daily_returns, optimum)

