import numpy as np


def simulate_soil_moisture(field_capacity: float,
                           wilting_point: float,
                           threshold: float,
                           irrigation_rate: float,
                           et_rate: float,
                           theta0: float,
                           t_end: float,
                           dt: float) -> dict:
    if not (0 <= theta0 <= field_capacity <= 1):
        raise ValueError("Valores de humedad deben estar entre 0 y 1 y θ0 ≤ capacidad de campo")

    n_steps = int(np.ceil(t_end / dt)) + 1
    t = np.linspace(0, t_end, n_steps)
    theta = np.zeros(n_steps)
    rain_events = np.zeros(n_steps, dtype=bool)
    balance = np.zeros(n_steps)

    theta[0] = theta0
    cum_balance = 0.0
    for i in range(1, n_steps):
        irr = 0.0
        et = et_rate * dt
        delta = -et
        if theta[i-1] <= threshold:
            irr = irrigation_rate * dt
            delta += irr
            rain_events[i] = True
        cum_balance += irr - et
        balance[i] = cum_balance
        theta[i] = np.clip(theta[i-1] + delta, wilting_point, field_capacity)

    return {'t': t, 'theta': theta, 'events': rain_events, 'balance': balance}