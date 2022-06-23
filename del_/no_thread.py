import numpy as np
import time

VAL = 3

class Gui:
    def __init__(self):
        self.result_mtx = np.zeros((VAL, VAL))

    def create_obj(self):
        return My_matrix()

    def fabric(self):
        for num_obj in range(2):
            num_obj = self.create_obj()
            num_obj.change_m()
            self.result_mtx = num_obj.mtx + self.result_mtx



class My_matrix:

    def __init__(self):

        self.mtx = np.zeros((VAL, VAL))
        # print(self.mtx)

    def change_m(self):
        i = 1
        for x in range(VAL):
            for y in range(VAL):
                time.sleep(1)
                self.mtx[x][y] = self.mtx[x][y] + i


if __name__ == "__main__":
    start_time = time.time()
    class_ = Gui()
    class_.fabric()
    print(class_.result_mtx)
    print("--- %s seconds ---" % (time.time() - start_time))
