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

def calculate_SW(df, rt_column, phit_column='PHIT_Calc', a=1, m=2, n=2, Rw=0.022):
  """
  Derive water saturation (SW)

  Arguments:
    df: dataframe
    rt_column: column name of RT (true resistivity)
    phit_column: column name of PHIT. default is 'PHIT_Calc'
    a: Archie factor, default 1
    m: cement exponent, default 2
    n: saturation exponent, default 2
    Rw: water resistivity, already extrapolated at depth
  
  Output:
    vsh: shale volume curve
  """    
  rt, phit = df[rt_column], df[phit_column]
  sw = (a * Rw / (phit**m * rt))**(1 / n)
  df['SW_Calc'] = sw

  # QC 
  # Set 'SW_Calc' values greater than 1 or less than 0 to NaN
  df.loc[df['SW_Calc'] > 1, 'SW_Calc'] = np.nan
  df.loc[df['SW_Calc'] < 0, 'SW_Calc'] = np.nan   
  return df

def calculate_VSH(df, gr_column):
  """
  Derive shale volume (VSH) curve

  Arguments:
    df: dataframe
    gr_column: column name of GR
  
  Output:
    vsh: shale volume curve
  """    
  gr = df[gr_column]
  gr_min, gr_max = gr.min(), gr.max()
  vsh = (gr - gr_min) / (gr_max - gr_min)
  df['VSH_Calc'] = vsh 
  return df
