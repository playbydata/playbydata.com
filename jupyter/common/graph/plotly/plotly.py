import os

import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots

import settings


# Setup Rendering
print(f"Using {settings.PLOTLY_RENDER}")
if settings.PLOTLY_RENDER == "png":
    pio.renderers.default = "png"
    pio.kaleido.scope.default_width = 800  # Set the width of the image in pixels
    pio.kaleido.scope.default_height = 600  # Set the height of the image in pixels
    pio.kaleido.scope.default_scale = 1
else:
    pio.renderers.default = "notebook_connected"
