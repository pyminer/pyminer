# 线程调用与后台任务执行器
示例可见：`widgets/examples/utilities/threadings`文件夹

>警告：
>
>- 在调用后台线程执行器PMGOneShot0hreadRunner\PMGLoopThreadRunner的时候，务必对执行器对象保持引用！否则执行器对象会被Python解释器垃圾回收，轻则任务无法完成，重则造成程序崩溃。
>
>- 注意：传入的callback函数不得在其中直接刷新UI（比如，调用文本框的setText方法），否则可能出现段错误(segmentation fault)。段错误会**立即导致界面崩溃**，且无法使用try...catch...或者cgitb等手段进行处理！
>
>注意：
>
>- 为了简单起见，本文档中的实例都是面向过程的。在示例中将执行器对象定义为全局变量，就是保持引用的一种方式。而当使用面向对象程序设计方式时，将其作为界面或者控件的属性，也不失为一种可行的解决方案。

## 后台线程只执行一次`PMGOneShotThreadRunner`
示例代码可以在`widgets/examples/utilities/threadings/singleshot.py`找到
```python
import sys
import time

from widgets import PMGOneShotThreadRunner  # 导入单线程任务运行器
from PySide2.QtWidgets import QTextEdit, QApplication, QWidget, QVBoxLayout, QPushButton


def run(loop_times):
    for i in range(loop_times):
        print(i)
        time.sleep(1)
    return 'finished!!', 'aaaaaa', ['finished', 123]


def single_shoot():
    global oneshot, textedit
    if oneshot is not None:
        if oneshot.is_running(): # 如果后台线程已经在运行，那么就不要重新创建，否则可能造成程序崩溃。在实际程序中可以考虑加一个弹出框来进行提示。
            return
    oneshot = PMGOneShotThreadRunner(run, args=(3,))
    oneshot.signal_finished.connect(lambda x: textedit.append('任务完成，函数返回值：' + repr(x)))


oneshot = None
app = QApplication(sys.argv)
basewidget = QWidget()
basewidget.setLayout(QVBoxLayout())

textedit = QTextEdit()
pushbutton = QPushButton('run')
pushbutton.clicked.connect(single_shoot)
basewidget.layout().addWidget(textedit)
basewidget.layout().addWidget(pushbutton)
basewidget.show()
sys.exit(app.exec_())

```
运行时，点击弹出的窗体的`run`按钮，即可触发运行事件。等待3秒钟过后，即可显示下面的文字。多次点击，可以多次执行。

![](doc_figures/test_oneshot_thread.png)



### `PMGOneShotThreadRunner`类介绍

#### 传入参数：
- callback:传入函数对象。
- args: 传入函数的参数，默认值为None。应当以元组形式依次传入。如果为None则不对函数传入参数。
#### 信号
signal_finished，需要连接到的槽函数有一个参数，代表传入函数对象的返回值。

#### 方法
is_running,返回线程是否在运行。

#### 注意事项
对于单步执行的子线程，`widgets`库**暂时不提供**强制停止未完成任务（或者出现错误而退出）的子线程的接口。用户需要保证子线程可以在一定时间后正确的退出。



## 后台线程执行有限次`PMGLoopThreadRunner`
后台线程执行有限次的例子可见`widgets/examples/utilities/threadings/loop_limited_times1.py`与
`widgets/examples/utilities/threadings/loop_limited_times2.py`。
首先，执行有限次的模型是这样的：执行有限次同一函数，但是每次执行时都要传入不同的参数。这样，我们只要传入一个函数，以及一个参数列表，
列表长度就是循环的次数。返回的参数由`signal_step_finished`传回。
代码看这里：(`widgets/examples/utilities/threadings/loop_limited_times1.py`)

```python
import sys
import time
from PySide2.QtWidgets import QTextEdit, QApplication
from widgets import PMGLoopThreadRunner


def run(i, j):
    time.sleep(0.1)
    return i + j


def on_step_finished(step, result):
    global text1
    text1.append('传入每步不同的可迭代参数\nstep:%d,result:%s\n' % (step, repr(result)))


def on_finished():
    global text1
    text1.append('所有任务完成！')


app = QApplication(sys.argv)
text1 = QTextEdit()
text1.show()
oneshot = PMGLoopThreadRunner(run, iter_args=[(i, i + 1) for i in range(36)])
# 传入一个列表可迭代对象（当然也可以是其他迭代器。）作为参数。列表的长度就是循环的次数，列表的每一个元素代表每一步传入的参数。
oneshot.signal_step_finished.connect(on_step_finished)  # 每一步执行后的结果由signal_step_finished传回。多参数则会放进tuple里面。
oneshot.signal_finished.connect(on_finished)

sys.exit(app.exec_())
```
### `PMGLoopThreadRunner`类介绍
#### 传入参数：
- callback:传入函数对象。
- iter_args: 传入函数的参数，默认值为None。应当以可迭代对象的形式传入，可迭代对象的每个元素都是元组。可以为None。
**注意：只有当iter_args为None的时候，才会解析loop_times和step_args参数**！
- loop_times:执行的次数。
- step_args:当loop_times生效时每步执行传入的参数，类型应为元组。

