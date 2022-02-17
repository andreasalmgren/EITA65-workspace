# LP2 Drone Project - Lab 2
Intall the requied Python packages, redis is added in the list
```
pip3 install -r requirements.txt
```
Go to `/webserver`, start your Redis server and run the two flask servers:

1. Run server that for writing data to the redis server
```
export FLASK_APP=database.py
export FLASK_ENV=development
flask run --port=5001
```
2. Open a new terminal, and run `build.py`
```
export FLASK_APP=build.py
export FLASK_ENV=development
flask run
```

Go to `/pi`, run the Pi controller:
```
python3 pi_controller.py
```
You can replace `pi_controller.py` with the one you created in Part 1, but keep `SERVER_URL` the same as in the file provied in this lab.

Note: Don't user `python3 build.py` to run the webserver, since this does not porvide all the functionalities requied by the application.

