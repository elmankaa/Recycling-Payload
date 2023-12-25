import sys
sys.path.append('../')
from Common.project_library import *

# Modify the information below according to you setup and uncomment the entire section

# 1. Interface Configuration
project_identifier = 'P3B' # enter a string corresponding to P0, P2A, P2A, P3A, or P3B
ip_address = '169.254.94.249' # enter your computer's IP address
hardware = False # True when working with hardware. False when working in the simulation

# 2. Servo Table configuration
short_tower_angle = 315 # enter the value in degrees for the identification tower 
tall_tower_angle = 90 # enter the value in degrees for the classification tower
drop_tube_angle = 180#270# enter the value in degrees for the drop tube. clockwise rotation from zero degrees

# 3. Qbot Configuration
bot_camera_angle = -21.5 # angle in degrees between -21.5 and 0

# 4. Bin Configuration
# Configuration for the colors for the bins and the lines leading to those bins.
# Note: The line leading up to the bin will be the same color as the bin 

bin1_offset = 0.10 # offset in meters
bin1_color = [1,0,0] # e.g. [1,0,0] for red
bin2_offset = 0.20
bin2_color = [0,1,0]
bin3_offset = 0.30
bin3_color = [0,0,1]
bin4_offset = 0.30
bin4_color = [1,0,1]

#--------------- DO NOT modify the information below -----------------------------

if project_identifier == 'P0':
    QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
    bot = qbot(0.1,ip_address,QLabs,None,hardware)
    
elif project_identifier in ["P2A","P2B"]:
    QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
    arm = qarm(project_identifier,ip_address,QLabs,hardware)

elif project_identifier == 'P3A':
    table_configuration = [short_tower_angle,tall_tower_angle,drop_tube_angle]
    configuration_information = [table_configuration,None, None] # Configuring just the table
    QLabs = configure_environment(project_identifier, ip_address, hardware,configuration_information).QLabs
    table = servo_table(ip_address,QLabs,table_configuration,hardware)
    arm = qarm(project_identifier,ip_address,QLabs,hardware)
    
elif project_identifier == 'P3B':
    table_configuration = [short_tower_angle,tall_tower_angle,drop_tube_angle]
    qbot_configuration = [bot_camera_angle]
    bin_configuration = [[bin1_offset,bin2_offset,bin3_offset,bin4_offset],[bin1_color,bin2_color,bin3_color,bin4_color]]
    configuration_information = [table_configuration,qbot_configuration, bin_configuration]
    QLabs = configure_environment(project_identifier, ip_address, hardware,configuration_information).QLabs
    table = servo_table(ip_address,QLabs,table_configuration,hardware)
    arm = qarm(project_identifier,ip_address,QLabs,hardware)
    bins = bins(bin_configuration)
    bot = qbot(0.1,ip_address,QLabs,bins,hardware)
    

#---------------------------------------------------------------------------------
# STUDENT CODE BEGINS
#---------------------------------------------------------------------------------
import random

def load_container(count):
    '''
    purpose: to load a single container onto the Qbot using a series of arm control commands and time.sleeps
    input: N/A
    output:N/A
   '''
    if count!=2:
        arm.move_arm (0.629,0.0,0.270)
        time.sleep(1)
        arm.control_gripper (38)
        time.sleep(1)
        arm.move_arm(0.01, -0.183,0.48)
        time.sleep(1)
        arm.move_arm(0.022, -0.500,0.550)
        time.sleep(1)
        arm.move_arm(0.022, -0.500,0.500)
        time.sleep(1)
        arm.control_gripper(-38)
        time.sleep(1)
        arm.move_arm(0.02, -0.540,0.490)
        time.sleep(1.5)
        arm.move_arm(0.02, -0.450,0.490)
        time.sleep(1)
        arm.home()
    else:
        arm.move_arm (0.629,0.0,0.270)
        time.sleep(1)
        arm.control_gripper (38)
        time.sleep(1)
        arm.move_arm(0.022,-0.183,0.48)
        time.sleep(1)
        arm.move_arm(0.022, -0.420,0.550)
        time.sleep(1)
        arm.move_arm(0.022, -0.420,0.500)
        time.sleep(1)
        arm.control_gripper(-38)
        time.sleep(1)
        arm.move_arm(0.022, -0.490,0.490)
        time.sleep(1.5)
        arm.move_arm(0.022, -0.30,0.490)
        time.sleep(1)
        arm.home()
    
def box_01():
   
    #range of positions
    position1 = (1.04,0.64,0.00075)
    position2 = (1.05,0.65,0.000751)
    position = bot.position()
    #line following code
    while True:
        x = bot.line_following_sensors()
        bot.set_wheel_speed([0.1,0.1])
        if x == [0,1]:
            bot.set_wheel_speed([0.1,0])
        elif x == [1,0]:
            bot.set_wheel_speed([0,0.1])
        else:
            bot.set_wheel_speed([0.1,0.1])
            color = bot.read_color_sensor()
        #if the color matches the color we are testing for, the bot lines itself up and dumps the containers
        if color[0] == ([1,0,0]):
            time.sleep(5)
            bot.stop()
            time.sleep(3)
            bot.rotate(8)
            bot.activate_linear_actuator()
            bot.dump()
            break
        else:
            bot.activate_color_sensor()

