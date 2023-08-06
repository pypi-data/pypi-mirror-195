from collections import namedtuple
import numpy as np
import mne
import statsmodels.api as sm

def rerp_ols(mne_epoch, X, pred_names=None):
    if pred_names == None:
        pred_names = []
        for i in range(np.shape(X)[1]):
            pred_names.append('x'+str(i))
            
    rERP_OLS_Wrapper = namedtuple('rERP_OLS_Wrapper', ['Coeffs', 'Fitted', 'Resids'])
    Coeffs_Info = namedtuple('Coeffs_Info', ['beta', 'tval', 'pval'])
    
    X_t = np.transpose(X)
    XX_t = np.matmul(X_t, X)
    inv_XX_t = np.linalg.inv(XX_t)
    
    data = mne_epoch.copy().get_data()
    num_ep = np.shape(data)[0]
    num_ch = np.shape(data)[1]
    num_t = np.shape(data)[2]
    
    coeffs = np.empty((np.shape(X)[1], num_ch, num_t))
    fitted = np.empty((num_ep, num_ch, num_t))
    resids = np.empty((num_ep, num_ch, num_t))
    
    for ch in range(num_ch):
        Y = data[:,ch,:]
        sol = np.matmul(inv_XX_t, X_t)
        coeffs[:,ch,:] = np.matmul(sol, Y)
        fitted[:,ch,:] = np.matmul(X, coeffs[:,ch,:])
        resids[:,ch,:] = np.subtract(Y, fitted[:,ch,:])
    
    beta_arr = np.empty((np.shape(X)[1], num_ch, num_t))
    tval_arr = np.empty((np.shape(X)[1], num_ch, num_t))
    pval_arr = np.empty((np.shape(X)[1], num_ch, num_t))
    
    rerp = mne.stats.linear_regression(mne_epoch, X, names=pred_names)
    for i in range(len(pred_names)):
        beta_arr[i] = rerp[pred_names[i]].beta.data
        tval_arr[i] = rerp[pred_names[i]].t_val.data
        pval_arr[i] = rerp[pred_names[i]].p_val.data
        
    coeffs_dict = {'coeffs_arr': coeffs}
    for i in range(len(pred_names)):
        coeffs_dict[pred_names[i]] = Coeffs_Info(beta_arr[i], tval_arr[i], pval_arr[i])
        
    rerp_ols_wrapper = rERP_OLS_Wrapper(coeffs_dict, fitted, resids)
    return rerp_ols_wrapper
