'''
Motor Module example program.
Ben Katz
'''

import motormodule as mm
import time
import csv


if __name__ == "__main__":
    mmc = mm.MotorModuleController(1)        # Connect to the controller's serial port
    # can_ids = [
    #     0x181080F5, 0x181081F5, 0x181082F5, 0x181083F5,
    #     0x181084F5, 0x181085F5, 0x181086F5, 0x181087F5,
    #     0x181088F5, 0x181089F5
    # ]
    tasks = []
    recep = []
    response_motor = ['Timestamp','POS', 'VEL', 'Torq']
    fields_2 = ['POS_Set_point', 'VEL_setpoint', 'POS gain', 'VEL gain', 'FOC']

    mmc.enable_motor()
    # Send a command:  
    # (CAN ID, position setpoint, velocity setpoint, position gain, velocity gain, feed-forward torque)
    # Units are:  Radians, Rad/s, N-m/rad, N-m/rad/s, N-m
    mmc.send_command( 0, 0, 0, 0,  0)
    time.sleep(.1)
    # This example reads the start position of the motor
    # Then sends position commands to ramp the motor position to zero 
    # With a 1st-order response
    # rx_values are ordered (CAN ID, Position, Velocity, Current)
    initial_msg = mmc.get_data()
    
    start_position = mmc.get_data()

    # Posicion inicial del motor
    p_des = start_position[1]
    
    # Posicion deseada
    print("msg_rec=",start_position)
    print("p_des =",p_des)
    p_obj = 3.14
    # while True:
    #     position = mmc.get_data()
    #     print("Position",position)
    while(p_des > 0.01):
        p_des = .99*p_des
        tasks.append(mmc.send_command(p_des , 0, 5, 0, 0))
        time.sleep(0.02)
        recep.append(mmc.get_data())
    # a=1000
    # while(a > 0):
    #     # p_des = .99*p_des
    #     tasks.append(mmc.send_command(p_des , 0, 1, 0, 0))
    #     time.sleep(0.02)
    #     # position = mmc.get_data()
    #     recep.append(mmc.get_data())
    #     a=a-1
        # print("Position",position)

    mmc.disable_motor()
    with open('response_kp_5', 'w') as f:
        write = csv.writer(f)
        write.writerow(response_motor)
        write.writerows(recep)
    with open('control_kp_5', 'w') as fa:
        write = csv.writer(fa)
        write.writerow(fields_2)
        write.writerows(tasks)

