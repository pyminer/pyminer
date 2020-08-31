# 插件Test Demo说明

本 test demo 主要用于插件规范编写测试。

## 功能说明

已实现的功能有：

- 插件 package.json 文件的定义和读取
- 插件可以继承 Entry 类，插件启动时 Entry 的 run 会被调用
- 插件可以继承 Menu 和 subwindow 类，插件管理器会自动检测，entry 可以调用提供的方法获取它们的实例，无需获取主程序的实例
- 插件可以自定义 Interface 类，插件管理器会自动创建一份实例和一份 wrap_interface。其中 entry 可以调用提供的方法获得自身的 interface 实例
- 插件可以通过插件 name 获取其他插件的 wrap_interface，这里的 wrap_interface 把 interface 的所有不是函数的成员隐藏，因为 interface 类通常可以访问插件的私有变量

尚未实现的功能：

- 插件的 dependency 检测（此项功能耦合性不高，可以直接编写）
- 插件的 Menu 和 Subwindow 类与 UI 的关系
- 检测插件错误。目前代码多处均假设插件是符合规范的，没有做容错处理，可能会抛异常

## Demo 介绍

本 demo 共创建了两个插件放在extensions文件夹，分别为 test_extension 和 test_extension2，其中 test_extension2 依赖于 test_extension。两个插件分别创建了各一个 Menu （menu 最多有一个实例，menu 此处指选项卡）和两个 subwindow。在 run 函数中，demo 程序展示了如何获取 menu 和 subwindows 实例。

Demo 中，mainform 采用将 menu 和 subwindow 添加到 list 的方法来模拟在 GUI 中加载这些控件。目前，已经可以完成 menu 和 subwindow 在 entry 指定时加载，在 entry.run 退出后卸载。因此，整个插件的周期就是 entry.run 的运行时间，如果插件的逻辑在 subwindow 执行，则 run 函数必须等待 subwindow 执行完成。

需要注意的是，通常 menu，subwindow，interface 和 entry 之间需要相互通信，这一点没有显示地完成。但是 entry 是可以拿到全部实例的，开发者自然可以自行将 entry 实例共享，这样就可以完成各个实例之间的通信。Demo 中展示了 entry 把自身实例发送给 interface 的例子。

正因如此，interface 可以拿到插件所有部件的实例，这是不安全的。wrap_interface 则很好地解决了这个安全问题，demo 中展示了 test_extension2 可以拿到 test_extension 的 wrap_interface，但是访问不了 entry。

运行此 demo，将文件夹切换到项目根目录，运行

~~~
python .\pyminer\features\extensions\test_demo\mainform.py
~~~

## 插件规范

整个插件必须包含在一个文件夹中，该文件夹名必须为插件名（name），此 name 必须是唯一标识。

插件文件夹内必须包含 package.json，其必须包含如下字段

~~~
{
    "name": "test_extension", # 唯一标识
    "displayName": "Test Extension",
    "version": "v0.1.0",
    "description": "This is a test extension",
    # 以下 module 是 py 文件名，class 是类名，config 是初始化参数
    "menu": {"module": "menu", "class": "MyMenu", "config": {"default_param": 1, "param":2}}, # 如不需要 menu 此项可以没有
    "subWindows": [
        {"module": "subwindow", "class": "MySubWindow1", "config": {}},
        {"module": "subwindow", "class": "MySubWindow2", "config": {}}
    ], # 如不需要 subwindow 此项可以没有或为 []
    "entry": {"module": "entry", "class": "MyEntry", "config": {}},
    "interface": {"module": "interface", "class": "MyInterface"}, # 如不提供 interface 此项可以没有
    # dependencies 是一个 dict，key 是插件名，value 是版本号区间
    "dependencies": {"text_extension": "v0.1.0-0.1.2"} # 可以为空
}
~~~

插件必须继承 Entry 类。通常需要改写 `__init__` 函数实现对 `config` 的解析。但是在 `__init__` 函数中不得创建任何 menu，subwindow 和 interface 实例，因为此时插件还未运行，且动态绑定尚未完成。改写 `run` 以启动插件，此时可以调用内建方法获取相应实例。开发者应自行解决各个部件之间的通信。

插件可以按需实现 Menu， Subwindow 和 interface，但是必须在 package.json 中准确声明。

## 实现方法

Entry 获取实例的方法是通过动态绑定完成的。主程序在读取插件包下的 package.json 时创建 Extension 类，按照配置文件依次找到开发者实现的 Entry 和其他类。在创建 entry 实例时，将其他实例创建方法动态地绑定到 entry 的内建方法上，主要采用了装饰器技术。

实现对 interface 的封装采用了类的装饰器，通过 `__getattribute__` 拦截对成员对象的请求，拦截所有非函数的成员对象并抛出 `AttributeError` 错误。原始的 interface 对象通过闭包访问，不能在外部访问，保证了安全性。