# 选择文档撰写位置

在进行文档撰写前，确定在哪里写文档是很重要的。

`PyMiner`的文档撰写工具提供了足够的灵活性，方便开发者根据自己的需要进行文档的撰写。

本文将以相对独立的插件为目标，描述文档的撰写位置。

## 将文档写在文档字符串中

对于采用 [Sphinx][sphinx] 进行生成的文档，利用其`.. automodule::`指令是一个不错的选择。

[sphinx]: https://www.sphinx-doc.org/en/master/

这存在一定的局限性，不过大部分的需求都是可以满足的。

对于函数、方法等短小的文档，优先采用此方案进行文档的撰写。

文档字符串采用[Google风格][google]，其详细内容请自行学习。
有时间的朋友可以附一篇中文教程的链接。

[google]: https://sphinxcontrib-napoleon.readthedocs.io/en/latest/index.html#docstring-sections

关于文档字符串在PyCharm中的自动补全，如下所示：

![](http://chevereto.panhaoyu.com/images/2020/11/26/PyCharmGoogle.png)

配置成功后的结果如下图所示：

![](http://chevereto.panhaoyu.com/images/2020/11/26/PyCharmGoogle.gif)

## 覆写自动生成的文档

有时，自动生成的文档并不能满足我们的需求，因此我们需要覆写自动生成的文档。

此处以`pyminer_algorithms`包为例，进行相关的介绍。

首先，在我们编辑之前，我们有如下格式的`python`代码：

[![01_python_code_before_modify.md.png](http://chevereto.panhaoyu.com/images/2020/11/27/01_python_code_before_modify.md.png)](http://chevereto.panhaoyu.com/image/jtt)

根据`sphinx`的`autodoc`，生成了如下格式的内容：

[![02_preview_before_modify.md.png](http://chevereto.panhaoyu.com/images/2020/11/27/02_preview_before_modify.md.png)](http://chevereto.panhaoyu.com/image/GdZ)

对于这个内容，我非常不满意，因为它把所有的函数都列在了这个文件中，
而我的本意是将每个函数独立地放在一个文件中。

同时，这个文件下的目录结构是两层的，而我希望显示为一层目录结构，
即只显示顶层子包，而不显示里面的函数。
不然，如果我有一千个函数的话，这个函数库页面，将同时包括一千个函数的索引，太乱了。

因此，我选择对默认生成的文件进行修改。

在编译后的文件夹中，我找到了自动生成的`rst`文件：`docs/build/rst/alg/index.rst`。

[![03_find_compiled_rst_file.md.png](http://chevereto.panhaoyu.com/images/2020/11/27/03_find_compiled_rst_file.md.png)](http://chevereto.panhaoyu.com/image/AF7)

将这个编译好的文件复制到源文件夹中，放在同样的目录结构的位置。

由于在生成`rst`文件的过程中，会先自动根据`*.py`文件生成`*.rst`文件，
然后将所有其他文件拷贝过去，
因此这个文件将覆盖掉默认的自动生成的`index.rst`文件。

[![04_copy_compiled_rst_file_to_python_dir.md.png](http://chevereto.panhaoyu.com/images/2020/11/27/04_copy_compiled_rst_file_to_python_dir.md.png)](http://chevereto.panhaoyu.com/image/1xO)

编译我从生成的文件夹中拷贝出来的`index.rst`文件。

这就是一个普通的`rst`文件，支持`sphinx`的一切功能，我可以随意在其中进行编辑。

[![05_modify_rst_file.md.png](http://chevereto.panhaoyu.com/images/2020/11/27/05_modify_rst_file.md.png)](http://chevereto.panhaoyu.com/image/UUH)

编辑好之后，重新运行文档编译程序。

[![06_compile_doc.md.png](http://chevereto.panhaoyu.com/images/2020/11/27/06_compile_doc.md.png)](http://chevereto.panhaoyu.com/image/zhM)

现在的文档如下所示。

[![07_preview_after_modify.md.png](http://chevereto.panhaoyu.com/images/2020/11/27/07_preview_after_modify.md.png)](http://chevereto.panhaoyu.com/image/TEX)

以及，一层的文档目录结构。

[![08_preview_after_modify_2.md.png](http://chevereto.panhaoyu.com/images/2020/11/27/08_preview_after_modify_2.md.png)](http://chevereto.panhaoyu.com/image/bX2)

一切正常，都是按我希望的格式来的，结束。

``` important::
        选择自定义就意味着放弃自动生成的功能！
```

当您选择将`index.rst`复制到源文件夹下后，您就放弃了这个文件的自动生成功能。
如果您在这个包中添加了新的`python module`，它将不会自动被文档收录，
您需要手动将`*.rst`文件添加至`toctree` 。

不过您也不必担心忘记添加，对于任何没有添加至 ``toctree`` 的 ``*.rst`` 或者 ``*.md`` 文件，
编译器都会给出编译警告的。

当然，您也可以学习一下[Sphinx][sphinx] 中的 [toctree][toctree] 中的 `glob` 参数的用法。

[sphinx]: https://www.sphinx-doc.org/en/master/

[toctree]: https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-toctree

## 将文档写在独立的`*.rst`文件或`*.md`文件中

对于一些有必要独立表达的部分，我们可能会想要将其写在独立的文件中，
比如您现在正在阅读的这一篇文档撰写介绍。

[![09_individual_file.md.png](http://chevereto.panhaoyu.com/images/2020/11/27/09_individual_file.md.png)](http://chevereto.panhaoyu.com/image/QD5)

简单地创建一个文件是没有意义的，我们必须告诉`sphinx`如何找到这个文件，
这就是`toctree`的一部分作用。

`sphinx`是一个层级关系明确的文档系统，不过这种层级不是通过文件夹结构来体现的，
而是通过`toctree`来进行定义的。

基于层级的文档结构，已经由本工具包自动创建于`docs/build/rst`文件夹下，
如下图所示。

[![10_auto_toctree.md.png](http://chevereto.panhaoyu.com/images/2020/11/27/10_auto_toctree.md.png)](http://chevereto.panhaoyu.com/image/WlQ)

在进行这个文档撰写指南时，我们需要将指南的主索引文件添加到`toctree`中的某一个环节。

[![11_add_doc_guide_to_toctree.md.png](http://chevereto.panhaoyu.com/images/2020/11/27/11_add_doc_guide_to_toctree.md.png)](http://chevereto.panhaoyu.com/image/a6v)

添加完成后的结果如下图所示，
在文档结构中已经可以找到我们的指南主页了。
同时，指南主页里面的二级文档也成功被识别。

[![12_add_toctree_finished_preview.md.png](http://chevereto.panhaoyu.com/images/2020/11/27/12_add_toctree_finished_preview.md.png)](http://chevereto.panhaoyu.com/image/tFf)

这个指南的首页比较简单，只有以下内容：

[![13_doc_guide_index.md.png](http://chevereto.panhaoyu.com/images/2020/11/27/13_doc_guide_index.md.png)](http://chevereto.panhaoyu.com/image/8Ub)

可以看出，里面的子文档，可以是markdown也可以ReST文档。
这两种文件格式都可以识别，只是需要指明其在`toctree`中的位置。
