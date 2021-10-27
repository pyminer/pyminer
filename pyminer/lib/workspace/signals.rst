==================
信号
==================

工作空间中发生的事件将通过信号的方式传递给插件。

.. note::

    在旧版工作空间中，变量的增删改查是通过回调函数的方式添加的，在新版的工作空间中，也同样是采用的回调函数。
    区别在于，旧版工作空间中是将回调的管理功能写入在了工作空间类中，而新版的工作空间是采用了 blinker_ 进行实现的。
    有关于 blinker_ 的用法，请参考相应的文档，这里不进行过多介绍。

.. _blinker: https://pythonhosted.org/blinker/

回调函数的使用方法可以直接参考测试用例： ``tests.test_workspace2.test_data_manager.TestSignals`` 中的用法。
由于正在开发中，可能会出现频繁的更新，因此以测试用例中的内容为准。

目前支持以下信号：

.. py:data:: workspace_data_created

    工作空间中添加了新的数据。

    .. code-block:: python

        @workspace_data_created.connect
        def created(sender: DataManager, key: str):
            pass

.. py:data:: workspace_data_changed

    工作空间中已有的数据发生了改变。

    .. code-block:: python

        @workspace_data_changed.connect
        def changed(sender: DataManager, key: str):
            pass

    .. note::

        这个信号的参数仅仅传入了一个 ``key`` ，因为如果需要获取其历史记录，这应该是 ``DataManager`` 提供方法进行调用，
        而不是通过信号的参数进行传输。

.. py:data:: workspace_data_deleted

    工作空间中的数据被删除了。

    .. code-block:: python

        @workspace_data_deleted.connect
        def deleted(sender: DataManager, key: str):
            pass

    .. note::

        这个数据并不会真的被删除，而是被移入了回收站，在工作空间中看不见了。

.. note::

    相比于之前的旧版 ``workspace`` ，通过传递 ``provider`` 以判断是否是本插件传递过去的数据，
    新版的 ``workspace`` 使用完全基于信号与事件的传递方式，不需要再判断 ``provider`` 。

这里支持的信号的数量比较少，因为并不清楚是否需要支持其他的信号。
比如是否可以在数据创建前，激发一个信号，根据信号的返回值判断是否阻止创建这个数据。
目前并没有发现相关需求，如果确实需要，可以添加。
