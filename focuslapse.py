import lumixlib
import requests
import time
import urllib2

#This sample function shows an example of how focus racking can be used together with capture. It is definitely not complete nor does it provide the correct number of shots*
#The user first sets his camera to the furthest point he wishes to capture, sets his camera mode to manual focus and then clicks enter
#The script will figure out how many focus steps are necessary to reach the closest focusing distance
#The camera then takes captures photos according to two user inputs, number of photos to take and interval duration

#*As this is just a quick test script, the total number of shots taken will likely not tally with the user input

initurl='http://192.168.54.1'

def main():
    while True:    # infinite loop
        n = raw_input("\n\nPlease set the focus at infinity or focus end point and press enter")
        infinity=lumixlib.focaldistance(initurl)
        if infinity != 999999:
            break  # stops the loop
        elif infinity==999999:
            print 'Error, camera is performing other functions or is not in manual focus mode'
    j=infinity
    jm1=j-1
    print 'Testing focus steps from infinity to closest focusing distance(slow)',
    # focus step data slow
    steps=0
    while j!=jm1:

        if j == 999999:
            print 'Error, camera is performing other functions or is not in manual focus mode'
            break
        jm1 = j
        j = lumixlib.focusstep(initurl, 0)
        print '.',
        time.sleep(0.3)
        steps=steps+1

    print '\nFocus step data infinity to closest focus distance sucessfully acquired\n'


    numberofshots = int(raw_input("\n\nPlease enter number of photos to take: "))
    interval = int(raw_input("\n\nPlease enter interval: "))

    rest=36
    shotsperstep=int(((numberofshots-rest)/2)/steps)
    rampsteps=int(steps)
    #To be fixed
    if steps>=(numberofshots-rest)/2:
        shotsperstep=1

    for i in range(0, steps):
        for j in range(0,shotsperstep):
            lumixlib.capture(initurl)
            time.sleep(interval)
        lumixlib.focusstep(initurl,2)
    time.sleep(interval)
    for i in range(0, rest):
        lumixlib.capture(initurl)
        time.sleep(interval)

    for i in range(0, steps):
        for j in range(0,shotsperstep):
            lumixlib.capture(initurl)
            time.sleep(interval)
            lumixlib.focusstep(initurl, 0)

lumixlib.handshake(initurl)
main()

