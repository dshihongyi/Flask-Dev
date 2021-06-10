>>>Install MySQL

sudo apt-get install mysql-server libmysqlclient-dev
 

------login mysql----

sudo mysql -u root


------create user----

SELECT User,Host FROM mysql.user;

CREATE USER 'daniel'@'localhost' IDENTIFIED BY '**********';

GRANT ALL PRIVILEGES ON myflaskapp.* TO 'daniel'@'localhost';


-----Create DB myflaskapp------

mysql> CREATE DATABASE myflaskapp;

mysql> USE myflaskapp;


-----Create Table Users------

mysql> CREATE TABLE users(id INT(11) AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100), email VARCHAR (100), username VARCHAR(30), password VARCHAR(100), register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);



-----Create Table isp_templates------

CREATE TABLE isp_templates (id INT(11) AUTO_INCREMENT PRIMARY KEY, isp VARCHAR(50), type VARCHAR(50), model VARCHAR(50), site VARCHAR(15), ci_name VARCHAR(50), config longtext, last_editor VARCHAR(100), create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);



mysql> SHOW TABLES;

+----------------------+

| Tables_in_myflaskapp |

+----------------------+

| sw_templates        |

| users               |

+----------------------+



mysql> ALTER TABLE sw_templates

   -> ADD COLUMN site VARCHAR(15) AFTER agent;





mysql> DESCRIBE isp_templates;

mysql> DESCRIBE isp_templates;
+-------------+--------------+------+-----+-------------------+----------------+
| Field       | Type         | Null | Key | Default           | Extra          |
+-------------+--------------+------+-----+-------------------+----------------+
| id          | int(11)      | NO   | PRI | NULL              | auto_increment |
| isp         | varchar(50)  | YES  |     | NULL              |                |
| type        | varchar(50)  | YES  |     | NULL              |                |
| model       | varchar(50)  | YES  |     | NULL              |                |
| site        | varchar(15)  | YES  |     | NULL              |                |
| ci_name     | varchar(50)  | YES  |     | NULL              |                |
| config      | longtext     | YES  |     | NULL              |                |
| last_editor | varchar(100) | YES  |     | NULL              |                |
| create_date | timestamp    | NO   |     | CURRENT_TIMESTAMP |                |
+-------------+--------------+------+-----+-------------------+----------------+
9 rows in set (0.00 sec)




mysql> SELECT * FROM sw_templates;

Empty set (0.04 sec)



mysql> ALTER TABLE sw_templates CHANGE config config MEDIUMTEXT;



mysql> DESCRIBE sw_templates;

+-------------+--------------+------+-----+-------------------+----------------+

| Field      | Type        | Null | Key | Default          | Extra         |

+-------------+--------------+------+-----+-------------------+----------------+

| id         | int(11)     | NO  | PRI | NULL             | auto_increment |

| brand      | varchar(100) | YES |    | NULL             |               |

| type       | varchar(100) | YES |    | NULL             |               |

| model      | varchar(100) | YES |    | NULL             |               |

| IOS        | varchar(255) | YES |    | NULL             |               |

| agent      | varchar(100) | YES |    | NULL             |               |

| site       | varchar(15) | YES |    | NULL             |               |

| ci_name    | varchar(100) | YES |    | NULL             |               |

| config     | longtext    | YES |    | NULL             |               |

| last_editor | varchar(100) | YES |    | NULL             |               |

| create_date | timestamp   | NO  |    | CURRENT_TIMESTAMP |               |

+-------------+--------------+------+-----+-------------------+----------------+

11 rows in set (0.01 sec)



mysql> SELECT ci_name FROM sw_templates;

+-------------------+

| ci_name          |

+-------------------+

| 116-0062-WLG-ASb1 |

+-------------------+

1 row in set (0.00 sec)