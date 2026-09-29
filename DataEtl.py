"""
Added a script that performs an automated ETL process.
It takes the raw car sales data from the CSV file and cleans the data using pandas
by handling missing values and fixing headers.
Then it loads the dataset into a local sqlite database for sql analysis and Tablau's visuals.
"""

import pandas as pd
import sqlite3
import sys


#Encapsulates the extraction transformation and loading phases.
class DataEtl:
    def __init__ (self, csv_filepath, db_filepath):
        #required file paths
        self.csv_filepath = csv_filepath
        self.db_filepath = db_filepath
        self.df = None
        self.df_clean = None


    #Reads raw CSV file into pandas df.
    def extract(self):
        print(f"Loading the raw data from {self.csv_filepath}...")

        try:
            self.df = pd.read_csv(self.csv_filepath)
            print(f"Successfully loaded {len(self.df)} rows.")

        except FileNotFoundError:
            print(f"ERROR: '{self.csv_filepath}' wasn't found...")
            sys.exit()

        except Exception as e:
            print(f"A unexpected error has occurred: {e}")
            sys.exit()


    #Cleans data by  dropping and standarizing column headers, and removes any rows containing missing data.
    def transform(self):
        print("Cleaning and validating data...")
        self.df_clean = self.df.dropna()


        #Data validation.
        if self.df_clean.empty:
            print("ERROR: The dataset is empty. Stoping... ")
            sys.exit()

        self.df_clean.columns = self.df_clean.columns.str.strip()

    #Connects to SQLite and loads the cleaned data into a database table.
    def load(self):
        print(f"Connecting to SQLite database '{self.db_filepath}'...")

        try:
            conn = sqlite3.connect(self.db_filepath)
            #Write the clean df directly to a SQL table
            self.df_clean.to_sql('car_sales_data', conn, if_exists='replace', index = False)
            conn.close()
            print("Clean data successfully loaded.")

        except sqlite3.Error as e:
            print(f"DATABASE ERROR: Failed to connect or write... {e}")

        except Exception as e:
            print(f"A unexpected error has occurred: {e}")

    #Executes the ETL methods in order.
    def run_pipeline(self):
        self.extract()
        self.transform()
        self.load()
    


if __name__ == "__main__":
    pipeline = DataEtl(csv_filepath='car_sales_data.csv',db_filepath='car_sales.db')
    pipeline.run_pipeline()