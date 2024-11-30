import matplotlib.pyplot as plt


__all__ = ("plt_show",)


def plt_show(plot=None, title=None, figsize=None):
    if title:
        plt.title(title)
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    plt.grid(color="grey", linestyle="--", linewidth=0.5)
    if figsize:
        plt.figure(figsize=figsize)
    plt.show()
