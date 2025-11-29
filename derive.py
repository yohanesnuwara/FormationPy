import pandas as pd
import numpy as np

def calculate_PHID(df, rhob_column, rho_ma=2.66, rho_fl=1):
  """
  Derive density porosity (PHID) curve

  Arguments:
    df: dataframe
    rhob_column: column name of RHOB
    rho_ma: Matrix density (g/cc), default 2.66
    rho_fl: Fluid density (g/cc), default 1
  
  Output:
    phid: density porosity curve
  """
  rhob = df[rhob_column]
  phid = (rho_ma - rhob) / (rho_ma - rho_fl)

  # Update dataframe
  df['PHID_Calc'] = phid
  return df

def calculate_PHIT(df, nphi_column, phid_column='PHID_Calc', A=0, B=0):
  """
  Derive density porosity (PHID) curve

  Arguments:
    df: dataframe
    nphi_column: column name of NPHI
    phid_column: column name of PHID. default is 'PHID_Calc'
    A: regression coeff for PHID, default 0
    B: regression coeff for PHID, default 0
  
  Output:
    phit total porosity curve
  """  
  phid, nphi = df[phid_column], df[nphi_column]
  phit = phid + (A * (nphi - phid)) + B
  df['PHIT_Calc'] = phit
  return df
