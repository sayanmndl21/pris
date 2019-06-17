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
- [ ] Check the map update to Carytown

- [ ] Check the history information 

### 2nd round of system test 
- [ ] 72hrs test 

- [ ] Record solar panel && battery charging discharging balance 

- [ ] Record the error message 

- [ ] Box hole drill
