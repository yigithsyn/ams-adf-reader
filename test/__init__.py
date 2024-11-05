import sys, pathlib

# setting path
sys.path.append('./src/')
import adf

# print(pathlib.Path.joinpath(pathlib.Path(__file__).parent.resolve(), "NFScan.adf"))
print("")

measurementFile = pathlib.Path.joinpath(pathlib.Path(__file__).parent.resolve(), "NFScan.adf")

measurement = adf.Measurement(measurementFile)

assert(print("Measurement start    :", measurement.start))    == None
assert(print("Measurement finish   :", measurement.finish))   == None
assert(print("Measurement duration :", measurement.duration())) == None

print("")

assert(print("Measurement axes :", ', '.join(measurement.axes))) == None
assert(print("Measurement type :", measurement.type())) == None

for i in range(len(measurement.axes)):
  assert(print(measurement.axes[i], ":"))  == None
  assert(print(measurement.axesValues[i])) == None

# assert(print(measurement.data)) == None

assert(print(measurement.axesPositionsInitial)) == None
assert(print(measurement.axesPositionsEnd))     == None


# assert(print(adf.measurementStart(measurementFile)))    == None
# assert(print(adf.measurementFinish(measurementFile)))   == None
# assert(print(adf.measurementDuration(measurementFile))) == None

# assert(print(adf.measurementAxes(measurementFile))) == None



# print(Array.amplitudeTaper(31, 30, "taylor"))
# print(Array.amplitudeTaper(31, 30, "taylor", taylor_nbar = 5))
# print(Array.amplitudeTaper(31, 30, "chebyshev"))

# pyplot.plot
# # assert round(Propagation.lineOfSight(10), 2)            == 11.29
# # assert round(Propagation.radioHorizon(10), 2)           == 13.03
# # assert round(Propagation.pathLoss(500, 11, 20, 0), 1)   == 87.3

