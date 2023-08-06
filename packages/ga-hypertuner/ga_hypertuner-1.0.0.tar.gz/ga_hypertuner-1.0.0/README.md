# GA Hypertuner

GA_HyperTuner is a Python package designed to help users fine-tune hyperparameters for their machine learning models using a genetic algorithm approach

## Features
Users can easily specify the hyperparameters they want to optimize, define the range and constraints for each hyperparameter, and set up the genetic algorithm parameters such as population size, combination probability, and mutation rates.

The package offers an intuitive interface that allows users to easily monitor the progress of the optimization process and visualize the results. With GA_HyperTuner, users can save a lot of time and effort that would otherwise be spent on manual hyperparameter tuning. 

By leveraging the power of genetic algorithm (Differential Evolution), GA_HyperTuner can help users find optimal hyperparameters for their models that lead to better accuracy and performance.

## Installation

Use pip to install ga_hypertuner.

```bash
pip install ga_hypertuner
```

## Usage

```python
from ga_hypertuner.tuner import Tuner
from sklearn import datasets
from sklearn.linear_model import LogisticRegression as lr
from xgboost import XGBRegressor as xgbr
##########################################################################
##########################################################################    
# Example 1
# loading data
x_train, y_train = datasets.load_iris(return_X_y=True, as_frame=True)

# creating model parameters, the solver and class_weight hyperparameters are static and won't change, the C parameter
# is the parameter that algorithm tries to optimize
model_parameters = {"solver": "liblinear", "class_weight": "balanced", "C": [None, float]}

# setting boundaries for parameter C
boundaries = {"C": [0, 1]}

# tuning the C parameter, the scoring criteria is accuracy.
# stratified cross validation is set to true and number of folds of cross validation is set to 3.
best_params = Tuner.tune(x_train, y_train, lr, Tuner.default_ga_parameters, model_parameters
           , boundaries, 'accuracy', stratified=True, k=3, verbosity=1)
           
##########################################################################
##########################################################################        
# Example 2
# loading data
x_train, y_train = datasets.load_diabetes(return_X_y=True, as_frame=True)

# setting genetic algorithm parameters
ga_parameters = {"pop_size": 15, "fscale": 0.6, "gmax": 200, "direction": "max", "cp": 0.6}

# setting xgboost model parameters
model_parameters = {"eta": [None, float], "min_child_weight": [None, float], "colsample_bytree": [None, float],
                    "n_estimators": 100, "alpha": [None, float], "gamma": [None, float]}

# setting boundaries for parameters
boundaries = {"eta": [0, 1], "min_child_weight": [0, 5], "colsample_bytree": [0, 1],
              "alpha": [0, 1], "gamma": [0, 1]}

# tuning parameters, a progress plot will be displayed every 10 generation
best_params = Tuner.tune(x_train, y_train, xgbr, ga_parameters, model_parameters
           , boundaries, 'r2', k=3, verbosity=3, show_progress_plot=True, plot_step=10)
##########################################################################
##########################################################################    
```
for more examples and info please refer to doc.

## Documentation

you can find tron_explorer [doc here](https://tron-explorer.readthedocs.io/en/latest/).

## Contributing

Any contribution is welcome. please open an issue to discuss changes or improvements.

## License

[MIT](https://github.com/AmiraliOmidvar/tron_explorer/blob/master/LICENCE.txt)
