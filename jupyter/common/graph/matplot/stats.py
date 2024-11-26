import matplotlib.pyplot as plt



__all__ = ('add_stats_legend',)


def add_stats_legend(data):
    mean = data.mean()
    plt.axvline(x=mean, color='r', label='μ')
    plt.axvline(x=data.median(), color='b', label='Median')
    std = data.std()
    plt.axvline(x=mean - 1.96*std, color='g', label='μ - 1.96*σ')
    plt.axvline(x=mean + 1.96*std, color='g', label='μ + 1.96*σ')
    plt.legend()