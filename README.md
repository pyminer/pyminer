<p></p>
<p></p>

<p align="center">
<img src="pyminer/resources/icons/logo.png" height="80"/> 
</p>


<div align="center">

[![Stars](https://gitee.com/py2cn/pyminer/badge/star.svg?theme=gvp)](https://gitee.com/py2cn/pyminer/stargazers)
[![Platform](https://img.shields.io/badge/python-v3.8-blue)](https://img.shields.io/badge/python-v3.8-blue)
[![Platform](https://img.shields.io/badge/PySide2-blue)](https://img.shields.io/badge/PySide2-blue)
[![License](https://img.shields.io/badge/license-LGPL-blue)](https://img.shields.io/badge/license-LGPL-blue)

</div>

<div align="center">
    <a src="https://img.shields.io/badge/QQ%e7%be%a4-orange">
        <img src="https://img.shields.io/badge/QQ%e7%be%a4-945391275-orange">
    </a>
</div>

<p></p>
<p></p>

<div align="center">
<h2>pyminer</h2>
<h3> 开源、友好、跨平台的数据分析解决方案</h3>

</div>
pyminer 是一款基于Python的开源、跨平台数据分析环境。它以方便Python初学者为己任，在Python的知识理论和工作实践之间搭建桥梁，竭诚为初学者服务。

它开箱即用，大大减少配置解释器环境的繁琐性。不仅提供了编程运行的功能，还能够以交互式的形式进行常见的数据分析操作，减少代码编写和文档查阅的时间。

同时，pyminer将提供面向新手的快速入门教程，教程正由开发团队编写中。同时，我们诚挚希望与Python培训机构合作，让我们的产品帮助到更多学习Python的人。

pyminer通过加载各种插件实现不同的需求，开发者可以通过编写插件，将pyminer扩展的更强大、更趁手，甚至创建一番自己的商用程序。

<p></p>
<p></p>

## 🔈 声明
pyminer 遵循LGPL协议，是一个开放、包容的开源项目，项目中的工具方法来源也非常广泛，因此允许并鼓励任何人在遵循LGPL协议的基础上：

1. 将pyminer用于商业、培训等任何合法场景；
2. 复制、修改 pyminer中的任意代码且无需声明；
3. 复制修改 pyminer官方文档；
4. 鼓励自行写作 pyminer 相关的书籍、博客、文档等内容（收费也可）；
5. 鼓励播主、培训机构培训 pyminer工具的任何内容（收费也可）；
6. 对于商业应用的技术咨询，pyminer团队保留服务的收费权。
pyminer希望成为一个伟大的开源项目，也希望得到大家的认可和赞美，仅此而已。


<p></p>
<p></p>

## 🎉 技术说明

1. 项目开发环境支持跨平台，windows,linux,mac 都支持。
2. Python版本：支持Python3.5及以上，但建议使用Python3.8及以上版本，性能更好。
3. Qt的Python接口：使用PySide2，版本为5.15.2。
4. 项目开发环境使用PyCharm

注意：

- pyminer 的官方发行版本为Python3.8+PySide2-5.15.2。开发者可自行使用其他版本的Python解释器配置相关环境。
- pyminer 曾经由PyQt5开发。但考虑到官方支持以及许可证的类型，我们已经迁移到了PySide2并改变许可证为LGPL。请勿使用PyQt5安装。
- 当使用Python3.8配置环境时，不支持3.8.0等低版本的Python3.8解释器。当使用Python3.8时，请使用3.8.5或者更高版本的解释器。

- 如果使用出现问题，欢迎提issue。



## 🎁 文档地址
- 项目文档：[https://gitee.com/py2cn/pyminer/wikis](https://gitee.com/py2cn/pyminer/wikis)
- API文档：[http://py2cn.gitee.io/pyminer](http://py2cn.gitee.io/pyminer)
- MATLAB与Numpy对比：[http://mathesaurus.sourceforge.net/matlab-numpy.html](http://mathesaurus.sourceforge.net/matlab-numpy.html)

<p></p>
<p></p>

## ⏳ 当前进度
[https://gitee.com/py2cn/pyminer/board](https://gitee.com/py2cn/pyminer/board)


## 🚄 开源地址

- Gitee：[https://gitee.com/py2cn/pyminer](https://gitee.com/py2cn/pyminer)
- GitHub：[https://github.com/aboutlong/pyminer](https://github.com/aboutlong/pyminer)

<p></p>
<p></p>

## 🥂 安装体验

<p></p>
<p></p>

### 发行版下载（仅Windows系统）
我们为Windows系统的用户提供了发行版的下载链接，你可以在我们的官网中下载发行版即刻体验。对于Mac OS和Linux系统的用户，暂时不提供发行版，可以参阅“开发者自行安装”一节。

官网链接：[请点击这里打开](http://www.pyminer.com/)

### 开发者自行安装（适合Windows、Mac OS以及各大Linux发行版）
#### 安装前准备：
1. 确认你的Python解释器版本。pyminer支持3.5~3.9。
	- 当使用Python3.8.x时，建议x>=5,也就是使用Python3.8.5及以上版本，否则安装PySide2可能遇到问题
	- 3.5.x/3.6.x/3.7.x/3.9.x下，由于开发人员不足，未进行充分测试。为稳定起见，建议解释器版本x>=5。
2. 建议新建全新的虚拟环境，尤其是当旧的虚拟环境中存在其他依赖于PyQt/PySide2的程序时。pyminer与这些程序可能发生依赖冲突。


#### Windows安装 pyminer

```bash
#第一步：下载源代码
git clone https://gitee.com/py2cn/pyminer.git
#安装依赖 (如果下载太慢，请复制源码目录下的 pip.ini 文件到python安装目录下)
pip install pyminer
#第三步：运行主程序
在控制台输入 pyminer 回车，即可打开pyminer 


```

#### 虚拟环境安装 pyminer

```bash
#第一步：创建pip虚拟环境
pip install pipenv
pipenv --three  # 使用当前系统中的python3创建环境
#第二步：启动当前目录下的虚拟环境
pipenv shell
#第三步：为虚拟环境安装pyminer
pipenv install pyminer -i https://mirrors.cloud.tencent.com/pypi/simple


```

## 开发重点（2021年4月修订）
pyminer项目现在的开发目标是，打造初学者友好的Python编程环境，方便更多的人与Python这位踏实可靠（也有点笨呆呆）的自动化助手相知、相熟。

因此pyminer的开发重点为：

1、计算、统计方面低代码化功能性开发。需求详见：[低代码化功能性开发](https://gitee.com/py2cn/pyminer/issues/I3HTG9?from=project-issue)

2、编写适用于Python入门的pyminer官方教程。需求详见：[编写教程](https://gitee.com/py2cn/pyminer/issues/I3I7FW?from=project-issue) 。在教程编写方面，
我们深知开发团队力量有限，因此诚挚希望可以和各位开发者或培训机构合作。

3、插件商店的开发。插件商店可以让pyminer如虎添翼。这一部分的开发需求详见：[插件商店](https://gitee.com/py2cn/pyminer/issues/I1TWAR?from=project-issue)

为了减少开发负担，样式表只使用浅色样式表（Fusion），不对深色样式表做优化，且不再进行界面语言翻译工作。
界面语言直接使用中文。

## 📱 加入我们

作者：pyminer Development Team

邮箱：team@pyminer.com

欢迎各位开发者大佬加入 

<p></p>
<p></p>

<img src="pyminer/resources/screenshot/group.jpg" width = "300" height = "500" alt="QQ群" align=center />

<p></p>
<p></p>


##  🚥 许可说明
本项目遵循LGPL许可证。

许可解释权归属 pyminer Development Team。

##  📸 预览截图

基本界面
![avatar](pyminer/resources/screenshot/main.png)

代码提示
![avatar](pyminer/resources/screenshot/code.png)

绘图
![avatar](pyminer/resources/screenshot/check_data.png)

