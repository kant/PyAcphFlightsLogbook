
import mysql.connector
from mysql.connector import errorcode

TABLES_NAME = {}
TABLES_NAME['logbook-by-aircraft'] = 'acph_aircraft_logbook'
TABLES_NAME['logbook-by-icao'] = 'acph_icao_logbook'

TABLES = {}
TABLES['logbook-by-aircraft'] = (
	"CREATE TABLE `acph_aircraft_logbook` ("
	"  `date` DATE NOT NULL,"
	"  `aircraft_id` VARCHAR(6) NOT NULL,"
	"  `flight_id` INT NOT NULL,"
	"  `status` VARCHAR(8) NOT NULL,"
	"  `status_last_airport` VARCHAR(4),"
	"  `aircraft_type` VARCHAR(255),"
	"  `aircraft_model` VARCHAR(255),"
	"  `registration` VARCHAR(255),"
	"  `cn` VARCHAR(3),"
	"  `tracked` VARCHAR(1),"
	"  `identified` VARCHAR(1),"
	"  `takeoff_time` DATETIME NULL DEFAULT NULL,"
	"  `takeoff_airport` VARCHAR(4),"
	"  `landing_time` DATETIME NULL DEFAULT NULL,"
	"  `landing_airport` VARCHAR(4),"
	"  `flight_duration` TIME DEFAULT 0,"
	"  `launch_type` VARCHAR(255),"
	"  `receivers` MEDIUMTEXT,"
	"  PRIMARY KEY  (`date`, `aircraft_id`, `flight_id`)"
	") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci")

TABLES['logbook-by-icao'] = (
	"CREATE TABLE `acph_icao_logbook` ("
	"  `date` DATE NOT NULL,"
	"  `icao` VARCHAR(4) NOT NULL,"
	"  `logbook` MEDIUMTEXT,"
	"  PRIMARY KEY (`date`, `icao`)"
	") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci")

def createTables(cursor):
	for table_name in TABLES:
		table_description = TABLES[table_name]
		# print('Table desciption is: {}'.format(table_description))
		try:
			print("  Creating table {}: ".format(table_name), end='')
			cursor.execute(table_description)
		except mysql.connector.Error as err:
			if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
				print("already exists.")
			else:
				print(err.msg)
		else:
			print("OK")

def main():

	print("ACPH LogBook - initialize database tables.")
	try:
		cnx = mysql.connector.connect(option_files='./acph-logbook.ini', option_groups='mysql_connector_python')

		cursor = cnx.cursor()
		createTables(cursor)
		cursor.close()
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is wrong with your user name or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")
		else:
			print(err)
	else:
		cnx.close()

if __name__ == '__main__':
	main()