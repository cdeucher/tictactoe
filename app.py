import random, time
import numpy as np
import json
from tools import encode_state,decode_state, getAllPossibleNextAction, try_action, win_or_loss
import train as T

world = T.oTrain()
world.try_train(10, 1)
world.save_train('easy.txt')

world1 = T.oTrain()
world1.try_train(50000, 1)
world1.save_train('medium.txt')

world2 = T.oTrain()
world2.try_train(3000000, 1)
world2.try_train(3000000, 2)
world2.save_train('hard.txt')

lvls = [world, world1, world2]