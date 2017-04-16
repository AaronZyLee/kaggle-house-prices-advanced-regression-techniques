import pandas as pd 
import numpy as np
from sklearn.ensemble import ExtraTreesRegressor
from matplotlib import pyplot
import time
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error
import sys

folds = 7
seed = 7

model='et'

def rmse_cv(model, X_train, y_train):
    kfold = KFold(n_splits=folds, random_state=seed)
    rmse = np.sqrt(-cross_val_score(model, X_train, y_train, scoring="neg_mean_squared_error", cv = kfold))
    return(rmse)

def main(predictions = False):

    # ----------------------------------------------------------------------------

    data = pd.read_csv("./data/clean_dataset.csv")

    train = data.loc[data.set == 'train', data.columns.values[1:]]
    test = data.loc[data.set == 'test', data.columns.values[1:]]

    X_train = train.drop(['Id', 'SalePrice', 'logSalePrice', 'set'], axis=1)
    y_train = np.log1p(train['SalePrice'])

    X_test = test.drop(['Id', 'SalePrice', 'logSalePrice', 'set'], axis=1)

    # ----------------------------------------------------------------------------

    # build model
    model_et = ExtraTreesRegressor()

    # fit model
    model_et.fit(X_train, y_train)

    # evaluate model
    results = rmse_cv(model_et, X_train, y_train)
    print("RMSE-{}-CV({})={}+-{}".format(model, folds, results.mean(), results.std()))

    # # predict
    if predictions:
        y_test_pred_log = model_et.predict(X_test)
        y_test_pred = np.expm1(y_test_pred_log)
        submission = pd.DataFrame({'Id':test['Id'], 'SalePrice':y_test_pred})

        print(submission)
        submission.to_csv("./output/sub-et-11_04_2017.csv", index=False)

# ----------------------------------------------------------------------------


if __name__ == "__main__":
    savePredict = False
    if len(sys.argv) > 1:
        if sys.argv[1] == 'save':
            savePredict = True
    main(predictions = savePredict)