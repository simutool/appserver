# Knowledge  Graph Service and its Web Application

Central unit of the SKM Platform, this project contains two modules:

* The *Knowledge Graph Service (kgservice), and its API interface*: Which is the semantic metadata store at the heart of the SKM Platform.
* The *Web Application* for administration and web access to the contents of the Knowledge Graph. 
* The File server.


## How to install (Debian)

Get web2py source and clone this repo

```shell
foo@bar:~$ mkdir /home/www-data
foo@bar:~$ cd /home/www-data
foo@bar:~$ wget https://mdipierro.pythonanywhere.com/examples/static/web2py_src.zip
foo@bar:~$ unzip web2py_src.zip
foo@bar:~$ rm web2py_src.zip
foo@bar:~$ cd web2py/applications
foo@bar:~$ git clone https://...../simutool/simutool_kms.git
foo@bar:~$ cp simutool_kms/private/appconfig.ini_template  simutool_kms/private/appconfig.ini 
```

Install pip and the required libraries

```shell
foo@bar:~$ apt-get install python-pip -y
foo@bar:~$ python -m pip install --upgrade pip
foo@bar:~$ cd /home/www-data/web2py/applications/simutool_kms
foo@bar:~$ pip install -r requirements.txt
```

Run web2py

```shell
foo@bar:~$ cd /home/www-data/web2py/
foo@bar:~$ python web2py.py --password="[select_a_password]"
```

You can access the the application at http://127.0.0.1:8000/simutool_kms/default/index

The first user login credentials (admin) can be found in `/home/www-data/web2py/applications/simutool_kms/private/appconfig.ini` under `admin_email = XXXX`, `admin_pass = YYYYYY`
