
def noiseTest(self):
    streamLength="15s"
    startTestTime="1s"
    endTestTime="11s"
    channelMaxLimits={"+3.3V:current:uA":"250uA", "+12V:current:uA":"250uA", "+3.3Vaux:current:uA":"250uA"}

    '''
    start stream
    wait streamLength time
    plot annos and start and end test point
    get stats
    for each channel in channelMaxLimits
        check its within its limit and record pass/fail
    '''

    filePath = os.path.dirname(os.path.realpath(__file__))
    if isQpsRunning() == False:
        startLocalQps()
    myQps = qpsInterface()

    myQuarchDevice = getQuarchDevice(myDeviceID, ConType="QPS")
    myQpsDevice = quarchQPS(myQuarchDevice)
    myQpsDevice.openConnection()
    print("Running QPS Automation Example")
    print("Module Name:")
    print(myQpsDevice.sendCommand("hello?"))
    setupPowerOutput(myQpsDevice)
    print(myQpsDevice.sendCommand("record:averaging 32k"))
    fileName = time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime())
    myStream = myQpsDevice.startStream(filePath + "\\" + fileName)
    print("File output path set: " + filePath + "\\" + fileName)
    time.sleep(2)
    myStream.addAnnotation('Adding an example annotation\\nIn real time!')
    time.sleep(1)
    myStream.addAnnotation('Adding an example annotation\\nAt a specific time!', time.time())
    time.sleep(1)
    print(myStream.get_stats())

