import numpy.random as npr
import numpy as np
import matplotlib.pyplot as plt

def wiener_process(dt=0.1, x0=0, n=1000):

    W = np.zeros(n+1)
    t = np.linspace(x0, n, n+1)

    W[1:n+1] = np.cumsum(np.random.normal(0, np.sqrt(dt), n))

    return t,W

def plot_process(t,W):
    plt.plot(t,W)
    plt.xlabel('Time(t)')
    plt.ylabel('Wiener-process W(t)')
    plt.title('Wiener-process')
    plt.show()

def simulate_geometric_random_walk(S0, T=2, N=1000, mu=0.1, sigma=0.05):
    dt = T/N
    t = np.linspace(0, T, N)
    W = np.random.standard_normal(size=N)
    W = np.cumsum(W)*np.sqrt(dt)

    X = (mu - 0.5*sigma**2)*t+sigma*W
    S = S0*np.exp(X)

    return t,S

def plot_simulation(t,S):
    plt.plot(t,S)
    plt.xlabel('Time(t)')
    plt.ylabel('Stock Price S(t)')
    plt.title('Geometric-Browmain Motion')
    plt.show()

if __name__ == '__main__':
    
    # time, data = wiener_process()
    time, data = simulate_geometric_random_walk(10)
    plot_simulation(time,data)