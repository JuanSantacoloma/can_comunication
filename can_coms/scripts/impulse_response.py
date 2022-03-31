'''
Motor Module example program.
Ben Katz
'''

import motormodule as mm
import time
import csv


if __name__ == "__main__":
    mmc = mm.MotorModuleController(3)        # Connect to the controller's serial port
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
    # With a 1st-order response
    # rx_values are ordered (CAN ID, Position, Velocity, Current)
    # initial_msg = mmc.get_data()
    start_position = mmc.get_data()
    # Posicion inicial del motor
    p_inicial = start_position[1]
    
    # Posicion objetivo
    p_obj = 3.14
    p_actual = start_position[1]
    print(p_actual)
    error = p_obj
    while(error > 0.1):
        # p_inicial = 1.01*p_inicial
        tasks.append(mmc.send_command(p_obj , 0, 1.0, 0, 0))
        time.sleep(0.02)
        p_actual = mmc.get_data()
        recep.append(p_actual)
        p_actual = p_actual[1]
        error =p_obj -p_actual
        
        # print(p_actual)
    mmc.disable_motor()
    with open('impulse_response_motor', 'w') as f:
        write = csv.writer(f)
        write.writerow(response_motor)
        write.writerows(recep)
    with open('impulse_response_control', 'w') as fa:
        write = csv.writer(fa)
        write.writerow(fields_2)
        write.writerows(tasks)

