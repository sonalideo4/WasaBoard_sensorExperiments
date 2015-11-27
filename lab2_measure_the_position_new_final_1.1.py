import time
import serial
import numpy as np
import matplotlib.pyplot as plt

# import scipy
# from scipy import special, optimize
from scipy.integrate import quad,simps

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/tty.usbserial-A6U2N87Y',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

print (ser.name)
x_position = 0
y_position = 0

L_x = list()
L_y = list()
L_t = list()

for i in range(50):

    L_value_x= list()
    L_time_x= list()
    L_velocity_x = list()
    calibrate_value_read_x = 0

    L_value_y= list()
    L_time_y= list()
    L_velocity_y = list()
    calibrate_value_read_y = 0


    ser.write("ATS200?\r")

    for k_x in range(4):
        calibrate_value_read_x = ser.readline()
        try:
            calibrate_value_x = float(calibrate_value_read_x)
            print
        except ValueError:
            pass

    ser.write("ATS201?\r")
    for k_y in range(4):
        calibrate_value_read_y = ser.readline()
        try:
            calibrate_value_y = float(calibrate_value_read_y)
            print
        except ValueError:
            pass


    time_begin = time.time()

    start = time.time() #measure the time latency to get the data


    for i in range(10):
        ser.write("ATS200?\r")
        for j_x in range(4):
            x_temp = ser.readline()
            try:
                result_x_temp= float(x_temp)
                result_x = abs(result_x_temp - calibrate_value_x)
                if result_x < 10 :
                    pass
                else:
                    done = time.time()
                    elapsed = done - start
                    L_value_x.append(result_x)
                    L_time_x.append(elapsed)

                    vx_temp = simps(L_value_x,L_time_x)
                    L_velocity_x.append(vx_temp)
                    # print(elapsed)
                    # print(result_light)
            except ValueError:
                pass

        ser.write("ATS201?\r")

        for j_y in range(4):
            y_temp = ser.readline()
            try:
                result_y_temp= float(y_temp)

                result_y = abs(result_y_temp - calibrate_value_y)
                if result_y < 10 :
                    pass
                else:
                    done = time.time()
                    elapsed = done - start
                    L_value_y.append(result_y)
                    L_time_y.append(elapsed)

                    vy_temp = simps(L_value_y,L_time_y)

                    L_velocity_y.append(vy_temp)
                    # print(elapsed)
                    # print(result_light)
            except ValueError:
                pass
    # *******************************simps caculate the value" 
    # mean_value = np.mean(L_value_ac)
    # print ("ac_mean is : ", mean_value) 
    # dir_temp = mean_value - calibrate_value

    # if dir_temp > 0:
    #     flag = 0
    # else:
    #     flag = 1

    if len(L_value_x) & len(L_value_y) == 0:
        print "Pisition is (%f,%f):" %(x_position,y_position)
    else:
        # print(L_velocity_x,L_velocity_y)
        position_x = simps(L_velocity_x,L_time_x)
        position_y = simps(L_velocity_y,L_time_y)

        t_done = time.time()
        t_i = t_done - time_begin
        # print ("position_x, position_y is : %f, %f", (position_x,position_y))


        x_position = x_position + position_x
        y_position = y_position + position_y
        L_t.append(t_i)

        print "Pisition is (%f,%f):"  %(x_position,y_position)
        L_x.append(x_position)
        L_y.append(y_position)

        position_x = 0
        position_y = 0

plt.plot(L_x)
plt.xlabel('Time')
plt.show()
    # time.sleep(1)result_light = abs(result_light_temp - calibrate_value)
# print(len(L_value))

# mean_value = reduce(lambda x, y: x + y, L) / len(L) #0.0157835292816
# print mean_value
# print np.mean(L) #0.0157835292816
# print np.std(L) #0.000169599444933


