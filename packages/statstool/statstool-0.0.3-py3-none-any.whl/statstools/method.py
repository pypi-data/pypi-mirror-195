import numpy as np
import statsmodels.api as sm
from collections import namedtuple

def my_OLS(Y, X, names=[]):
    if names == []:
        for i in range(np.shape(X)[1]):
            names.append('x'+str(i))
            
    my_OLS_Wrapper = namedtuple('my_OLS_Wrapper', ['Coeffs', 'Fitted', 'Resids', 'Stats'])
    Coeff_Info = namedtuple('Coeff_Info', ['beta', 'tval', 'pval'])
    
    X_t = np.transpose(X)
    XX_t = np.matmul(X_t, X)
    inv_XX_t = np.linalg.inv(XX_t)
    sol = np.matmul(inv_XX_t, X_t)
    coeffs = np.matmul(sol, Y)
    
    fitted = np.matmul(X, coeffs)
    resids = np.subtract(Y, fitted)
    
    num_t = np.shape(Y)[1]
    beta_arr = np.empty((np.shape(X)[1], num_t))
    tval_arr = np.empty((np.shape(X)[1], num_t))
    pval_arr = np.empty((np.shape(X)[1], num_t))
    adjR_arr = np.empty((num_t))
    llike_arr = np.empty((num_t))
    AIC_arr = np.empty((num_t))
    for t in range(num_t):
        ols_fit = sm.OLS(Y[:,t], X).fit()
        beta_arr[:,t] = ols_fit.params
        tval_arr[:,t] = ols_fit.tvalues
        pval_arr[:,t] = ols_fit.pvalues
        adjR_arr[t] = ols_fit.rsquared_adj
        llike_arr[t] = ols_fit.llf
        AIC_arr[t] = ols_fit.aic
        
    coeffs_dict = {'coeffs_arr': coeffs}
    for i in range(len(names)):
        coeffs_dict[names[i]] = Coeff_Info(beta_arr[i], tval_arr[i], pval_arr[i])
        
    stats_dict = {'adj_Rsqr': adjR_arr, 'log_like': llike_arr, 'AIC': AIC_arr}
    
    my_ols_wrapper = my_OLS_Wrapper(coeffs_dict, fitted, resids, stats_dict)
    
    return my_ols_wrapper
