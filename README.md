"# covid19_fesh" 
## Notes on using the python package

- This app was made to run on python 3.7. Other versions >3.7 should work.
- After forking or downloading the repo, go into the folder 'covid19_fesh' and activate the virtual environment
  *..\covid19_fesh>Scripts\activate* (Windows)
  *source ..\covid19_fesh$Scripts/activate* (Unix)
- Go ahead and run the python file to retrieve info from ArcGIS with JHU data
  *(covid_env)...\covid19_fesh>python covid_fesh_v2.py* (Windows)
  *(covid_env)...\covid19_fesh>python3 covid_fesh_v2.py* (Unix)
- If all goes well, your retrieved data will be in the data folder.
- The script opens a chrome browser and loads the target webpage, sleeps to hold it for a while for the page to load. Adjust the sleep time on line 20 to suit your internet speed constraints.
- The script reads the page source and closes the browser instance it started. If the page finished loading, data will be pulled successfully otherwise there will be an error as the operation on the expected contents will fail. If so, the script ends and you will need to restart it.
- You can run this script daily to get latest world figures: historic and current infection rates and vaccine coverage. PS: The script makes a new file of the data each time it is run, named according to the day's date and run time.

### In case you want to make your own virtual environment
- If you make your own virtual environment, install the dependencies in the requirements file.
  *pip install -r requirements.txt*

  PS: Should you have issues working with the Chrome driver in the folder, check the version of your Chrome and download the the matching version from
  https://chromedriver.storage.googleapis.com/index.html
  At the time of this update the version was 100.0.4896.60 for Windows