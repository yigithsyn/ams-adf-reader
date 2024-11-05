import sys, pathlib

# setting path
sys.path.append('./src/')
import adf
from adf import MeasurementType

pathlib.Path(pathlib.Path.joinpath(pathlib.Path(__file__).parent.resolve(), "data")).mkdir(parents=True, exist_ok=True)
print("")
measurementFile = pathlib.Path.joinpath(pathlib.Path(__file__).parent.resolve(), "NFScan.adf")

measurement = adf.Measurement(measurementFile)

assert(print("Measurement start    :", measurement.start))    == None
assert(print("Measurement finish   :", measurement.finish))   == None
assert(print("Measurement duration :", measurement.duration())) == None

print("")
assert(print("Measurement axes :", ', '.join(measurement.axes))) == None
assert(print("Measurement type :", measurement.type()))          == None
assert(print(measurement.type() in MeasurementType.PLANAR))      == None

for i in range(len(measurement.axes)):
  assert(print(measurement.axes[i], ":"))  == None
  assert(print(measurement.axesValues[i])) == None

assert(type(measurement.data) == list)

assert(print(measurement.axesPositionsInitial)) == None
assert(print(measurement.axesPositionsEnd))     == None

assert(measurement.exportForNSI(pathlib.Path.joinpath(pathlib.Path(__file__).parent.resolve(), "data"))) == None



