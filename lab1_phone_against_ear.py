#-------------------------------------------------------------------------------
# Name:        Proximity detection using light sensor & accelormeter
#
# Purpose:     Lab 1 Sensor Based Systems
#
# Author:      Krishnaswamy Kannan, Sonali Deo
#
#-------------------------------------------------------------------------------
import serial

def main():
    ser=serial.Serial(port='COM12',
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout = 1)

    while True:
        table_flag = 0
        acc_flag = 0
        light_flag = 0
        data = []
        acc =[]
        acc_val = []
        light = []
        val = []
        #get accelerometer data
        ser.write("AT +OAW?\r")
        for line in ser:
            r = ser.readline()
            data = r.strip("\n").split(":")
            acc = data[1:2]
            for j in acc:
                acc_val = j.split(",")

        #print "X : ",acc_val[0],"Y : ",acc_val[1],"Z ; ",acc_val[2]
        #on the table
        if (int(acc_val[0]) in range(-4,6)) and (int(acc_val[1]) in range(-5,6)) :
            table_flag = 1
        #held against the user's head
        if (int(acc_val[0]) in range(-19,-5)) and (int(acc_val[1]) in range(-21,-10)):
            acc_flag = 1
        #get light sensor data
        ser.write("AT S203?\r")
        for line in ser:
            r = ser.readline()
            light = r.strip("\n").split("\r")
            val = light[0]
            if(light[0] != "OK"):
                if(int(val) >2200):
                    light_flag = 1

       #print table_flag,light_flag,acc_flag
        if table_flag == 1:# and light_flag == 0:
         print "\n The phone is on the table"
        elif acc_flag == 1 and light_flag == 1:
         print "\n The phone is held against the user's head"

    #ser.close()

if __name__ == '__main__':
    main()
