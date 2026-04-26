"""
This module gathers useful auxiliary functions for ML2 (classification).
"""

# Authors: Eugenio Sánchez Úbeda <eugenio.sanchez@comillas.edu>
# Date: September 2024

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import seaborn as sns

from sklearn.metrics import confusion_matrix
from sklearn.base import clone
from sklearn.inspection import DecisionBoundaryDisplay
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.utils.multiclass import unique_labels


# smaller figures
plt.rcParams['figure.dpi'] = 75

# set of functions

def compute_expanded_confusion_matrix(clf, X, y):

    """By definition a confusion matrix :math:`C` is such that :math:`C_{i, j}`
    is equal to the number of observations known to be in group :math:`i` and
    predicted to be in group :math:`j`.

    Thus in binary classification, the count of true negatives is
    :math:`C_{0,0}`, false negatives is :math:`C_{1,0}`, true positives is
    :math:`C_{1,1}` and false positives is :math:`C_{0,1}`.
    """

    # Predict output using the classification model
    y_pred = clf.predict(X)


    # labels (can be less than expected)
    labels = unique_labels(y, y_pred)

    # Compute confusion matrix and obtain main diagonal
    conf_matrix = confusion_matrix(y, y_pred, labels=labels)
    diag_conf_matrix = np.diagonal(conf_matrix)

    # Create dataframe to prepare final matrix
    expanded_conf_matrix_df = pd.DataFrame(conf_matrix, index=labels , columns=labels).T

    # Add column first and then the new row
    expanded_conf_matrix_df['ALL'] = conf_matrix.sum(axis=0)
    expanded_conf_matrix_df.loc['ALL'] = np.append(conf_matrix.sum(axis=1),  conf_matrix.sum(axis=1).sum())

    # Normalize the matrix (%)
    conf_matrix_prtge = 100 * conf_matrix / np.sum(conf_matrix)

    # Create dataframe to prepare final matrix
    expanded_conf_matrix_prtge_df = pd.DataFrame(conf_matrix_prtge, index=labels , columns=labels).T

    # Add column first and then the new row
    expanded_conf_matrix_prtge_df.loc['ALL'] = 100 * diag_conf_matrix / conf_matrix.sum(axis=1)
    expanded_conf_matrix_prtge_df['ALL'] = np.append(100 * diag_conf_matrix / conf_matrix.sum(axis=0), 
                                                     100 * np.sum(diag_conf_matrix) / np.sum(conf_matrix))
  
    return expanded_conf_matrix_df, expanded_conf_matrix_prtge_df


def plot_expanded_confusion_matrix(clf, X_train, y_train, X_test, y_test):

    conf_matrix_train_df, conf_matrix_prtge_train_df = compute_expanded_confusion_matrix(clf, X_train, y_train)
    conf_matrix_test_df, conf_matrix_prtge_test_df = compute_expanded_confusion_matrix(clf, X_test, y_test)

    # plot
    plt.figure(figsize=(13, 8))

    ax = plt.subplot(2,2,1)
    sns.heatmap(conf_matrix_train_df, annot=True, fmt='g', cmap='viridis', ax = ax)
    plt.ylabel('Output class (Predicted label)')
    plt.title ('TRAINING SET')

    ax = plt.subplot(2,2,2)
    sns.heatmap(conf_matrix_test_df, annot=True, fmt='g', cmap='viridis', ax = ax)
    plt.title ('TEST SET')

    ax = plt.subplot(2,2,3)
    sns.heatmap(conf_matrix_prtge_train_df/100, annot=True, fmt=".1%", cmap='viridis', ax = ax)
    plt.title ('TRAINING SET (%)')
    plt.xlabel('Target class (True label)')
    plt.ylabel('Output class (Predicted label)')

    ax = plt.subplot(2,2,4)
    sns.heatmap(conf_matrix_prtge_test_df/100, annot=True, fmt=".1%", cmap='viridis', ax = ax)
    plt.title ('TEST SET (%)')
    plt.xlabel('Target class (True label)')
    return

