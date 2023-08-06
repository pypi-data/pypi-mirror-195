#######################################################  
#                                                     #
#                 SWAgent Crawler                     #
#                                                     #
#######################################################

This is a simple web crawler specifically designed to 
scrape data from swranking.com continuously in order 
to build a database with data useful enoughn to train
a ML model to make RTA draft predictions in real time.

The package contains two helper classes: 

    - USERAGENT: creates randomized user_agents to
send through the REST request t obtain data from the
websites API.

    - SEEKER: this is the actual crawler that finds
the information for us and then sends it out as a 
json object.

The package main routine focuses on a basic ETL 
schema. afte obtaining the data from the seeker object
it then transfoms the data to be in the format wanted
by the Database. Then we send it to the local db of
the VM to store for further processing by other jobs.

