# Workspace 设计记录

## 2020/08/29

本次更新完成以下两个内容：

- 变量的读写，基于 JSON 的传输。提供了 `read` 和 `write` 函数，便于数据服务器调用。
- 简单的数据结构合法性检查。

尚未实现的功能有数据的锁定等。

### 数据结构规范

变量指变量名及其对应的数据。变量名是一个字符串，该字符串首位字符必须为 `[_a-zA-Z]`，其余字符必须为 `[_a-zA-Z0-9]`。

数据必须是一个 `dict` 结构，该结构必须包含至少两个字段，其中一个字段为 `'type'`，表示变量的类型。变量的类型也是变量，其类型为 `'type'`。示例：

~~~
a = {'type':'matrix', 'value':[[1,2,3],[3,2,1]]}

matrix = {'type':'type', 'structure':{'value':[['float']]}})
~~~

则 `a` 是一个 `matrix`，`matrix` 是一种 `type`。`type` 是一个特殊的类型，定义如下：

~~~
type = {'type':'type', 'structure':{'structure':'dict'}}
~~~

### 数据结构的形式化定义

在 `type` 的定义中，`'structure'` 字段自指性地说明了这种类型的实例应该包含哪些字段，且这些字段的类型是什么（注意，此处的类型包括了变量的类型和 json 的五种 object，分别是 dict, list, int, float, str）。从 `type` 的定义可以得知，每一个 `type` 都必须包含 `'structure'` 字段，该字段的类型是 dict。`type` 也自指地完成了定义。

而 `matrix` 是一种 `type`，其定义必须符合它的类型要求，即 `type` 的要求。可以看到，`matrix` 的确包含 `'structure'` 字段，且其类型的确为 dict。进一步，又有 `a` 是一个 `matrix`，按照 `matrix` 的要求，`a` 必须包含 `'value'` 字段，且其类型必须是 list。 该 list 的子元素仍然必须为 list，内部的 list 的子元素则应是 `float`（一般认为，`int` 属于 `float` 而 `float` 不属于 `int`）。经检查，`a` 符合要求，因此 `a` 是合法的。

此例中，`type` 和 `matrix` 就是对数据结构的形式化定义。

### 数据结构合法性检查

数据结构合法性检查是通过 `compare` 函数的递归调用实现的。注意到每个变量都显示声明了自己的类型，取得该类型的定义后，该变量的剩余部分（即除 `'type'` 字段外）和其类型的 `'structure'` 所指向的 dict 是同构的。因此，如果类型规定的是不包含子元素的结构，如 `int`，直接判断二者是否相同；如果是包含子元素的结构，则递归地比较各个子元素。

如果子元素是不确定的，例如在 `type` 的定义中，`'structure'` 字段的 dict 定义是不确定的，则可以用 `'dict'` 来代替。同理，`'list'` 也可以用来指代不确定的 list。

如前所述，字段也可以是已经定义好的类型。此时，先检查字段的类型是否正确，如果正确，再检查字段结构是否合法。

需要注意的是，数据的结构合法性检查通过了，并不代表数据就是合法的。此形式化定义有其局限性，比如，`matrix` 要求 `'value'` 字段的值的各行元素数目相等，这个目前暂时无法判断。

## 2020/08/30

本次更新主要完成 `Variable` 类和 `Converter` 类的设计。目前系统架构为：

~~~
              [            DataManager             ]
InnerUser <-> [<-> VarSet <-Converter-> DataSet <->] <-> DataServer <-> OuterUser
              [    History              RecycleBin ]
~~~

### 名词定义和介绍

`VarSet` 实时保存 Python 变量，比如 `np.ndarray`，`int`，`timeseries`等，其中 `timeseris` 是继承于 `Variable` 的类。`DataSet` 则缓存 `dict`，如上次更新所述。

`Variable` 类是可以直接和上述数据结构（`dict`）转化的类。数据结构转化为 `Variable` 类的子类，类型为数据结构的 `type`。

`Converter` 实现在 Python 对象和上述数据结构之间相互转化。其中还特殊定义了一些数据结构转化成特殊的对象（非 `Variable` 子类），比如 `matrix` 应转化成 `numpy.ndarray`。相应地，还提供从 `numpy.ndarray` 到 `matrix` 的转化。

