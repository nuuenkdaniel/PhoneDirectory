Phone directory to help store contact information

### Python Packages ###
* Flask
* mariadb

### Venv setup ###
```
paru -S python
paru -S python-pip
python -m venv phone_dir
source phone_dir/bin/activate
pip install Flask
pip install mariadb
```

### Running the website ###
```
python main.py
```
Make sure you are in the venv before you execute main

### Extra info ###
* You don't need multiple tables. I just have multiple tables because I wanted to see what JOIN does
