# Open the SQL file with UTF-8 encoding
with open("insert_queries.sql", "r", encoding="utf-8") as file:
    lines = file.readlines()

# Filter out lines containing the exact match
filtered_lines = [line for line in lines if ", 'Name', 'Mobile No.');" not in line]

# Write the filtered lines back to the same file or to a new file
with open("insert_queries_cleaned.sql", "w", encoding="utf-8") as file:
    file.writelines(filtered_lines)


print(f"Lines containing ', 'Name', 'Mobile No.');' have been removed and saved to insert_queries_cleaned.sql")
print(f"Lines containing ', 'Name', 'Mobile No.');' have been removed and saved to insert_queries_cleaned.sql")


