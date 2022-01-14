import sqlite3
import time
import csv 
import os

class DataModel():
    
    def __init__(self, filename):
        self.filename = filename
        try:
            self.con = sqlite3.connect(filename)
            self.con.row_factory = sqlite3.Row 
            self.cursor = self.con.cursor()
            print("Successful connection to database", filename)
            sqlite_select_Query = "select sqlite_version();"
            self.cursor.execute(sqlite_select_Query)
            record = self.cursor.fetchall()
            for rec in record:
                print("SQLite Database Version is: ", rec[0])
        except sqlite3.Error as error:
            print("Error while connecting to database: ", error)
    
    def close(self):
        self.con.commit()
        self.con.close()
    
    def executeSQL(self, query, show=False):
        try:
            t1 = time.perf_counter()
            for statement in query.split(";"):
                if statement.strip():
                    self.cursor.execute(statement)
                    sql_time = time.perf_counter() - t1
                    print("Query executed.")
            if show:
                for row in self.cursor.fetchall():
                    print(", ".join([str(item)for item in row]))
            self.con.commit()
            return True
        except sqlite3.Error as error:
            print(f"Error while executing query: ", error)
            return False

    def createTable(self, sql): 
        self.cursor.execute(sql)

    def readTable(self, table):
        
        try:
            query = f'''SELECT * FROM {table};'''
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            result = []
            for row in records:
                result.append(dict(row))
            return result
        except sqlite3.Error as error:
            print(f"Error while loading table: {table}", error)

    def insert(self, sql, row): 
        self.cursor.execute(sql, row)

