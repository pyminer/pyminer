============
文档编译工具
============

.. toctree::
    :maxdepth: 2

    file_tree.rst
    rst_generator.rst
    doc_guide/index.rst

..  note::

    本文档仅用于对文档编译工具本身进行介绍，不包括文档的具体撰写指南。
    相关内容将在额外的一个专题页面中介绍 。

这个包用于进行文档的编译工作，是 `sphinx-apidoc`_ 的替代品。

基于源文件夹自动生成代码的主要思路是通过读取项目中的文档字符串，重新排版后形成具有层级关系的项目文档。

在常见的 `sphinx`_ 项目中，开发者将需要手动维护 ``*.rst`` 的文档结构。
`sphinx`_ 提供了一系列的指令集，可以用于自动从 python 的文档字符串中读取文档。

在常见的 `sphinx`_ 项目中通过 `sphinx-apidoc`_ 创建初始的 ``*.rst`` 文档结构，
之后，如果 python 代码结构发生调整，程序员需要手动更新 ``*.rst`` 的文档结构。

.. _sphinx: https://www.sphinx-doc.org/en/master/
.. _sphinx-apidoc: https://www.sphinx-doc.org/en/master/man/sphinx-apidoc.html
.. _python: https://docs.python.org

对于本项目而言，代码将长期进行开发，一次性生成代码的方案显然是不可行的。
而如果每写一段代码就要求程序员重新进行开发，这显然会降低程序员撰写文档的积极性。

因此，我开发了这款可以持续从 python_ 源文件夹进行文档集成的工具。
本工具将对 `sphinx-apidoc`_ 进行优化，可以完全基于 python_ 的项目结构生成 rst 文档结构。

本工具可以保证开发者无需关注 ``doc`` 文件夹中发生的事情，
不需要修改完 ``*.py`` 文件后再去相应的文件夹修改相应的 ``*.rst`` 文件，
而是将 ``*.rst`` 文件放在 ``*.py`` 文件的同一个文件夹下。
这可以极大地保证程序员更新代码后同步更新文档的积极性。

本文将首先介绍文档结构，然后给出推荐的文档撰写风格。

Rst 文档结构生成过程
====================

本包采用完全尊重 python_ 文件结构的方案进行编译。

对于任何一个 ``python package`` ，我们都可以将其子文件（夹）分为五个部分：

1. ``__init__.py`` ，这个文件与其他文件的地位不同，它表明这是一个 `python package` ，
是一个索引文件，需要用 ``package`` 的模板生成文档；
#. ``*.py`` ， python_ 模块，可以用 automodule_ 指令自动生成文档；
#. 其他文件，直接简单复制；
#. ``python package`` 文件夹，表明这是一个子包，是需要建立索引的；
#. 其他文件夹，直接简单复制。

.. _automodule: https://www.sphinx-doc.org/zh_CN/latest/usage/extensions/autodoc.html#directive-automodule

基于这样的编译流程，所有的文档文件、资源文件等，都可以放在与源代码 ``*.py`` 文件所在的同一个文件夹下。
在进行文档生成时，这些文件将被复制到 ``docs/rst`` 文件夹下，
因此在 ``*.rst`` 和 ``*.md`` 中都可以使用相对路径访问资源文件。

对于首次生成，本包简单地进行复制与生成，没有任何可能造成困扰的点。

在进行增量生成时，本程序包采用递归的方式对每一个 python 包进行生成，
其主要逻辑在 :meth:`~generate_python_package_files` 中，可以归纳为以下顺序：

#. 根据 ``__init__.py`` 索引文件生成 ``index.rst`` 索引文件；
#. 根据 ``module_name.py`` 生成 ``module_name.rst`` ；
#. 将变更后的其他文件复制到目标文件夹；
#. 将所有的资源文件夹复制到目标文件夹；
#. 将所有的子程序包进行递归生成；
#. 删除目标文件夹中多余的文件和文件夹。

这里的一个很关键的思路是，首先根据 ``*.py`` 文件生成 ``*.rst`` 文件，
而如果我们对自动生成的文件不满意，我们可以在源文件夹中创建对应的 ``*.rst`` 文件，
它会在下一阶段被复制到目标文件夹，并覆盖自动生成的文件。
这是本程序的一个重要特性。

.. automodule:: pyminer_devutils.doc
    :members:
    :undoc-members:
