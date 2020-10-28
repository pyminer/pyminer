# Import the PyQt5 module with some of the GUI widgets
import keyword

import PyQt5.QtWidgets
# Import the QScintilla module
import PyQt5.Qsci
# Import Python's sys module needed to get the application arguments
import sys
import re


# Create a custom Nim lexer
class CythonLexer(PyQt5.Qsci.QsciLexerCustom):
    styles = {
        "Default": 0,
        "Keyword": 1,
        "Unsafe": 2,
        "MultilineComment": 3,
    }
    keyword_list = keyword.kwlist + ['cdef', 'cpdef', 'cimport', 'enum', 'ctypedef', 'struct',
                                     'extern', 'api', 'public', 'private']
    unsafe_keyword_list = ['int', 'float', 'bool', 'void', 'double', 'long', 'unsigned', 'char'] +\
    ['__name__', '__doc__', '__package__', '__loader__', '__spec__', '__build_class__', '__import__',
     'abs', 'all', 'any', 'ascii', 'bin', 'breakpoint', 'callable', 'chr', 'compile',
     'delattr', 'dir', 'divmod', 'eval', 'exec', 'format', 'getattr', 'globals', 'hasattr',
     'hash', 'hex', 'id', 'input', 'isinstance', 'issubclass', 'iter', 'len', 'locals',
     'max', 'min', 'next', 'oct', 'ord', 'pow', 'print',
     'repr', 'round', 'setattr', 'sorted', 'sum', 'vars',
     'None', 'Ellipsis',
     'NotImplemented',
     'False',
     'True',
     'bool',
     'memoryview',
     'bytearray',
     'bytes',
     'classmethod',
     'complex',
     'dict',
     'enumerate',
     'filter',
     'float',
     'frozenset',
     'property',
     'int',
     'list',
     'map',
     'object',
     'range',
     'reversed',
     'set',
     'slice',
     'staticmethod',
     'str',
     'super',
     'tuple',
     'type',
     'zip',
     '__debug__',
     'BaseException',
     'Exception',
     'TypeError',
     'StopAsyncIteration',
     'StopIteration',
     'GeneratorExit',
     'SystemExit',
     'KeyboardInterrupt',
     'ImportError',
     'ModuleNotFoundError',
     'OSError',
     'EnvironmentError',
     'IOError',
     'WindowsError',
     'EOFError',
     'RuntimeError',
     'RecursionError',
     'NotImplementedError',
     'NameError',
     'UnboundLocalError',
     'AttributeError',
     'SyntaxError',
     'IndentationError',
     'TabError',
     'LookupError',
     'IndexError',
     'KeyError',
     'ValueError',
     'UnicodeError',
     'UnicodeEncodeError',
     'UnicodeDecodeError',
     'UnicodeTranslateError',
     'AssertionError',
     'ArithmeticError',
     'FloatingPointError',
     'OverflowError',
     'ZeroDivisionError',
     'SystemError',
     'ReferenceError',
     'MemoryError',
     'BufferError',
     'Warning',
     'UserWarning',
     'DeprecationWarning',
     'PendingDeprecationWarning',
     'SyntaxWarning',
     'RuntimeWarning',
     'FutureWarning',
     'ImportWarning',
     'UnicodeWarning',
     'BytesWarning',
     'ResourceWarning',
     'ConnectionError',
     'BlockingIOError',
     'BrokenPipeError',
     'ChildProcessError',
     'ConnectionAbortedError',
     'ConnectionRefusedError',
     'ConnectionResetError',
     'FileExistsError',
     'FileNotFoundError',
     'IsADirectoryError',
     'NotADirectoryError',
     'InterruptedError',
     'PermissionError',
     'ProcessLookupError',
     'TimeoutError',
     'open',
     'copyright',
     'credits',
     'license',
     'help',
     'execfile',
     'runfile',
     '__IPYTHON__',
     'display',
     'get_ipython']

    def __init__(self, parent=None):
        # Initialize superclass
        super().__init__(parent)
        assert isinstance(parent,PyQt5.Qsci.QsciScintilla)
        self.setEditor(parent)
        # Set the default style values
        self.setDefaultColor(PyQt5.QtGui.QColor(0x00, 0x00, 0x00))
        self.setDefaultPaper(PyQt5.QtGui.QColor(0xff, 0xff, 0xff))
        self.setDefaultFont(PyQt5.QtGui.QFont("Courier", 8))
        # Initialize all style colors
        self.init_colors()
        # Init the fonts
        for i in range(len(self.styles)):
            if i == self.styles["Keyword"]:
                # Make keywords bold
                self.setFont(PyQt5.QtGui.QFont("Courier", 8, weight=PyQt5.QtGui.QFont.Black), i)
            else:
                self.setFont(PyQt5.QtGui.QFont("Courier", 8), i)
        # Set the Keywords style to be clickable with hotspots
        # using the scintilla low level messaging system
        parent.SendScintilla(
            PyQt5.Qsci.QsciScintillaBase.SCI_STYLESETHOTSPOT,
            self.styles["Keyword"],
            True
        )
        parent.SendScintilla(
            PyQt5.Qsci.QsciScintillaBase.SCI_SETHOTSPOTACTIVEFORE,
            True,
            PyQt5.QtGui.QColor(0x00, 0x7f, 0xff)
        )
        parent.SendScintilla(
            PyQt5.Qsci.QsciScintillaBase.SCI_SETHOTSPOTACTIVEUNDERLINE, True
        )

        # Define a hotspot click function
        def hotspot_click(position, modifiers):
            """
            Simple example for getting the clicked token
            """
            text = parent.text()
            delimiters = [
                '(', ')', '[', ']', '{', '}', ' ', '.', ',', ';', '-',
                '+', '=', '/', '*', '#'
            ]
            start = 0
            end = 0
            for i in range(position + 1, len(text)):
                if text[i] in delimiters:
                    end = i
                    break
            for i in range(position, -1, -1):
                if text[i] in delimiters:
                    start = i
                    break
            clicked_token = text[start:end].strip()
            # Print the token and replace it with the string "CLICK"
            print("'" + clicked_token + "'")
            parent.setSelection(0, start + 1, 0, end)
            # parent.replaceSelectedText("CLICK")

        # Attach the hotspot click signal to a predefined function
        parent.SCN_HOTSPOTCLICK.connect(hotspot_click)
        self.cython_imported = False

    def init_colors(self):
        # Font color
        self.setColor(PyQt5.QtGui.QColor(0x00, 0x00, 0x00), self.styles["Default"])
        self.setColor(PyQt5.QtGui.QColor(0x00, 0x00, 0x7f), self.styles["Keyword"])
        self.setColor(PyQt5.QtGui.QColor(0x7f, 0x00, 0x00), self.styles["Unsafe"])
        self.setColor(PyQt5.QtGui.QColor(0x7f, 0x7f, 0x00), self.styles["MultilineComment"])
        # Paper color
        for i in range(len(self.styles)):
            self.setPaper(PyQt5.QtGui.QColor(0xff, 0xff, 0xff), i)

    def language(self):
        return "Python"

    # def lexer(self) -> str:
    #     return 'Python'

    def description(self, style):
        if style < len(self.styles):
            description = "Custom lexer for the Nim programming languages"
        else:
            description = ""
        return description

    def styleText(self, start, end):
        if self.cython_imported == True:
            self.cython_module.cython_style_text(start, end, self, self.parent())
        else:
            # Initialize the styling
            self.startStyling(start)
            # Tokenize the text that needs to be styled using regular expressions.
            # To style a sequence of characters you need to know the length of the sequence
            # and which style you wish to apply to the sequence. It is up to the implementer
            # to figure out which style the sequence belongs to.
            # THE PROCEDURE SHOWN BELOW IS JUST ONE OF MANY!
            splitter = re.compile(r"(\{\.|\.\}|\#|\'|\"\"\"|\n|\s+|\w+|\W)")
            # Scintilla works with bytes, so we have to adjust the start and end boundaries.
            # Like all Qt objects the lexers parent is the QScintilla editor.
            text = bytearray(self.parent().text(), "utf-8")[start:end].decode("utf-8")
            tokens = [
                (token, len(bytearray(token, "utf-8")))
                for token in splitter.findall(text)
            ]
            # Multiline styles
            multiline_comment_flag = False
            # Check previous style for a multiline style
            editor = self.editor()
            if start != 0:
                previous_style = editor.SendScintilla(editor.SCI_GETSTYLEAT, start - 1)
                if previous_style == self.styles["MultilineComment"]:
                    multiline_comment_flag = True
            # Style the text in a loop
            for i, token in enumerate(tokens):
                if multiline_comment_flag == False and token[0] == "#" and tokens[i + 1][0] == "[":
                    # Start of a multiline comment
                    self.setStyling(token[1], self.styles["MultilineComment"])
                    # Set the multiline comment flag
                    multiline_comment_flag = True
                elif multiline_comment_flag == True:
                    # Multiline comment flag is set
                    self.setStyling(token[1], self.styles["MultilineComment"])
                    # Check if a multiline comment ends
                    if token[0] == "#" and tokens[i - 1][0] == "]":
                        multiline_comment_flag = False
                elif token[0] in self.keyword_list:
                    # Keyword
                    self.setStyling(token[1], self.styles["Keyword"])
                elif token[0] in self.unsafe_keyword_list:
                    # Keyword
                    self.setStyling(token[1], self.styles["Unsafe"])
                else:
                    # Style with the default style
                    self.setStyling(token[1], self.styles["Default"])


if __name__ == '__main__':
    # Create the main PyQt application object
    application = PyQt5.QtWidgets.QApplication(sys.argv)

    # Create a QScintila editor instance

    editor = PyQt5.Qsci.QsciScintilla()
    # Set the lexer to the custom Nim lexer
    nim_lexer = CythonLexer(editor)
    editor.setLexer(nim_lexer)
    # Set the initial text
    initial_text = """
cdef public struct Vehicle:
    int speed
    float power

cdef api void activate(Vehicle *v):
    if v.speed >= 88 and v.power >= 1.21:
        print("Time travel achieved")
    """
    # Set the editor's text to something huge
    editor.setText(initial_text)

    # For the QScintilla editor to properly process events we need to add it to
    # a QMainWindow object.
    # main_window = PyQt5.QtWidgets.QMainWindow()
    # # Set the central widget of the main window to be the editor
    # main_window.setCentralWidget(editor)
    # # Resize the main window and show it on the screen
    # main_window.resize(800, 600)
    # main_window.show()
    editor.show()
    # Execute the application
    application.exec_()
