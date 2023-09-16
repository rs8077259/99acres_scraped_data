# 99acres_scraped_data
django project extract data from web and push it to mogodb in every 11.5 haours

libarary used
      django
      requests
      BeautifulSoup
      pymongo
      selenium
      ...

to run this project you have to add mogodb "URI" in utils.py file in "Mongoclient" function

additionally if you want to activate cron job 
run command 
      "python3 manage.py crontab add"

finally to run the server run
      "python3 manage.py runserver"
