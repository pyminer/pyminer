"""
这个包用于容纳所有PyMiner的数据结构。
数据结构主要用于实现适配功能，将不同包里面的优秀数据结构进行整合，包装为PyMiner对象，以达到为PyMiner所用的目的。
在用户端，并不会看到这些数据结构，而是仍会拿到各个包里面的原始数据结构。
TODO 数据结构并没有进行社区讨论，是我拍脑袋写的，后面应当再进行接口及结构类型的合理性分析。
目前需要讨论的点是，数据结构是采用大而全的方式，还是采用小而精的方式？
具体的数据结构还要部分依赖于Reco的C共享内存实现，目前只是一个快速开发的版本。
> 之前考虑过直接继承numpy.ndarray等数据结构，不过在实际的操作中发现较多问题，目前已放弃，转为采用Adapter的思路。 -- panhaoyu
"""

from .array import ArrayAdapter
from .base_structure import BaseAdapter
from .universal import UniversalAdapter
