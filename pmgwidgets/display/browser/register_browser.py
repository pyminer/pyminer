def register_web_browser():
    import webbrowser

    webbrowser.register("qtbrowser", None,
                        webbrowser.GenericBrowser(
                            r"python E:\Python\pmgwidgetsproj\pmgwidgets\display\browser\browser.py"))

    # c.NotebookApp.browser = 'qtbrowser'
    webbrowser.get('qtbrowser').open_new('https://cn.bing.com')


register_web_browser()
