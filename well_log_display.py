def well_log_display(df, column_depth, column_list,
                     column_semilog=None, min_depth=None, max_depth=None,
                     column_min=None, column_max=None, colors=None,
                     fm_tops=None, fm_depths=None,
                     tight_layout=1, title_size=10):
  """
  Display log side‑by‑side style
  Input:
  df is your dataframe
  specify min_depth and max_depth as the upper and lower depth limit
  column_depth is the column name of your depth
  column_list is the LIST of column names that you will display

  column_semilog is specific for resistivity column; if your resistivities are
    in column 3, specify as: column_semilog=2. Default is None, so if you don't
    specify, the resistivity will be plotted in normal axis instead

  column_min is list of minimum values for the x‑axes.
  column_max is list of maximum values for the x‑axes.

  colors is the list of colors specified for each log names. Default is None,
    so if don't specify, the colors will be Matplotlib default (blue)
  fm_tops and fm_depths are the list of formation top names and depths.
    Default is None, so no tops are shown. Specify both lists, if you want
    to show the tops
  """
  import numpy as np
  import matplotlib.pyplot as plt
  import pandas as pd
  import random

  # Ensure column_semilog is a list for consistent processing
  if column_semilog is None:
      column_semilog = []
  elif not isinstance(column_semilog, list):
      column_semilog = [column_semilog]

  logs = column_list

  # create the subplots; ncols equals the number of logs
  fig, ax = plt.subplots(nrows=1, ncols=len(logs), figsize=(20,10))

  # looping each log to display in the subplots
  if colors==None:
    # color is None (default)
    for i in range(len(logs)):
      if i in column_semilog:
        # for specified columns, semilog plot
        ax[i].semilogx(df[logs[i]], df[column_depth])
      else:
        # for non-specified columns, normal plot
        ax[i].plot(df[logs[i]], df[column_depth])

      ax[i].set_title(logs[i], size=title_size)
      ax[i].minorticks_on()
      ax[i].grid(which='major', linestyle='-', linewidth='0.5', color='lime')
      ax[i].grid(which='minor', linestyle=':', linewidth='0.5', color='black')
      if column_min!=None and column_max!=None:
        # x-axis limits defined
        ax[i].set_xlim(column_min[i], column_max[i])
      if min_depth!=None and max_depth!=None:
        # y-axis limit defined
        ax[i].set_ylim(min_depth, max_depth)
      ax[i].invert_yaxis()

  else:
    # colors are defined (as list)
    for i in range(len(logs)):
      if i in column_semilog:
        # for specified columns, semilog plot
        ax[i].semilogx(df[logs[i]], df[column_depth], color=colors[i])
      else:
        # for non-specified columns, normal plot
        ax[i].plot(df[logs[i]], df[column_depth], color=colors[i])

      ax[i].set_title(logs[i], size=title_size)
      ax[i].minorticks_on()
      ax[i].grid(which='major', linestyle='-', linewidth='0.5', color='lime')
      ax[i].grid(which='minor', linestyle=':', linewidth='0.5', color='black')
      if column_min!=None and column_max!=None:
        # x-axis limits defined
        ax[i].set_xlim(column_min[i], column_max[i])
      if min_depth!=None and max_depth!=None:
        # y-axis limit defined
        ax[i].set_ylim(min_depth, max_depth)
      ax[i].invert_yaxis()

  # ---------------------------------------------------------------------------
  #  NEW: draw formation tops AND put the text label on each line
  # ---------------------------------------------------------------------------
  if fm_tops!=None and fm_depths!=None:
    # produce a stable colour per top
    rgb = [(random.random(), random.random(), random.random())
           for _ in fm_tops]

    for i in range(len(logs)):
      for j, top in enumerate(fm_tops):
        depth = fm_depths[j]
        ax[i].axhline(y=depth, linestyle=":", c=rgb[j])

        # place the formation‑name text slightly inside the left axis
        xmin, xmax = ax[i].get_xlim()
        xpos = xmin + 0.02 * (xmax - xmin)   # 2 % from left edge
        ax[i].text(
          xpos, depth, top,
          color=rgb[j], va='center', ha='left',
          fontsize=7,
          bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.6)
        )

  if tight_layout:
    plt.tight_layout()
  plt.show()
