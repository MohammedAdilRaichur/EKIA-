from langchain.tools import tool
import sqlite3
import os

@tool
def query_database(query: str) -> str:
    """
    Query the enterprise SQLite database for structured data.
    The database has the following tables:
    - departments(dept_id, dept_name, manager_id)
    - employees(emp_id, name, dept_id, title, email)
    - projects(project_id, project_name, status, budget, dept_id)
    - expenses(expense_id, emp_id, amount, category, date, status)
    
    Ensure queries are read-only (SELECT only).
    """
    query = query.strip()
    if not query.upper().startswith("SELECT"):
        return "Error: Only read-only SELECT queries are allowed."
        
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    db_path = os.path.join(base_dir, "data", "database", "enterprise.db")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        conn.close()
        
        if not rows:
            return "No results found."
            
        result_str = " | ".join(columns) + "\n"
        for row in rows:
            result_str += " | ".join([str(val) for val in row]) + "\n"
            
        return result_str
    except Exception as e:
        return f"Error executing query: {str(e)}"
