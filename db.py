import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Aishwarya@123",
        database="harvard_artifacts"
    )
