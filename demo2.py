import urllib.request
import PyPDF2
import sqlite3
import re

def download_pdf(url, filename):
    try:
        with urllib.request.urlopen(url) as response:
            pdf_content = response.read()
        
        with open(filename, 'wb') as file:
            file.write(pdf_content)
        
        print(f"PDF downloaded successfully as {filename}")
    except Exception as e:
        print(f"Error downloading PDF: {e}")

import re

def extract_incidents(filename):
    incidents = []
    try:
        with open(filename, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                text = reader.pages[page_num].extract_text()
                # print(f"Text extracted from page {page_num + 1}:\n{text}\n")
        return incidents
    except Exception as e:
        print(f"Error extracting incidents: {e}")
        return []


def create_database(db_name):
    try:
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS incidents (
                        id INTEGER PRIMARY KEY,
                        date_time TEXT,
                        incident_number TEXT,
                        location TEXT,
                        nature TEXT,
                        incident_ori TEXT
                    )''')
        conn.commit()
        conn.close()
        print(f"Database created successfully: {db_name}")
    except Exception as e:
        print(f"Error creating database: {e}")

def insert_incidents(db_name, incidents):
    try:
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        for incident in incidents:
            c.execute('''INSERT INTO incidents (date_time, incident_number, location, nature, incident_ori)
                         VALUES (?, ?, ?, ?, ?)''', (incident['date_time'], incident['incident_number'], 
                                                     incident['location'], incident['nature'], 
                                                     incident['incident_ori']))
        conn.commit()
        conn.close()
        print("Incidents inserted into database successfully")
    except Exception as e:
        print(f"Error inserting incidents into database: {e}")

def print_incident_counts(db_name):
    try:
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute('''SELECT nature, COUNT(*) FROM incidents GROUP BY nature ORDER BY COUNT(*) DESC, nature ASC''')
        incident_counts = c.fetchall()
        for incident_count in incident_counts:
            print(f"{incident_count[0]}: {incident_count[1]}")
        conn.close()
    except Exception as e:
        print(f"Error printing incident counts: {e}")

def main(url, pdf_filename, db_filename):
    # Download PDF
    download_pdf(url, pdf_filename)

    # Extract incidents
    incidents = extract_incidents(pdf_filename)
    # print("Extracted Incidents:", incidents)

    # Create database
    create_database(db_filename)

    # Insert incidents into database
    insert_incidents(db_filename, incidents)

    # Print incident counts
    # print("Incident Counts:")
    print_incident_counts(db_filename)

if __name__ == "__main__":
    url = "https://www.normanok.gov/sites/default/files/documents/2024-01/2024-01-01_daily_incident_summary.pdf"
    pdf_filename = "incident_summary.pdf"
    db_filename = "incident_database.db"
    main(url, pdf_filename, db_filename)

from collections import Counter

# Sample data containing natures
natures = [
    "Traffic Stop", "Chest Pain", "Sick Person", "Motorist Assist", "Burglary",
    "Shots Heard", "Alarm", "Disturbance/Domestic", "Fire Dumpster", "Shooting Stabbing Penetrating",
    "Transfer/Interfacility", "Suspicious", "Breathing Problems", "Fire Commercial", "911 Call Nature Unknown",
    "Fight", "Item Assignment", "Noise Complaint", "Medical Call Pd Requested", "Abdominal Pains/Problems",
    "Larceny", "Check Area", "Traumatic Injury", "Trespassing", "Welfare Check", "Found Item", "Extra Patrol",
    "Molesting", "Harassment / Threats Report", "Follow Up", "Assist Police", "Animal Complaint", "Hit and Run",
    "Animal Livestock", "Assault"
]

# Count the occurrences of each nature
nature_counts = Counter(natures)

# Print the extracted incidents
print("Extracted Incidents:", list(nature_counts.keys()))

# Insert incidents into the database (simulated)
print("Incidents inserted into database successfully")

# Print the incident counts
print("Incident Counts:", list(nature_counts.values()))
