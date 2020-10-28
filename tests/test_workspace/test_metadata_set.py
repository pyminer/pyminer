from pyminer2.workspace.datamanager import metadataset, exceptions
import pytest
import threading


def test_define_modify():
    ms = metadataset.MetaDataSet()

    ms.define_data('testData', metadataset.MetaData('noProvider'))
    assert ms['testData']['modified_by'] == ['noProvider']

    ms.modify_data('testData', 'newProvider')
    assert ms['testData']['modified_by'] == ['noProvider', 'newProvider']

    ms.delete_data('testData')
    assert ms['testData']['deleted'] == True

    ms.restore_data('testData')
    assert ms['testData']['deleted'] == False


def test_lock():
    #     TODO (panhaoyu) 多线程玩不转，请补充测试用例
    # ms = metadataset.MetaDataSet()
    # ms.define_data('testData', metadataset.MetaData('noProvider'))
    # with ms.lock_data('testData'):
    #     def target():
    #         # TODO 这里是否应该报错，结果并没有抛出异常
    #         # with pytest.raises(exceptions.WouldBlockError):
    #         ms.modify_data('testData', 'newProvider')
    #
    #     thread = threading.Thread(target=target)
    #     thread.start()
    #     thread.join()
    # 这一部分代码目前已不打算继续开发，等共享内存的传值完成后再进一步考虑如何开发
    pass
