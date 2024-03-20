import urllib.request
import PyPDF2
import pymysql.cursors
import re
from datetime import datetime

def download_pdf(url, filename):
    try:
        with urllib.request.urlopen(url) as response:
            pdf_content = response.read()
        
        with open(filename, 'wb') as file:
            file.write(pdf_content)
        
        print(f"PDF downloaded successfully as {filename}")
    except Exception as e:
        print(f"Error downloading PDF: {e}")

def extract_incidents(filename):
    incidents = []
    try:
        with open(filename, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                text = reader.pages[page_num].extract_text()
                # print(f"Text extracted from page {page_num + 1}:\n{text}\n")
                # Assuming the data is in the format "Date / Time Incident Number Location Nature Incident ORI"
                matches = re.findall(r'(\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{2}) (\d{4}-\d+) (.+?) (.+?) (.+?)', text)
                for match in matches:
                    date_time, incident_number, location, nature, incident_ori = match
                    # Convert date_time to the correct format
                    date_time = datetime.strptime(date_time, '%m/%d/%Y %H:%M').strftime('%Y-%m-%d %H:%M:%S')
                    incidents.append({
                        'date_time': date_time,
                        'incident_number': incident_number,
                        'location': location,
                        'nature': nature,
                        'incident_ori': incident_ori
                    })
        return incidents
    except Exception as e:
        print(f"Error extracting incidents: {e}")
        return []

def create_database():
    try:
        # Connect to the MySQL database (change the connection parameters as needed)
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='Ska@2557',
            db='dataeng',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        with conn.cursor() as cursor:
            # Create incidents table if it doesn't exist
            cursor.execute('''CREATE TABLE IF NOT EXISTS incidents (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                date_time DATETIME,
                                incident_number VARCHAR(255),
                                location VARCHAR(255),
                                nature VARCHAR(255),
                                incident_ori VARCHAR(255)
                            )''')
        
        print("Database created successfully.")
        return conn
    except Exception as e:
        print(f"Error creating database: {e}")

def insert_incidents(conn, incidents):
    try:
        with conn.cursor() as cursor:
            for incident in incidents:
                # Insert incident data into the MySQL table
                cursor.execute('''INSERT INTO incidents (date_time, incident_number, location, nature, incident_ori)
                                 VALUES (%s, %s, %s, %s, %s)''',
                               (incident['date_time'], incident['incident_number'],
                                incident['location'], incident['nature'], incident['incident_ori']))
        
        conn.commit()
        print("Incidents inserted into the database successfully.")
    except Exception as e:
        print(f"Error inserting incidents into the database: {e}")

def print_incident_counts(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute('''SELECT nature, COUNT(*) FROM incidents GROUP BY nature ORDER BY COUNT(*) DESC, nature ASC''')
            incident_counts = cursor.fetchall()
            for incident_count in incident_counts:
                print(f"{incident_count['nature']}: {incident_count['COUNT(*)']}")
    except Exception as e:
        print(f"Error printing incident counts: {e}")

def main(url, pdf_filename):
    # Download PDF
    download_pdf(url, pdf_filename)

    # Extract incidents
    incidents = extract_incidents(pdf_filename)

    # Create MySQL database and get the connection
    conn = create_database()

    if conn:
        # Insert incidents into MySQL database
        insert_incidents(conn, incidents)

        # Print incident counts
        print_incident_counts(conn)

        # Close the MySQL connection
        conn.close()

if __name__ == "__main__":
    url = "https://www.normanok.gov/sites/default/files/documents/2024-01/2024-01-01_daily_incident_summary.pdf"
    pdf_filename = "incident_summary.pdf"
    main(url, pdf_filename)








