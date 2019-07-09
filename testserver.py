# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 12:51:47 2019

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
i = 0
bandpass = [600,10000]#filter unwanted frequencies
prev_time= tm.time()#initiate time
reccount = 0
recdata = np.array([],dtype="float32")
basename = "drone"
labels=[]
"""save server recodings in assets folder"""
for root, dirs, files in os.walk("assets"):
    for file in files:
        if file.endswith(".wav"):
            data, fs = librosa.load(os.path.join(root, file))
            tests = np.split(data, 10)
            for test in tests:
                fs = 44100
                ns = fil.bandpass_filter(test,bandpass)
                mfcc, chroma, mel, spect, tonnetz = fex.extract_feature(ns,fs)
                mfcc1, chroma1, mel1, spect1, tonnetz1 = fex.extract_feature(test,fs)
                #a,e,k = lpg.lpc(ns,10)
                mfcc_test = par.get_parsed_mfccdata(mfcc, chroma,mel,spect,tonnetz)
                mfcc_test1 = par.get_parsed_mfccdata(mfcc1, chroma1,mel1,spect1,tonnetz1)
                #lpc_test = par.get_parsed_lpcdata(a,k,freq)
                x1 = clf.predict(mfcc_test)
                x11 = clf.predict(mfcc_test1)
                label = dist_prediction_label(int(x1))
                label1 = dist_prediction_label(int(x11))
                labels.append([i,file,label,label1])
                i+=1

import pandas as pd
df = pd.DataFrame(labels)
df.columns=['idx','filename','labelwithfilter','labelwithrawdata']
df
df.to_csv(r'servertest.csv')