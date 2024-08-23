'''


    @Author: Shivraj Yelave
    @Date: 22-08-24
    @Last modified by: Shivraj Yelave
    @Last modified time: 22-08-24
    @Title: Class-based SQL CURD Operations Script using pyodbc


'''

import pyodbc  # Library to connect to SQL Server
from dotenv import load_dotenv  # Library to load environment variables
import os  # Library to interact with the operating system


class SqlOperations:
    '''
    Description:
    A class to handle SQL operations including creating databases, tables, 
    inserting, updating, deleting, and selecting data using pyodbc.
    '''

    def __init__(self):
        '''
        Description:
        Initializes the SqlOperations object by setting up the SQL connection using environment variables.
        
        Parameters: None
        Returns: None
        '''
        load_dotenv()

        # Set up SQL connection parameters
        server = os.getenv('SERVER_NAME', 'DESKTOP-ND5NF8I\\SQLEXPRESS')  # Default server if not in .env
        username = os.getenv('USER_NAME')  # Fetch username from environment variables
        password = os.getenv('PASSWORD')  # Fetch password from environment variables

        # Create the connection string
        connection_string = f"""
            DRIVER={{ODBC Driver 17 for SQL Server}};
            SERVER={server};
            UID={username};
            PWD={password};
            Trusted_Connection=yes;
        """

        # Establish a connection to SQL Server
        self.conn = pyodbc.connect(connection_string, autocommit=True)
        self.cursor = self.conn.cursor()

    def show_database(self):
        '''
        Description:
        Fetches the list of databases in the SQL Server.
        
        Returns:
            list: A list of tuples containing the names of databases.
        '''
        try:
            query = "SELECT name FROM sys.databases;"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return rows
        except pyodbc.Error as e:
            print(f"Error fetching databases: {e}")
            return None

    def use_database(self, database_name):
        '''
        Description:
        Switches the connection to the specified database.
        
        Parameters:
            database_name (str): The name of the database to switch to.
        
        Returns:
            None
        '''
        try:
            self.cursor.execute(f"USE {database_name};")
            return f"Using database '{database_name}'."
        except pyodbc.Error as e:
            print(f"Error using database: {e}")
            return None

    def show_tables(self):
        '''
        Description:
        Fetches the list of user-defined tables in the current database.
        
        Returns:
            list: A list of tuples containing the names of tables.
        '''
        try:
            query = "SELECT name FROM sys.tables WHERE type = 'U';"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return rows
        except pyodbc.Error as e:
            print(f"Error fetching tables: {e}")
            return None

    def show_columns(self, table_name):
        '''
        Description:
        Fetches the list of columns in the specified table.
        
        Parameters:
            table_name (str): The name of the table to fetch columns from.
        
        Returns:
            list: A list of tuples containing the names of columns.
        '''
        try:
            query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}';"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return rows
        except pyodbc.Error as e:
            print(f"Error fetching columns: {e}")
            return None

    def create_database(self, database_name):
        '''
        Description:
        Creates a new database with the specified name.
        
        Parameters:
            database_name (str): The name of the database to create.
        
        Returns:
            None
        '''
        try:
            self.cursor.execute(f"CREATE DATABASE {database_name};")
            print(f"Database '{database_name}' created successfully.")
        except pyodbc.Error as e:
            print(f"Error creating database: {e}")

    def create_table(self, database_name, table_name, table_structure):
        '''
        Description:
        Creates a new table with the specified structure in the specified database.
        
        Parameters:
            database_name (str): The name of the database to create the table in.
            table_name (str): The name of the table to create.
            table_structure (str): The structure of the table (e.g., "id INT PRIMARY KEY, name VARCHAR(255)").
        
        Returns:
            None
        '''
        try:
            self.use_database(database_name)
            self.cursor.execute(f"CREATE TABLE {table_name} ({table_structure});")
            print(f"Table '{table_name}' created successfully in database '{database_name}'.")
        except pyodbc.Error as e:
            print(f"Error creating table: {e}")

    def insert_data_in_table(self, table_name, columns, values):
        '''
        Description:
        Inserts data into the specified table and columns.
        
        Parameters:
            table_name (str): The name of the table to insert data into.
            columns (str): The columns to insert data into (comma-separated).
            values (str): The values to insert (comma-separated).
        
        Returns:
            None
        '''
        try:
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({values});"
            self.cursor.execute(query)
            print(f"Data inserted into '{table_name}' successfully.")
        except pyodbc.Error as e:
            print(f"Error inserting data: {e}")

    def select_data(self, table_name, columns='*'):
        '''
        Description:
        Selects data from the specified table and columns.
        
        Parameters:
            table_name (str): The name of the table to select data from.
            columns (str, optional): The columns to select (comma-separated). Defaults to '*' for all columns.
        
        Returns:
            list: A list of tuples containing the selected rows.
        '''
        try:
            query = f"SELECT {columns} FROM {table_name};"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return rows
        except pyodbc.Error as e:
            print(f"Error selecting data: {e}")
            return []

    def update_data(self, table_name, set_statement, condition):
        '''
        Description:
        Updates data in the specified table.
        
        Parameters:
            table_name (str): The name of the table to update.
            set_statement (str): The column and new value to set (e.g., "name = 'John'").
            condition (str): The condition to match for the update (e.g., "id = 1").
        
        Returns:
            None
        '''
        try:
            query = f"UPDATE {table_name} SET {set_statement} WHERE {condition};"
            self.cursor.execute(query)
            print(f"Data updated in '{table_name}' successfully.")
        except pyodbc.Error as e:
            print(f"Error updating data: {e}")

    def delete_entry(self, table_name, condition):
        '''
        Description:
        Deletes an entry from the specified table.
        
        Parameters:
            table_name (str): The name of the table to delete the entry from.
            condition (str): The condition to match for the deletion (e.g., "id = 1").
        
        Returns:
            None
        '''
        try:
            query = f"DELETE FROM {table_name} WHERE {condition};"
            self.cursor.execute(query)
            print(f"Entry deleted from '{table_name}' successfully.")
        except pyodbc.Error as e:
            print(f"Error deleting entry: {e}")

    def delete_database(self, database_name):
        '''
        Description:
        Deletes the specified database.
        
        Parameters:
            database_name (str): The name of the database to delete.
        
        Returns:
            None
        '''
        try:
            self.cursor.execute(f"DROP DATABASE {database_name};")
            print(f"Database '{database_name}' deleted successfully.")
        except pyodbc.Error as e:
            print(f"Error deleting database: {e}")

    def close_connection(self):
        '''
        Description:
        Closes the SQL connection and cursor.
        
        Parameters: None
        Returns: None
        '''
        self.cursor.close()
        self.conn.close()


