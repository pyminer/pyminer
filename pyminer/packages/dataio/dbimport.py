import database_sample


class dbimportutils():
    def import_mysql_display(self):
        """
        显示"从mysql数据库导入表"窗口
        """

        self.import_mysql_database = database_sample.ImportMysql()
        self.import_mysql_database.exec_()

    def import_oracle_display(self):
        """
        显示"从Oracle数据库导入表"窗口
        """
        self.import_oracle_database = database_sample.ImportOracle()
        self.import_oracle_database.exec_()

    def import_postgresql_display(self):
        """
        显示"从PostgreSQL数据库导入表"窗口
        """
        self.import_postgresql_database = database_sample.ImportPostgreSQL()
        self.import_postgresql_database.exec_()

    def doImportEngine(self):
        return {
            "mysql": self.import_mysql_display,
            "oracle": self.import_oracle_display,
            "postgresql": self.import_postgresql_display
        }
