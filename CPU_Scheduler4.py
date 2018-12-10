def display_main_menu():
    print("MAIN MENU")
    print("1    -   FCFS: First Come, First Serve - non-preemptive")
    print("2    -   SJF: Shortest Job First - non-preemptive")
    print("3    -   MLFQ: Multilevel Feedback Queue - Absolute priority in higher queue")
    print("0    -   Exit Program")
    print()

#GLOBAL PROCESS TUPLES/ARRAYS

processes = {"P1":(4, 24, 5, 73, 3, 31, 5, 27, 4, 33, 6, 43, 4, 64, 5, 19, 2),            #352
             "P2":(18, 31, 19, 35, 11, 42, 18, 43, 19, 47, 18, 43, 17, 51, 19, 32, 10),   #473
             "P3":(6, 18, 4, 21, 7, 19, 4, 16, 5, 29, 7, 21, 8, 22, 6, 24, 5),            #222  
             "P4":(17, 42, 19, 55, 20, 54, 17, 52, 15, 67, 12, 72, 15, 66, 14),           #537
             "P5":(5, 81, 4, 82, 5, 71, 3, 61, 5, 62, 4, 51, 3, 77, 4, 61, 3, 42, 5),     #629
             "P6":(10, 35, 12, 41, 14, 33, 11, 32, 15, 41, 13, 29, 11),                   #297
             "P7":(21, 51, 23, 53, 24, 61, 22, 31, 21, 43, 20),                           #370
             "P8":(11, 52, 14, 42, 15, 31, 17, 21, 16, 43, 12, 31, 13, 32, 15)}           #365
process_key = ("P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8")



#FIRST COME FIRST SERVE FUNCTION

