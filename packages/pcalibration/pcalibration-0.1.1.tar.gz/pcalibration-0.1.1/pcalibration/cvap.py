import numpy as np

from scipy.stats import gmean
from sklearn.model_selection import StratifiedKFold
from pcalibration.ivap import InductiveVennAbers


class CrossVennAbers:
    """
    Cross Venn Abers Predictor (CVAP) algorithm
    
    Ref: https://arxiv.org/abs/1511.00213
    """
    
    def __init__(self, k: int = 5):
        self.k = k
        self.calibrators = []
        
    def fit(self, X: np.ndarray, y: np.ndarray):
        """
        Fit the model
        
        Args:
            X: input data
            y: target data
        """

        kf = StratifiedKFold(n_splits=self.k)
        for train_index, _ in kf.split(X, y):
            X_train, y_train = X[train_index], y[train_index]
            
            ivap = InductiveVennAbers()
            ivap.fit(X_train, y_train)
            
            self.calibrators.append(ivap)
            
    def predict_proba(self, X: np.ndarray, info: bool = False) -> np.ndarray:
        """
        Predict the calibrated probability
        
        Args:
            X: predicted scores
            info: whether to return additional information
            
        Returns:
            calibrated probability
        """
        
        P0 = []
        P1 = []
        for k, calibrator in enumerate(self.calibrators):
            prob, i = calibrator.predict_proba(X, info=True)
            P0K = i["P0"]
            P1K = i["P1"]
            
            P0.append(P0K)
            P1.append(P1K)
            
        P0 = np.concatenate(P0, axis=1)
        P1 = np.concatenate(P1, axis=1)
        
        prob1 = gmean(P1, axis=1) / (gmean(1 - P0, axis=1) + gmean(P1, axis=1))
        prob0 = 1 - prob1
        prob = np.stack((prob0, prob1), axis=1)
        
        if not info:
            return prob
        
        return prob, dict(P0=P0, P1=P1)
        