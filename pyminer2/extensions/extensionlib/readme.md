# 插件开发指南：
## PyMiner自带的可停靠子窗口名称：
|中文名称|程序内部名称|
|---------|------------|
| 编辑器 | code_editor|   
|ipython控制台|  ipython_console|
|工作空间显示器|    workspace_inspector|
|变量视图|data_view_table|
|文件树|file_explorer|

这些控件都有便捷的借口函数方式对其进行访问。将它们的名称列在这里的原因是，
插件和以上系统自带的控件，**名称不能相同**。

## Pyminer工具栏中按钮的获取
### 主页工具栏
|内部名称 |中文名称|
|---------|---------| 
|'button_new_script'|'新建\n脚本'|
|'button_new'|'新建'|
|'button_open'|'打开'|
|'button_import_data'|'导入\n数据',|
|'button_save_workspace'|'保存\n工作区',|
|'button_new_variable'|'新建变量'|
|'button_open_variable'|'打开变量'|
|'button_clear_workspace'|'清除工作区'|
|'button_search_for_files'|'查找文件'|
|'button_compare_files'|'文件比较'|
|'button_settings'|'设置'|
|'button_help'| '帮助'|
|'view_config'|'视图'|

