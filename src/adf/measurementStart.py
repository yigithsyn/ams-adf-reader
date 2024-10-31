import os, datetime, pathlib
import h5py

def measurementStart(filename: float):
  r""" Return measurement start date

  Parameters
  ----------
  filename : str
             measurement file name

  Returns
  -------
  datetime : datetime.datetime
             measurement date and time object

  """


  if os.path.exists(filename):
    if pathlib.Path(filename).suffix == ".adf":
      try:
        measurement = h5py.File(filename, 'r')
        return measurement['Radiation Pattern']['ATTRIBUTES']['History'].attrs['Measurement Start']
      except:
        raise Exception
    raise ValueError("Filename must be valid .ADF type")
  else:
    raise FileNotFoundError