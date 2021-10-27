import markdown


class MarkdownRenderer(object):
    @staticmethod
    def render(content: str) -> str:
        return markdown.markdown(content)
