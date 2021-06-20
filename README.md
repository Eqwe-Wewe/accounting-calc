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
- with writing results:
  - if want to use MySQL:
    - [install MySQL](https://dev.mysql.com/doc/mysql-installation-excerpt/8.0/en/windows-installation.html)
    - configure and launch:
      - create_database.py (if necessary)
      - create_user.py (if necessary)
      - create_table.py
    - configure MySQL login and database to use in config.py
       ```python
          config = {
          'host': '127.0.0.1',
          'user': 'defaultname',
          'password': 'defaultpassword',
          'database': 'defaultdatabase'}
       ```
  - launch main.py
- without writing results:
  - launch main_not_write.py
# Additional Resource:
  [MySQL Connector/Python Developer Guide](https://dev.mysql.com/doc/connector-python/en/)
# How to view the results of calculations:
- csv_viewer.py
- json_viewer.py
- mysql_viewer.py
