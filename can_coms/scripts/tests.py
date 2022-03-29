import struct
import time
import os
import can

def uint_to_float(x, x_min, x_max, bits):
    # Converts unsigned int to float, given range and number of bits
    span = x_max - x_min
    offset = x_min
    return (float(x))*span/(float(((1<<bits)-1))) + offset

p_min =-95.5
p_max = 95.5
v_min = -45.0
v_max = 45.0
kp_min = 0.0
kp_max = 500.0
kd_min = 0.0
kd_max = 5.0
i_min = -18.0
i_max = 18.0
b_driver = [0x3,0x7b,0xa4,0x80,0x38,0x01]

p_int = (b_driver[1]<<8)|b_driver[2]
v_int = (b_driver[3]<<4)|(b_driver[4]>>4)
i_int = ((b_driver[4]&0xF)<<8)|b_driver[5]

controller =[]
controller.append(b_driver[0])
controller.append(uint_to_float(p_int, p_min, p_max, 16))
controller.append(uint_to_float(v_int, v_min, v_max, 12))
controller.append(uint_to_float(i_int, i_min, i_max, 12))
print("p_des",controller[0])
print("v_des", controller[1])
print("t_ff", controller[2])