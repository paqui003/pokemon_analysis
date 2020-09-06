import pandas as pd
import sqlite3

class DatabaseManager(): 
    def __init__(self, database, table): 
        self.database = database
        self.table = table
        self.connection = None
          
    def __enter__(self): 
        con = sqlite3.connect(self.database)
        self.connection = con
        return self
      
    def __exit__(self, exc_type, exc_value, exc_traceback): 
        self.connection.close() 
  

    def read(self):
        try:
            df = pd.read_sql_query(f"SELECT * from {self.table}", self.connection)
        except:
            df = None
            
        return df
    
    

    
   
