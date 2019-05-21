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
from main import *
import time

starttime=time.time()

while True:
    main()#define main and a workaround with nohup
    #write one for running the continuous function for 5 mins
    time.sleep(1800.0 - ((time.time() - starttime) % 60.0))

