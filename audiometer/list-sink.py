import pulsectl

with pulsectl.Pulse() as pulse:
    print(pulse.sink_list())
    print(pulse.source_list())