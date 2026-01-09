import psycopg2
from google.cloud import aiplatform
from sec_tools import fetch_sec_filings

# 1. DATABASE TOOL: This function lets the AI "read" your Postgres data
def get_property_financials(metro_area: str):
    """Retrieves financial data for properties in a specific city from the local DB."""
    try:
        # Connect using 'trust' (no password) as we configured
        conn = psycopg2.connect(
            dbname="real_estate_corp",
            user="postgres",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()
        
        query = """
            SELECT p.address, p.property_type, f.revenue, f.net_income 
            FROM Properties p 
            JOIN Financials f ON p.property_id = f.property_id 
            WHERE p.metro_area = %s;
        """
        cur.execute(query, (metro_area,))
        rows = cur.fetchall()
        
        cur.close()
        conn.close()
        
        if not rows:
            return f"No properties found in {metro_area}."
        return rows
    except Exception as e:
        return f"Database error: {str(e)}"

# 2. AGENT CONFIGURATION: Setting up the 'Brain'
# In a real scenario, you'd use the ADK wrapper, 
# but here is the logic for the Gemini model integration

def ask_financial_sage(user_query):
    if "ticker" in user_query.lower() or "sec" in user_query.lower():
        # Step 1: Extract ticker (e.g., 'AAPL')
        # Step 2: Call the SEC Scraper
        status = fetch_sec_filings("AAPL") 
        return f"I've retrieved the SEC data. {status}"
    
    elif "property" in user_query.lower():
        # Logic for your Postgres DB
        return "Checking local property records..."

