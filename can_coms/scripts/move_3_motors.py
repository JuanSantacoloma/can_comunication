'''
Motor Module example program.
Ben Katz
'''

import motormodule as mm
import time
import csv


if __name__ == "__main__":
    tasks = []
    # def motors
    m_t = mm.MotorModuleController(1)        # Connect to the controller's serial port
    m_f = mm.MotorModuleController(2) 
    m_h = mm.MotorModuleController(3) 
    # enable motors
    m_t.enable_motor()
    m_f.enable_motor()
    m_h.enable_motor()
    # Send a command:  
    # (CAN ID, position setpoint, velocity setpoint, position gain, velocity gain, feed-forward torque)
    # Units are:  Radians, Rad/s, N-m/rad, N-m/rad/s, N-m
    m_t.send_command( 0, 0, 0, 0, 0)
    m_f.send_command( 0, 0, 0, 0, 0)
    m_h.send_command( 0, 0, 0, 0, 0)

    time.sleep(.1)
    # This example reads the start position of the motor
    # Then sends position commands to ramp the motor position to zero 
    # With a 1st-order response
    # rx_values are ordered (CAN ID, Position, Velocity, Current)
    initial_msg_m_t = m_t.get_data()
    initial_msg_m_f = m_f.get_data()
    initial_msg_m_h = m_h.get_data()

    if m_t.get_data()[0] == 1:
        st_pos_m_t = m_t.get_data()
    if m_f.get_data()[0] == 2:
        st_pos_m_f = m_f.get_data()
    if m_h.get_data()[0] == 3:
        st_pos_m_h = m_h.get_data()

    # Posicion inicial del motor
    p_actual_m_t = st_pos_m_t[2]
    p_actual_m_f = st_pos_m_f[2]
    p_actual_m_h = st_pos_m_h[2]
    
    # Posicion actual motores
    print("p_actual_m_t =",p_actual_m_t)
    print("p_actual_m_f =",p_actual_m_f)
    print("p_actual_m_h =",p_actual_m_h)

    while(p_actual_m_t > 0.01 or p_actual_m_f > 0.01 or p_actual_m_h > 0.01):
        if st_pos_m_t[0] == 1:
            p_actual_m_t = .99*p_actual_m_t
            tasks.append(mmc.send_command(p_actual_m_t , 0, 1, 0, 0))
        if st_pos_m_f[0] == 2:
            p_actual_m_f = .99*p_actual_m_f
            tasks.append(mmc.send_command(p_actual_m_f , 0, 1, 0, 0))
        if st_pos_m_h[0] == 3:
            p_actual_m_h = .99*p_actual_m_h
            tasks.append(mmc.send_command(p_actual_m_f , 0, 1, 0, 0))
        time.sleep(0.02)
    
    m_f.disable_motor()
    m_h.disable_motor()
    m_t.disable_motor()