def FCFS():

    #DEFINE FUNCTION VARIABLES
    cpu_utilization_time = 0
    cpu_counter = 0
    io_timer = {"P1":0, "P2":0, "P3":0, "P4":0, "P5":0, "P6":0, "P7":0, "P8":0}
    #READY ARRAY 9 = START STATE, 8 = BURSTING, 7 = FINISHED, 1 = READY, 0 = IN IO
    ready_array = {"P1":0, "P2":9, "P3":9, "P4":9, "P5":9, "P6":9, "P7":9, "P8":9}
    ready_queue = []
    time_response = {"P1":0, "P2":0, "P3":0, "P4":0, "P5":0, "P6":0, "P7":0, "P8":0}
    time_turn = {"P1":0, "P2":0, "P3":0, "P4":0, "P5":0, "P6":0, "P7":0, "P8":0}
    time_wait = {"P1":0, "P2":0, "P3":0, "P4":0, "P5":0, "P6":0, "P7":0, "P8":0}
    finished_processes = []
    process_index = {"P1":0, "P2":0, "P3":0, "P4":0, "P5":0, "P6":0, "P7":0, "P8":0}   #Position in process

    #At CPU Counter = 0 - Set ready queue from process key tuple
    print("Count: ", cpu_counter)
    ready_queue = list(process_key)
    final_process_first_pass = ready_queue[-1]
    process_list = list(process_key)
    cpu_counter += 1
    cpu_utilization_time += 1

    
    print("Ready Queue: ", ready_queue)
    process = ready_queue[0]
    print("Process: ", process)
    current_process = processes[process]
    print("Current Process: ", ready_queue[0], "=", current_process)
    current_process_index = process_index[process]
    print("Current Process Index: ", current_process_index)
    current_burst = current_process[current_process_index]
    print("Current Burst: ", current_burst)
    if current_process_index < (len(current_process) - 1):
       current_io = current_process[current_process_index + 1]
    else:
       current_io = 0
    print("Current IO: ", current_io)
    ready_array[process] = 8
    del ready_queue[0]


    while process_list:

        print("\n")
        print("Ready Queue:", ready_queue)
        print("Count: ", cpu_counter)
        print("Current Burst in process ", process, ":", current_burst)
        print("Current IO", current_io)
        print("Ready Array: ", ready_array)
        print("Time Wait: ", time_wait)

        #Subtract burst
        current_burst = current_burst - 1

        #Subtract IO
        for y in range(len(io_timer)):
            z = process_key[y]
            if io_timer[z] != 0:
                io_timer[z] = io_timer[z] - 1

        #Compute Time-Wait for processes in ready queue
        for y in range(len(time_wait)):
            z = process_key[y]
            if ready_array[z] == 9 or ready_array[z] == 1:
                time_wait[z] = time_wait[z] + 1
        
        #Move any finished IO to ready queue
        for y in range(len(io_timer)):
            z = process_key[y]
            if io_timer[z] == 0 and ready_array[z] == 0:
                ready_queue.append(z)
                ready_array[z] = 1

        #Compute Time-Response
        if ready_array[final_process_first_pass] == 9:
            for y in range(len(ready_array)):
                z = process_key[y]
                if ready_array[z] == 9:
                    time_response[z] = time_response[z] + 1

        #Increment CPU Counter
        cpu_counter += 1
        cpu_utilization_time += 1
        
        #When burst finishes, process moves to IO and next process pulled from ready queue
        if current_burst == 0:
             #IF PROCESS FINISHED
            if current_io == 0:
                print(ready_queue)
                finished_processes.append(process)
                print("REMOVING", process)
                process_list.remove(process)
                time_turn[process] = cpu_counter - 1 #Subtract 1 because counter already incremented
                ready_array[process] = 7
                print("Ready Queue: ", ready_queue)    
                print("Finished Processes: ", finished_processes)
                print("Remaining Processes: ", process_list)
                print("Time Wait:", time_wait)

            else:
                io_timer[process] = current_io
                ready_array[process] = 0
                process_index[process] += 2
                print("IO Timer", io_timer)

            if not process_list:
                break
            
            #IO CONVOY HANDLING
            while ready_queue == []:
                for y in range(len(process_key)):
                    z = process_key[y]
                    io_timer[z] = io_timer[z] - 1
                    if io_timer[z] == 0:
                        ready_queue.append(z)
                        ready_array[z] = 1
                cpu_counter += 1

            print("Ready Queue: ", ready_queue)
            process = ready_queue[0]
            print("Process: ", process)
            current_process = processes[process]
            print("Current Process: ", ready_queue[0], "=", current_process)
            current_process_index = process_index[process]
            print("Current Process Index: ", current_process_index)
            current_burst = current_process[current_process_index]
            print("Current Burst: ", current_burst)
            #print("Length of Current Process: ", len(current_process))
            if current_process_index < (len(current_process) - 1):
                current_io = current_process[current_process_index + 1]
            else:
                current_io = 0
            print("Current IO: ", current_io)
            print("Time Response: ", time_response)
            print("Time Wait: ", time_wait)
            ready_array[process] = 8
            del ready_queue[0]

    print("\n")
    print("FINAL RESULTS")
    print("---------------------")
    print("CPU Utilization: ", (cpu_utilization_time / cpu_counter))
    print("Time Response: ", time_response)
    print("Time Turnaround: ", time_turn)
    print("Time Wait: ", time_wait)
    print("FINISHED")



