# Pris

Todo list by June 20 
### PM2  
- [ ] PM2 log files extend recording lines 

- [x] PM2 error log files to store all the error information

      > │ error log path    │ /home/pi/.pm2/logs/main-error.log

- [ ] PM2 error log files add error occurrence time, edit the ecosystem file 

pm2 log management: (http://pm2.keymetrics.io/docs/usage/log-management/)
(https://pm2.io/doc/en/runtime/guide/log-management/)


### Server 
Server information: 

- For all predictions: ../api/..
- For sound file information: (http://mlc67-cmp-00.egr.duke.edu/api/soundInfos)
- For complete javacriptsound files recordings: (http://mlc67-cmp-00.egr.duke.edu/api/sound-clips) 

- [x] Update server location for Carytown test: 
      - For the prison, it is /api/events
      - For Cary, it is /api/caryevents
      
- [x] Server upload files to ../sound-clips
      - apicall.py: def wavsendtoken()
      
      - Directly access url to listen: 
      
      (http://mlc67-cmp-00.egr.duke.edu/api/sound-clips/container/download/sounfile_name.wav)

- [x] Download files to check the recording information: 

      - Directly download through url link 
      - [ ] Download through Postman get requrest 

### Timer 
- [ ] Set up for Pi-3B

- [ ] Set up for Pi-3B+ model 

### Mobile app 
- [x] Check the map update to Carytown

- [x] Check the history information: updates successfully 

- [ ] Check the history information: only store history when detection vnear/ near/ midrange 

- [ ] Check the history information: coherent with the server information, as well as the pm2 log information 

### 2nd round of system test 
- [x] 72hrs test:

      - started on Monday 06/17 10am, with both batteries 25% level 
      
      - Monday weather: 93 F, strong sunshine 
      
      - Stop system at night: 8pm, record battery level  
      
      - Restart system in the morning Tuesday 06/18 7am 
      

- [ ] Record solar panel && battery charging discharging balance 

- [ ] Record the error message 

- [ ] Box hole drill
