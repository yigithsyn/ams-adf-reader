import sys, pathlib

# setting path
sys.path.append('./src/')
import adf

# print(pathlib.Path.joinpath(pathlib.Path(__file__).parent.resolve(), "NFScan.adf"))
print("")

measurementFile = pathlib.Path.joinpath(pathlib.Path(__file__).parent.resolve(), "NFScan.adf")

measurement = adf.Measurement(measurementFile)

assert(print(measurement.start()))    == None
assert(print(measurement.finish()))   == None
assert(print(measurement.duration())) == None

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