### 数据传递链路

InnerUser 写入数据，直接保存至 VarSet，VarSet 通知 DataSet 该数据发生改变。数据链路结束。

InnerUser 读取数据，直接从 VarSet 获取。

OuterUser 写入数据，保存至 DataSet，DataSet 调用 Converter 将数据写入 VarSet，更新该数据的状态为已知。

OuterUser 读取数据，从 DataSet 读取。DataSet 检测数据状态是否已知，如果已知，直接返回；如果未知，则调用 Converter 从 VarSet 获取值，修改数据状态为已知。

以上读取数据链路都是基于该值存在，若不存在，按正常逻辑返回错误或空值。

## 2020/08/30 #2

本次更新完成 `DataManager` 全部功能，实现了 `VarSet`，`RecycleBin`，`HistorySet` 和 `MetaDataSet` 四个组件。

### 为什么把 MetaDataSet 分离出来？

因为删除或者撤销（回退）数据不应该引起元数据的变化。

### 为什么 RecycleBin 继承于 list 而不是 dict？

因为一个数据可以被删多次（删除后手动创建新的，又删除），避免覆盖

### 如何实现撤销？为什么撤销需要传参？

撤销传参是因为可以对特定参数进行撤销。暂不支持全局按顺序撤销。

撤销时，先把当前数据推入 HistorySet，否则当前数据将被覆盖而无法重做。然后将指针进一，即可得到撤销后的值。

### 为什么在 DataManager 内部，恢复值要传值？

因为可能出现以下情况，准备在 RecycleBin 中恢复 `a`，但是当前 `VarSet` 中已经存在 `a`，这时候就要把当前的值放入 RecycleBin。

### 什么时候会进行数据转换（上述数据结构和 Python 对象）？

Python 对象转换成上述数据结构，仅发生在数据服务器请求一个值，当前值在 DataSet 中不存在或者不是最新版。

上述数据结构转换成 Python 对象，仅发生在数据服务器向 DataSet 写入一个值，DataManager 自动同步到 VarSet。

## 2020/08/31

添加对数据上锁的功能。默认对数据上非阻塞可重入锁，如果需要阻塞锁，可以加上一层。

## 2020/08/31 # 2

添加数据增删改的 callback 函数，以便可视化界面刷新。具体用法见测试用例，用户向 DataManager 注册 callback 函数，在数据发生变化时回调。其中新增和修改被放在同一个回调函数中。

## 2020/08/31 # 3 （修改 2020/09/01）

增加数据服务器功能，并将 DataManager 和 DataServer 合并到主程序中。~~由于 DataServer 采用 FastAPI 框架，需要用到 signal 模块，因此不得不在主线程运行，所以 GUI 程序只能在新的线程运行。目前已经实现这个功能。~~目前，数据服务器采用 json-rpc 框架，可以运行在新的线程上。但此框架对 POST 请求有更复杂的规定，且不支持 GET 请求。故更改了 API。

数据服务器目前支持两个 API：

~~~
post:
    path: /
    content-type: application/json
    json: method: read
          params: [dataname]
          jsonrpc: 2.0
          id: 0
    func: datamanager.read_data(dataname)

post:
    path: /
    content-type: application/json
    json: method: read
          params: [dataname, data, provider]
          jsonrpc: 2.0
          id: 0
    func: datamanager.write_data(dataname, data, provider)
~~~

如果请求失败，失败的原因可以检测 response 的 `detail`。目前有如下几种：

| 方法 | detail | 描述 |
|--|--|--|
| read | WOULD_BLOCK_ERROR | 数据被其他线程占用 |
| read | NOT_FOUND_ERROR | 未找到请求的数据 |
| read | INTERNAL_ERROR | 未知错误 |
| write | WOULD_BLOCK_ERROR | 数据被其他线程占用 |
| write | INVALID_VALUE_ERROR | 不合法的数据名或数据 |
| write | CONFLICT_ERROR | 没有权限修改数据（内建类型） |
| write | INTERNAL_ERROR | 未知错误 |

