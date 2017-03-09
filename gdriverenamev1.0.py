#!/usr/bin/env python

# scans through all files on the authorised GDRIVE account and renames
# duplicates with the same name plus --DUP-- and a datetime string
#
# comfort markers of a * are printed for each file reviewed
# files are reviewed in batches, and a line is printed for each new batch started
# when duplicates are found, the file name and two file ids are printed
#
# the client_secrets.json file must be present in same directory
# containing the GDRIVE API key required for access to GDRIVE

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from datetime import datetime

# firstly, authorise the google account owning the gdrive to be deduped
gauth = GoogleAuth()
gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.

# access the drive to be deduped
drive = GoogleDrive(gauth)

# write a file to the gdrive recording in the title that this script has run
file0 = drive.CreateFile()
file0['title'] = 'pydedupe-'+datetime.now().strftime("%Y%m%d%H%M%S")
# {'convert': True} triggers conversion to a Google Drive document.
file0.Upload({'convert': True})

# to check for duplicates, need to have copy of the 'previous' filename in a loop, so fake it for first pass
file0['title'] = '' # null so duplicate comparison fails if this is first file!
 
# loop through each file name in batches (paginated)
for file_list in drive.ListFile({'q': 'trashed=false', 'maxResults': 500}):
  print('Received %s files from Files.list()' % len(file_list)) # so user knows something is happening
  for file1 in file_list:
      print('*',end='') # comfort marker for use on each file being processed
      if(file0['title']==file1['title']):
          print('\nDUP: %s, ids: %s & %s' % (file0['title'], file0['id'], file1['id'])) # tell user about duplicate
          file1['title']=file1['title']+'---DUP---'+datetime.now().strftime("%Y%m%d%H%M%S%f") # rename second file
          file1.Upload()
          # keep backmarker (previous filename) the same in case there is another duplicate, and move on to next file
      else:
          file0 = file1 # no duplicate so move backmarker (previous filename) forward one file, and move on to next file
  print('')
