import glob
import os

if __name__ == "__main__":
    csq_path = "/home/inseo/Desktop/csq"
    out_path = "/home/inseo/Desktop/csq/output"
    csq_list = glob.glob(os.path.join(csq_path, '*.csq'))
    for csq in csq_list:
        #create output path
        print("### extract {0} ###".format(os.path.basename(csq)))
        out_path_csq = os.path.join(out_path, os.path.basename(csq))
        os.makedirs(out_path_csq,exist_ok=True)
        os.system('./fromcsq.sh {0} {1}'.format(csq, out_path_csq))