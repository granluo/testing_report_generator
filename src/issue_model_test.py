import json
import json_generator
import unittest

class TestTable(unittest.TestCase):
    def setUp(self):
        self.valid_test_table = json_generator.Table(
                table_name = "table1",
                column_names = ["column1","column2"],
                contents = [
                    {
                        "column1":"content1",
                        "column2":"content2",
                    }])
        self.invalid_test_table = json_generator.Table(
                table_name = "table1",
                column_names = ["column1","column2"],
                contents = [
                    {
                        "column1":"content1",
                        "column2":"content2",
                    },
                    {
                        "nonexistant_column":"content3",
                        "column1":"content4"}])

    def test_content_validate(self):
        with self.assertRaises(ValueError):
            self.invalid_test_table.validate_all_contents()

    def test_add_column_name(self):
        self.valid_test_table.add_column_name("new_column")
        self.assertListEqual(self.valid_test_table.column_names, ["column1","column2", "new_column"])

    def test_add_valid_content(self):
        self.valid_test_table.add_content({"column1":"content5"})
        self.assertListEqual(self.valid_test_table.contents, [
                    {
                        "column1":"content1",
                        "column2":"content2",
                    },
                    {
                        "column1":"content5"
                    }
                    ])
    def test_add_invalid_content(self):
        with self.assertRaises(ValueError):
            self.valid_test_table.add_content({"invalid_column":"content5"})

    def test_convert_to_data_container_valid(self):
        output = self.valid_test_table.convert_to_data_container()
        self.assertDictEqual(output,
                {
                    "table_name":"table1",
                    "column_names":["column1","column2"],
                    "contents":[
                    {
                        "column1":"content1",
                        "column2":"content2",
                    }]
                }
            )

    def test_convert_to_data_container_invalid(self):
        with self.assertRaises(ValueError):
            self.invalid_test_table.convert_to_data_container()
    

class TestIssue(unittest.TestCase):
    def setUp(self):
        self.issue_sample = json_generator.Issue(
                title = "title1",
                description = "description")
        self.valid_test_table = json_generator.Table(
                table_name = "valid_table",
                column_names = ["column1","column2"],
                contents = [
                    {
                        "column1":"content1",
                        "column2":"content2",
                    }])
        self.invalid_test_table = json_generator.Table(
                table_name = "invalid_table",
                column_names = ["column1","column2"],
                contents = [
                    {
                        "column1":"content1",
                        "column2":"content2",
                    },
                    {
                        "nonexistant_column":"content3",
                        "column1":"content4"}])

    def test_add_invalid_table(self):
        with self.assertRaises(ValueError):
            self.issue_sample.add_table(self.invalid_test_table)

    def test_add_valid_table(self):
        self.issue_sample.add_table(self.valid_test_table)
        self.assertEqual(len(self.issue_sample.test_results),1)
        self.assertEqual(self.issue_sample.test_results[0].table_name, "valid_table")
        
    def test_convert_to_data_container(self):
        self.issue_sample.add_table(self.valid_test_table)
        self.assertDictEqual(self.issue_sample.convert_to_data_container(), 
                {
                    "title":"title1",
                    "description":"description",
                    "test_results":[
                        {
                            "table_name":"valid_table",
                            "column_names":["column1","column2"],
                            "contents":[
                                {
                                    "column1":"content1",
                                    "column2":"content2",
                                }
                            ]
                        }

                    ]
                }
            )
        print(json.dumps(self.issue_sample.convert_to_data_container()))

if __name__ == '__main__':
    unittest.main()
