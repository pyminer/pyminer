# PyMiner基础控件类generalwidgets
## 概述
generalwidgets是对pyqt中基础控件的直接封装。其中的控件可能存在相互引用的关系。
其中，以`PMG`开头的控件（代表`PyMiner General Widgets`）未引用pyminer项目中的其他内容，
而以`PM`开头的控件大多不可独立于PyMiner使用。
## 布局
### 流式布局PMFlowLayout
```python
class PMFlowLayout(QGridLayout):
    def __init__(self, parent=None, column_width=100):
```
其操作方式与QGridLayout是完全相同的。初始化的时候需要指定`column_width`(若不指定，默认为100px),作为控件默认宽度。
- 开始时是按照QGridLayout的形式进行插入的。
- 初始化时可以设定控件的宽度，当监测到窗口的宽度变化足以改变控件布局之时，
就重新排布控件。
- 重排的策略写在了on_resize方法之中，但是这个方法并不会自动执行，需要在`PMFlowLayout`所在的控件的`resizeEvent`中调用。
