"""
绘图函数包
-----------

每一个数据处理软件都有优秀的绘图功能， ``PyMiner`` 也不例外。
本函数包旨在提供大量的方便可用的绘图函数，
以实现快速绘图。

``MatPlotLib`` 的主打功能是实现印刷级别的图像，
因此性能可能会非常差。
不过对于一般的数据分析和科研需求，
性能是完全达标的了。

数据结构
-----------

首先需要定义这个算法包的通用数据结构。
所谓通用数据结构就是在进行面向过程的函数调用时，
函数的参数默认允许哪些类型。

``MatPlotLib`` 在绘图时主要用到的对象依次有以下几个：

#. ``Canvas`` : 画布对于用户来说一般是不可见的，非特殊需求不需要考虑设计画布。
#. ``Figure`` : 图像对象表示一张图，它支持显示为一张图片或保存为一个文件。
#. ``Axes`` : 坐标轴，同一张图下可以有多个坐标轴，这可以用于实现子图，也可以用于实现左右上下不同坐标系等内容。
#. ``Artist`` : 实际的图元，可能是一个点、一个圆、一条线等内容。

同时，整型、浮点型、字符串和 ``numpy.ndarray`` 、 ``pandas.DataFrame`` 一定是要支持的。

函数库
---------

类似于 ``MatPlotLib`` ，我们需要一个全局的图像对象，
当然用户可以自己手动指定一个新的图像对象。
同时，我们需要一个全局的坐标系，
同样，用户也可以手动指定一个坐标系。
这一部分的内容事实上 ``MatPlotLib`` 已经做得很好了，
通常来说我们没必要对 ``MatPlotLib`` 做加法，
而是需要做减法删去其中过于复杂的功能。
以下是具体的函数构想：

#. 全局对象的操控及图片持久化
    #. ``savefig`` : 保存图片（未实现）
    #. ``gcf`` : 获取全局图像对象（未实现）
    #. ``gca`` : 获取全局坐标轴对象（未实现）
    #. ``gci`` : 获取当前图像（是否需要实现）


#. 以下是 ``matplotlib.pyplot`` 中的所有全局函数，需要进行整理归类。
    #. ``cycler`` : 
    #. ``interactive`` : 
    #. ``figaspect`` : 
    #. ``get_backend`` : 
    #. ``get_scale_names`` : 
    #. ``get_cmap`` : 
    #. ``register_cmap`` : 
    #. ``install_repl_displayhook`` : 
    #. ``uninstall_repl_displayhook`` : 
    #. ``set_loglevel`` : 
    #. ``findobj`` : 
    #. ``switch_backend`` : 
    #. ``new_figure_manager`` : 
    #. ``draw_if_interactive`` : 
    #. ``show`` : 
    #. ``isinteractive`` : 
    #. ``ioff`` : 关闭交互模式，不打算实现，默认开启
    #. ``ion`` : 关闭交互模式，不打算实现，默认开启
    #. ``pause`` : 
    #. ``rc`` : 
    #. ``rc_context`` : 
    #. ``rcdefaults`` : 
    #. ``getp`` : 
    #. ``get`` : 
    #. ``setp`` : 
    #. ``xkcd`` : 
    #. ``figure`` : 
    #. ``_auto_draw_if_interactive`` : 
    #. ``gcf`` : 
    #. ``fignum_exists`` : 
    #. ``get_fignums`` : 
    #. ``get_figlabels`` : 
    #. ``get_current_fig_manager`` : 
    #. ``connect`` : 
    #. ``disconnect`` : 
    #. ``close`` : 
    #. ``clf`` : 
    #. ``draw`` : 
    #. ``savefig`` : 
    #. ``figlegend`` : 
    #. ``axes`` : 
    #. ``delaxes`` : 
    #. ``sca`` : 
    #. ``subplot`` : 
    #. ``subplots`` : 
    #. ``subplot_mosaic`` : 
    #. ``subplot2grid`` : 
    #. ``twinx`` : 
    #. ``twiny`` : 
    #. ``subplot_tool`` : 
    #. ``tight_layout`` : 
    #. ``box`` : 
    #. ``xlim`` : 
    #. ``ylim`` : 
    #. ``xticks`` : 
    #. ``yticks`` : 
    #. ``rgrids`` : 
    #. ``thetagrids`` : 
    #. ``plotting`` : 
    #. ``get_plot_commands`` : 
    #. ``colormaps`` : 
    #. ``_setup_pyplot_info_docstrings`` : 
    #. ``colorbar`` : 
    #. ``clim`` : 
    #. ``set_cmap`` : 
    #. ``imread`` : 
    #. ``imsave`` : 
    #. ``matshow`` : 
    #. ``polar`` : 
    #. ``figimage`` : 
    #. ``figtext`` : 
    #. ``ginput`` : 
    #. ``subplots_adjust`` : 
    #. ``suptitle`` : 
    #. ``waitforbuttonpress`` : 
    #. ``acorr`` : 
    #. ``angle_spectrum`` : 
    #. ``annotate`` : 
    #. ``arrow`` : 
    #. ``autoscale`` : 
    #. ``axhline`` : 
    #. ``axhspan`` : 
    #. ``axis`` : 
    #. ``axline`` : 
    #. ``axvline`` : 
    #. ``axvspan`` : 
    #. ``bar`` : 
    #. ``barbs`` : 
    #. ``barh`` : 
    #. ``boxplot`` : 
    #. ``broken_barh`` : 
    #. ``cla`` : 
    #. ``clabel`` : 
    #. ``cohere`` : 
    #. ``contour`` : 
    #. ``contourf`` : 
    #. ``csd`` : 
    #. ``errorbar`` : 
    #. ``eventplot`` : 
    #. ``fill`` : 
    #. ``fill_between`` : 
    #. ``fill_betweenx`` : 
    #. ``grid`` : 
    #. ``hexbin`` : 
    #. ``hist`` : 
    #. ``hist2d`` : 
    #. ``hlines`` : 
    #. ``imshow`` : 
    #. ``legend`` : 
    #. ``locator_params`` : 
    #. ``loglog`` : 
    #. ``magnitude_spectrum`` : 
    #. ``margins`` : 
    #. ``minorticks_off`` : 
    #. ``minorticks_on`` : 
    #. ``pcolor`` : 
    #. ``pcolormesh`` : 
    #. ``phase_spectrum`` : 
    #. ``pie`` : 
    #. ``plot`` : 
    #. ``plot_date`` : 
    #. ``psd`` : 
    #. ``quiver`` : 
    #. ``quiverkey`` : 
    #. ``scatter`` : 
    #. ``semilogx`` : 
    #. ``semilogy`` : 
    #. ``specgram`` : 
    #. ``spy`` : 
    #. ``stackplot`` : 
    #. ``stem`` : 
    #. ``step`` : 
    #. ``streamplot`` : 
    #. ``table`` : 
    #. ``text`` : 
    #. ``tick_params`` : 
    #. ``ticklabel_format`` : 
    #. ``tricontour`` : 
    #. ``tricontourf`` : 
    #. ``tripcolor`` : 
    #. ``triplot`` : 
    #. ``violinplot`` : 
    #. ``vlines`` : 
    #. ``xcorr`` : 
    #. ``sci`` : 
    #. ``title`` : 
    #. ``xlabel`` : 
    #. ``ylabel`` : 
    #. ``xscale`` : 
    #. ``yscale`` : 
    #. ``autumn`` : 
    #. ``bone`` : 
    #. ``cool`` : 
    #. ``copper`` : 
    #. ``flag`` : 
    #. ``gray`` : 
    #. ``hot`` : 
    #. ``hsv`` : 
    #. ``jet`` : 
    #. ``pink`` : 
    #. ``prism`` : 
    #. ``spring`` : 
    #. ``summer`` : 
    #. ``winter`` : 
    #. ``magma`` : 
    #. ``inferno`` : 
    #. ``plasma`` : 
    #. ``viridis`` : 
    #. ``nipy_spectral`` : 

关于  ``MATLAB`` 和 ``R`` 中的优秀经验也需要进行参考，
需要进行需求的详细分析才能开始写代码。

"""