def box_02():

    #range of positions
    position1 = (0.03,0.738,0.00075)
    position2 = (0.04,0.742,0.000751)
    position = bot.position()
    while True:
        x = bot.line_following_sensors()
        bot.set_wheel_speed([0.1,0.1])
        if x == [0,1]:
            bot.set_wheel_speed([0.1,0])
        elif x == [1,0]:
            bot.set_wheel_speed([0,0.1])
        else:
            bot.set_wheel_speed([0.1,0.1])
            color = bot.read_color_sensor()
        #if the color matches the color we are testing for, the bot lines itself up and dumps the containers
        if color[0] == ([0,1,0]):
            time.sleep(6)
            bot.stop()
            bot.rotate(-90)
            bot.forward_distance(0.05)
            bot.rotate(90)
            time.sleep(2)
            bot.activate_linear_actuator()
            bot.dump()
            time.sleep(1)
            bot.rotate(90)
            bot.forward_distance(0.05)
            bot.rotate(-90)
            break
        else:
            bot.activate_color_sensor()

def box_03():
       
    #range of positions
    position1 = (-0.1,-0.68,0.00075)
    position2 = (-0.09,-0.67,0.000751)
    position = bot.position()
    while True:
        x = bot.line_following_sensors()
        bot.set_wheel_speed([0.1,0.1])
        if x == [0,1]:
            bot.set_wheel_speed([0.1,0])
        elif x == [1,0]:
            bot.set_wheel_speed([0,0.1])
        else:
            bot.set_wheel_speed([0.1,0.1])
            color = bot.read_color_sensor()
        #if the color matches the color we are testing for, the bot lines itself up and dumps the containers
        if color[0] == ([0,0,1]):
            time.sleep(3.5)
            bot.stop()
            bot.rotate(-90)
            bot.forward_distance(0.15)
            bot.rotate(90)
            time.sleep(2)
            bot.activate_linear_actuator()
            bot.dump()
            time.sleep(1)
            bot.rotate(90)
            bot.forward_distance(0.15)
            bot.rotate(-90)
            break
        else:
            bot.activate_color_sensor()

def box_04():
       
    #range of positions
    position1 = (0.94,-0.737,0.00075)
    position2 = (0.97,-0.733,0.000751)
    position = bot.position()
    while True:
        x = bot.line_following_sensors()
        bot.set_wheel_speed([0.1,0.1])
        if x == [0,1]:
            bot.set_wheel_speed([0.1,0])
        elif x == [1,0]:
            bot.set_wheel_speed([0,0.1])
        else:
            bot.set_wheel_speed([0.1,0.1])
            color = bot.read_color_sensor()
            #if the color matches the color we are testing for, the bot lines itself up and dumps the containers
            if color[0] == ([1,0,1]):
                time.sleep(3)
                bot.stop()
                bot.rotate(-90)
                bot.forward_distance(0.16)
                bot.rotate(90)
                time.sleep(3)
                bot.activate_linear_actuator()
                bot.dump()
                time.sleep(1.5)
                bot.rotate(90)
                bot.forward_distance(0.19)
                bot.rotate(-90)
                break
            else:
                bot.activate_color_sensor
      


def deposit_container(binid):
    '''
    purpose: uses given bin id to call the correct function
    input: bin id
    output:n/a
    author:  Ameen Elmankabady 
    '''
    if binid == 'Bin01':
        box_01()
    elif binid == 'Bin02':
        box_02()
    elif binid == "Bin03":
        box_03()
    elif binid == 'Bin04':
        box_04()
    else:
        None


def return_home():
    '''
    purpose:
    input:N/A
    output:N/A
    author: Ameen Elmankabady 
    '''
    #range of positions
    variable1 = (1.4485,-0.08,0.00075)
    variable2 = (1.4515,-0.097,0.000751)
    #line following code
    while True:
        x = bot.line_following_sensors()
        bot.set_wheel_speed([0.08,0.08])
        if x == [0,1]:
            bot.set_wheel_speed([0.08,0])
        elif x == [1,0]:
            bot.set_wheel_speed([0,0.08])
        else:
            bot.set_wheel_speed([0.08,0.08])
            position = bot.position()
            #if the positions match up, stop the bot
            if variable1 < position < variable2:
                bot.stop()
                bot.rotate(3)
                bot.forward_distance(0.085)
                break
            else:
                bot.activate_ultrasonic_sensor


def main(container_present,last_mass,last_binid):
    '''
    purpose: to spawn random containers onto the table and call each respective function
    input:N/A
    output:N/A
    author: Ameen Elmankabady
    '''

    #setting list of containers
    container_list = [1,2,3,4,5,6]
    bot.activate_color_sensor()

    #checks if there is a container already present on table
    if not container_present:
        count=0
        total_mass=0
    else:
        count=1
        total_mass=last_mass
        binid=last_binid
        time.sleep(1)
        load_container(1)

    while count < 3:
        rand_container=random.choice(container_list)
        container = table.dispense_container(rand_container,True)
        print(container[2])
        container_mass=container[1]
        container_binid=container[2]
        total_mass=total_mass+container_mass
        
        if count==0 and total_mass < 90:
            count=count+1
            load_container(0)
            time.sleep(1)
            
            binid = container_binid
            mass=container_mass
            
              
        elif count==1 and total_mass < 90 and container_binid == binid:
            count=count+1
            time.sleep(1)
            load_container(1)
                
        elif count==2 and total_mass < 90 and container_binid == binid:
            count=count+1
            time.sleep(1)
            load_container(2)
            deposit_container(binid)
            return_home()
            print("cart is full")
            return False, container_mass, container_binid
                
        else:
            #if total_mass >90 or if the containers bin ids dont match
            print("binid's dont match or overweight")
            deposit_container(binid)
            return_home()
            return True, container_mass, container_binid


def run():
   
    check_container=False
    while True:
        if check_container==False:
            check_container,last_container_mass,last_container_binid = main(False,0,"None")
        else:
            check_container,last_container_mass,last_container_binid = main(check_container,last_container_mass,last_container_binid)
    
       
#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------
