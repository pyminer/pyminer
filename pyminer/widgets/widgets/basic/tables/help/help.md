# 数据查看与编辑 帮助 Help
## 操作说明
### 跳转到行： 

点击“跳转到行”按钮，或者快捷键`Ctrl+G`均可。

但是注意，很多时候pandas的Index是从0开始的。因此行的索引为399时，实际的行号应该是400.


# 高亮颜色说明
### Pandas
Pandas的数据类型是相当复杂的，不同的数据类型之间常常发生混淆。

让我们考虑下面的情况：字符串`'2017-06-27'`和pandas的TimeStamp型数据`'2017-06-27'`，这两个数据其实是完全不同的。
但是在数据集难以明显的区分出来。
因此我们就用这样的高亮方式，方便区分数据集的数据类型。

在PyMiner对Pandas数据的高亮方式中，可以很好很方便的区分这个问题。

- 如果是字符串，就会用黄色背景这样显示：<font style="background: rgba(200,200,0,0.4)">2017-06-27</font>

- 如果是时间戳类型，则会用绿色背景这样显示：<font style="background: rgba(0,200,0,0.4)">2017-06-27</font>

高亮颜色的说明如下：
- 数值型：

    - 整数：<font style="background: rgba(0,0,128,0.4)">123</font>
    - 浮点数：<font style="background: rgba(0,64,128,0.4)">3.1415</font>
    - 复数：<font style="background: rgba(100,0,128,0.4)">1+1j</font>
      
- 布尔型：
<font style="background: rgba(0,200,200,0.4)">True</font>
- 时间型：
<font style="background: rgba(0,200,0,0.4)">2017-07-20</font>
- 字符串型：黄色
<font style="background: rgba(200,200,0,0.4)">John Strauss</font>  
- 其他类型：灰色
    - <font style="background: rgba(0,0,0,0.3125)">None</font>  
    - <font style="background: rgba(0,0,0,0.3125)">person</font>(自定义数据类型)  
    - <font style="background: rgba(0,0,0,0.3125)">NaN</font>  
    - <font style="background: rgba(0,0,0,0.3125)">NaT</font>  

### Numpy
目前没有高亮效果，未来的高亮效果计划以大小值为依据，配色方案参考pandas的方案。