def compute_prunning_sequence(model, X_train, y_train, X_test, y_test):

    # generate the path of cost complexity alphas
    path = model.cost_complexity_pruning_path(X_train, y_train, sample_weight=None)

    # for each alpha, build the corresponding tree and compute main metrics
    ccp_alphas, impurities = path.ccp_alphas, path.impurities

    # ccp_alpha must be [0, inf]
    ccp_alphas[ccp_alphas < 0] = 0

    # clfs = []
    numbers_of_nodes=[]
    depths=[]
    errors_training=[]
    errors_test=[]

    for ccp_alpha in ccp_alphas:
        clf = clone(model) # copy hyperparams
        clf.ccp_alpha = ccp_alpha
        clf.fit(X_train, y_train)
        
        # clfs.append(clf) # save the list of all the trees (memory warning ...)

        # emtrics for this tree
        numbers_of_nodes.append(clf.tree_.node_count)
        depths.append(clf.tree_.max_depth)
        errors_training.append(1-clf.score(X_train, y_train))
        errors_test.append(1-clf.score(X_test, y_test))

    # select only ccp_alphas with different number of nodes (i.e. different trees)
    numbers_of_nodes_u, indices = np.unique(numbers_of_nodes, return_index=True)

    depths_u = np.array(depths)[indices.astype(int)]
    errors_training_u = np.array(errors_training)[indices.astype(int)]
    errors_test_u = np.array(errors_test)[indices.astype(int)]
    ccp_alphas_u = np.array(ccp_alphas)[indices.astype(int)]

    # remove complex trees with the same TR error to avoid non-effective cuts
    errors_training_u, indices = np.unique(errors_training_u, return_index=True)

    depths_u = np.array(depths_u)[indices.astype(int)]
    numbers_of_nodes_u = np.array(numbers_of_nodes_u)[indices.astype(int)]
    errors_test_u = np.array(errors_test_u)[indices.astype(int)]
    ccp_alphas_u = np.array(ccp_alphas_u)[indices.astype(int)]


    levels_of_prune_u = np.array(range(len(numbers_of_nodes_u),0,-1))


    # save prunning sequence in a dictionary
    prunning_sequence = {"level_of_prune": levels_of_prune_u,
                         "number_of_nodes": numbers_of_nodes_u,
                         "depth": depths_u,
                         "error_training": errors_training_u,
                         "error_test": errors_test_u,
                         "ccp_alpha": ccp_alphas_u,
                        }

    # print(pd.DataFrame.from_dict(prunning_sequence))

    return prunning_sequence


def plot_prunning_sequence(prunning_sequence):

    # obtain the complexity where the error in TS is minimum
    index_min_error_test = np.argmin(prunning_sequence['error_test'])
    level_optim = prunning_sequence['level_of_prune'][index_min_error_test]

    # plot the error curves
    fig = plt.figure(2,figsize=(15,6))
    plt.plot(prunning_sequence['level_of_prune'], prunning_sequence['error_training'], '.-b', label='Error in TR')
    plt.plot(prunning_sequence['level_of_prune'], prunning_sequence['error_test'], '.-r', label='Error in TS')
    plt.plot(level_optim, prunning_sequence['error_test'][index_min_error_test], 'ks', alpha = 0.5, label=f'Min Error in TS (level: {level_optim})')
    plt.grid()
    plt.title('Error curves')
    plt.xlabel('Pruning level (1 node - full tree)')
    plt.ylabel('Error (1 - accuracy)')
    plt.legend()
    plt.show()
    return


