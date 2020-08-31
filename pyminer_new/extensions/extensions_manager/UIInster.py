class BaseInserter:
    @classmethod
    def insert(cls, widget, config=None):
        print(f"BaseInserter.insert({widget},{config})")
        #raise NotImplementedError

class NewTab(BaseInserter):
    pass

class InsertIntoTab(BaseInserter):
    pass

class NewSubWindow(BaseInserter):
    pass

ui_inserters={
    'new_tab':NewTab,
    'insert_into_tab':InsertIntoTab,
    'new_subwindow':NewSubWindow
}