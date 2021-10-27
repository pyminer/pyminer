===========================
``Markdown`` 撰写指南
===========================

很遗憾您点开了这个页面，这里并不能为您提供一份详细的文档指南，因为这着实没有必要。
不过，这里为您准备了一些链接。

Sphinx_ 采用 recommonmark_ 处理 ``Markdown`` 格式的文档，
您可以分别点击这两个链接查看详细的内容。

.. _Sphinx: https://www.sphinx-doc.org/en/master/index.html
.. _recommonmark: https://recommonmark.readthedocs.io/en/latest/auto_structify.html

.. note::

    由于 ``PyMiner`` 的文档生成工具的作者并不采用 ``Markdown`` 进行 ``PyMiner`` 的撰写，
    因此这一部分内容需要有兴趣的朋友来补全。

    同时，由此导致的 ``Markdown`` 支持并不健全，也希望有时间的朋友能帮忙贡献。

示例
============

此处提供一个采用 ``Markdown`` 撰写文档的示例。

.. code-block:: markdown

    # 一级标题

    这是第一行正文。

    ## 二级标题

    这是第二行正文。

.. note::

    标题从一级标题开始写。

    如果上一级页面是 ``*.rst`` 格式的页面，则页面标题将作为上一级页面中的 ``toctree`` 中的显示文本。