#!/usr/bin/env python

import game_thread

game = game_thread.GameThread(2)
game.start()
game.loop()





