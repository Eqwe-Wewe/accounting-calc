# Accounting calculator with the style of an [Epson PX-8](https://en.wikipedia.org/wiki/Epson_PX-8_Geneva) Vintage Laptop
![](docs/Screenshot.png)<br>
Designed for standard accounting calculations.<br>
Gui powered by PyQt5.<br>
 # Features:
 - showing the entered operation
 - write calculations results in CSV, JSON, MySQL database
 - 12-digit display
 - arithmetic calculations
 - percentage calculations
 - memory
 # For running application:
 * Python 3.8.6
 * [PyQt5](https://pypi.org/project/PyQt5/)
 * [mysql-connector](https://pypi.org/project/mysql-connector/)
 * [MySQL](https://dev.mysql.com/downloads/)
 # How to use:
 - if you want use database then configure MySQL login and database to use in config.py
    ```python
    config = {'host': '127.0.0.1',
              'user': 'defaultname',
              'password': 'defaultpassword',
              'database': 'defaultdatabase'}
    ```
 - launch main.py
# How to view the results of calculations:
- csv_viewer.py
- json_viewer.py
- mysql_viewer.py
