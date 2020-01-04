import os

import numpy as np
import pandas as pd
import pytest

from data.path import DATA_PATH
from fifo.fifo import FIFO_ARGS, fifo


# FIFO Testing Function
def test_fifo():

    # Load Testing Table
    test_df = fifo(FIFO_ARGS)

    # File Name
    fname = os.path.join(DATA_PATH, 'df_out.csv')
    # Load Truth Table
    true_df = pd.read_csv(fname)

    true_df["transactionDate_earn"] = pd.to_datetime(true_df["transactionDate_earn"])
    true_df["transactionDate_burn"] = pd.to_datetime(true_df["transactionDate_burn"])

    # Assert both tables are the same
    assert np.array_equal(test_df.values, true_df.values), "Datasets do not match."
