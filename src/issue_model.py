import json

TABLE_NAME = "table_name"
COLUMN_NAMES = "column_names"
CONTENTS = "contents"
TITLE = "title"
DESCRIPTION = "description"
TEST_RESULTS = "test_results"

class Table:
    def __init__(self, table_name: str, column_names: list, contents: list = []):
        """ Construct a table class

        Args:
          table_name: A name of a table.
          column_names: An array of column names of a table, key in contents
            should be from here.
          contents: A list of dictionary with each column name mapping to its contents.
        """
        self.table_name = table_name
        self.column_names = column_names
        self.contents = contents

    def validate_all_contents(self):
        """ Validate if keys in contents have values not in column_names."""
        for content in self.contents:
            self.validate_content(content)

    def validate_content(self, content:dict):
        """ Validate if a content is valid.

        A valid content should have all its column name in the self.column_names.
        Args:
          content: A dictionary mapping from column name to its value.
          
        Raise:
          ValueError: An error occurred when column names do not include key in
          the content.
        """
        for key in content:
            if key not in self.column_names:
                raise ValueError("{} is not one of column names: {}.".format(key, ",".join(self.column_names)))

    def add_column_name(self, name:str):
        self.column_names.append(name)

    def add_content(self, content:dict):
        """ Add content to a list, contents.

        Args:
          content: A dictionary maping from column name to its content.
        """
        self.validate_content(content)
        self.contents.append(content)

    def convert_to_data_container(self) -> str:
        self.validate_all_contents()
        output = {}
        output[TABLE_NAME] = self.table_name
        output[COLUMN_NAMES] = self.column_names
        output[CONTENTS] = self.contents
        return output

class Report:
    def __init__(
            self,
            title: str,
            description: str = ""):
        self.title = title
        self.description = description
        self.test_results = []

    def add_table(self, table: Table):
        table.validate_all_contents()
        self.test_results.append(table)

    def convert_to_data_container(self):
        output = {}
        output[TITLE] = self.title
        output[DESCRIPTION] = self.description
        output[TEST_RESULTS]=[]
        for content in self.test_results:
            output[TEST_RESULTS].append(content.convert_to_data_container())
        return output

    def convert_to_json(self, file_name = None):
        output = self.convert_to_data_container()
        if file_name is not None:
            with open(file_name, 'w') as f:
                json.dump(output, f)
        return json.dumps(output, indent = 2, sort_keys = True)

