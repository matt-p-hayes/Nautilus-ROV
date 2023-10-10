# file: main.py
# description: main file for GUI
# Nautilus 2021-2022 contributors: Nathan Burke, Mandeep Singh

from imports import *

nmea_string = None
data = None
map_dict = {}
map2_dict = {}
closed_loop_dict={"head" : 0, "depth" : 0, "altitude" : 0}
pid_dict={"head": None, "depth": None, "altitude": None}
gui = None
gamepad = None
gamepad2 = None
port = '/dev/ttyUSB1'
ard = None
logFile = None



# function: startup()
# description: called first to initialize components
def startup():
    global ard, logFile    

    
    logFile = initialize_log_folder()

    #prepare necessary resources for gamepad
    if config.gamepad_flag:
        global gamepad
        print("gamepad initializing...")
        #gamepad initialization
        generate_dictionaries("map.txt") 
        gamepad = Gamepad()
        config.gamepad_flag = gamepad.init(0)
        print("gamepad initialized")
    #prepare necessary resources for second gamepad
    if config.gamepad2_flag:
    	global gamepad2
    	print("second gamepad initializing...")
    	#second gamepad initialization
    	generate_dictionaries("map2.txt")
    	gamepad2 = Gamepad()
    	config.gamepad2_flag = gamepad2.init(1)
    	print("second gamepad initialized")
    	
    # socket initialization
    if config.socket_flag:
        ard = serial.Serial(port,115200,timeout=6)
    
    # camera initialization
    if config.cam_flag:
        cam_init()

    # if config.altitude_lock_flag:
    #     init_altitude_pid(20)


# function: processes()
# description: called to send control strings over socket
# and update GUI overlay video and data
def processes():
    global nmea_string, gamepad, gamepad2, ard, closed_loop_dict, pid_dict, logFile 

    #listen for gamepad
    if config.gamepad_flag:
        gamepad.listen(gamepad2)
        interpret(gamepad)
        interpret2(gamepad2)
        pass
    else:      
        pass
        
    

    nmea_string = generate(config.top_data, config.sub_data, closed_loop_dict, pid_dict, gui.return_arm(), config.arm_inputs)

    nmea_string_stripped = nmea_string.replace(" ", "")

    #WRITE SEND MESSAGE TO LOG
    write_to_log(nmea_string_stripped, logFile)

    #print(nmea_string_stripped)
    nmea_string_utf = nmea_string_stripped.encode(encoding='ascii')
    print(nmea_string_utf)

    if config.socket_flag:
        #send control string over socket s
        startTime = time.time()
        ard.write(nmea_string_utf)
        #print("ard written")
        receive_string = ard.read()
        endTime = time.time()
        #print(endTime-startTime)
        #print("ard received")
        while('*' not in str(receive_string)):
            receive_string += ard.read()	
        #print("Receive String:", receive_string)
        str_receive_string = str(receive_string)
        receive_string_tokens = str_receive_string.split(',', 8)
        tmpr = receive_string_tokens[2]
        depth = receive_string_tokens[3]
        head = receive_string_tokens[4]
        altitude = receive_string_tokens[5]
        leak = receive_string_tokens[6]
        voltage = receive_string_tokens[7]
        
        #add values coming up from ROV to the sub_data dictionary to pass to generator
        config.sub_data.assign("TMPR", tmpr)
        config.sub_data.assign("DEPTH", depth)
        config.sub_data.assign("HEAD", head)
        config.sub_data.assign("ALT", altitude)
        #print("Leak: ", leak)
        #print("Voltage: ", voltage)
        #print("Altitude in Feet:", altitude)
        gui.sensor_display("ALT", altitude)
        gui.sensor_display("DEPTH", depth)
        gui.sensor_display("HEAD", head)
        #gui.rotation_display(head)
        gui.sensor_readout(tmpr, depth, head, altitude, voltage)
        closed_loop_dict = gui.closed_loop_control()
        pid_dict = gui.return_pids()
        #print(pid_dict["depth"].calculate_next(pres))    
        pass
    
    # update camera
    if config.cam_flag:
        cam_update(head, depth)
        pass

    #WRITE RECEIVED MESSAGE TO LOG
    write_to_log(str_receive_string,logFile)

    # print("begin_dummy: ", receive_string_tokens[0])
    # print("id_val: ", receive_string_tokens[1])
    # print("tmpr", receive_string_tokens[2])
    # print("pressure", receive_string_tokens[3])
    # print("head:", receive_string_tokens[4])


    gui.status_display(nmea_string)
    gui.after(config.PROCESS_RATE, processes)


# function: on_closing()
# description: called on exit to kill camera and GUI processes
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        if config.gamepad_flag:
            pass
        
        if config.socket_flag:
            pass

        if config.cam_flag:
            cam_kill()
            pass
            
        gui.destroy()


# main module to execute functions
if __name__ == "__main__":

    startup()

    #build GUI
    gui = neptuneGUI()
    ani = gui.sensor_animate(config.PROCESS_RATE * 2)

    gui.after(50, processes)

    gui.protocol("WM_DELETE_WINDOW", on_closing)
    gui.mainloop()





