import sqlite3
from sqlite3 import Error


def insert_emp(self):
    insert_sql = "insert into employees(First_Name, Last_Name, Address, Phone_Number) " \
                 "values('{0}','{1}','{2}','{3}');" \
        .format(self.firstName.text(), self.lastName.text(), self.address.text(), self.phoneNumber.text())
    try:
        conn = sqlite3.connect("Employees.db")
        c = conn.cursor()
        c.execute(insert_sql)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
            print('Database insert successful')


def emp_list():
    conn = sqlite3.connect("Employees.db")
    c = conn.cursor()
    c.execute("SELECT * FROM employees order by Emp_ID")
    results = c.fetchall()
    conn.close()
    results
    return results


def in_db(row, emp_id):
    results = False
    print("checking if row {0} is in database".format(row))
    sql = "select count(*) from payroll where Pay_Id = {0} and Emp_id = {1}".format(row, emp_id)
    print(sql)
    conn = sqlite3.connect("Employees.db")
    c = conn.cursor()
    k = c.execute(sql).fetchone()[0]
    if k > 0:
        results = True

    conn.close()
    return results


def insert(pay, id, row):
    sql = "insert into payroll" \
          "(Pay_ID, Emp_ID, Date, Hours, Gross, Withholding, Social_Security, IRA, Net, Notes, Emp_ID) " \
          "values" \
          "('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','1');"\
        .format(row, id, pay[0], pay[1], pay[2], pay[3], pay[4], pay[5], pay[6], pay[7])
    conn = sqlite3.connect("Employees.db")
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    conn.close()
    return True


def update(pay, row):
    sql = "update payroll " \
          "set date = '{0}', Hours = '{1}', Gross = '{2}', Withholding = '{3}', Social_Security = '{4}', " \
          "IRA = '{5}', Net = '{6}', Notes = '{7}' where Pay_ID = '{8}'" \
        .format(pay[0], pay[1], pay[2], pay[3], pay[4], pay[5], pay[6], pay[7], row)
    conn = sqlite3.connect("Employees.db")
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    conn.close()
    return True


def selectemp(id):
    conn = sqlite3.connect("Employees.db")
    c = conn.cursor()
    sql = "SELECT  Date, Hours, Gross, Withholding, Social_Security, IRA, Net, Notes " \
          "FROM payroll " \
          "WHERE Emp_ID = {}".format(id)

    c.execute(sql)
    results = c.fetchall()
    conn.close()
    return results


def init_database():
    print('No database detected. Creating new')
    try:
        conn = sqlite3.connect("Employees.db")
        c = conn.cursor()
        c.execute(
            '''create table employees (
            [Emp_ID] integer PRIMARY KEY, 
            [First_Name] text NOT NULL, 
            [Last_Name] text NOT NULL, 
            [Address] text NOT NULL, 
            [Phone_Number] text NOT NULL);''')

        c.execute(
            '''create table payroll (
            [Pay_ID] integer PRIMARY_KEY,
            [Emp_ID] integer NOT NULL, 
            [Date] date, 
            [Hours] integer,
            [Gross] integer,
            [Withholding] integer,
            [Social_Security] integer,
            [IRA] integer,
            [Net] integer,
            [Notes] text,
            FOREIGN KEY (Emp_ID) REFERENCES employees(Emp_ID) );''')

        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
            print('Database initialized successfully')