def main():
    '''
    Main function that provides a menu for performing various SQL operations.
    
    Parameters: None
    Returns: None
    '''
    db = SqlOperations()

    while True:
        print("\nSelect an operation:")
        print("1. Create Database")
        print("2. Create Table")
        print("3. Insert Data")
        print("4. Update Data")
        print("5. Delete Entry")
        print("6. Delete Database")
        print("7. Show Data")
        print("8. Exit")

        choice = input("Enter your choice (1-8): ")

        if choice == '1':
            print("Existing Databases:", db.show_database())
            db_name = input("Enter database name: ")
            db.create_database(db_name)

        elif choice == '2':
            print("Existing Databases:", db.show_database())

            db_name = input("Enter database name: ")

            if not db.use_database(db_name):
                continue
            db.use_database(db_name)

            print("Existing tables are:", db.show_tables())
            table_name = input("Enter table name: ")
            table_structure = input("Enter table structure (e.g., id INT PRIMARY KEY, name VARCHAR(255)): ")
            db.create_table(db_name, table_name, table_structure)

        elif choice == '3':
            print("Existing Databases:", db.show_database())
            db_name = input("Enter database name: ")
            if not db.use_database(db_name):
                continue
            db.use_database(db_name)

            print("Existing tables are:", db.show_tables())
            table_name = input("Enter table name: ")
            if not db.show_columns(table_name):
                continue
            print("Existing  columns are:", db.show_columns(table_name))

            columns = input("Enter columns (comma-separated e.g., id,name): ")
            values = input("Enter values (comma-separated  e.g., 1,'shiv'): ")
            db.insert_data_in_table(table_name, columns, values)

        elif choice == '4':
            print("Existing Databases:", db.show_database())
            db_name = input("Enter database name: ")
            if not db.use_database(db_name):
                continue
            db.use_database(db_name)

            print("Existing tables are:", db.show_tables())
            table_name = input("Enter table name: ")
            if not db.show_columns(table_name):
                continue
            print("Existing  columns are:", db.show_columns(table_name))
            set_statement = input("Enter the update statement (e.g., name = 'John'): ")
            condition = input("Enter the condition (e.g., id = 1): ")
            db.update_data(table_name, set_statement, condition)

        elif choice == '5':
            print("Existing Databases:", db.show_database())
            db_name = input("Enter database name: ")
            if not db.use_database(db_name):
                continue
            db.use_database(db_name)

            print("Existing tables are:", db.show_tables())
            table_name = input("Enter table name: ")
            if not db.show_columns(table_name):
                continue
            print("Existing  columns are:", db.show_columns(table_name))
            condition = input("Enter the condition (e.g., id = 1): ")
            db.delete_entry(table_name, condition)

        elif choice == '6':
            print("Existing Databases:", db.show_database())
            db_name = input("Enter database name: ")

            db.delete_database(db_name)

        elif choice == '7':
            print("Existing Databases:", db.show_database())
            db_name = input("Enter database name: ")
            if not db.use_database(db_name):
                continue
            db.use_database(db_name)

            print("Existing tables are:", db.show_tables())
            table_name = input("Enter table name: ")
            if not db.show_columns(table_name):
                continue
            print("Existing  columns are:", db.show_columns(table_name))
            columns = input("Enter columns to show (comma-separated or '*' for all): ")
            data = db.select_data(table_name, columns)
            print("Selected Data:", data)

        elif choice == '8':
            db.close_connection()
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
