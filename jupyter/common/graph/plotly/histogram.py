import numpy as np
from .plotly import *

from scipy.stats import gaussian_kde


def plot_overlap_histogram(data, figure, name, bins=25, color="blue", row=None, col=None, ay=-140, max_row=None):
    # X Axis
    x = np.linspace(data.min(), data.max())
    # Histogram
    hist_values, bin_edges = np.histogram(data, bins=bins)
    max_hist_values = max(hist_values)
    figure.add_trace(
        go.Bar(
            x=(bin_edges[:-1] + bin_edges[1:]) / 2,            # Bin centers for x-axis
            y=hist_values,
            width=(bin_edges[1] - bin_edges[0]),
            name=name,
            marker=dict(color=color, opacity=0.1),
        ),
        **(dict(row=row, col=col) if row and col else {})
    )
    # Calculate KDE
    kde = gaussian_kde(data)
    y = kde(x)
    figure.add_trace(
        go.Scatter(
            x=x,
            y=y / max(y) * max_hist_values,  # Use scaled KDE values
            mode="lines",
            name=f"{name} Trend",
            showlegend=False,
            line=dict(color=color, dash="dash")  # Increased width
        ),
        **(dict(row=row, col=col) if row and col else {})
    )
    # Calculate mean and standard deviation
    mean = data.mean()
    std = data.std()
    count = data.count()
    figure.add_trace(
        go.Scatter(
            x=[mean, mean],
            y=[0, max_hist_values],  # Match histogram height
            mode="lines",
            name=f"{name} Mean",
            showlegend=False,
            line=dict(color=color)  # Increased width
        ),
        **(dict(row=row, col=col) if row and col else {})
    )
    # Add annotation for the mean
    ann_pos = None
    if col and row and max_row:
        ann_pos = col+(row-1)*max_row
    figure.add_annotation(
        x=mean,  # Position at the mean
        y=max_hist_values,  # Position at the top of the vertical line
        text=f"<br>μ={mean:.2f}<br>cv={int(std*100/mean)}%",  # Display mean and std
        showarrow=True,
        arrowhead=2,
        ax=0,  # Horizontal offset for the arrow"s tail
        ay=ay,  # Vertical offset for the arrow"s tail
        font=dict(color=color, size=12),
        align="left",  # Align text to the left for better readability,
        **(dict(xref=f"x{ann_pos}", yref=f"y{ann_pos}") if col and row and max_row else {})
    )
    return figure