def SJF():
 #DEFINE FUNCTION VARIABLES
    cpu_utilization_time = 0
    cpu_counter = 0
    io_timer = {"P1":0, "P2":0, "P3":0, "P4":0, "P5":0, "P6":0, "P7":0, "P8":0}
    #READY ARRAY 9 = START STATE, 8 = BURSTING, 7 = FINISHED, 1 = READY, 0 = IN IO
    ready_array = {"P1":0, "P2":9, "P3":9, "P4":9, "P5":9, "P6":9, "P7":9, "P8":9}
    ready_bursts = []
    ready_queue = []
    new_ready_queue = []
    
    time_response = {"P1":0, "P2":0, "P3":0, "P4":0, "P5":0, "P6":0, "P7":0, "P8":0}
    time_turn = {"P1":0, "P2":0, "P3":0, "P4":0, "P5":0, "P6":0, "P7":0, "P8":0}
    time_wait = {"P1":0, "P2":0, "P3":0, "P4":0, "P5":0, "P6":0, "P7":0, "P8":0}
    finished_processes = []
    process_index = {"P1":0, "P2":0, "P3":0, "P4":0, "P5":0, "P6":0, "P7":0, "P8":0}   #Position in process

    #At CPU Counter = 0 - Set ready queue from process key tuple
    print("Count: ", cpu_counter)
    ready_queue = list(process_key)
    
    #Sorts Ready Queue so shortest burst goes first
    #Creates Ready Burst array of bursts in ready queue
    for y in range(len(ready_queue)):
        z = ready_queue[y]
        a = process_index[z]
        burst = processes[z][a]
        ready_bursts.append(burst)
    print("Ready Bursts: ", ready_bursts)
    #Puts bursts in a Dictionary for sorting
    ready_dict = dict(zip(ready_queue, ready_bursts))
    print("Ready Dictionary: ", ready_dict)
    #Sorts dictionary
    for s in sorted(ready_dict, key=ready_dict.get):     # value-based sorting
        print(s, ready_dict[s])
        new_ready_queue.append(s)
    print("New Ready Queue: ", new_ready_queue)
    ready_queue = new_ready_queue
    new_ready_queue = []
    final_process_first_pass = ready_queue[-1]
    #print(final_process_first_pass)
    	




    process_list = list(process_key)
    cpu_counter += 1
    cpu_utilization_time += 1

    
    print("Ready Queue: ", ready_queue)
    print("Ready Bursts: ", ready_bursts)
    process = ready_queue[0]
    print("Process: ", process)
    current_process = processes[process]
    print("Current Process: ", ready_queue[0], "=", current_process)
    current_process_index = process_index[process]
    print("Current Process Index: ", current_process_index)
    current_burst = current_process[current_process_index]
    print("Current Burst: ", current_burst)
    if current_process_index < (len(current_process) - 1):
       current_io = current_process[current_process_index + 1]
    else:
       current_io = 0
    print("Current IO: ", current_io)
    ready_array[process] = 8
    del ready_queue[0]


    while process_list:

        print("\n")
        print("Ready Bursts: ", ready_bursts)
        print("Ready Queue:", ready_queue)
        print("Count: ", cpu_counter)
        print("Current Burst in process ", process, ":", current_burst)
        print("Current IO", current_io)
        print("Ready Array: ", ready_array)
        print("Time Wait: ", time_wait)

        #Subtract burst
        current_burst = current_burst - 1

        #Subtract IO
        for y in range(len(io_timer)):
            z = process_key[y]
            if io_timer[z] != 0:
                io_timer[z] = io_timer[z] - 1

        #Compute Time-Wait for processes in ready queue
        for y in range(len(time_wait)):
            z = process_key[y]
            if ready_array[z] == 9 or ready_array[z] == 1:
                time_wait[z] = time_wait[z] + 1
        
        #Move any finished IO to ready queue
        for y in range(len(io_timer)):
            z = process_key[y]
            ready_bursts = []
            if io_timer[z] == 0 and ready_array[z] == 0:
                ready_queue.append(z)
                ready_array[z] = 1

                #Sorts Ready Queue so shortest burst goes first
                for y in range(len(ready_queue)):
                    z = ready_queue[y]
                    a = process_index[z]
                    burst = processes[z][a]
                    ready_bursts.append(burst)
                print("Ready Bursts: ", ready_bursts)
                ready_dict = dict(zip(ready_queue, ready_bursts))
                print("Ready Dictionary: ", ready_dict)
                for s in sorted(ready_dict, key=ready_dict.get):     # value-based sorting
                    print(s, ready_dict[s])
                    new_ready_queue.append(s)
                print("New Ready Queue: ", new_ready_queue)
                ready_queue = new_ready_queue
                new_ready_queue = []

        #Compute Time-Response
        if ready_array[final_process_first_pass] == 9:
            for y in range(len(ready_array)):
                z = process_key[y]
                if ready_array[z] == 9:
                    time_response[z] = time_response[z] + 1

        #Increment CPU Counter
        cpu_counter += 1
        cpu_utilization_time += 1
        
        #When burst finishes, process moves to IO and next process pulled from ready queue
        if current_burst == 0:
             #IF PROCESS FINISHED
            if current_io == 0:
                print(ready_queue)
                finished_processes.append(process)
                print("REMOVING", process)
                process_list.remove(process)
                time_turn[process] = cpu_counter - 1 #Subtract 1 because counter already incremented
                ready_array[process] = 7
                print("Ready Queue: ", ready_queue)    
                print("Finished Processes: ", finished_processes)
                print("Remaining Processes: ", process_list)
                print("Time Wait:", time_wait)

            else:
                io_timer[process] = current_io
                ready_array[process] = 0
                process_index[process] += 2
                print("IO Timer", io_timer)

            if not process_list:
                break
            
            #IO CONVOY HANDLING
            while ready_queue == []:
                for y in range(len(process_key)):
                    z = process_key[y]
                    io_timer[z] = io_timer[z] - 1
                    if io_timer[z] == 0:
                        ready_queue.append(z)
                        ready_array[z] = 1
                cpu_counter += 1

            print("Ready Bursts: ", ready_bursts)
            print("Ready Queue: ", ready_queue)
            process = ready_queue[0]
            print("Process: ", process)
            current_process = processes[process]
            print("Current Process: ", ready_queue[0], "=", current_process)
            current_process_index = process_index[process]
            print("Current Process Index: ", current_process_index)
            current_burst = current_process[current_process_index]
            print("Current Burst: ", current_burst)
            #print("Length of Current Process: ", len(current_process))
            if current_process_index < (len(current_process) - 1):
                current_io = current_process[current_process_index + 1]
            else:
                current_io = 0
            print("Current IO: ", current_io)
            print("Time Response: ", time_response)
            print("Time Wait: ", time_wait)
            ready_array[process] = 8
            del ready_queue[0]

    print("\n")
    print("FINAL RESULTS")
    print("---------------------")
    print("CPU Utilization: ", (cpu_utilization_time / cpu_counter))
    print("Time Response: ", time_response)
    print("Time Turnaround: ", time_turn)
    print("Time Wait: ", time_wait)
    print("FINISHED")

