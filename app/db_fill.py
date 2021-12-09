import sqlite3
from werkzeug.security import generate_password_hash

con = sqlite3.connect(r'G:\SynologyDrive\Uni\6. Semester\Anwendungsprojekt\Development\Git\Git_Repo\Anwendungsprojekt\app\main_db.db')
cur = con.cursor()

# Insert a row of data
"""for i in range(5):
    pw = generate_password_hash(
                f"start1234{i}", 
                method='pbkdf2:sha256', 
                salt_length=8
            )
    cur.execute(f"INSERT INTO User(email,password,role) VALUES ('testkunde{i}@testmail.com',?,'Kunde')",(pw,))

for i in range(5):
    pw = generate_password_hash(
                f"start1234{i}", 
                method='pbkdf2:sha256', 
                salt_length=8
            )
    cur.execute(f"INSERT INTO User(email,password,role) VALUES ('testdienstleister{i}@testmail.com',?,'Dienstleister')",(pw,))"""

#for i in range(5):
cur.execute(f"INSERT INTO User(email,password,role) VALUES ('testdienstleister{i}@testmail.com',?,'Dienstleister')")

# Save (commit) the changes
con.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
con.close()
