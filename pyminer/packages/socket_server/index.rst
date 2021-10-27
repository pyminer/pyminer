==============================================================================
Socket数据服务器
==============================================================================

.. toctree::
   :maxdepth: 2


   main.rst
   server_by_socket.rst

.. automodule:: packages.socket_server
    :members:
    :undoc-members:

数据服务器基于 ``Widgets`` 里面的 ``server`` ，是一个简单的基于 ``PyQt`` 的连接。

目前的方法：

简介
========

数据服务器之前考虑过用共享内存的方式，但是后来，@Reco由于时间原因暂时搁置了这块开发任务，
所以暂时用socket的tcp传输顶上。

这个数据服务器就是socket-server插件。它需要调用PyMiner的插件接口，借以访问和修改工作空间的数据。
至于端口号，目前还是写死的——12306。这一点之后应该也需要克服。

**[TODO]:之后还需要增加端口选择的功能！**

服务器的主代码定义在插件中，当然还有一个服务器基类，定义在widgets里面。大致的工作原理是：

#. 服务器启动，用一个QThread开始监听套接字。
**为什么不用Threading？盖因Qt的界面与其不兼容。使用起来可能导致程序崩溃。**
#. 服务器收到连接请求。请求分为两种，若为“long_conn”，则开启一个新线程，维护一个长连接，
在连接中回复一条确认报文；对于其他请求则直接回复一个确认报文。
#. 对于2中的前一种情况，长连接需要监听同一个端口发送过来的事件。当没有收到消息的时候，自然就是挂起的。
#. 对于2中的第二种情况，服务器直接用前台线程进行处理，并且发送回相应信息。
#. 除了以上长连接和短连接，服务器每10秒发送一个心跳广播，如果发现端口断连，就将其踢下去。
**注意：针对踢下线这一点，目前还没有重连机制。**
#. 广播的报文内容不只是心跳保活。如工作空间数据发生变化时会发送一条这样的报文：

“{'name': 'broadcast', 'message': 'data_changed', 'data_name': 'a', 'data_source': 'ipython'}”

.. important::::

    为了节省传输的字节数，在上面这条数据变化的报文里面不会包含数据的值具体是多少等非关键信息。
    若要获取相应的值，客户端可以拿到变量名之后，向服务端请求这个数据。

事实上，报文解析的方式已经预定义好了，就在pyminer_algorithm类里面，有get_var和set_var方法，
可以直接访问或者修改工作空间中的变量。



对于心跳包的接收，定义在widgets里面。如果是普通的程序，可以用GeneralClient;
（基于Threading）如果是想要嵌入其他PyQt程序，就用PMClient(基于QThread)。



**未来相应的接口可以而且应该整合到统一的接口pip包中！**

未来的任务
===========

1、尽量减少用pickle传递数据！

比如说，对于可用json传递的数据，可以考虑用json进行传递。这样也可以方便解析。

如果要这样做，那么就能增强程序的通用性。

目前用debug在pandas等程序的编码和解码方面还是不尽如人意。

比如说，set_var函数可否增加一个属性，比如说 ``method='json'`` 或者 ``method='pickle'`` ?

2、metadata的概念，需要用起来。

什么叫数据的metadata?如何使用？

3、注意线程安全性！

回调方法列表
=============

返回pickle形式的变量
----------------------------

名称
^^^^^^

``self.read_pickle_data``

输入值
^^^^^^^^

无

返回值
^^^^^^^^

``{'message': 'succeeded', 'var_dic': data_b64}``

以pickle形式设置变量
-------------------------

'write_p': self.set_pickle_data,

获取PyMiner主界面的设置项
--------------------------

'get_settings': self.get_settings,

设置PyMiner的设置项
--------------------------

'set_settings_param': self.set_settings_param

获取PyMiner主界面的样式表
------------------------------

'get_style_sheet': self.get_style_sheet

获取所有的变量名称
------------------------

'get_all_variable_names': self.get_all_data_names

获取所有的公共可访问变量的名称
-------------------------------

'get_all_public_variable_names': self.get_all_public_data_names

以字典的形式一次设置多个变量
-----------------------------------

'write_var_dic': self.update_pickle_data_dict

获取全部公共可访问的变量
--------------------------------

'get_var_dic': self.get_var_dic

删除变量
---------------

'delete_variable': self.delete_variable

