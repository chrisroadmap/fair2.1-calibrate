#!/usr/bin/env python
# coding: utf-8

# # Convert EBM to IRM
#
# This notebook takes the three-layer energy balance model tunings from Donald Cummins and converts them to a three-layer impulse response function.
#
# It will then save these into a CSV file.

# In[ ]:


import os

import numpy as np
import pandas as pd
import scipy.linalg
from tqdm import tqdm
from dotenv import load_dotenv

from fair.constants import DOUBLING_TIME_1PCT
from fair.earth_params import seconds_per_year, earth_radius
from fair.forcing.ghg import meinshausen2020
from fair.energy_balance_model import EnergyBalanceModel
from fair import __version__

# Get environment variables
load_dotenv()

cal_v = os.getenv('CALIBRATION_VERSION')
fair_v = os.getenv('FAIR_VERSION')
constraint_set = os.getenv('CONSTRAINT_SET')

df = pd.read_csv(f'../../../../../output/fair-{fair_v}/v{cal_v}/{constraint_set}/calibrations/4xCO2_cummins_ebm3_cmip6.csv')

models = df['model'].unique()

params = {}
for model in models:
    params[model] = {}
    for run in df.loc[df['model']==model, 'run']:
        condition = (df['model']==model) & (df['run']==run)
        params[model][run] = {}
        params[model][run]['gamma_autocorrelation'] = df.loc[condition, 'gamma'].values[0]
        params[model][run]['ocean_heat_capacity'] = df.loc[condition, 'C1':'C3'].values.squeeze()
        params[model][run]['ocean_heat_transfer'] = df.loc[condition, 'kappa1':'kappa3'].values.squeeze()
        params[model][run]['deep_ocean_efficacy'] = df.loc[condition, 'epsilon'].values[0]
        params[model][run]['sigma_eta'] = df.loc[condition, 'sigma_eta'].values[0]
        params[model][run]['sigma_xi'] = df.loc[condition, 'sigma_xi'].values[0]
        params[model][run]['forcing_4co2'] = df.loc[condition, 'F_4xCO2'].values[0]

co2 = 284.3169988
ch4 = 808.2490285
n2o = 273.021047

double_co2 = co2 * 2
quadruple_co2 = co2 * 4

rf_4co2 = meinshausen2020(
    np.array([4*co2, ch4, n2o]).reshape((1, 1, 1, 3)),
    np.array([co2, ch4, n2o]).reshape((1, 1, 1, 3)),
    np.array([1, 1, 1]).reshape((1, 1, 1, 3)),
    np.ones((1, 1, 1, 3)),
    0, 1, 2, []
).squeeze()[0]

rf_2co2 = meinshausen2020(
    np.array([2*co2, ch4, n2o]).reshape((1, 1, 1, 3)),
    np.array([co2, ch4, n2o]).reshape((1, 1, 1, 3)),
    np.array([1, 1, 1]).reshape((1, 1, 1, 3)),
    np.ones((1, 1, 1, 3)),
    0, 1, 2, []
).squeeze()[0]

forcing_2co2_4co2_ratio=rf_2co2/rf_4co2

for model in models:
    for run in df.loc[df['model']==model, 'run']:
        condition = (df['model']==model) & (df['run']==run)
        ebm = EnergyBalanceModel(**params[model][run])
        ebm.emergent_parameters()
        params[model][run] = ebm.__dict__

# reconstruct a data table and save
df_out = pd.DataFrame(columns=['model', 'run', 'ecs', 'tcr', 'tau1', 'tau2', 'tau3', 'q1', 'q2', 'q3'])

count = 0
for model in models:
    for run in df.loc[df['model']==model, 'run']:
        values_to_add = {
            'model': model,
            'run': run,
            'ecs': params[model][run]['ecs'],
            'tcr': params[model][run]['tcr'],
            'tau1': params[model][run]['timescales'][0],
            'tau2': params[model][run]['timescales'][1],
            'tau3': params[model][run]['timescales'][2],
            'q1': params[model][run]['response_coefficients'][0],
            'q2': params[model][run]['response_coefficients'][1],
            'q3': params[model][run]['response_coefficients'][2],
        }
        row_to_add = pd.Series(values_to_add, name=count)
        df_out = df_out.append(row_to_add)
        count = count + 1

df_out.sort_values(['model', 'run'], inplace=True)

os.makedirs(f'../../../../../output/fair-{fair_v}/v{cal_v}/{constraint_set}/calibrations/', exist_ok=True)

df_out.to_csv(f'../../../../../output/fair-{fair_v}/v{cal_v}/{constraint_set}/calibrations/4xCO2_impulse_response_ebm3_cmip6.csv', index=False)