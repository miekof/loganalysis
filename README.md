# Log Analysis 
Log Analysis reads the data from the database displays the following information.
* The top 3 most popular articles and their number of views
* The most popular authors and their number of views
* Dates when fail rate exceeds 1 %

# Installation & Requirements
* Python 3 
* Database (This should be downloaded from Udacity's site)

# Usage
```bash
python logAnalysis.py
```

# Database views
Following views must be created in order to run the application correctly. 
```mysql-psql
CREATE VIEW fails AS
SELECT to_char(time, 'Mon D, YYYY') as date, count(*) as fails from log where status not like '200%' GROUP BY date;

CREATE VIEW total as
SELECT to_char(time, 'Mon D, YYYY') as date, count(*) as total from log GROUP BY date;
```