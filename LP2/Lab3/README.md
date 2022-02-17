# LP2 Drone Project - Lab 3

Intall the requied Python packages, geopy is added in the list
```
pip3 install -r requirements.txt
```

Open terminal 1, start Redis:
    
    redis-server

Go to `/webserver`, run flask servers:

1. Open terminal 2, run server that for writing data to the redis server
    ```
    export FLASK_APP=database.py
    export FLASK_ENV=development
    flask run --port=5001
    ```
2. Open termibal 3, run route planner
    ```
    export FLASK_APP=route_planner.py
    export FLASK_ENV=development
    flask run --port=5002
    ```

3. Open terminal 4, and run website server
    ```
    export FLASK_APP=build.py
    export FLASK_ENV=development
    flask run
    ```

Note: Don't use `python3 build.py` to run the webserver, since this does not porvide all the functionalities requied by the application.