def MLQF():

        #DEFINE FUNCTION VARIABLES
    cpu_utilization_time = 0
    cpu_counter = 0
    burst_waiting = {"P1":0, "P2":0, "P3":0, "P4":0, "P5":0, "P6":0, "P7":0, "P8":0}
    io_timer = {"P1":0, "P2":0, "P3":0, "P4":0, "P5":0, "P6":0, "P7":0, "P8":0}
    #READY ARRAY 9 = START STATE, 8 = BURSTING, 7 = FINISHED, 5 = mid-burst wating 1 = READY, 0 = IN IO
    ready_array = {"P1":0, "P2":9, "P3":9, "P4":9, "P5":9, "P6":9, "P7":9, "P8":9}
    ready_queue_1 = []
    ready_queue_2 = []
    ready_queue_3 = []
    current_queue = 1
    time_quantum_1 = 6
    time_quantum_2 = 11
    time_response = {"P1":0, "P2":0, "P3":0, "P4":0, "P5":0, "P6":0, "P7":0, "P8":0}
    time_turn = {"P1":0, "P2":0, "P3":0, "P4":0, "P5":0, "P6":0, "P7":0, "P8":0}
    time_wait = {"P1":0, "P2":0, "P3":0, "P4":0, "P5":0, "P6":0, "P7":0, "P8":0}
    finished_processes = []
    process_index = {"P1":0, "P2":0, "P3":0, "P4":0, "P5":0, "P6":0, "P7":0, "P8":0}   #Position in process
    process_queue = {"P1":1, "P2":1, "P3":1, "P4":1, "P5":1, "P6":1, "P7":1, "P8":1}

    #At CPU Counter = 0 - Set ready queue from process key tuple
    print("Count: ", cpu_counter)
    ready_queue_1 = list(process_key)
    final_process_first_pass = ready_queue_1[-1]
    process_list = list(process_key)
    cpu_counter += 1
    cpu_utilization_time += 1

    
    print("Ready Queue: ", ready_queue_1, ready_queue_2, ready_queue_3)
    process = ready_queue_1[0]
    print("Process: ", process)
    current_process = processes[process]
    print("Current Process: ", ready_queue_1[0], "=", current_process)
    current_process_index = process_index[process]
    print("Current Process Index: ", current_process_index)
    current_burst = current_process[current_process_index]
    print("Current Burst: ", current_burst)
    current_quantum = time_quantum_1
    print("Current Time Quantum: ", current_quantum)
    
    #This is only necessary if the first process only has one burst
    if current_process_index < (len(current_process) - 1):
       current_io = current_process[current_process_index + 1]
    else:
       current_io = 0

    print("Current IO: ", current_io)
    ready_array[process] = 8
    del ready_queue_1[0]


    while process_list:

        print("\n")
        print("Ready Queue:", ready_queue_1, ready_queue_2, ready_queue_3)
        print("Ready Array:", ready_array)
        print("Burst Waiting:", burst_waiting)
        print("Count: ", cpu_counter)
        print("Current Burst in process ", process, ":", current_burst)
        print("Current Time Quantum: ", current_quantum)
        print("Current IO", current_io)
        print("IO Timer:", io_timer)
        print("Ready Array: ", ready_array)
        print("Time Wait: ", time_wait)
        print("Process Queue: ", process_queue)

        #Subtract burst
        current_burst = current_burst - 1

        #Subract quantum
        current_quantum = current_quantum - 1

        #Subtract IO
        for y in range(len(io_timer)):
            z = process_key[y]
            if io_timer[z] != 0:
                io_timer[z] = io_timer[z] - 1

        #Compute Time-Wait for processes in ready queue
        for y in range(len(time_wait)):
            z = process_key[y]
            if ready_array[z] == 9 or ready_array[z] == 1:
                time_wait[z] = time_wait[z] + 1
        
        #Move any finished IO to ready queue
        for y in range(len(io_timer)):
            z = process_key[y]
            if io_timer[z] == 0 and ready_array[z] == 0:
                if process_queue[z] == 1:
                    ready_queue_1.append(z)
                    ready_array[z] = 1
                elif process_queue[z] == 2:
                    ready_queue_2.append(z)
                    ready_array[z] = 1
                elif process_queue[z] == 3:
                    ready_queue_3.append(z)
                    ready_array[z] = 1

        #Compute Time-Response
        if ready_array[final_process_first_pass] == 9:
            for y in range(len(ready_array)):
                z = process_key[y]
                if ready_array[z] == 9:
                    time_response[z] = time_response[z] + 1

        #Increment CPU Counter
        cpu_counter += 1
        cpu_utilization_time += 1
        
        #Time Quantum ends but Burst not finished
        if current_quantum == 0 and current_burst != 0 and current_io != 0:
            #moves the time remaining in the 
            burst_waiting[process] = current_burst
            #Allows the current burst to switch to a new process
            current_burst = 0
            #Moves process to the next queue
            process_queue[process] += 1
            print("Process Queue: ", process_queue)
            if process_queue[process] == 1:
                ready_queue_1.append(process)
                ready_array[process] = 5
            elif process_queue[process] == 2:
                ready_queue_2.append(process)
                ready_array[process] = 5
            elif process_queue[process] == 3:
                ready_queue_3.append(process)
                ready_array[process] = 5

        #When burst/time quantum finishes, process moves to IO and next process pulled from ready queue
        if current_burst == 0:
             #IF PROCESS FINISHED
            if current_io == 0:
                print(ready_queue_1, ready_queue_2, ready_queue_3)
                finished_processes.append(process)
                print("REMOVING", process)
                process_list.remove(process)
                time_turn[process] = cpu_counter - 1 #Subtract 1 because counter already incremented
                ready_array[process] = 7
                print("Ready Queue: ", ready_queue_1, ready_queue_2, ready_queue_3)    
                print("Finished Processes: ", finished_processes)
                print("Remaining Processes: ", process_list)
                print("Time Wait:", time_wait)

            else:
                #Burst must be finished for io to start
                if burst_waiting[process] == 0:
                    io_timer[process] = current_io
                    ready_array[process] = 0
                    process_index[process] += 2
                    print("IO Timer", io_timer)

            if not process_list:
                break
            
            #IO CONVOY HANDLING
            while ready_queue_1 == [] and ready_queue_2 == [] and ready_queue_3 == []:
                for y in range(len(process_key)):
                    z = process_key[y]
                    io_timer[z] = io_timer[z] - 1
                    if io_timer[z] == 0:
                        if process_queue[z] == 1:
                            ready_queue_1.append(z)
                            ready_array[z] = 1
                        elif process_queue[z] == 2:
                            ready_queue_2.append(z)
                            ready_array[z] = 1
                        elif process_queue[z] == 3:
                            ready_queue_3.append(z)
                            ready_array[z] = 1
                cpu_counter += 1

            print("Ready Queue: ", ready_queue_1, ready_queue_2, ready_queue_3)
            if ready_queue_1:
                process = ready_queue_1[0]
            elif ready_queue_2:
                process = ready_queue_2[0]
            elif ready_queue_3:
                process = ready_queue_3[0]
            print("Process: ", process)
            current_process = processes[process]
            print("Current Process: ", process, "=", current_process)
            current_process_index = process_index[process]
            print("Current Process Index: ", current_process_index)
            if burst_waiting[process] == 0:
                current_burst = current_process[current_process_index]
            else:
                current_burst = burst_waiting[process]
                burst_waiting[process] = 0
            print("Current Burst: ", current_burst)
            if process_queue[process] == 1:
                current_quantum = time_quantum_1
            elif process_queue[process] == 2:
                current_quantum = time_quantum_2
            #This part is a trick to make sure current_quantum never equals 0 for FCFS in queue 3
            elif process_queue[process] == 3:
                current_quantum = -1

            #print("Length of Current Process: ", len(current_process))
            if current_process_index < (len(current_process) - 1):
                current_io = current_process[current_process_index + 1]
            else:
                current_io = 0
            print("Current IO: ", current_io)
            print("Time Response: ", time_response)
            print("Time Wait: ", time_wait)
            ready_array[process] = 8
            if process_queue[process] == 1:
                del ready_queue_1[0]
            elif process_queue[process] == 2:
                del ready_queue_2[0]
            elif process_queue[process] == 3:
                del ready_queue_3[0]

    print("\n")
    print("FINAL RESULTS")
    print("---------------------")
    print("CPU Utilization: ", (cpu_utilization_time / cpu_counter))
    print("Time Response: ", time_response)
    print("Time Turnaround: ", time_turn)
    print("Time Wait: ", time_wait)
    print("FINISHED")

def main():

    

    display_main_menu()
    while True:
        command = input("Command: ")
        if command == "1":
            FCFS()
        elif command == "2":
            SJF()
        elif command == "3":
            MLQF()
        elif command == "0":
            break
        else:
            print("Not a valid command.  Please try again. \n")
            display_main_menu()

if __name__ == "__main__":
    main()