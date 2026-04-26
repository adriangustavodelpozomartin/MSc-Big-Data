"""
This module gathers useful auxiliary functions for ML2 (regression).
"""

# Authors: Eugenio Sánchez Úbeda <eugenio.sanchez@comillas.edu>
# Date: January 2025


def plot_histogram_residuals_tr_ts(name_model, y_train, y_train_est, y_test, y_test_est, mse_tr, mse_ts):

    # Plot histogram of residuals
    plt.figure(figsize=(15, 12))

    ax=plt.subplot(3,1,2)
    plt.hist(y_train - y_train_est, bins = 40, label='Residuals training set')
    plt.grid()
    plt.title(f'{name_model}:: Residuals training set (y_real - y_est)  MSE(TR) = {mse_tr}')

    plt.subplot(3,1,3, sharex = ax)
    plt.hist(y_test - y_test_est, bins = 40, label='Residuals training set')
    plt.grid()
    plt.title(f'{name_model}:: Residuals test set (y_real - y_est) MSE(TS) = {mse_ts}')
    plt.show()

    return