if __name__ == "__main__":

    real_path = os.path.realpath(__file__)
    path  = os.path.dirname(real_path)
    path_data = str(path) + "\data"
    path_db = str(path) + "\zoo.db"

    if (os.path.exists(path_db) == True): 
        filename = "zoo.db"
        open(filename, 'w').close()
        print("File rewritten.")

    
    dbfile = "zoo.db"
    d = DataModel(dbfile) 

    def load_ANIMAL():
        with open(path_data+'\ANIMAL.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=";", quotechar='"')
            create = '''CREATE TABLE "ANIMAL" (
                        "Animal_ID"	TEXT NOT NULL,
                        "Name"	TEXT,
                        "Sex"	TEXT,
                        "Age"	INTEGER,
                        "Date_of_birth"	INTEGER,
                        "Origin"	TEXT,
                        "Date_of_arrival"	INTEGER,
                        "Diseases"	TEXT,
                        "Species_ID"	TEXT NOT NULL,
                        "Diet_program_code"	TEXT,
                        "Medication_code"	TEXT,
                        "Space_code"	TEXT,
                        PRIMARY KEY("Animal_ID"),
                        FOREIGN KEY("Species_ID") REFERENCES "SPECIES"("Species_ID"),
                        FOREIGN KEY("Diet_program_code") REFERENCES "DIET_PROGRAM"("Diet_program_code"),
                        FOREIGN KEY("Medication_code") REFERENCES "MEDICATION"("Medication_code"),
                        FOREIGN KEY("Space_code") REFERENCES "SPACE"("Space_code")
                    );'''

            d.createTable(create)
            for row in reader:
                sql = f'INSERT INTO ANIMAL VALUES("{row["Animal_ID"]}", "{row["Name"]}","{row["Sex"]}", "{row["Age"]}", "{row["Date_of_birth"]}", "{row["Origin"]}", "{row["Date_of_arrival"]}", "{row["Diseases"]}", "{row["Species_ID"]}", "{row["Diet_program_code"]}", "{row["Medication_code"]}", "{row["Space_code"]}");\n'             
                d.insert(sql, row)   

    def load_ANIMAL_CARE_EMPLOYEE(): 
        with open(path_data+'\ANIMAL_CARE_EMPLOYEE.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=";", quotechar='"')
            create = '''CREATE TABLE "ANIMAL_CARE_EMPLOYEE" (
                        "Animal_care_emp_ID"	TEXT NOT NULL,
                        "Emp_category"	TEXT,
                        PRIMARY KEY("Animal_care_emp_ID"),
                        FOREIGN KEY("Animal_care_emp_ID") REFERENCES "EMPLOYEE"("Employee_ID")
                    );'''

            d.createTable(create)
            for row in reader:
                sql = f'INSERT INTO ANIMAL_CARE_EMPLOYEE VALUES("{row["Animal_care_emp_ID"]}", "{row["Emp_category"]}");\n'
                d.insert(sql, row)  

    def load_CARD_OWNER(): 
        with open(path_data+'\CARD_OWNER.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=";", quotechar='"')
            create = '''CREATE TABLE "CARD_OWNER" (
                        "Owner_ID"	TEXT NOT NULL,
                        "Name"	TEXT,
                        "Status"	TEXT,
                        "Visits"	INTEGER,
                        "TelNumber"	INTEGER,
                        "Card_code"	TEXT NOT NULL,
                        PRIMARY KEY("Owner_ID"),
                        FOREIGN KEY("Card_code") REFERENCES "YEARLY_CARD"("Card_code")
                    );'''

            d.createTable(create)
            for row in reader:
                sql = f'INSERT INTO CARD_OWNER VALUES("{row["Owner_ID"]}", "{row["Name"]}", "{row["Status"]}", "{row["Visits"]}", "{row["TelNumber"]}", "{row["Card_code"]}");\n'
                d.insert(sql, row)    

    def load_CUSTOMER_SUPPORT(): 
        with open(path_data+'\CUSTOMER_SUPPORT.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=";", quotechar='"')
            create = '''CREATE TABLE "CUSTOMER_SUPPORT" (
                        "CustSup_emp_ID"	TEXT NOT NULL,
                        "Emp_category"	TEXT,
                        PRIMARY KEY("CustSup_emp_ID"),
                        FOREIGN KEY("CustSup_emp_ID") REFERENCES "EMPLOYEE"("Employee_ID")
                    );'''

            d.createTable(create)
            for row in reader:
                sql = f'INSERT INTO CUSTOMER_SUPPORT VALUES("{row["CustSup_emp_ID"]}", "{row["Emp_category"]}");\n'
                d.insert(sql, row) 

    def load_DIET_PROGRAM(): 
        with open(path_data+'\DIET_PROGRAM.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=";", quotechar='"')
            create = '''CREATE TABLE "DIET_PROGRAM" (
                        "Diet_program_code"	TEXT NOT NULL,
                        "Start_date"	INTEGER,
                        "End_date"	INTEGER,
                        PRIMARY KEY("Diet_program_code")
                    );'''

            d.createTable(create)
            for row in reader:
                sql = f'INSERT INTO DIET_PROGRAM VALUES("{row["Diet_program_code"]}", "{row["Start_date"]}", "{row["End_date"]}");\n'             
                d.insert(sql, row)

    def load_EMPLOYEE(): 
        with open(path_data+'\EMPLOYEE.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=";", quotechar='"')
            create = '''CREATE TABLE "EMPLOYEE" (
                        "Employee_ID"	TEXT NOT NULL,
                        "Name"	TEXT,
                        "Address"	TEXT,
                        "TelNumber"	INTEGER,
                        "Work_hours"	TEXT,
                        PRIMARY KEY("Employee_ID")
                    );'''

            d.createTable(create)
            for row in reader:
                sql = f'INSERT INTO EMPLOYEE VALUES("{row["Employee_ID"]}", "{row["Name"]}", "{row["Address"]}", "{row["TelNumber"]}", "{row["Work_hours"]}");\n'
                d.insert(sql, row)

    def load_ENTRANCE_DOCUMENT(): 
        with open(path_data+'\ENTRANCE_DOCUMENT.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=";", quotechar='"')
            create = '''CREATE TABLE "ENTRANCE_DOCUMENT" (
                        "Document_code"	TEXT NOT NULL,
                        "Price"	TEXT,
                        "Reservation_number"	TEXT,
                        "Sale_code"	TEXT,
                        FOREIGN KEY("Sale_code") REFERENCES "SALE_CATEGORY"("Sale_code"),
                        PRIMARY KEY("Document_code"),
                        FOREIGN KEY("Reservation_number") REFERENCES "RESERVATION"("Reservation_number")
                    );'''

            d.createTable(create)
            for row in reader:
                sql = f'INSERT INTO ENTRANCE_DOCUMENT VALUES("{row["Document_code"]}", "{row["Price"]}", "{row["Reservation_number"]}", "{row["Sale_code"]}");\n'
                d.insert(sql, row)

    def load_EVENT(): 
        with open(path_data+'\EVENT.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=";", quotechar='"')
            create = '''CREATE TABLE "EVENT" (
                        "Event_code"	TEXT NOT NULL,
                        "Name"	TEXT,
                        "Start_time"	TEXT,
                        "Duration"	TEXT,
                        "Weekly_program"	TEXT,
                        "Event_space_code"	TEXT,
                        FOREIGN KEY("Event_space_code") REFERENCES "EVENT"("Event_code"),
                        PRIMARY KEY("Event_code")
                    );'''

            d.createTable(create)
            for row in reader:
                sql = f'INSERT INTO EVENT VALUES("{row["Event_code"]}", "{row["Name"]}", "{row["Start_time"]}", "{row["Duration"]}", "{row["Weekly_program"]}", "{row["Event_space_code"]}");\n'             
                d.insert(sql, row)

    def load_FOOD_SUPPLY(): 
        with open(path_data+'\FOOD_SUPPLY.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=";", quotechar='"')
            create = '''CREATE TABLE "FOOD_SUPPLY" (
                        "Food_supply_code"	TEXT NOT NULL,
                        FOREIGN KEY("Food_supply_code") REFERENCES "SUPPLY"("Supply_code"),
                        PRIMARY KEY("Food_supply_code")
                    );'''

            d.createTable(create)
            for row in reader:
                sql = f'INSERT INTO FOOD_SUPPLY VALUES("{row["Food_supply_code"]}");\n'             
                d.insert(sql, row)

    def load_FOOD_TYPE(): 
        with open(path_data+'\FOOD_TYPE.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=";", quotechar='"')
            create = '''CREATE TABLE "FOOD_TYPE" (
                        "Food_type_code"	TEXT NOT NULL,
                        "Name"	TEXT,
                        "Stock"	TEXT,
                        PRIMARY KEY("Food_type_code")
                    );'''

            d.createTable(create)
            for row in reader:
                sql = f'INSERT INTO FOOD_TYPE VALUES("{row["Food_type_code"]}", "{row["Name"]}", "{row["Stock"]}");\n'             
                d.insert(sql, row)

    def load_MEDICATION(): 
        with open(path_data+'\MEDICATION.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=";", quotechar='"')
            create = '''CREATE TABLE "MEDICATION" (
                        "Medication_code"	TEXT NOT NULL,
                        "Start_date"	INTEGER,
                        "End_date"	INTEGER,
                        PRIMARY KEY("Medication_code")
                    );'''

            d.createTable(create)
            for row in reader:
                sql = f'INSERT INTO MEDICATION VALUES("{row["Medication_code"]}", "{row["Start_date"]}", "{row["End_date"]}");\n'
                d.insert(sql, row)

    def load_MEDICINE(): 
        with open(path_data+'\MEDICINE.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=";", quotechar='"')
            create = '''CREATE TABLE "MEDICINE" (
                        "Medicine_code"	TEXT NOT NULL,
                        "Stock (pcs)"	TEXT,
                        "Name"	TEXT,
                        PRIMARY KEY("Medicine_code")
                    );'''

            d.createTable(create)
            for row in reader:
                sql = f'INSERT INTO MEDICINE VALUES("{row["Medicine_code"]}", "{row["Stock (pcs)"]}", "{row["Name"]}");\n'
                d.insert(sql, row)

    def load_MEDICINE_SUPPLY(): 
        with open(path_data+'\MEDICINE_SUPPLY.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=";", quotechar='"')
            create = '''CREATE TABLE "MEDICINE_SUPPLY" (
                        "Medicine_supply_code"	TEXT NOT NULL,
                        FOREIGN KEY("Medicine_supply_code") REFERENCES "SUPPLY"("Supply_code"),
                        PRIMARY KEY("Medicine_supply_code")
                    );'''

            d.createTable(create)
            for row in reader:
                sql = f'INSERT INTO MEDICINE_SUPPLY VALUES("{row["Medicine_supply_code"]}");\n'
                d.insert(sql, row)

    def load_RESERVATION(): 
        with open(path_data+'\RESERVATION.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=";", quotechar='"')
            create = '''CREATE TABLE "RESERVATION" (
                        "Reservation_number"	TEXT NOT NULL,
                        "Name"	TEXT,
                        "Reservation_date"	INTEGER,
                        "Num_of_visitors"	INTEGER,
                        PRIMARY KEY("Reservation_number")
                    );'''

            d.createTable(create)
            for row in reader:
                sql = f'INSERT INTO RESERVATION VALUES("{row["Reservation_number"]}", "{row["Name"]}", "{row["Reservation_date"]}", "{row["Num_of_visitors"]}");\n'
                d.insert(sql, row)

    def load_SALE_CATEGORY(): 
        with open(path_data+'\SALE_CATEGORY.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=";", quotechar='"')
            create = '''CREATE TABLE "SALE_CATEGORY" (
                        "Sale_code"	TEXT NOT NULL,
                        "Required_documents"	TEXT,
                        "Sale_percentage"	TEXT,
                        PRIMARY KEY("Sale_code")
                    );'''

            d.createTable(create)
            for row in reader:
                sql = f'INSERT INTO SALE_CATEGORY VALUES("{row["Sale_code"]}", "{row["Required_documents"]}", "{row["Sale_percentage"]}");\n'
                d.insert(sql, row)

    def load_SPACE(): 
        with open(path_data+'\SPACE.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=";", quotechar='"')
            create = '''CREATE TABLE "SPACE" (
                        "Space_code"	TEXT NOT NULL,
                        "Name"	TEXT,
                        "Location"	TEXT,
                        "Op_hours"	TEXT,
                        PRIMARY KEY("Space_code")
                    );'''

            d.createTable(create)
            for row in reader:
                sql = f'INSERT INTO SPACE VALUES("{row["Space_code"]}", "{row["Name"]}", "{row["Location"]}", "{row["Op_hours"]}");\n'             
                d.insert(sql, row)

    def load_SPACE_EMPLOYEE(): 
        with open(path_data+'\SPACE_EMPLOYEE.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=";", quotechar='"')
            create = '''CREATE TABLE "SPACE_EMPLOYEE" (
                        "Space_emp_ID"	TEXT NOT NULL,
                        "Emp_category"	TEXT,
                        FOREIGN KEY("Space_emp_ID") REFERENCES "EMPLOYEE"("Employee_ID"),
                        PRIMARY KEY("Space_emp_ID")
                    );'''

            d.createTable(create)
            for row in reader:
                sql = f'INSERT INTO SPACE_EMPLOYEE VALUES("{row["Space_emp_ID"]}", "{row["Emp_category"]}");\n'
                d.insert(sql, row)
        
    def load_SPECIES(): 
        with open(path_data+'\SPECIES.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=";", quotechar='"')
            create = '''CREATE TABLE "SPECIES" (
                        "Species_ID"	TEXT NOT NULL,
                        "Name"	TEXT,
                        "Scientific_name"	TEXT,
                        "Category"	TEXT,
                        "Diet_type"	TEXT,
                        "Natural_environment"	TEXT,
                        PRIMARY KEY("Species_ID")
                    );''' 

            d.createTable(create)
            for row in reader:
                sql = f'INSERT INTO SPECIES VALUES("{row["Species_ID"]}", "{row["Name"]}", "{row["Scientific_name"]}", "{row["Category"]}", "{row["Diet_type"]}", "{row["Natural_environment"]}");\n'             
                d.insert(sql, row)

    def load_SUPPLIER(): 
        with open(path_data+'\SUPPLIER.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=";", quotechar='"')
            create = '''CREATE TABLE "SUPPLIER" (
                        "Supplier_ID"	TEXT NOT NULL,
                        "Name"	TEXT,
                        "HQ"	TEXT,
                        "Supply_category"	TEXT,
                        "TelNum"	TEXT,
                        "E-mail"	TEXT,
                        "Description"	TEXT,
                        PRIMARY KEY("Supplier_ID")
                    );''' 

            d.createTable(create)
            for row in reader:
                sql = f'INSERT INTO SUPPLIER VALUES("{row["Supplier_ID"]}", "{row["Name"]}", "{row["HQ"]}", "{row["Supply_category"]}", "{row["TelNum"]}", "{row["E-mail"]}", "{row["Description"]}");\n'
                d.insert(sql, row)

    def load_SUPPLY(): 
        with open(path_data+'\SUPPLY.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=";", quotechar='"')
            create = '''CREATE TABLE "SUPPLY" (
                        "Supply_code"	TEXT NOT NULL,
                        "Supply_date"	INTEGER,
                        "Price"	TEXT,
                        "Supplier_ID"	TEXT,
                        FOREIGN KEY("Supplier_ID") REFERENCES "SUPPLIER"("Supplier_ID"),
                        PRIMARY KEY("Supply_code")
                    );''' 

            d.createTable(create)
            for row in reader:
                sql = f'INSERT INTO SUPPLY VALUES("{row["Supply_code"]}", "{row["Supply_date"]}", "{row["Price"]}", "{row["Supplier_ID"]}");\n'
                d.insert(sql, row)

    def load_TICKET(): 
        with open(path_data+'\TICKET.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=";", quotechar='"')
            create = '''CREATE TABLE "TICKET" (
                        "Ticket_code"	TEXT NOT NULL,
                        "Ticket_date"	INTEGER,
                        FOREIGN KEY("Ticket_code") REFERENCES "ENTRANCE_DOCUMENT"("Document_code"),
                        PRIMARY KEY("Ticket_code")
                    );'''

            d.createTable(create)
            for row in reader:
                sql = f'INSERT INTO TICKET VALUES("{row["Ticket_code"]}", "{row["Ticket_date"]}");\n'
                d.insert(sql, row)

    def load_YEARLY_CARD(): 
        with open(path_data+'\YEARLY_CARD.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=";", quotechar='"')
            create = '''CREATE TABLE "YEARLY_CARD" (
                        "Card_code"	TEXT NOT NULL,
                        "Start_date"	INTEGER,
                        "End_date"	INTEGER,
                        FOREIGN KEY("Card_code") REFERENCES "ENTRANCE_DOCUMENT"("Document_code"),
                        PRIMARY KEY("Card_code")
                    );'''

            d.createTable(create)
            for row in reader:
                sql = f'INSERT INTO YEARLY_CARD VALUES("{row["Card_code"]}", "{row["Start_date"]}", "{row["End_date"]}");\n'
                d.insert(sql, row)

    def load_belongs_in_diet(): 
        with open(path_data+'\\belongs_in_diet.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=";", quotechar='"')
            create = '''CREATE TABLE "belongs_in_diet" (
                        "Food_type_code"	TEXT NOT NULL,
                        "Diet_program_code"	TEXT NOT NULL,
                        FOREIGN KEY("Food_type_code") REFERENCES "FOOD_TYPE"("Food_type_code"),
                        FOREIGN KEY("Diet_program_code") REFERENCES "DIET_PROGRAM"("Diet_program_code"),
                        PRIMARY KEY("Food_type_code","Diet_program_code")
                    );''' 

            d.createTable(create)
            for row in reader:
                sql = f'INSERT INTO belongs_in_diet VALUES("{row["Food_type_code"]}", "{row["Diet_program_code"]}");\n'
                d.insert(sql, row)

    def load_belongs_in_medication(): 
        with open(path_data+'\\belongs_in_medication.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=";", quotechar='"')
            create = '''CREATE TABLE "belongs_in_medication" (
                        "Dosage"	TEXT,
                        "Medicine_code"	TEXT NOT NULL,
                        "Medication_code"	TEXT NOT NULL,
                        FOREIGN KEY("Medication_code") REFERENCES "MEDICATION"("Medication_code"),
                        FOREIGN KEY("Medicine_code") REFERENCES "MEDICINE"("Medicine_code"),
                        PRIMARY KEY("Medicine_code","Medication_code")
                    );'''

            d.createTable(create)
            for row in reader:
                sql = f'INSERT INTO belongs_in_medication VALUES("{row["Dosage"]}", "{row["Medicine_code"]}", "{row["Medication_code"]}");\n'
                d.insert(sql, row)

    def load_cares_for(): 
        with open(path_data+'\cares_for.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=";", quotechar='"')
            create = '''CREATE TABLE "cares_for" (
                        "Animal_ID"	TEXT NOT NULL,
                        "Emp_ID"	TEXT NOT NULL,
                        FOREIGN KEY("Animal_ID") REFERENCES "ANIMAL"("Animal_ID"),
                        FOREIGN KEY("Emp_ID") REFERENCES "EMPLOYEE"("Employee_ID"),
                        PRIMARY KEY("Animal_ID","Emp_ID")
                    );''' 

            d.createTable(create)
            for row in reader:
                sql = f'INSERT INTO cares_for VALUES("{row["Animal_ID"]}", "{row["Emp_ID"]}");\n'
                d.insert(sql, row)

    def load_consists_of_diet(): 
        with open(path_data+'\consists_of_diet.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=";", quotechar='"')
            create = '''CREATE TABLE "consists_of_diet" (
                        "Quantity"	TEXT,
                        "Price"	TEXT,
                        "Food_supply_code"	TEXT NOT NULL,
                        "Food_type_code"	TEXT NOT NULL,
                        FOREIGN KEY("Food_supply_code") REFERENCES "FOOD_SUPPLY"("Food_supply_code"),
                        FOREIGN KEY("Food_type_code") REFERENCES "FOOD_TYPE"("Food_type_code"),
                        PRIMARY KEY("Food_supply_code","Food_type_code")
                    );''' 

            d.createTable(create)
            for row in reader:
                sql = f'INSERT INTO consists_of_diet VALUES("{row["Quantity"]}", "{row["Price"]}", "{row["Food_supply_code"]}", "{row["Food_type_code"]}");\n'
                d.insert(sql, row)

    def load_consists_of_medication(): 
        with open(path_data+'\consists_of_medication.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=";", quotechar='"')
            create = '''CREATE TABLE "consists_of_medication" (
                        "Quantity"	TEXT,
                        "Price_per_piece"	TEXT,
                        "Medicine_code"	TEXT NOT NULL,
                        "Medicine_supply_code"	TEXT NOT NULL,
                        FOREIGN KEY("Medicine_supply_code") REFERENCES "MEDICINE_SUPPLY"("Medicine_supply_code"),
                        FOREIGN KEY("Medicine_code") REFERENCES "MEDICINE"("Medicine_code"),
                        PRIMARY KEY("Medicine_supply_code","Medicine_code")
                    );'''

            d.createTable(create)
            for row in reader:
                sql = f'INSERT INTO consists_of_medication VALUES("{row["Quantity"]}", "{row["Price_per_piece"]}", "{row["Medicine_code"]}", "{row["Medicine_supply_code"]}");\n'
                d.insert(sql, row)       

    def load_contains(): 
        with open(path_data+'\contains.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=";", quotechar='"')
            create = '''CREATE TABLE "contains" (
                        "Event_code"	TEXT NOT NULL,
                        "Document_code"	TEXT NOT NULL,
                        FOREIGN KEY("Event_code") REFERENCES "EVENT"("Event_code"),
                        FOREIGN KEY("Document_code") REFERENCES "ENTRANCE_DOCUMENT"("Document_code"),
                        PRIMARY KEY("Event_code","Document_code")
                    );'''

            d.createTable(create)
            for row in reader:
                sql = f'INSERT INTO contains VALUES("{row["Event_code"]}", "{row["Document_code"]}");\n'
                d.insert(sql, row)

    def load_oversees(): 
        with open(path_data+'\oversees.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=";", quotechar='"')
            create = '''CREATE TABLE "oversees" (
                        "Space_code"	TEXT NOT NULL,
                        "Emp_ID"	TEXT NOT NULL,
                        FOREIGN KEY("Emp_ID") REFERENCES "EMPLOYEE"("Employee_ID"),
                        FOREIGN KEY("Space_code") REFERENCES "SPACE"("Space_code"),
                        PRIMARY KEY("Space_code","Emp_ID")
                    );'''

            d.createTable(create)
            for row in reader:
                sql = f'INSERT INTO oversees VALUES("{row["Space_code"]}", "{row["Emp_ID"]}");\n'
                d.insert(sql, row)

    def load_participates_in(): 
        with open(path_data+'\participates_in.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=";", quotechar='"')
            create = '''CREATE TABLE "participates_in" (
                        "Event_code"	TEXT NOT NULL,
                        "Animal_ID"	TEXT NOT NULL,
                        FOREIGN KEY("Animal_ID") REFERENCES "ANIMAL"("Animal_ID"),
                        FOREIGN KEY("Event_code") REFERENCES "EVENT"("Event_code"),
                        PRIMARY KEY("Event_code","Animal_ID")
                    );''' 

            d.createTable(create)
            for row in reader:
                sql = f'INSERT INTO participates_in VALUES("{row["Event_code"]}", "{row["Animal_ID"]}");\n'
                d.insert(sql, row)

    def receive_input():

        status = 1
        while (status!=0): 

            print("Type QUIT to end program.")
            user_input = input("SQLite query: \n")

            if (user_input == "QUIT"): 
                status = 0

            else: 
                sql = user_input
                d.executeSQL(sql, show = True)

    load_ANIMAL()
    load_DIET_PROGRAM()
    load_EVENT()
    load_FOOD_SUPPLY()
    load_FOOD_TYPE()
    load_SPACE()
    load_SPECIES()
    load_SUPPLIER()
    load_SUPPLY()
    load_ANIMAL_CARE_EMPLOYEE()
    load_CARD_OWNER()
    load_CUSTOMER_SUPPORT()
    load_EMPLOYEE()
    load_ENTRANCE_DOCUMENT()
    load_MEDICATION()
    load_MEDICINE()
    load_MEDICINE_SUPPLY()
    load_RESERVATION()
    load_SALE_CATEGORY()
    load_SPACE_EMPLOYEE()
    load_TICKET()
    load_YEARLY_CARD()
    load_belongs_in_diet()
    load_consists_of_diet()
    load_participates_in()
    load_belongs_in_medication()
    load_consists_of_medication()
    load_oversees()
    load_contains()
    load_cares_for()

    receive_input()

    d.close()
