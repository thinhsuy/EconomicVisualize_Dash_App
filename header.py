import numpy as np
import pandas as pd
import plotly.express as px
import pycountry
from sklearn.datasets import make_moons
from dash import Dash, html, dcc
import plotly.graph_objects as go
from dash.dependencies import Input,Output
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

app = Dash()
server = app.server