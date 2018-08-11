# statsbomb-womens-datasette

In-Progress work to turn StatsBomb's JSON files into CSVs and SQLite database for analysis. The Travis-CI build will pull the files, build the database, and then push back into the repo, keeping it up-to-date (every 24h). This also uses [CSVs-to-SQLite](https://github.com/simonw/csvs-to-sqlite) to convert the generated CSVs and then [Datasette](https://github.com/simonw/datasette/) to analyse the data. (both by Simon Willison). 

![alt text](https://github.com/statsbomb/open-data/raw/master/img/statsbomb-logo.jpg "StatsBomb")

If you fork or download this repo, please sign up with them to get updates! https://github.com/statsbomb/open-data

## Some example SQL commands and results:

Top 5 performances in the dataset (as of August 11)
```sql
select sum(shot_xg), count(shot_xg), sum(case when (shot_result_id = "Goal") then 1 else 0 end) goals, team_name, match_id from events group by team_id,match_id order by sum(shot_xg) desc limit 5;

-- sum(shot_xg)  count(shot_xg)  goals       team_name               match_id  
-- ------------  --------------  ----------  ----------------------  ----------
-- 5.055359992   25              4           North Carolina Courage  7484      
-- 4.85068797    18              4           North Carolina Courage  7519      
-- 4.785423994   23              2           Orlando Pride           7492      
-- 4.227053421   26              3           North Carolina Courage  7457      
-- 3.9535856346  25              2           Chelsea LFC             7298     
```

Match 7484 had a strong performance by NCC, let's dive deeper:

```sql
select team_id, team_name, sum(shot_xg) from events where match_id = 7484 group by team_id order by team_id;

-- team_id	team_name	    sum(shot_xg)  goals
-- 763	    Sky Blue FC  	1.294180172   0
-- 766	    NCC         	5.055359992   4
```

North Carolina won 4-0 over Sky Blue, let's take a look at those shots:
```sql
select team_id, group_concat(shot_xg) from events where match_id = 7484 group by team_id order by team_id;
Sky Blue:
0.07350879,0.1796834,0.27943647,0.038806017,0.011712668,0.26406175,0.24766278,0.086957514,0.007751182,0.0066016633,0.0046319677,0.09336597
North Carolina: 0.05631416,0.17085318,0.09822809,0.3465824,0.2865825,0.046823706,0.30133966,0.32593086,0.58293796,0.016741328,0.020553188,0.035217896,0.032307904,0.09717659,0.07574744,0.6563366,0.016718904,0.34044597,0.034964826,0.014901155,0.3784764,0.41904968,0.016814005,0.51733595,0.16697964
```

View those shot results in the [Match xG Simulator](http://dannypage.github.io/expected_goals.html?share=AwOmFYDYGYEYBZaQDSlgdmADnHLqwBOLAJhK2EIOnknFPgPLtPAOFtOkxVGmFjRohSLxDQS4Qvyxj6JaehHsk6RBPyhgJCLlhZNYaOBIYsyrRP5KO7Qugx0qW9ODVrGoOjGiiVkB3NbPngOeCl0dhoReFIxAXhCAVhwNj50LHh0SE8QRCTEyEMBIoRgCAJwDCEpNJAkSHsYgB8XY2wlAgwRLBomJXhfLKiDYEgBSK1YDFgSUUM50MgMOpIs0RIM9llCNyrc8vRXadJ2MfGGoTPaOBEjuyEndCA).

North Carolina winning by 4 was the most likely result, though they could have easily scored more. 

||**Goals**|**M_A_Dev**|**Shots**|**Win%**|**PPG**
:-----:|:-----:|:-----:|:-----:|:-----:|:-----:
TeamA:|5.06|±1.39|25|95%|2.88
TeamB:|1.29|±0.83|12|2%|0.08
