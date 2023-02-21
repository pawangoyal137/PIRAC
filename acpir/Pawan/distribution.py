import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.use('tkagg')

from scipy.optimize import curve_fit
from scipy.special import factorial
from scipy.stats import expon

class Server():
    def __init__(self):
        self.counter = 0

    def increment(self):
        self.counter+=1

class User():
    def __init__(self):
        self.counters = []
    
    def make_request(self, counter):
        return self.counters.append(counter)

def simulation(users, N):
    user_dict = {}
    for i in range(users):
        user_dict[i] = User()
    
    for i in range(N):
        user = np.random.randint(0, users)
        user_dict[user].make_request(i)
    
    dis = []
    for i in range(users):
        for j in range(len(user_dict[i].counters)-1):
            dis.append(user_dict[i].counters[j+1]-user_dict[i].counters[j])
    
    fit_poisson(dis)


# def fit_function(k, lamb):
#     '''poisson function, parameter lamb is the fit parameter'''
#     return poisson.pmf(k, lamb)

def fit_poisson(data):

    # # the bins should be of integer width, because poisson is an integer distribution
    # bins = np.arange(11) - 0.5
    # entries, bin_edges, patches = plt.hist(data, bins=bins, density=True, label='Data')

    # # calculate bin centers
    # bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])

    # # fit with curve_fit
    # parameters, cov_matrix = curve_fit(fit_function, bin_centers, entries)

    # # plot poisson-deviation with fitted parameter
    # x_plot = np.arange(0, 15)

    # plt.plot(
    #     x_plot,
    #     fit_function(x_plot, *parameters),
    #     marker='o', linestyle='',
    #     label='Fit result',
    # )
    # plt.show()


    #MLE
    fitted_parameters = expon.fit(data)
    print(fitted_parameters)

    #plotting
    rX = np.linspace(0,max(data), 400)
    rP = expon.pdf(rX, *fitted_parameters)
 
    #need to plot the normalized histogram with `normed=True`
    plt.hist(data, np.arange(0,max(data),step=1), density=True)
    plt.plot(rX, rP)

    plt.show()

simulation(50, 10000)