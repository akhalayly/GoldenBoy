from typing import List, Any

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import Positions_Traits as posT
import helperFunctions as hf

if __name__ == '__main__':
    dataset = pd.read_csv("Success_" + "CAMS" + ".csv")
    attrbs: List[Any] = []
    for role in posT.CAMs_Traits:
        attrbs = attrbs + hf.roleTraitIndexesFinder(role,dataset.columns,hf.year_2012)
    X = dataset.iloc[:, attrbs]
    y = dataset.iloc[:, -1].values
    print("")
