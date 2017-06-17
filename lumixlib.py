__author__ = 'lippyt'
import urllib2
import time
import requests

initurl='http://192.168.54.1'
UUID='b094f3c0-22c4-4eaa-82e3-fdcf40e41369'

#cam url refers to the IP address of the camera, by default this should be http://192.168.54.1

#Handshake before the camera can receive commands
def handshake(camurl):
    requests.get(camurl + '/cam.cgi?mode=accctrl&type=req_acc&value='+ UUID +'&value2=duck')
    time.sleep(2)
    requests.get(camurl + '/cam.cgi?mode=camcmd&value=recmode')
    time.sleep(2)
    requests.get(camurl + '/cam.cgi?mode=startstream&value=49199')

#focusstep(camurl,mode) shifts the focal distance it has 4 modes which affect speed and direction (mode =0,1,2,3)
#Mode 0 and 1 move the focal distance nearer to the camera, mode 0 takes a small focus step while mode 1 takes a large focus step
#Mode 0 and 1 move the focal distance further way from the camera, mode 0 takes a small focus step while mode 1 takes a large focus step
#Focus step returns the focal distance bit of the lens after it takes the focus step. It returns the value 999999 if there is any error
def focusstep(camurl,mode):
    if mode==0:
        response = urllib2.urlopen(camurl + '/cam.cgi?mode=camctrl&type=focus&value=wide-normal')
        html = response.read()
    if mode==1:
        response = urllib2.urlopen(camurl + '/cam.cgi?mode=camctrl&type=focus&value=wide-fast')
        html = response.read()
    if mode==2:
        response = urllib2.urlopen(camurl + '/cam.cgi?mode=camctrl&type=focus&value=tele-normal')
        html = response.read()
    if mode==3:
        response = urllib2.urlopen(camurl + '/cam.cgi?mode=camctrl&type=focus&value=tele-fast')
        html = response.read()
    #This returns the value 999999 if the first two characters in the response aren't 'ok'
    if html[0]!='o' and html[1]!='k':
        return 999999
    k=len(html)
    i0=0
    i1=0
    for i in range(0,k):
        if html[i]==',':
            if i0!=0:
                i1=i
                break
            i0=i+1
    dist= int(html[i0:i1])
    return dist


def pullfar(k0,k1):
    j=k1
    #return from k1 to k0 (pull far to near)
    while j<k0:
        j=focusstep(initurl,0)
        print '.',
        time.sleep(0.1)
    print '\n Reached starting focus point'
    raw_input('\n Press Enter to pull focus to ending point')
    print 'Pulling to ending point...',
    while j>k1:
        j=focusstep(initurl,2)
        print '.',
        time.sleep(0.2)
    print '\nEnding focus point reached'

def pullnear(k0,k1):
    j=k1
    #return from k1 to k0 (pull near to far)
    while j>k0:
        j=focusstep(initurl,2)
        print '.',
        time.sleep(0.1)
    print '\n Reached starting focus point'
    raw_input('\n Press Enter to pull focus to ending point')
    print 'Pulling to ending point...',
    while j<k1:
        j=focusstep(initurl,0)
        time.sleep(0.2)
        print '.',

#Returns the current focal distance of the lens. It does this by stepping the focal distance one step in the tele direction and then later in the wide direction.
#The two steps cancel each other out and provide us with the initial focal distance the lens was at
def focaldistance(camurl):

    requests.get(camurl + '/cam.cgi?mode=camctrl&type=focus&value=tele-normal')
    time.sleep(0.3)

    response = urllib2.urlopen(camurl + '/cam.cgi?mode=camctrl&type=focus&value=wide-normal')
    html = response.read()
    if html[0]!='o' and html[1]!='k':
        return 999999
    k=len(html)
    i0=0
    i1=0
    for i in range(0,k):
        if html[i]==',':
            if i0!=0:
                i1=i
                break
            i0=i+1

    dist= int(html[i0:i1])
    return dist

#This is code for a primitive focus puller
def main():
    handshake()
    time.sleep(1)


    while True:    # infinite loop
        n = raw_input("\n\nPlease set the initial focal distance and click enter ")
        k0=focaldistance(initurl)
        if k0 != 999999:
            break  # stops the loop
        elif k0==999999:
            print 'Error, camera is performing other functions or is not in manual focus mode'

    while True:    # infinite loop
        n = raw_input("\n\nPlease set the ending focal distance and click enter, camera will return to initial focus point after ")
        k1=focaldistance(initurl)
        if k1 != 999999:
            break  # stops the loop
        elif k1==999999:
            print 'Error, camera is performing other functions or is not in manual focus mode'

    print '\nreturning to initial focus point...'

    #k0>k1 near to far
    if k0>k1:
        pullfar(k0,k1)
    #k0<k1 far to near
    elif k0<k1:
        pullnear(k0,k1)

    elif k0==k1:
        print 'Two focus points are the same'

#This code returns the total focus bits (eg 0-1024, 0 being farthest and 1024 being closest focal distance) of the camera by receiving the response after initiating a focus step
def totalfocusbits(camurl):
    requests.get(camurl + '/cam.cgi?mode=camctrl&type=focus&value=tele-normal')
    time.sleep(0.3)

    response = urllib2.urlopen(camurl + '/cam.cgi?mode=camctrl&type=focus&value=wide-normal')
    html = response.read()
    if html[0]!='o' and html[1]!='k':
        return 999999
    k=len(html)
    i0=0
    i1=0
    for i in range(0,k):
        if html[i]==',':
            if i0!=0:
                i1=i
                break
            i0=i+1

    dist= int(html[i1+1:k])
    return dist

#Initiates a capture. Returns nothing
def capture(camurl):
    requests.get(camurl + '/cam.cgi?mode=camcmd&value=capture')