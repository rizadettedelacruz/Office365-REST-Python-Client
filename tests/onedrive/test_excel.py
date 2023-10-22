import os

from office365.onedrive.driveitems.driveItem import DriveItem
from office365.onedrive.drives.drive import Drive
from office365.onedrive.workbooks.tables.table import WorkbookTable
from tests.graph_case import GraphTestCase


def upload_excel(target_drive):
    # type: (Drive) -> DriveItem
    path = "{0}/../data/Financial Sample.xlsx".format(os.path.dirname(__file__))
    with open(path, "rb") as content_file:
        file_content = content_file.read()
    file_name = os.path.basename(path)
    return target_drive.root.upload(file_name, file_content).execute_query()


class TestExcel(GraphTestCase):
    """OneDrive specific test case base class"""

    target_item = None  # type: DriveItem
    table = None  # type: WorkbookTable

    @classmethod
    def setUpClass(cls):
        super(TestExcel, cls).setUpClass()
        cls.target_item = upload_excel(cls.client.me.drive)
        assert cls.target_item.resource_path is not None

    @classmethod
    def tearDownClass(cls):
        cls.target_item.delete_object().execute_query_retry()

    def test1_get_workbook(self):
        workbook = self.__class__.target_item.workbook.get().execute_query_retry()
        self.assertIsNotNone(workbook.resource_path)

    def test2_create_workbook_table(self):
        table = self.__class__.target_item.workbook.tables.add(
            "A10000:C10002", True
        ).execute_query()
        self.assertIsNotNone(table.resource_path)
        self.__class__.table = table

    def test3_list_workbook_tables(self):
        tables = self.__class__.target_item.workbook.tables.get().execute_query_retry()
        self.assertIsNotNone(tables.resource_path)
        self.assertGreater(len(tables), 0)

    def test4_data_body_range(self):
        result = self.__class__.table.data_body_range().execute_query()
        self.assertIsNotNone(result.address)

    def test5_create_table_column(self):
        column = self.__class__.table.columns.add(3, "Column4").execute_query()
        self.assertIsNotNone(column.resource_path)

    def test6_create_table_column_count(self):
        result = self.__class__.table.columns.count().execute_query()
        self.assertGreater(result.value, 0)

    def test7_list_table_columns(self):
        columns = self.__class__.table.columns.get().execute_query()
        self.assertIsNotNone(columns.resource_path)

    def test8_list_table_rows(self):
        rows = self.__class__.table.rows.get().execute_query()
        self.assertIsNotNone(rows.resource_path)

    def test9_create_table_rows(self):
        rows = self.__class__.table.rows.add(
            [["Val11", "Val12", "Val13", "Val14"]]
        ).execute_query()
        self.assertIsNotNone(rows.resource_path)

    def test_10_table_range(self):
        result = self.__class__.table.range().execute_query()
        self.assertIsNotNone(result.address)

    def test_11_delete_workbook_table(self):
        self.__class__.table.delete_object().execute_query()

    # def test_12_workbook_create_session(self):
    #    result = self.__class__.target_item.workbook.create_session().execute_query()
    #    self.assertIsNotNone(result.value)

    # def test_13_workbook_close_session(self):
    #    self.__class__.target_item.workbook.close_session().execute_query()
