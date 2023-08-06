from . import Mvi
import threading
import os
from . import mudeConstant as mc


class mvi_Thread(threading.Thread):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.layer = os.path.basename(path).split('_')[1]

    def run(self) -> None:
        self.result = Mvi.mvi(self.path)

    def get_result(self):
        return self.layer, self.result


def func(a: int, b: int) -> int:
    return a + b


def mvi_read(project):
    pro_path = os.path.join(mc.Project_Path, project, '0_101')
    mvis = os.listdir(pro_path)
    mvis = [i for i in mvis if i.find('.mvi') > 0]
    threads = []
    for mvi in mvis:
        threads.append(mvi_Thread(path=os.path.join(pro_path, mvi)))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    result = []
    for thread in threads:
        result.append(thread.get_result())
    return result


if __name__ == '__main__':
    pass