通过以上的示例我们可以看出，loop_times的功能完全可以被iter_args替代。但为了简洁方便，还是设计了这一方法。
若要用loop_times配合step_args，则必须设置iter_args为None。
使用loop_times配合step_args的示例详见`widgets/examples/utilities/threadings/loop_limited_times2.py`
#### 信号
signal_step_finished:传递两个参数，分别是步数（整数，从0开始）和单步执行的结果。
signal_finished，意思后台线程执行完规定次数退出前发出的信号。它没有传递参数，在这点上与单步执行器不同。
这是因为在结束时，他只是通知一下前台程序”任务已经完成，后台线程要退出了“；而程序每一步的执行结果，都已经在signal_step_finished中传过了。





## 后台线程无限反复运行`PMGEndlessLoopThreadRunner`
后台线程反复运行无数次的例子可见
`widgets/examples/utilities/threadings/endlessloop.py`。
首先，执行有限次的模型是这样的：执行有限次同一函数，但是每次执行时都要传入不同的参数。这样，我们只要传入一个函数，以及一个参数列表，
列表长度就是循环的次数。返回的参数由`signal_step_finished`传回。
### 例程
```python
import sys
import time
from PySide2.QtWidgets import QTextEdit, QApplication, QPushButton, QWidget, QVBoxLayout
from widgets import PMGEndlessLoopThreadRunner


def run(i, j):
    time.sleep(0.1)
    return i + j


def on_step_finished(result):
    global text1, stepcount
    text1.append('step:%d,result:%s\n' % (stepcount,repr(result)))
    stepcount += 1


def on_finished():
    global text1
    text1.append('thread quit, all tasks completed!')


def start_thread():
    global endless_loop
    if endless_loop is not None:
        if endless_loop.is_running():
            return
    endless_loop = PMGEndlessLoopThreadRunner(run, args=(0, 0))
    endless_loop.signal_step_finished.connect(on_step_finished)
    endless_loop.signal_finished.connect(on_finished)

def stop_thread():
    global endless_loop
    endless_loop.shut_down()

stepcount = 0
endless_loop:PMGEndlessLoopThreadRunner = None

app = QApplication(sys.argv)
basewidget = QWidget()
basewidget.setLayout(QVBoxLayout())

text1 = QTextEdit()
pushbutton_run = QPushButton('Run')
pushbutton_stop = QPushButton('Stop')
pushbutton_run.clicked.connect(start_thread)
pushbutton_stop.clicked.connect(stop_thread)
basewidget.layout().addWidget(text1)
basewidget.layout().addWidget(pushbutton_run)
basewidget.layout().addWidget(pushbutton_stop)
basewidget.show()
sys.exit(app.exec_())
```
直接运行，则可以看到以下界面：
![image-20201128192325593](doc_figures/endlessloop_ui.png)

在这个界面上点击`Run`即可运行。看到以下效果：
![image-20201128192325593](doc_figures/endlessloop_running.png)

在这个界面上点击`Stop`即可停止。看到以下效果：
![image-20201128192325593](doc_figures/endlessloop_stop.png)

再次点击`Run`，可以继续运行。

### `PMGEndlessLoopThreadRunner`类介绍

#### 传入参数：
- callback: 回调函数。函数每执行一次，信号`signal_step_finished`将发出，信号只有一个参数，也就是我们输入的callback的返回值。
- args:参数

#### 信号
signal_step_finished:传递两个参数，分别是步数（整数，从0开始）和单步执行的结果。
signal_finished，意思后台线程执行完规定次数退出前发出的信号。它没有传递参数，在这点上与单步执行器不同。
这是因为在结束时，他只是通知一下前台程序”任务已经完成，后台线程要退出了“；而程序每一步的执行结果，都已经在signal_step_finished中传过了。

#### 方法
is_running,返回线程是否在运行。