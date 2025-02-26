# PROJECT ASSIGNMENT
```
Nama: Richie Zakaria 
Kelas: MC-07
Cohort ID : richie_rich100
```


# Dicoding Collection Dashboard ✨

## Setup Environment - Anaconda
```
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

## Run steamlit app
```
streamlit run dashboard.py
```
