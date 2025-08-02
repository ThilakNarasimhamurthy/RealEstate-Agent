# app/mcp/tools/database_tools.py
"""
Database tools for MCP - MongoDB/SQLite operations.
"""

import sqlite3
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

class DatabaseTools:
    """Database operations for MCP."""
    
    def __init__(self, db_path: str = "data/app.db"):
        self.db_path = db_path
        
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Execute a SQL query and return results as list of dictionaries."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(query, params)
                
                if query.strip().upper().startswith('SELECT'):
                    rows = cursor.fetchall()
                    return [dict(row) for row in rows]
                else:
                    conn.commit()
                    return [{"affected_rows": cursor.rowcount}]
                    
        except Exception as e:
            logger.error(f"Database error: {e}")
            return [{"error": str(e)}]
            
    def create_table(self, table_name: str, columns: Dict[str, str]) -> bool:
        """Create a new table with specified columns."""
        column_defs = ", ".join([f"{col} {dtype}" for col, dtype in columns.items()])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_defs})"
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(query)
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error creating table: {e}")
            return False
            
    def insert_record(self, table_name: str, data: Dict[str, Any]) -> bool:
        """Insert a record into a table."""
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(query, list(data.values()))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error inserting record: {e}")
            return False
            
    def get_table_info(self, table_name: str) -> List[Dict[str, Any]]:
        """Get information about a table structure."""
        query = f"PRAGMA table_info({table_name})"
        return self.execute_query(query)
        
    def list_tables(self) -> List[str]:
        """List all tables in the database."""
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        result = self.execute_query(query)
        return [row["name"] for row in result if row["name"] != "sqlite_sequence"]
        
    def backup_database(self, backup_path: str) -> bool:
        """Create a backup of the database."""
        try:
            import shutil
            shutil.copy2(self.db_path, backup_path)
            return True
        except Exception as e:
            logger.error(f"Error backing up database: {e}")
            return False 