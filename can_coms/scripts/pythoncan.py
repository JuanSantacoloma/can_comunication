import can
can.rc['interface'] = 'socketcan'
can.rc['channel'] = 'can0'
can.rc['bitrate'] = 1000000
from can.interface import Bus
from can import Message
bus = Bus()

#filters = [{"can_id": 0x4, "can_mask": 0x7FF, "extended": False},]
#bus = can.interface.Bus(can_filters=filters)
bus.recv()

for msg in bus:
    print(Message(data =msg.data,is_extended_id=False))