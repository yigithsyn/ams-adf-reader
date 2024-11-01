import os, datetime, pathlib
import h5py

def measurementAxes(filename: float):
  r""" Return measurement axes

  Parameters
  ----------
  filename : str
             measurement file name

  Returns
  -------
  axes : tuple
         measurement axes ordered

  """

  if os.path.exists(filename):
    if pathlib.Path(filename).suffix == ".adf":
      measurement = h5py.File(filename, 'r')
      return tuple(measurement['Radiation Pattern']['Radiation Pattern'].attrs['DIMENSION_LABELS'])
    raise ValueError("Filename must be valid .ADF type")
  else:
    raise FileNotFoundError