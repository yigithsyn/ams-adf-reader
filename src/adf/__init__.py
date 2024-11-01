# from .measurementStart import measurementStart
# from .measurementFinish import measurementFinish
# from .measurementDuration import measurementDuration
# from .measurementAxes import measurementAxes

import os, pathlib, datetime
import h5py

class Measurement:
  r""" Antenna Measurement System (AMS) data file object

  Parameters
  ----------
  filename : str
             measurement file name

  """
  def __init__(self, filename: str):
    if os.path.exists(filename):
      if pathlib.Path(filename).suffix == ".adf":
        self.hdf = h5py.File(filename, 'r')
      else:
        raise ValueError("Filename must be valid .adf type")
    else:
      raise FileNotFoundError
    
  def start(self):
    r""" Return measurement start date

      Returns
      -------
      datetime : datetime.datetime
                measurement start, date and time object
    """
    datetimestr = self.hdf['Radiation Pattern']['ATTRIBUTES']['History'].attrs['Measurement Start'].strip()
    return datetime.datetime.strptime(datetimestr, "%a %b %d %H:%M:%S %Y")
  
  def finish(self):
    r""" Return measurement finish date

      Returns
      -------
      datetime : datetime.datetime
                 measurement finish, date and time object
    """
    datetimestr = self.hdf['Radiation Pattern']['ATTRIBUTES']['History'].attrs['Measurement Finished'].strip()
    return datetime.datetime.strptime(datetimestr, "%a %b %d %H:%M:%S %Y")
  
  def duration(self):
    r""" Return measurement duration in seconds

      Returns
      -------
      duration : float
                measurement duration in seconds
    """
    return (self.finish() - self.start()).total_seconds()