def plot_zoom_prunning_sequence(prunning_sequence, min_level, max_level, show_table):

    # zoom in the region of interest selected by min y max complexity

    # check correct values of zoom
    if min_level < 0 or min_level > len(prunning_sequence['level_of_prune']):
        raise ValueError(f"Invalid min level for zoom: {min_level}. Minimum level must be between {0} and {len(prunning_sequence['level_of_prune'])}.")

    if max_level < 0 or max_level > len(prunning_sequence['level_of_prune']):
        raise ValueError(f"Invalid max level for zoom:{max_level}. Maximum level must be between {0} and {len(prunning_sequence['level_of_prune'])}.")
    
    # obtain the complexity where the error in TS is minimum
    index_min_error_test = np.argmin(prunning_sequence['error_test'])
    level_optim = prunning_sequence['level_of_prune'][index_min_error_test]

    # plot the error curves
    fig = plt.figure(2,figsize=(15,6))
    plt.plot(prunning_sequence['level_of_prune'], prunning_sequence['error_training'], '.-b', label='Error in TR')
    plt.plot(prunning_sequence['level_of_prune'], prunning_sequence['error_test'], '.-r', label='Error in TS')
    plt.plot(level_optim, prunning_sequence['error_test'][index_min_error_test], 'ks', alpha = 0.5, label=f'Min Error in TS (level: {level_optim})')
    plt.grid()
    plt.title('Error curves (zoom)')
    plt.xlabel('Pruning level')
    plt.ylabel('Error (1 - accuracy)')
    
    # zoom
    plt.xlim([min_level, max_level])
    plt.legend()
    plt.show()

    # show the pruning seq. in a table
    if show_table:
        table = pd.DataFrame(prunning_sequence).loc[(prunning_sequence['level_of_prune']>=min_level) & (prunning_sequence['level_of_prune'] <=max_level)]
        print(table.drop(columns=['depth', 'ccp_alpha'])[::-1].to_string(index=False))
    
    return

def plot_input_space_partition(model, X_train, show_training_data=True):
         
    # obtain inputs from model
    inputs = model.feature_names_in_

    if len(inputs) != 2:
        raise ValueError(f"Invalid model for this plot: number of inputs is {len(inputs)}. Number of input vars must be 2.")

    colors = ['yellow', 'green', 'red', 'blue']
    dic_colors = {'AUTUMN': 'yellow', 'SPRING': 'green', 'SUMMER': 'red', 'WINTER': 'blue'}

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # plot the means to set a valid legend
    yest = model.predict(X_train)
    X_train_yest = X_train.copy()
    X_train_yest['yest'] = yest
    means = X_train_yest.groupby('yest').first()
    outputs = np.unique(yest)

    # colormap for the existing outputs
    if len(outputs) == 3:
        colors_new = colors.copy()
        colors_new[0] = dic_colors[outputs[0]]
        colors_new[2] = dic_colors[outputs[1]]
        colors_new[3] = dic_colors[outputs[2]]
        cmap = ListedColormap(colors_new)      
    else:
        cmap = ListedColormap([dic_colors[key] for key in outputs])
    
    
    for output in outputs:
        ax1.plot(means.loc[output,inputs[0]],  means.loc[output,inputs[1]], 's', 
                 color = dic_colors[output], label = output)

    # plt.figure(figsize=(15, 6))
    DecisionBoundaryDisplay.from_estimator(
        model,
        X_train,
        xlabel=inputs[0],
        ylabel=inputs[1],
        cmap=cmap,
        plot_method='pcolormesh',
        response_method='predict',
        alpha=1,
        grid_resolution=400,
        ax = ax1,
    )

    ax1.legend()
    ax1.grid()

    for output in outputs:
        ax2.plot(means.loc[output,inputs[0]],  means.loc[output,inputs[1]], 's', 
                 color = dic_colors[output], label = output)

    DecisionBoundaryDisplay.from_estimator(
        model,
        X_train,
        xlabel=inputs[0],
        ylabel=inputs[1],
        cmap=cmap,
        plot_method='pcolormesh',
        response_method='predict',
        alpha=1,
        grid_resolution=400,
        ax = ax2,
    )

    ax2.plot(X_train[inputs[0]], X_train[inputs[1]], '.k', alpha=1, label='TR data')
    ax2.legend()
    ax2.grid()

    return