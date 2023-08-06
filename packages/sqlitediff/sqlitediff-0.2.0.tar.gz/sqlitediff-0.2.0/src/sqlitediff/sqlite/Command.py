from string import Template

class Command():
    TABLE_NAMES = "SELECT name FROM sqlite_master where type = 'table'"
    SELECT_ALL = Template("SELECT * FROM $table")
    SELECT_ID = Template("SELECT $column from $table")
    SELECT_ALL_WHERE = Template("SELECT * from $table WHERE $condition")