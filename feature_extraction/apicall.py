#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 09:53:05 2018

@author: sayan
"""
import requests
import json
import os
import sys
 
class apicalls(object):
    def __init__(self, api_url, apikey, push_url, pushkey, sound_url, soundkey, wav_url, wavkey, location):
        self.url = api_url
        self.key = apikey
        self.pushurl = push_url
        self.pushKey = pushkey
        self.soundurl = sound_url
        self.soundKey = soundkey
        self.wavurl = wav_url
        self.wavKey = wavkey
        self.location = location
    
    """-----------------------All tokens definitions returns the url of the api where you can view what you have sent-------------------"""
    ##Lacks proper security encoding, can be accessed by anyone
    """before making the project public make sure you remove the server ids in the main script"""
    def sendtoken(self, record):##tokens are sent using the format in self.log
        self.x = record['Label']
        self.Label = self.getLabel(int(self.x))
        self.timestamp =record['Timestamp']
        self.confidence = record['Confidence']
        #self.confidenceLabel = self.getConfidence(int(self.confidence))
        self.log = {"type": "Drone",
        "distance" : self.Label,
        "confidence": self.confidence,
        "location": self.location,
        "time": self.timestamp
        }
        while True:
            try:
                # do stuff
                self.r =  requests.post(self.url, data = self.log)
            except requests.exceptions.Timeout:
                # Maybe set up for a retry, or continue in a retry loop
                continue
            except requests.exceptions.RequestException as e:
                # catastrophic error. bail.
                print(e)
                sys.exit(1)
            break
        return self.r.text
    
    def sendtoken1(self, record):##this token is for a different script, the only difference is the labelling because it is trained for different model
        self.x = record['Label']
        self.Label1 = self.getLabel1(int(self.x))
        self.timestamp =record['Timestamp']
        self.confidence = record['Confidence']
        #self.confidenceLabel = self.getConfidence(int(self.confidence))
        self.log = {"type": "Drone",
        "distance" : self.Label1,
        "confidence": self.confidence,
        "location": self.location,
        "time": self.timestamp
        }
        while True:
            try:
                # do stuff
                self.r =  requests.post(self.url, data = self.log)
            except requests.exceptions.Timeout:
                # Maybe set up for a retry, or continue in a retry loop
                continue
            except requests.exceptions.RequestException as e:
                # catastrophic error. bail.
                print(e)
                sys.exit(1)
            break
        return self.r.text
    
    def sendtoken2(self, record):##the same as token2
        self.x = record['Label']
        self.Label2 = self.getLabel2(int(self.x))
        self.timestamp =record['Timestamp']
        self.confidence = record['Confidence']
        #self.confidenceLabel = self.getConfidence(int(self.confidence))
        self.log = {"type": "Drone",
        "distance" : self.Label2,
        "confidence": self.confidence,
        "location": self.location,
        "time": self.timestamp
        }
        while True:
            try:
                # do stuff
                self.r =  requests.post(self.url, data = self.log)
            except requests.exceptions.Timeout:
                # Maybe set up for a retry, or continue in a retry loop
                continue
            except requests.exceptions.RequestException as e:
                # catastrophic error. bail.
                print(e)
                sys.exit(1)
            break
        return self.r.text

    def infosendtoken(self, record, recfname):##tokens are sent using the format in self.log
        self.x = record['Label']
        self.Label = self.getLabel(int(self.x))
        self.timestamp =record['Timestamp']
        self.confidence = record['Confidence']
        #self.confidenceLabel = self.getConfidence(int(self.confidence))
        self.infolog = {"fileName":recfname,#wav file to send
        "length":"10",
        "comment":"ok",
        "distance" : self.Label,
        "confidence": self.confidence,
        "locationRecorded": self.location,#need to change
        "date": self.timestamp
        }
        while True:
            try:
                # do stuff
                self.reqn =  requests.post(self.soundurl, data = self.infolog)
            except requests.exceptions.Timeout:
                # Maybe set up for a retry, or continue in a retry loop
                continue
            except requests.exceptions.RequestException as e:
                # catastrophic error. bail.
                print(e)
                sys.exit(1)
            break
        return self.reqn.text
    
    def wavsendtoken(self, recfname):##tokens are sent using the format in self.log
        # recname = os.path.abspath(os.path.join(os.getcwd(),'../'+recfname))
	# edit the recname file path 
	recname = os.path.abspath(os.path.join(os.getcwd(),recfname))
        self.wavfile = {"file":(recfname, open(recname,'rb'),'application/x-www-form-urlencoded',{'Expires':'0'})}#wav file to send
        while True:
            try:
                # do stuff
                self.sreqn =  requests.post(self.wavurl, files = self.wavfile)
            except requests.exceptions.Timeout:
                # Maybe set up for a retry, or continue in a retry loop
                continue
            except requests.exceptions.RequestException as e:
                # catastrophic error. bail.
                print(e)
                sys.exit(1)
            break
        return self.sreqn.text
        
    
    def getLabel(self,x):
        if x == 0:
            self.label = "far"
        elif x == 1:
            self.label = "midrange"
        elif x == 2:
            self.label = "near"
        elif x == 3:
            self.label = "very_far"
        elif x == 4:
            self.label = "very_near"
        return self.label

    def getLabel1(self,x):
        if x == 0:
            self.label = "far"
        elif x == 1:
            self.label = "midrange"
        elif x == 2:
            self.label = "near"
        elif x == 3 or x == 4:
            self.label = "very_far"
        elif x == 5:
            self.label = "very_near"
        return self.label

    def getLabel2(self,x):
        if x == 0:
            self.label = "far"
        elif x == 1:
            self.label = "midrange"
        elif x == 2:
            self.label = "near"
        elif x == 3:
            self.label = "vnear"
        return self.label
    
    def push_notify(self):##This uses the api Chunge built.
        """
        self.header = {"Content-Type": "application/json; charset=utf-8",
        "Authorization": "Basic NDMyMTM5MjctMzYxZC00OTM3LTkxODEtYjljNDY5OTdmNGE0"}
        self.payload = {"app_id": "2ebe188c-34d4-423f-8c7f-21bd0483fc95",
        "contents": {"en": "Drone Detected!!"},
	    "template_id": "658d2118-ea02-4902-88e0-b708fa2e4fcd",
        "included_segments": ["All"]}
        """

        # Updates of Cary
        self.header = {"Content-Type": "application/json; charset=utf-8",
                       "Authorization": "Basic NTEzMmU2YjAtYTdjOC00OGE0LWI0MWUtM2NiYzA5YmQ5NmU1"}
        self.payload = {"app_id": "e2d74d80-93dd-48f7-879f-ed4cb8cebe5f",
        "contents": {"en": "Drone Detected!!"},
	    "template_id": "8c1498e3-403f-4b94-9a72-9d0ea002e4db",
        "included_segments": ["All"]}

        self.req = requests.post(self.pushurl,headers = self.header,data = json.dumps(self.payload))
        return self.req.text

    
#    def getConfidence(self,y):
#        if y < 50:
#            self.confidencelabel = "Low at \n"+str(y)+"%"
#        elif y >= 50 and y < 85:
#            self.confidencelabel = "Medium at \n"+str(y)+"%"
#        elif y >= 85:
#            self.confidencelabel = "High at \n"+str(y)+"%"
#        return self.confidencelabel


 


