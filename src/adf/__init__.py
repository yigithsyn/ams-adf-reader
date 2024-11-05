# from .measurementStart import measurementStart
# from .measurementFinish import measurementFinish
# from .measurementDuration import measurementDuration
# from .measurementAxes import measurementAxes

import os, pathlib, datetime
from enum import Enum, auto
import h5py

class MeasurementType(Enum):
  PLANAR_XSCAN = auto()
  PLANAR_YSCAN = auto()
  CUSTOM       = auto()

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

        datetimestr = self.hdf['Radiation Pattern']['ATTRIBUTES']['History'].attrs['Measurement Start'].strip()
        self.start  = datetime.datetime.strptime(datetimestr, "%a %b %d %H:%M:%S %Y")

        datetimestr = self.hdf['Radiation Pattern']['ATTRIBUTES']['History'].attrs['Measurement Finished'].strip()
        self.finish = datetime.datetime.strptime(datetimestr, "%a %b %d %H:%M:%S %Y")

        self.axes = tuple(self.hdf['Radiation Pattern']['Radiation Pattern'].attrs['DIMENSION_LABELS'])
        self.axesValues = tuple()
        for item in self.axes:
          print(item)
          self.axesValues += (self.hdf['Radiation Pattern'][item][:],)
        
        self.data = self.hdf['Radiation Pattern']['Radiation Pattern'][:].tolist()

        self.axesPositionsInitial = self.hdf['Radiation Pattern']['ATTRIBUTES']['Status after Init'].attrs['Positions']
        self.axesPositionsEnd     = self.hdf['Radiation Pattern']['ATTRIBUTES']['Status after Measurement'].attrs['Positions']

      else:
        raise ValueError("Filename must be valid .adf type")
    else:
      raise FileNotFoundError
    
  
  def duration(self):
    r""" Return measurement duration in seconds

      Returns
      -------
      duration : float
                measurement duration in seconds
    """
    return (self.finish - self.start).total_seconds()
  

  def type(self):
    r""" Returns measurement type

      Returns
      -------
      type : enum
             measurement type
    """
    axes = self.axes
    if axes[0] == "Pol" and axes[1] == "x" and axes[2] == "y" and axes[3] == "Frequency":
      return MeasurementType.PLANAR_YSCAN
    elif axes[0] == "Pol" and axes[1] == "y" and axes[2] == "x" and axes[3] == "Frequency":
      return MeasurementType.PLANAR_XSCAN
    else:
      return MeasurementType.CUSTOM

