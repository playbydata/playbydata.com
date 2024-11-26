import numpy as np



__all__ = (
    "generate_white_noise",
    "generate_autoregressive1",
    "generate_ma1"
)


def generate_white_noise(n, std=1):
    mean = 0
    return np.random.normal(mean, std, size=n)


def generate_autoregressive1(n, a1, a0=0, noise_std=1):
    data = np.zeros(n)
    white_noise = generate_white_noise(n, std=noise_std)
    data[0] = white_noise[0]
    for i in range(1, len(data)):
        data[i] = a0 + a1*data[i-1] + white_noise[i]
    return data


def generate_ma1(n, a1, a0=0, noise_std=1):
    """
    Moving Average
    """
    data = np.zeros(n)
    white_noise = generate_white_noise(n, std=noise_std)
    data[0] = white_noise[0]
    for i in range(1, len(data)):
        data[i] = a0 + a1*white_noise[i-1] + white_noise[i]
    return data