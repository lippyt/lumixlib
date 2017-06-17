import lumixlib
import requests
import time
import urllib2

initurl='http://192.168.54.1'


lumixlib.handshake(initurl)

#lensdata tries to gather motor step data for each specific lens. It writes each focus step in a text file named 'Lens Data.txt'

def main():
    raw_input('Please set your camera to manual focus, then press enter. Do not touch the focus ring before the lens profiling is complete')
    print 'Looking for total focus bits: ',
    while True:    # infinite loop
        time.sleep(0.2)
        totalfocusbits = lumixlib.totalfocusbits(initurl)
        time.sleep(0.2)
        if totalfocusbits != 999999:
            print 'Success'
            print 'Total Focus Bits are: ' + str(totalfocusbits)
            break  # stops the loop
        elif totalfocusbits==999999:
            print '\nError, camera is performing other functions or is not in manual focus mode'
    print 'Shifting to farthest focus distance...'
    j=lumixlib.focaldistance(initurl)
    while j>0:
        if j==999999:
            print 'Error, camera is performing other functions or is not in manual focus mode'
            break
        j=lumixlib.focusstep(initurl,3)
        time.sleep(0.1)
    print 'Lens has reached farthest focus distance'
    time.sleep(0.2)
    print 'Testing focus steps from far to near (slow)...',
    #focus step data slow
    fsdfnslow=[j]
    while j<totalfocusbits:
        if j==999999:
            print 'Error, camera is performing other functions or is not in manual focus mode'
            break
        j=lumixlib.focusstep(initurl,0)
        fsdfnslow.append(j)
        print '.',
        time.sleep(0.1)

    print '\nFocus step data far to near (slow) sucessfully acquired\n'

    print 'Testing focus steps from near to far (slow)...',
    #focus step data slow
    fsdnfslow=[j]
    while j>0:
        if j==999999:
            print 'Error, camera is performing other functions or is not in manual focus mode'
            break
        j=lumixlib.focusstep(initurl,2)
        fsdnfslow.append(j)
        print '.',
        time.sleep(0.1)

    print '\nFocus step data near to far (slow) sucessfully acquired\n'

    print 'Testing focus steps from far to near (slow)...',
    #focus step data fast
    fsdfnfast=[j]
    while j<totalfocusbits:
        if j==999999:
            print 'Error, camera is performing other functions or is not in manual focus mode'
            break
        j=lumixlib.focusstep(initurl,1)
        fsdfnfast.append(j)
        print '.',
        time.sleep(0.1)

    print '\nFocus step data far to near (fast) sucessfully acquired\n'

    print 'Testing focus steps from near to far (fast)...',
    #focus step data slow
    fsdnffast=[j]
    while j>0:
        if j==999999:
            print 'Error, camera is performing other functions or is not in manual focus mode'
            break
        j=lumixlib.focusstep(initurl,3)
        fsdnffast.append(j)
        print '.',
        time.sleep(0.1)

    print '\nFocus step data near to far (fast) sucessfully acquired\n'

    with open('Lens Data.txt', 'w') as f:
        f.write('Total Focus Bits: ' + str(totalfocusbits) + '\n')
        for s in fsdfnslow:
            f.write(str(s) + '\n')
        f.write('Near to Far Slow:\n')
        for s in fsdnfslow:
            f.write(str(s) + '\n')
        f.write('Far to Near Fast:\n')
        for s in fsdfnfast:
            f.write(str(s) + '\n')
        f.write('Near to Far Fast:\n')
        for s in fsdnffast:
            f.write(str(s) + '\n')

main()







