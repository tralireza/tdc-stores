TDC-Stores
===

This is a Python based api and cli that implements the requirement for 
the software engineer task. It runs inside Docker.

A bash script "**run.sh**" has been provided
to allow building the docker image, running the tests 
and api server as well as running the cli.

The directory structure can be cloned from github:

git clone https://github.com/AlirezaTorabi/tdc-stores


### TL;DR
1. ./run.sh build && ./run.sh test && ./run.sh api

Once the api server is running in another terminal or a browser:


1. curl http://127.0.0.1:5000/stores/admin/load_database

    Loads the geo data from postcodes.io.
    
2. curl http://127.0.0.1:5000/stores

    Lists all the stores with the their geo data in 
    alphabetical order.
    
3. curl http://127.0.0.1:5000/stores/al12rj/circle?q=17 
(curl http://127.0.0.1:5000/stores/al12rj/circle?q=17km for Kilometer)

    Searches for all stores within **17 miles** from the 
    postcode **AL1 2RJ** sorted from north to south.

4. curl http://127.0.0.1:5000/stores/admin/reset_database

    Resets the stores to only their name and postcode data, 
    ie removing the geo data.

5. curl http://127.0.0.1:5000/stores/admin/load_database
    
    Reloads the geo data updating records if necessary while 
    allowing the readers to list or search on the exiting data.
    
    (could be done the same time as 4)


## Requirements


### Bash

To run "run.sh" bash script for building the Docker image and running 
the code. Available in Mac terminal or Linux terminal.

<pre>
$ bash --version
GNU bash, version 3.2.57(1)-release (x86_64-apple-darwin18)
Copyright (C) 2007 Free Software Foundation, Inc. 
</pre>


### Docker

Code has been packaged into a Docker container which means it requires 
the Docker on the machine running it. Docker CE (Community Edition) is 
freely available on

* Mac: https://docs.docker.com/docker-for-mac/install/
* Linux: https://docs.docker.com/install/

<pre>
$ docker version
Client: Docker Engine - Community
 Version:           19.03.1
 API version:       1.40
 Go version:        go1.12.5
 Git commit:        74b1e89
 Built:             Thu Jul 25 21:18:17 2019
 OS/Arch:           darwin/amd64
 Experimental:      false

Server: Docker Engine - Community
 Engine:
  Version:          19.03.1
  API version:      1.40 (minimum version 1.12)
  Go version:       go1.12.5
  Git commit:       74b1e89
  Built:            Thu Jul 25 21:17:52 2019
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          v1.2.6
  GitCommit:        894b81a4b802e4eb2a91d1ce216b8817763c29fb
 runc:
  Version:          1.0.0-rc8
  GitCommit:        425e105d5a03fabd737a126ad93d62a9eeede87f
 docker-init:
  Version:          0.18.0
  GitCommit:        fec3683
</pre>

### Internet connectivity

During building the Docker image,
running tests (while testing fetching data from postcodes.io) and 
while loading the database during run.

## Directory Structure

After cloning the repository or un-zipping the archive the 
directory structure is looking like this:

<pre>
$ ls -l
total 56
-rw-r--r--  1 alireza  staff     688 18 Sep 12:34 Dockerfile
-rw-r--r--  1 alireza  staff    1872 18 Sep 15:22 Finally.md
-rw-r--r--  1 alireza  staff    5138 18 Sep 15:25 README.md
-rw-r--r--@ 1 alireza  staff  268147 18 Sep 15:19 Shoei.jpg
drwxr-xr-x  5 alireza  staff     160 18 Sep 14:50 api
drwxr-xr-x  3 alireza  staff      96 18 Sep 09:06 cli
-rw-r--r--  1 alireza  staff     293 18 Sep 10:26 docker-entrypoint.sh
drwxr-xr-x  6 alireza  staff     192 18 Sep 14:34 lib
drwxr-xr-x  2 alireza  staff      64 18 Sep 13:16 output
-rw-r--r--  1 alireza  staff      91 18 Sep 09:35 pytest.ini
-rwxr-x---  1 alireza  staff    1175 18 Sep 13:16 run.sh
-rw-r--r--  1 alireza  staff     286 18 Sep 18:31 requirements.txt
-rw-r--r--  1 alireza  staff     124 18 Sep 11:53 stores-subset.json
-rw-r--r--  1 alireza  staff    5760 17 Sep 19:39 stores.json
drwxr-xr-x  7 alireza  staff     224 18 Sep 14:41 tests
</pre>


## Building & Running

* Make sure the bash script "run.sh" in the top directory is executable by running 
<pre>
$ chmod 750 run.sh
$ ls -l run.sh
-rwxr-x---  1 alireza  staff  1305 18 Sep 09:23 run.sh
$ ./run.sh
# ---
# version: Show Docker Image Version
# build: Build Docker Image
# api: Run API Server
# cli: Run CLI
# test: Run tests
# ---
</pre>

* Building the Docker image
<pre>
$ ./run.sh build
...
Successfully built 1c59928422ec
Successfully tagged tdc-stores:latest
tdc-stores                                     latest              1c59928422ec        17 minutes ago      94.4MB
</pre>

* Running the tests
<pre>
$ ./run.sh test
...
</pre>

* Running api server (could interrupt and stop the api server by pressing CTRL+C at any time)
<pre>
$ ./run.sh api
 * Serving Flask app "api" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
2019-09-18 14:47:03 INFO werkzeug|_internal|_log|122  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
2019-09-18 14:47:03 INFO werkzeug|_internal|_log|122  * Restarting with stat
2019-09-18 14:47:03 WARNING werkzeug|_internal|_log|122  * Debugger is active!
2019-09-18 14:47:03 INFO werkzeug|_internal|_log|122  * Debugger PIN: 247-169-878...
</pre>

* Running CLI (allows to list all the store with or without 
geo data and searching for all stores within distance (miles/km) 
from a postcode)
<pre>
$ ./run.sh cli -h
usage: cli [-h] [-v] [-g] [-p postcode] [-d distance] action
...
$ ./run.sh cli -g list
...
  {
    "name": "Wokingham",
    "postcode": "RG40 2NU",
    "longitude": -0.837922,
    "latitude": 51.405767
  },
...
$ ./run.sh cli -p rg402nu -d 10 search
[
  {
    "name": "Bracknell",
    "postcode": "RG12 1EN",
    "longitude": -0.755313,
    "latitude": 51.414577,
    "distance": 4
  },
...
  {
    "name": "Winnersh",
    "postcode": "RG41 5HH",
    "longitude": -0.894323,
    "latitude": 51.435581,
    "distance": 3
  }
]
</pre>


## API Endpoints
<pre>
Endpoint              Methods  Path
--------------------  -------  ----------------------------
stores.get            GET      /stores/< postcode >
stores.load_database  GET      /stores/admin/reset_database
stores.load_database  GET      /stores/admin/load_database
stores.search         GET      /stores/< postcode >/circle?q=< radius [m|km]>
stores.stores         GET      /stores
</pre>
