

import pyodbc
import threading
import time

# SQL Server/Azure SQL Connection
conn_str = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=tcp:sql-ps-prod-001.database.windows.net,1433;"
    "Database=sqldb-ps-prod-001;"
    "Uid=SQLETLUser;"
    "Pwd=RvTg9$nCS!u@N#22;"
    "Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
)

# Name of the stored procedure
stored_proc_name = 'DL.usp_AggregationandCalculationWrapper'

# Unique session ID or check tag (if needed)
session_tag = 'DL.usp_AggregationandCalculationWrapper'

def is_sp_running(cursor):
    check_sql = f"""
    SELECT 1 as [IsSpRunning]
    FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_SCHEMA = 'dbo'
      AND TABLE_NAME = 'WrapperStatusTable'
    """
    try:
        cursor.execute(check_sql)
        results = cursor.fetchall()
        #cursor.commit()
        for row in results:
            return True
        return False
    except Exception as e:
        print("Error checking SP status:", e)
        return False

def call_stored_procedure():
    try:
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            if not is_sp_running(cursor):
                print("Calling stored procedure...")
                getSPParametersValue = f"""
                                SELECT Top(1) *
                                FROM DL.ExecuteCalculationWrapper
                                where CompletedDate is null
                                order by createddate
                                """
                cursor.execute(getSPParametersValue)
                results = cursor.fetchall()
                
                for row in results:
                    ModelId = row[2]
                    StartDate = row[3]
                    SPCalledFrom = row[1]
                    callWrapperStoredProcedure = f""" EXEC {stored_proc_name} '{ModelId}', '{StartDate}', '{SPCalledFrom}' """
                    print(callWrapperStoredProcedure)            
                    cursor.execute(callWrapperStoredProcedure)
                    conn.commit()                    
            else:
                print("Stored procedure is already running. Skipping.")
    except Exception as e:
        print("Error during procedure execution:", e)

def schedule_runner():
    while True:
        call_stored_procedure()
        time.sleep(1)  # Wait 30 seconds before next attempt

# Run in background thread
thread = threading.Thread(target=schedule_runner)
thread.daemon = True
thread.start()

# Keep script alive
print("Scheduler started. Press Ctrl+C to stop.")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Scheduler stopped.")
