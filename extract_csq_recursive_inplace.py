#-*- encoding: utf-8 -*-
import glob
import os
import shutil
import sys
from multiprocessing import Process

import time

def extract_dir(path):
    csq_list = glob.glob(os.path.join(path, '**/*.csq'), recursive=True)
    os.makedirs('./tmp',exist_ok=True)
    print(path, " ", len(csq_list))

    for csq in csq_list:
        #create output path
        csq_file_name = os.path.basename(csq) #FLIRXXXXX.csq
        csq_name = os.path.splitext(csq_file_name)[0] #FLIRXXXXX
        out_path_csq = os.path.splitext(csq)[0]
        tmp_file_name = './tmp/'+csq_file_name
        tmp_flir_path = './tmp/'+csq_name
        
        print(csq_name)
        print("### extract {0} ###".format(csq_name))
        print('out_path: ', out_path_csq)
        shutil.copy2(csq, tmp_file_name)
        os.makedirs(tmp_flir_path, exist_ok=True)
        os.system('./fromcsq.sh {0} {1}'.format(tmp_file_name, tmp_flir_path))
        shutil.rmtree(out_path_csq, ignore_errors=True)
        shutil.copytree(tmp_flir_path, out_path_csq)
        shutil.rmtree(tmp_flir_path, ignore_errors=True)
        os.unlink(tmp_file_name)

if __name__ == "__main__":
    start_time = time.time()
    
    csq_path = u"/mnt/INSEO/전원전 열화상 데이터/대상 목록 분류"
    if len(sys.argv) > 1:
        csq_path = sys.argv[1]
        print("CSQ PATH: ", csq_path)
    
    procs = []
    sub_dir_list = glob.glob(os.path.join(csq_path, '*'))
    print("SUB DIR LIST")
    for dir in sub_dir_list:
        proc = Process(target=extract_dir, args=(dir,))
        procs.append(proc)
        proc.start()
    
    # wait processes
    for porc in procs:
        proc.join()    

    end_time = time.time()
    print("extract takes ", end_time-start_time, "seconds")