import numpy as np


def simulate_soil_moisture(field_capacity: float,
                           wilting_point: float,
                           threshold: float,
                           irrigation_rate: float,
                           et_rate: float,
                           theta0: float,
                           t_end: float,
                           dt: float) -> dict:
    """
    Simula la dinámica de la humedad del suelo con riego automático y balance hídrico.

    Parámetros:
      field_capacity: capacidad de campo (máx. humedad en fracción [0-1])
      wilting_point: punto de marchitez (mín. humedad en fracción [0-1])
      threshold: umbral de humedad para activar riego (fracción)
      irrigation_rate: aporte de agua al regar (mm/h)
      et_rate: evapotranspiración constante (mm/h)
      theta0: humedad inicial (fracción)
      t_end: tiempo total simulación (h)
      dt: paso temporal (h)

    Retorna:
      dict con arrays 't', 'theta', 'events', 'balance'
    """
    # Validación de rangos básicos
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
        # evapotranspiración
        et = et_rate * dt
        delta = -et
        # activar riego si bajo umbral
        if theta[i-1] <= threshold:
            irr = irrigation_rate * dt
            delta += irr
            rain_events[i] = True
        # actualizar balance
        cum_balance += irr - et
        balance[i] = cum_balance
        # actualizar humedad y recortar
        theta[i] = np.clip(theta[i-1] + delta, wilting_point, field_capacity)

    return {'t': t, 'theta': theta, 'events': rain_events, 'balance': balance}