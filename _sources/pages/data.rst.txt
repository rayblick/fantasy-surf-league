Data
=====
Before collecting these data I had a fairly good idea of what I wanted to achieve. Specifically I wanted a leader board containing cumulative point totals and position change information (e.g. drop from 1st to 5th position after x event). All points are to be derived from the event results which needs to include points from bonus rounds.

All data were "manually" collected (not webscrapping) in a partially normalised form by creating three dimensions and two fact tables. The dimensions contain information that are not likely to change throughout the year but there could be some duplication. For example, multiple events can occur in the same country, if I added a country column to the events table then I would not create a countries table. The dimensions include event information, player information (us not the surfers) and round information. The fact tables include picks (player selections) and events (surfer results).  


Files 
------

**Events_DIM.csv**

+ Event id
+ Name
+ Location
+ Country

**Rounds_DIM.csv**

+ Round id
+ Name

**Player_DIM.csv**

+ Player id
+ Name

**Picks_FACT.csv**

+ id
+ Player id
+ Event id
+ Round start #No points for missed rounds e.g. a player makes pick late
+ Surfer Name

**Events_FACT.csv**

+ id
+ Event id
+ Round id
+ Heat Number
+ Surfer Name
+ Score 1
+ Score 2
+ Total heat score
+ Info Flag
+ Notes

