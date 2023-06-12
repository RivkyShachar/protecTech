import sqlite3

def process_and_insert_data(SiteName, DangerType, DateAndHour, DangerAmount):
    # Perform operations on the data

    # Connect to the SQLite database
    conn = sqlite3.connect('geeks2.db')
    c = conn.cursor()

    # Insert the processed data into the database
    # # Display data inserted
    print("Data Inserted in the table: ")
    data = c.execute('''SELECT * FROM Site''')
    for row in data:
        print(row)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Usage example
# process_and_insert_data('0', 'Helmet', '08/06/23 10:55:26',2)
# process_and_insert_data('0', 'Helmet', '08/06/23 10:55:26',1)
# process_and_insert_data('0', 'Helmet', '08/06/23 11:55:26',4)
# process_and_insert_data('0', 'Helmet', '08/06/23 13:55:26',5)
# process_and_insert_data('0', 'Helmet', '08/06/23 13:55:26',1)
# process_and_insert_data('0', 'Helmet', '08/06/23 14:55:26',0)
# process_and_insert_data('0', 'Helmet', '08/06/23 15:55:26',0)
# process_and_insert_data('0', 'Helmet', '08/06/23 17:55:26',3)
# process_and_insert_data('1', 'Helmet', '08/06/23 17:55:26',6)
# process_and_insert_data('1', 'Helmet', '08/06/23 17:55:26',2)
# process_and_insert_data('1', 'Helmet', '08/06/23 18:55:26',7)
# process_and_insert_data('0', 'Helmet', '08/06/23 18:55:26',2)
# process_and_insert_data('0', 'Helmet', '08/06/23 19:55:26',6)
process_and_insert_data('0', 'Helmet', '08/06/23 20:55:26',2)
