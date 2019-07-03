##use this script
##This script has modified noise filter rather than frequency filter
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 09:53:05 2018

@author: sayan
"""
import os, sys, math, select
import numpy as np
import pandas as pd
import librosa
import sounddevice as sd
import time as tm
import scipy.io.wavfile as wavf
import datetime
import warnings
import tempfile

from feature_extraction import filters as fil
from feature_extraction import lpcgen as lpg
from feature_extraction import calcspectrum as csp
from feature_extraction import harmonics as hmn
from feature_extraction import fextract as fex
from feature_extraction import parsedata as par
from feature_extraction.getconfi import logdata
from feature_extraction.apicall import apicalls
from feature_extraction.specsub import reduce_noise

from sklearn import svm
from sklearn.externals import joblib
import pickle

warnings.filterwarnings("ignore")
"""clf = joblib.load('input/detection_iris_new.pkl')## this is the vnear robust one"""
clf = joblib.load('input/detection_new18july.pkl')## this is taken at the beach
#clm = joblib.load('input/detection_new18july.pkl')
#clf1 = joblib.load('input/dronedetectionfinal_new.pkl')
#discard this part----------------------------------------------------------
rows = 10
cols = 60
winlist = []

"""set this part to the number of logs you want to save before computing confidence level"""
log = logdata(3) ##check getconfi.py for more details(in feature_extraction folder)

######################################################################################################
global itervalue #I used this when I needed to get only a certain number o iterations
itervalue = 0

"""this is the script which would record data"""
def record(time = 1, fs = 44100):
    file = 'temp_out'
    duration = time
    recording = sd.rec(int(duration*fs),samplerate=fs, channels=1, blocking  = False)
    for i in range(time):
        i += 1
        tm.sleep(1)
    recording = recording[:,0]
    np.save(file,recording)
    np.seterr(divide='ignore', invalid='ignore')
    scaled = np.int16(recording/np.max(np.abs(recording)) * 32767) #I am using normalised data so that the processing doesnt throw errors
    wavf.write(file+'.wav', fs, scaled)
    """uncomment the following if you want to save data"""#use the commented portion only when you need to collect data at the same time you do processing
    ##################################################################################################
    #wavf.write(file+'_'+str(itervalue)+'.wav', fs, scaled)
    #data, fs = librosa.load(file+'_'+str(itervalue)+'.wav')
    ######################################################################################################
    data, fs = librosa.load(file+'.wav')
    #os.remove(file+'.npy')
    #os.remove(file+'.wav')
    return data, fs

def dist_prediction_label(value):
    if value == 0:
        label = "far"
    elif value == 1:
        label = "midrange"
    elif value == 2:
        label = "near"
    elif value == 3:
        label = "vfar or nodrone"
    elif value == 4:
        label = "vnear"
    return label

#noise, sfr = record(time = 15)##set time appropriately for good results

# def drone_prediction_label(value):
#     if value == 1:
#         label = "drone"
#     elif value == 0:
#         label = "no drone"
#     return label

######################################################################################################################
"""set api and initiate calls"""
# api_url = 'http://mlc67-cmp-00.egr.duke.edu/api/events' ##This is dukes server which Chunge created
api_url = 'http://mlc67-cmp-00.egr.duke.edu/api/caryevents' ##This is carytown server  
apikey = None
push_url = "https://onesignal.com/api/v1/notifications"
pushkey = None
sound_url = 'http://mlc67-cmp-00.egr.duke.edu/api/soundInfos'
soundkey = None
wav_url = ' http://mlc67-cmp-00.egr.duke.edu/api/sound-clips/container/upload'
wavkey = None
LOCATION = "Drone Detector A"
send = apicalls(api_url,apikey, push_url,pushkey, sound_url, soundkey, wav_url,wavkey, LOCATION)##This initiates the push notification and mongodb database
log.insertdf(3,str(datetime.datetime.now())[:-7]) #inserted dummy value to eliminate inconsistency
i = 0
bandpass = [600,10000]#filter unwanted frequencies
prev_time= tm.time()#initiate time
reccount = 0
recdata = np.array([],dtype="float32")
basename = "drone"
"""main code"""
try:#don't want useless user warnings
    while True:
        if reccount == 0: 
            data, fs = record()
            #out = reduce_noise(data,noise)
            ns = fil.bandpass_filter(data,bandpass)
            try:
                p,freq, b = hmn.psddetectionresults(data)
            except IndexError:
                pass
                b = False
        b = True
        
        if b:
            if reccount == 0: 
                mfcc, chroma, mel, spect, tonnetz = fex.extract_feature(ns,fs)
                #a,e,k = lpg.lpc(ns,10)
                mfcc_test = par.get_parsed_mfccdata(mfcc, chroma,mel,spect,tonnetz)
                #lpc_test = par.get_parsed_lpcdata(a,k,freq)
                x1 = clf.predict(mfcc_test)
                #x02 = clm.predict(mfcc_test)
                #x1 = ((x01[0]+x01[0])/2)
                #x2 = clf1.predict(lpc_test) 
                print("Drone at %s"% dist_prediction_label(int(x1)))
                log.insertdf(int(x1),str(datetime.datetime.now())[:-7])
                print(x1)
                output = log.get_result()
                '''-----------uncomment if you want to save logs-----------------'''
                #log.logdf(sys.argv[1],x01[0],x02[0],str(datetime.datetime.now())[:-7])
                '''---------------------------------------------------------------'''
            
            if True:#i > 9:
                if reccount == 0: 
                    print(int(output['Label']))
                    #win.addstr(7,5,"Recieved a Result!")
                    dt = tm.time() - prev_time
                    if dt > 30:#send output every 30secs
                        # Now dummy sent
                        print('sent %s'% int(output['Label']))
                        # send.sendtoken(output)#This line sends the log to srver(recent detection with confidence)
                        prev_time = tm.time()
                        if int(output['Label']) == int(4) or int(output['Label']) == int(2):
                            # move the previous line here, to send info only when detection happens 
                            send.sendtoken(output)#This line sends the log to srver(recent detection with confidence)
                            send.push_notify()#when drone is detected this sends push notification to user in his app
                            if reccount == 0:
                                suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
                                reccount=1
                                print("Recording started!")
                            print("pushed %s"% int(output['Label']))
                        #win.addstr(8,5,"Data Sent!")
                
                #recording for 10 secs:
                if reccount > 0 and reccount < 12:
                    data, fs = record(time=10)
                    recdata = np.concatenate([recdata, data])
                    np.seterr(divide='ignore', invalid='ignore')
                    recscaled = np.int16(recdata/np.max(np.abs(recdata)) * 32767)
                    reccount += 10
                    if reccount == 11:
                        sfilename = "_".join([basename, suffix])+".wav" # e.g. 'mylogfile_120508_171442'
                        #np.save(tf.name,recscaled)
                        wavf.write(sfilename, fs, recscaled)
                        send.infosendtoken(output, sfilename)
                        send.wavsendtoken(sfilename)
                        print("file succesfully uploaded to server!")
                        os.remove(sfilename)
                        recdata = np.array([],dtype="float32")
                        reccount = 0


            ######################################################################################################
            # if itervalue > int(sys.argv[3]):
            #     log.savedf(sys.argv[2])
            #     exit()
            # itervalue+=1
        else:
            print("Wait for result")
        
        
        i+=1


except KeyboardInterrupt:
    pass


print('iter_num:',i)

