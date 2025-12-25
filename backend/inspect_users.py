#!/usr/bin/env python3
"""
Script to inspect user tables in the MySQL database
"""
import pymysql
from app.core.config import settings
import re
from urllib.parse import urlparse

def parse_database_url(database_url):
    """
    Parse the database URL to extract connection parameters
    """
    # Example: mysql+pymysql://username:password@host:port/database
    parsed = urlparse(database_url)
    
    # Extract components
    username = parsed.username
    password = parsed.password
    host = parsed.hostname
    port = parsed.port or 3306  # Default MySQL port
    database = parsed.path.lstrip('/')
    
    return {
        'host': host,
        'port': port,
        'user': username,
        'password': password,
        'database': database
    }

def main():
    # Get database connection parameters from settings
    db_params = parse_database_url(settings.DATABASE_URL)
    
    print(f"Attempting to connect to database: {db_params['host']}:{db_params['port']}/{db_params['database']}")
    print(f"User: {db_params['user']}")
    
    try:
        # Connect to the database
        connection = pymysql.connect(
            host=db_params['host'],
            port=db_params['port'],
            user=db_params['user'],
            password=db_params['password'],
            database=db_params['database'],
            charset='utf8mb4'
        )
        
        print("Connected successfully!")
        
        with connection.cursor() as cursor:
            # Query auser_table (admin users)
            print("\n=== auser_table (Admin Users) ===")
            cursor.execute("DESCRIBE auser_table;")
            auser_columns = cursor.fetchall()
            print("Columns:")
            for col in auser_columns:
                print(f"  {col[0]}: {col[1]} {col[4] if col[4] else ''} {col[2] if col[2] else ''}")
            
            # Query records in auser_table
            cursor.execute("SELECT * FROM auser_table;")
            auser_records = cursor.fetchall()
            print("Records:")
            for record in auser_records:
                print(f"  {record}")
            
            print("\n=== buser_table (Regular Users) ===")
            cursor.execute("DESCRIBE buser_table;")
            buser_columns = cursor.fetchall()
            print("Columns:")
            for col in buser_columns:
                print(f"  {col[0]}: {col[1]} {col[4] if col[4] else ''} {col[2] if col[2] else ''}")
            
            # Query records in buser_table
            cursor.execute("SELECT id, uname, bname, phoneNo, userlvl FROM buser_table LIMIT 10;")
            buser_records = cursor.fetchall()
            print("Records (limited to 10):")
            for record in buser_records:
                print(f"  {record}")
            
            # Check if there are any admin-level users in buser_table
            cursor.execute("SELECT id, uname, bname, userlvl FROM buser_table WHERE userlvl = 'admin' OR userlvl LIKE '%admin%';")
            admin_users = cursor.fetchall()
            print(f"\nAdmin-level users in buser_table: {len(admin_users)}")
            for record in admin_users:
                print(f"  {record}")
                
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")
        print("Make sure MySQL server is running and accessible at the specified address.")
    
    finally:
        if 'connection' in locals():
            connection.close()
            print("\nConnection closed.")

if __name__ == "__main__":
    main()