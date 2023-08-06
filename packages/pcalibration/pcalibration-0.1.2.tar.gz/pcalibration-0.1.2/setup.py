# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pcalibration']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.7.1,<4.0.0', 'scikit-learn>=1.2.1,<2.0.0']

setup_kwargs = {
    'name': 'pcalibration',
    'version': '0.1.2',
    'description': '',
    'long_description': '# probability-calibration\n\nProbability calibration is a technique to calibrate the probabilities of a classifier. This package provides a simple interface to calibrate the probabilities of a sklearn-stype classifier. The package also provides a set of calibration methods.\n\n## Methods\n\n- Platt Scaling\n- Isotonic Regression\n- Inductive Venn-Abers Predictor (IVAP)\n- Cross Venn-Abers Predictor (CVAP)\n\n## Installation\n\n```zsh\n$ pip install pcalibration\n```\n\n## Usage\n\n```python\nfrom pcalibration import CalibratorWrapper, CrossVennAbers\n\n# Load the data\nX_train, X_test, y_train, y_test = ...\n\n# Create a CalibratorWrapper object\ncalibrator = CalibratorWrapper(model, CrossVennAbers(k=5))\n\n# Fit the calibrator\ncalibrator.fit(X_train, y_train)\n\n# Predict the probabilities\ny_pred = calibrator.predict_proba(X_test)\n```\n',
    'author': 'nutorbit',
    'author_email': 'nutorbitx@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
