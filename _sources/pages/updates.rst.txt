Updating
==========

This project has a manual data entry component. It takes about 30 mins to enter the new records (Fantasy team of 7 players picking 8 surfers). It is important that the names of the surfers match in each csv file. I decided against using an ID key for surfer names because it took longer from continuously double checking my entries, and the convienience of tab completion helped to spot errors immediately. 

Development
--------------

+ Add new data to the csv files (.data/)
+ Run the sqlite fantasy DB ($> sqlite fantasydb) 
+ Rerun the entire sql script (.db/DB_CREATOR.txt) 
+ Copy new DB across to the Django project 
+ Test that the scores match/check typos etc  
+ Modify HTML to include the event selection buttons
+ Update development log if changes are made
+ git push all changes to github

Production
------------

+ git pull changes to git hub repository to Pythonanywhere server
