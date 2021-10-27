# 文档的编译与调试

文档编译比较简单，通过`docs/make_doc.py`脚本就可以完成。

首先，找到这个脚本。不管采用什么办法，执行这个脚本。

[![01_find_make_doc_script.md.png](http://chevereto.panhaoyu.com/images/2020/11/27/01_find_make_doc_script.md.png)](http://chevereto.panhaoyu.com/image/VXU)

执行成功后，可以看到左面多出来了一个`build`文件夹和三个子文件夹。

文档编译的基本流程是，基于`python`文件夹生成`rst`文件夹，
然后基于`rst`文件夹生成`doctrees`文件夹，
最后基于`doctrees`文件夹生成`html`文件夹。

[![02_compile_doc.md.png](http://chevereto.panhaoyu.com/images/2020/11/27/02_compile_doc.md.png)](http://chevereto.panhaoyu.com/image/h8e)

在生成`html`文件夹之后，我们找到这个`html`文件夹下面的`index.html`，然后复制到浏览器中，
就可以打开编译好的文档。

[![03_find_index_html_and_open.md.png](http://chevereto.panhaoyu.com/images/2020/11/27/03_find_index_html_and_open.md.png)](http://chevereto.panhaoyu.com/image/Odh)

生成的文档的主页如图所示，在上面的“开发者文档”里面，就是我们程序的具体的API文档。

[![04_open_index_page.md.png](http://chevereto.panhaoyu.com/images/2020/11/27/04_open_index_page.md.png)](http://chevereto.panhaoyu.com/image/YDS)

打开后我们的API文档如下图所示。

[![05_open_doc.md.png](http://chevereto.panhaoyu.com/images/2020/11/27/05_open_doc.md.png)](http://chevereto.panhaoyu.com/image/Bqn)



## 文档的调试

本工具旨在通过`python`文件夹结构生成`rst`文件夹结构，因此这一部分没有进行充分的调试，
且部分功能并不完善，可能会出现一些问题。

在进行调试时，我们需要明确我们文档生成过程中的对应关系。

每一个`*.py`文件都会生成一个`*.rst`文件，然后每一个`*.rst`文件也会生成一个`*.html`文件。
如果您觉得网页中的哪一个页面存在问题，可以直接根据URL反查到相应的`*.py`文件或者`*.rst`文件。

[![06_dir_structure.md.png](http://chevereto.panhaoyu.com/images/2020/11/27/06_dir_structure.md.png)](http://chevereto.panhaoyu.com/image/MEc)

基于正确的`*.rst`文件，[Sphinx][sphinx]的被充分验证过的编译功能一般不会出错。

[sphinx]: https://www.sphinx-doc.org/en/master/index.html

