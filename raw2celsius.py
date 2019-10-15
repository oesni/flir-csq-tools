from math import sqrt, exp, log
from itertools import islice
import numpy as np
import csv
import sys
import os

def raw2temp(raw, E=1, OD=1, RTemp=20, ATemp=20, IRWTemp=20, IRT=1, RH=50, PR1=21106.77, PB=1501, PF=1, PO=-7340,
                 PR2=0.012545258):
    """
    convert raw values from the flir sensor to temperatures in C
    # this calculation has been ported to python from
    # https://github.com/gtatters/Thermimage/blob/master/R/raw2temp.R
    # a detailed explanation of what is going on here can be found there
    """

    # constants
    ATA1 = 0.006569
    ATA2 = 0.01262
    ATB1 = -0.002276
    ATB2 = -0.00667
    ATX = 1.9

    # transmission through window (calibrated)
    emiss_wind = 1 - IRT
    refl_wind = 0

    # transmission through the air
    h2o = (RH / 100) * exp(1.5587 + 0.06939 * (ATemp) - 0.00027816 * (ATemp) ** 2 + 0.00000068455 * (ATemp) ** 3)
    tau1 = ATX * exp(-sqrt(OD / 2) * (ATA1 + ATB1 * sqrt(h2o))) + (1 - ATX) * exp(
        -sqrt(OD / 2) * (ATA2 + ATB2 * sqrt(h2o)))
    tau2 = ATX * exp(-sqrt(OD / 2) * (ATA1 + ATB1 * sqrt(h2o))) + (1 - ATX) * exp(
        -sqrt(OD / 2) * (ATA2 + ATB2 * sqrt(h2o)))

    # radiance from the environment
    raw_refl1 = PR1 / (PR2 * (exp(PB / (RTemp + 273.15)) - PF)) - PO
    raw_refl1_attn = (1 - E) / E * raw_refl1
    raw_atm1 = PR1 / (PR2 * (exp(PB / (ATemp + 273.15)) - PF)) - PO
    raw_atm1_attn = (1 - tau1) / E / tau1 * raw_atm1
    raw_wind = PR1 / (PR2 * (exp(PB / (IRWTemp + 273.15)) - PF)) - PO
    raw_wind_attn = emiss_wind / E / tau1 / IRT * raw_wind
    raw_refl2 = PR1 / (PR2 * (exp(PB / (RTemp + 273.15)) - PF)) - PO
    raw_refl2_attn = refl_wind / E / tau1 / IRT * raw_refl2
    raw_atm2 = PR1 / (PR2 * (exp(PB / (ATemp + 273.15)) - PF)) - PO
    raw_atm2_attn = (1 - tau2) / E / tau1 / IRT / tau2 * raw_atm2
    raw_obj = (raw / E / tau1 / IRT / tau2 - raw_atm1_attn -
                raw_atm2_attn - raw_wind_attn - raw_refl1_attn - raw_refl2_attn)

    # temperature from radiance
    temp_celcius = PB / log(PR1 / (PR2 * (raw_obj + PO)) + PF) - 273.15
    return temp_celcius

if __name__ == "__main__":
    
    # temp = raw2temp(x, 0.95, 1.0, 20, 20, 20, 1.0, 50, 15727.867, 1412.6, 1, -4266, 0.014448789)
    # TODO: read parameters form file exif
    tFrom = lambda raw : raw2temp(raw, 0.95, 1.0, 20, 20, 20, 1.0, 50, 15727.867, 1412.6, 1, -4266, 0.014448789)

    input_file = sys.argv[1]
    output_dir = sys.argv[2]

    name = os.path.basename(input_file)
    name = os.path.splitext(name)[0]
    output_file = output_dir+name+'.csv'
    
    with open(input_file,"r") as ifile, open(output_file,"w") as ofile:
        # ifile_skip = islice(ifile, 4, None)
        
        csv_reader = csv.reader(ifile, delimiter=',')
        csv_writer = csv.writer(ofile, delimiter=',')
        
        # timeinfo_str = next(csv_reader)
        # filename = next(csv_reader)
        width, height = 640,480
        # maxvalue = next(csv_reader)
        maxvalue = 65536

        # print(timeinfo_str)
        # print(filename)
        # print("size: ",width, '-', height)
        # print('max value: ', maxvalue)

        data = []
        
        for row in csv_reader:
            # csv_writer.writerow(row)
            # print(row)
            # print(row)
            data.extend(row)
            # print(len(data))
            # break
        data = list(filter(None, data))
        tdata = [round(tFrom(int(rawValue)), 2) for rawValue in data]
        tdata = np.reshape(tdata, (480, 640))
        csv_writer.writerows(tdata)
