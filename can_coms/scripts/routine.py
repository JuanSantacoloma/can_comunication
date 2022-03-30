'''
Motor Module example program.
Ben Katz
'''

import motormodule as mm
import time
#define P_MIN -95.5f
#define P_MAX 95.5f
#define V_MIN -45.0f
#define V_MAX 45.0f
#define KP_MIN 0.0f
#define KP_MAX 500.0f
#define KD_MIN 0.0f
#define KD_MAX 5.0f
#define I_MIN -18.0f
#define I_MAX 18.0f
p_min =-95.5
p_max = 95.5
v_min = -45.0
v_max = 45.0
kp_min = 0.0
kp_max = 50.0
kd_min = 0.0
kd_max = 5.0
i_min = -18.0
i_max = 18.0
# Send a command:  
# (CAN ID, position setpoint, velocity setpoint, position gain, velocity gain, feed-forward torque)
# Units are:  Radians, Rad/s, N-m/rad, N-m/rad/s, N-m
# mmc.send_command(1, 0, 0, 0, 0,  0)
# time.sleep(.1)

# This example reads the start position of the motor
# Then sends position commands to ramp the motor position to zero 
# With a 1st-order response
# rx_values are ordered (CAN ID, Position, Velocity, Current)

if __name__ == "__main__":
    mmc = mm.MotorModuleController(3)        # Connect to the controller's serial port
    # can_ids = [
    #     0x181080F5, 0x181081F5, 0x181082F5, 0x181083F5,
    #     0x181084F5, 0x181085F5, 0x181086F5, 0x181087F5,
    #     0x181088F5, 0x181089F5
    # ]
    tasks = []
    mmc.enable_motor()
    mmc.send_command( 0, 0, 0, 0,  0)
    time.sleep(.1)

    initial_msg = mmc.get_data()
    
    start_position = mmc.get_data()

    # msg_rec = [x for x in start_position.data]
    p_des = start_position[0]
    # p_des = 1
    print("msg_rec=",start_position)
    print("p_des =",p_des)
    # while True:
    #     position = mmc.get_data()
    #     print("Position",position)
    while(p_des > .1):
        # p_des = .99*p_des
        tasks.append(mmc.send_command(p_des , 0, 5, 0, 0))
        time.sleep(0.02)
        position = mmc.get_data()
        print("Position",position)

    mmc.disable_motor()
