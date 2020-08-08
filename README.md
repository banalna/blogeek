# [Blogeek](https://blogeek.herokuapp.com)
### Home toy social blog project on the Python+Flask+SQL+Elasticsearch+Redis.
##### Demo version [Blogeek](https://blogeek.herokuapp.com) on heroku (Elasticsearch and Redis function is disabled).
##### For start app from docker launch ```run.ps1```. This script run 5 containers (Elasticsearch, MySql, Blogeek app, Redis and redis worker)
### API:
``` api/users [GET, POST]```  
``` api/users/<id> [GET, PUT]```  
``` api/users/<id>/followers [GET]```  
``` api/users/<id>/followed [GET]```