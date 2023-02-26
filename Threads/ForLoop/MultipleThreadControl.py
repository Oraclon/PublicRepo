from SingleThreadControl import MainThread

for i in range(6):
    s = MainThread(counter=i)
    s.start()