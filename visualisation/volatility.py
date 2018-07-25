#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: fenc=utf-8:et:ts=4:sts=4:sw=4

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib import rc
import pandas as pd
import numpy as np
import os

# Matplotlib style
plt.rcdefaults()
rc('text', usetex=True)

# Constants
WIN_SIZE = 90
Y_DESC = ''
DATA_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
OUTPUT_DIRECTORY = os.path.join(DATA_DIRECTORY, 'graphics/volatility.png')

# Prepare dataframe
print('Building dataframe...')
# Data source: Icelandic Central Bank
df = pd.read_csv(DATA_DIRECTORY + '/usd-isk_exchange_rates.csv', decimal=",")
df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y')
df = df.set_index('Date')

# Get STD
print('Calculating standard deviation...')
df_isk_eur = df['EUR'].pct_change().rolling(WIN_SIZE).std()
df_isk_usd = df['USD'].pct_change().rolling(WIN_SIZE).std()

# Plot
print('Plotting...')
fig, ax = plt.subplots()

ax.plot(df_isk_usd, color='r', label='ISK/USD')
ax.plot(df_isk_eur, color='#003399', label='ISK/EUR')

# Make it pretty
ax.legend()

ax.set_ylim(bottom=0)
ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y)))
ax.set_ylabel(Y_DESC)
ax.set_xlabel("\\'{A}r")

ax.xaxis_date()
fig.autofmt_xdate()
fig.tight_layout()
print('Saving to {}'.format(OUTPUT_DIRECTORY))
fig.savefig(OUTPUT_DIRECTORY)
