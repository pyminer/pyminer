from typing import Tuple, List, Union

import parso
from parso.tree import Leaf, Node


class GrammarAnalyzer:
    def __init__(self):
        """
        代码静态分析工具，用于识别括号匹配等内容
        """
        self.__code = ''
        self.__parsed_node_cache = None

    def feed(self, code: str) -> None:
        """使用当前编辑器里面的代码替换之前分析器中的代码

        Args:
            code: 当前编辑器中的代码
        """
        self.__code = code
        self.__parsed_node_cache = None

    @property
    def __parsed_node(self) -> Node:
        """使用parso进行解析后的代码"""
        if self.__parsed_node_cache is None:
            self.__parsed_node_cache = parso.parse(self.__code)
        return self.__parsed_node_cache

    def _convert_position_to_row_col(self, position: int) -> Tuple[int, int]:
        left_part = self.__code[:position]
        row = left_part.count('\n') + 1
        col = position - left_part.rfind('\n') - 1
        return row, col

    __PAIRS = {'(': ')', '[': ']', '{': '}'}

    def is_not_matched(self, position: Union[Tuple[int, int], int], left='('):
        """是否需要添加另一个配对项

        对于如下代码：``print(a, b, c#)`` ，在光标位于#处时，按下右括号键，是不需要再添加一个括号的。
        本方法即是为了解决这个问题，识别是否需要添加额外的括号。

        Args:
            position: 匹配位置
            left: 配对的左侧一项

        Returns:
            bool, 是否需要添加
        """
        if isinstance(position, int):
            position = self._convert_position_to_row_col(position)
        position: Tuple[int, int]
        right = self.__PAIRS[left]
        leaf: Leaf = self.__parsed_node.get_leaf_for_position(position)
        node: Node = leaf.parent
        child: Node
        leaves: List[Node] = [leaf]
        while node is not None:
            # print(node.children)
            leaves.extend([child for child in node.children if child is not leaf and child.type == 'operator'])
            node, leaf = node.parent, leaf.parent
        characters: List[str] = [leaf.get_code().strip() for leaf in leaves]
        # print(characters, characters.count(left), characters.count(right))
        return characters.count(left) - characters.count(right) > 0
