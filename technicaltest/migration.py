# Django
from django.contrib.auth.hashers import make_password

# Python
from datetime import datetime
import os
import pandas as pd
from psycopg2 import connect
import requests

# Set the environment variable for this script to run
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "technicaltest.settings")

def main():
    '''
    Main Function to migrate csv data to PostgreSQL
    '''
    
    # Read the csv file
    df = pd.read_csv('data.csv')
    
    # Drop the id column
    df.drop('id', axis=1, inplace=True)
    
    # Setting the params to make the migration
    params = {
        'user':         os.environ.get("POSTGRES_USER",     "admin"),
        'password':     os.environ.get("POSTGRES_PASSWORD", "admin"),
        'host':         os.environ.get("POSTGRES_HOST",     "localhost"),
        'database':     os.environ.get("POSTGRES_DB",       "django"),
        'port':         os.environ.get("POSTGRES_PORT",     "5432")
    }

    # Connect to the database
    with connect(**params) as conn:
        # Create a cursor
        with conn.cursor() as cursor:
            
            # Verify first start
            print('Verify if the table users is empty')
            cursor.execute("SELECT * FROM authentication_app_user")
            res = cursor.fetchall()
            if res:
                print('Migration already done')
                return
            
            datenow = datetime.now().isoformat()
            print('Creating the admin user...')
            cursor.execute("""
                INSERT INTO authentication_app_user (name, username, password, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s) RETURNING id;
            """, ('admin', 'admin', make_password('admin'), datenow, datenow))
            user_id = cursor.fetchone()
            
            # If something fails, return
            if not user_id:
                return None
            print('User registered successfully')
            # Set all the products user_id to the user_id
            df['user_id'] = user_id[0]
            
            # Change the type of the user_id to int
            df['user_id'] = df['user_id'].astype(int)
            
            # Set updated_at and created_at to the current date
            df['created_at'] = datenow
            df['updated_at'] = datenow
            
            # Fill the empty values with ''
            df[['articulo', 'descripcion']] = df[['articulo', 'descripcion']].fillna('')
            
            # We need to verify if the table is empty
            print('Verify if the table products is empty')
            cursor.execute("SELECT * FROM products_app_product")
            res = cursor.fetchall()
            
            # If the table is empty then we need to migrate the data
            if not res:
                # Insert many rows to the table
                print('Migrating data...')
                cursor.executemany("""
                    INSERT INTO products_app_product 
                    (name, description, user_id, created_at, updated_at) 
                    VALUES (%s, %s, %s, %s, %s)
                """, df.values.tolist())
                
                # Commit the transaction
                conn.commit()
                
                # Print the number of rows inserted
                print(f"Migration complete: {cursor.rowcount} record inserted.")

if __name__ == "__main__":
    main()