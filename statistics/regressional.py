import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import linregress
import matplotlib.pyplot as plt

current_path = "temp_vs_dsi.npy"
x, y = np.load(current_path, allow_pickle=True)

def linear_regression(x, y):
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    return {
        'model': 'Linear Regression',
        'slope': slope,
        'intercept': intercept,
        'r_value': r_value,
        'p_value': p_value,
        'std_err': std_err
    }

def polynomial_regression(x, y, degree):
    coefficients = np.polyfit(x, y, degree)
    return {
        'model': f'Polynomial Regression (degree {degree})',
        'coefficients': coefficients,
        'p_value': None
    }

def exponential_regression(x, y):
    def model(x, a, b):
        return a * np.exp(b * x)
    params, _ = curve_fit(model, x, y, p0=(1, 0.1), maxfev=10000)
    return {
        'model': 'Exponential Regression',
        'a': params[0],
        'b': params[1],
        'p_value': None
    }

def logarithmic_regression(x, y):
    def model(x, a, b):
        return a + b * np.log(x)
    params, _ = curve_fit(model, x, y, p0=(1, 1), maxfev=10000)
    return {
        'model': 'Logarithmic Regression',
        'a': params[0],
        'b': params[1],
        'p_value': None
    }

def power_law_regression(x, y):
    def model(x, a, b):
        return a * np.power(x, b)
    params, _ = curve_fit(model, x, y, p0=(1, 1), maxfev=10000)
    return {
        'model': 'Power-Law Regression',
        'a': params[0],
        'b': params[1],
        'p_value': None
    }

def logistic_regression(x, y):
    def model(x, L, k, x0):
        return L / (1 + np.exp(-k * (x - x0)))
    params, _ = curve_fit(model, x, y, p0=(max(y), 1, np.median(x)), maxfev=10000)
    return {
        'model': 'Logistic Regression',
        'L': params[0],
        'k': params[1],
        'x0': params[2],
        'p_value': None
    }

def quadratic_regression(x, y):
    coefficients = np.polyfit(x, y, 2)
    return {
        'model': 'Quadratic Regression',
        'a': coefficients[0],
        'b': coefficients[1],
        'c': coefficients[2],
        'p_value': None
    }

def cubic_regression(x, y):
    coefficients = np.polyfit(x, y, 3)
    return {
        'model': 'Cubic Regression',
        'a': coefficients[0],
        'b': coefficients[1],
        'c': coefficients[2],
        'd': coefficients[3],
        'p_value': None
    }

def display_results(results):
    print("\n========================")
    print(f"Model: {results['model']}")
    for key, value in results.items():
        if key != 'model':
            print(f"{key}: {value}")
    print("========================\n")

def plot_regressions(x, y):
    plt.scatter(x, y, label="Data", color="black")

    # Linear Regression
    lin_res = linear_regression(x, y)
    lin_y = lin_res['slope'] * x + lin_res['intercept']
    plt.plot(x, lin_y, label=f"Linear (R={lin_res['r_value']:.2f})", linestyle='--')

    # Polynomial Regression
    poly_res = polynomial_regression(x, y, degree=2)
    poly_y = np.polyval(poly_res['coefficients'], x)
    plt.plot(x, poly_y, label="Polynomial (deg 2)")

    # Exponential Regression
    exp_res = exponential_regression(x, y)
    exp_y = exp_res['a'] * np.exp(exp_res['b'] * x)
    plt.plot(x, exp_y, label="Exponential")

    # Logarithmic Regression
    log_res = logarithmic_regression(x, y)
    log_y = log_res['a'] + log_res['b'] * np.log(x)
    plt.plot(x, log_y, label="Logarithmic")

    # Power-Law Regression
    power_res = power_law_regression(x, y)
    power_y = power_res['a'] * np.power(x, power_res['b'])
    plt.plot(x, power_y, label="Power-Law")

    # Logistic Regression
    logis_res = logistic_regression(x, y)
    logistic_y = logis_res['L'] / (1 + np.exp(-logis_res['k'] * (x - logis_res['x0'])))
    plt.plot(x, logistic_y, label="Logistic")

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.title("Regression Models")
    plt.xlim(0, 1)
    plt.ylim(0.775, 0.84)
    plt.show()

# Perform regressions and display results
display_results(linear_regression(x, y))
display_results(polynomial_regression(x, y, degree=2))
display_results(exponential_regression(x, y))
display_results(logarithmic_regression(x, y))
display_results(power_law_regression(x, y))
display_results(logistic_regression(x, y))
display_results(quadratic_regression(x, y))
display_results(cubic_regression(x, y))

# Plot regressions
plot_regressions(x, y)
