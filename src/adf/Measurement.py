import os, pathlib, datetime
from enum import Flag, auto
import h5py

class MeasurementType(Flag):
  PLANAR_XSCAN = auto()
  PLANAR_YSCAN = auto()
  PLANAR       = PLANAR_XSCAN | PLANAR_YSCAN
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
    

  def exportForNSI(self, path, **kwargs):
    r""" Exports measurement data for NSI2000 import

      Parameters
      ----------
      path    : str
                folder which data will be stored
      **kwargs: dict
                prm file specific properties. Valid keyword arguments are: 

                probeDist: float: distance between probe aperture to rotation center [m] (antenna aperture instead of rotation for PNF)
                mre      : float: maximum radial extent of positioned antenna [m] (only for SNF and CNF)
                autWidth : float: AUT width [m]
                autHeight: float: AUT height [m]

      Abbreviations
      -------------
      PNF: planar nearfield
      CNF: cylindrical nearfield
      SNF: spherical nearfield
      AUT: antenna under test
    """
    if not os.path.exists(path):
      raise FileNotFoundError("Output folder does not exists.")
    
    if self.type() not in MeasurementType.PLANAR:
      raise ValueError("Unsupported measurement type.")
    
    probeDist = 1.0 if "probeDist" not in kwargs.keys() else kwargs["probeDist"]
    mre       = 1.0 if "mre" not in kwargs.keys() else kwargs["mre"]
    autWidth  = 1.0 if "autWidth" not in kwargs.keys() else kwargs["autWidth"]
    autHeight = 1.0 if "autHeight" not in kwargs.keys() else kwargs["autHeight"]

    if type(probeDist) != float:
      raise TypeError("%s must be float"%probeDist)
    if type(mre) != float:
      raise TypeError("%s must be float"%mre)
    if type(autWidth) != float:
      raise TypeError("%s must be float"%autWidth)
    if type(autHeight) != float:
      raise TypeError("%s must be float"%autHeight)
    
    with open(os.path.join(path, "NFScan.prm"), '+w', encoding='utf-8') as file:
      if self.type() in MeasurementType.PLANAR:
        file.write("PNF\n")
      file.write("%.3f, %.3f, %.3f, %.3f\n"%(probeDist, mre, autWidth, autHeight))
      if self.type() in MeasurementType.PLANAR:
        file.write("%+.3f, %+.3f, %.3f\n"%(self.axesValues[1][0], self.axesValues[1][-1], (self.axesValues[1][1]-self.axesValues[1][0])))
        file.write("%+.3f, %+.3f, %.3f\n"%(self.axesValues[2][0], self.axesValues[2][-1], (self.axesValues[2][1]-self.axesValues[2][0])))
      for i in range(len(self.axesValues[3])-1):
        file.write("%.6f, "%(self.axesValues[3][i]/1E9))
      file.write("%.6f\n"%(self.axesValues[3][-1]/1E9))
      for i in range(len(self.axesValues[3])-1):
        file.write("NF_%.0f.txt\n"%(self.axesValues[3][i]/1E3))
      file.write("NF_%.0f.txt"%(self.axesValues[3][-1]/1E3))
      
    for i in range(len(self.axesValues[3])):
      with open(os.path.join(path, "NF_%.0f.txt"%(self.axesValues[3][i]/1E3)), '+w', encoding='utf-8') as file:
        file.write("# pol\t\tstep\t\tscan\t\treal\t\timag\n"%(self.axesValues[3][i]/1E3))
        for k in range(len(self.axesValues[0])):
          for l in range(len(self.axesValues[1])):
            for m in range(len(self.axesValues[2])):
              dataIndex = k*len(self.axesValues[1])*len(self.axesValues[2]) + l*len(self.axesValues[2]) + len(self.axesValues[2])
              file.write("%.3f\t\t%+.3f\t\t%+.3f\t\t%+.16f\t\t%+.16f\n"%(self.axesValues[0][k], self.axesValues[1][l], self.axesValues[2][m], self.data[k][l][m][i][0], self.data[k][l][m][i][1]))
