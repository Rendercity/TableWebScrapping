# Open the SQL file with UTF-8 encoding
with open("insert_queries.sql", "r", encoding="utf-8") as file:
    lines = file.readlines()

# Initialize a counter for lines with the exact match
count = 0

# Loop through each line and check for the exact match
for line in lines:
    if ", 'Name', 'Mobile No.');" in line:
        count += 1

print(f"Total lines containing the exact match: {count}")
