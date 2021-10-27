=====================
``ReST`` 撰写指南
=====================


很遗憾您点开了这个页面，这里并不能为您提供一份详细的文档指南，因为这着实没有必要。
不过，这里为您准备了一些链接：

#. https://www.cnblogs.com/seayxu/p/5603876.html
#. https://3vshej.cn/rstSyntax/
#. https://docutils-zh-cn.readthedocs.io/zh_CN/latest/ref/rst/restructuredtext.html

另外，在大部分的由 Sphinx_ 生成的页面中，都是可以看到其 ``ReST`` 源码的，
包括 `Python帮助文档`_ 、 `MatPlotLib帮助文档`_ 、 `NumPy帮助文档`_ 。

.. _Python帮助文档: https://docs.python.org/
.. _Sphinx: https://www.sphinx-doc.org/en/master/index.html
.. _MatPlotLib帮助文档: https://matplotlib.org/3.3.3/contents.html
.. _NumPy帮助文档: https://numpy.org/doc/

.. image:: http://chevereto.panhaoyu.com/images/2020/11/26/ReST.png

本页面更多地定义了本项目中的一些 ``ReST`` 文档规范。

标题的设置
===========

每一个 ``*.rst`` 文件都有需要有一个页面标题，否则它无法被收录到 ``toctree`` 中。

标题应当采用双等号的形式，也就是 ``ReST`` 中的一级标题，它将在 ``html`` 中渲染为 ``<h1>title</h1>`` 。

.. code-block::

    ================
    这是页面的标题
    ================

.. note::

    请注意保证上下两排有相同的长度。


在主标题之下的次级标题，就可以按 ``ReST`` 的顺序，依次向下排列了。

图片等静态资源
================

如果您需要添加图片等二进制静态资源，请尽量不要直接添加在源文件夹中。
有很多方便的地方可以生成它的链接。

在项目中添加过多的二进制文件，一方面不利用源码的上传与下载，另一方面容易被git托管商列入黑名单。

目前项目的图床正在配置中，可以临时采用我的图床，如有需要可以联系QQ1641210337。

此处分享一个采用chevereto图床进行静态资源上传的方案。

.. toctree::
    use_chevereto.rst
