import numpy as np


class CalibratorWrapper:
    """
    Wrapper for calibrator
    
    Args:
        base_model: base model instance
        calibrator: calibrator instance
    """
    
    def __init__(self, base_model, calibrator):
        self.base_model = base_model
        self.calibrator = calibrator
    
    def fit(self, X: np.ndarray, y: np.ndarray):
        """
        Fit the model
        
        Args:
            X: input data
            y: target data
        """
        
        self.base_model.fit(X, y)
        y_prob = self.base_model.predict_proba(X)[:, 1]
        self.calibrator.fit(y_prob, y)
        
    def predict_proba(self, X: np.ndarray, info: bool = False) -> np.ndarray:
        """
        Predict the calibrated probability
        
        Args:
            X: input data
            info: whether to return additional information
            
        Returns:
            calibrated probability
        """
        
        y_prob = self.base_model.predict_proba(X)[:, 1]
        y_prob_calibrated = self.calibrator.predict_proba(y_prob, info)
        
        return y_prob_calibrated
