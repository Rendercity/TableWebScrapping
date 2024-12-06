import re

# Open the SQL file with UTF-8 encoding
with open("insert_queries_cleaned.sql", "r", encoding="utf-8") as file:
    lines = file.readlines()

# Regular expression to match and remove the ID and its value
# This assumes the ID is the first value after "INSERT INTO bloogdonnerslist (..."
pattern = r"INSERT INTO bloogdonnerslist\s*\(ID,\s*(.*?)\)\s*VALUES\s*\([^,]+,\s*(.*)\);"

# Create a new list of lines without the ID and its value
modified_lines = [re.sub(pattern, r"INSERT INTO bloogdonnerslist (\1) VALUES (\2);", line) for line in lines]

# Write the modified lines to a new file or overwrite the original
with open("insert_queries_removedID.sql", "w", encoding="utf-8") as file:
    file.writelines(modified_lines)

print("ID and its value have been removed from the insert queries.")
