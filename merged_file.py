## file pj1_1
 
from machine import Pin
import time

led = Pin(12, Pin.OUT)# Build an LED object, connect the external LED light to pin 0, and set pin 0 to output mode
while True:
    led.value(1)# turn on led
    time.sleep(1)# delay 1s
    led.value(0)# turn off led
    time.sleep(1)# delay 1s

#file pj1_2
import time
from machine import Pin,PWM

#The way that the ESP32 PWM pins output is different from traditionally controllers.
#It can change frequency and duty cycle by configuring PWM’s parameters at the initialization stage.
#Define GPIO 0’s output frequency as 10000Hz and its duty cycle as 0, and assign them to PWM.
pwm =PWM(Pin(12,Pin.OUT),10000)

try:
    while True: 
#The range of duty cycle is 0-1023, so we use the first for loop to control PWM to change the duty
#cycle value,making PWM output 0% -100%; Use the second for loop to make PWM output 100%-0%.  
        for i in range(0,1023):
            pwm.duty(i)
            time.sleep_ms(1)
            
        for i in range(0,1023):
            pwm.duty(1023-i)
            time.sleep_ms(1)  
except:
#Each time PWM is used, the hardware Timer will be turned ON to cooperate it. Therefore, after each use of PWM,
#deinit() needs to be called to turned OFF the timer. Otherwise, the PWM may fail to work next time.
    pwm.deinit()


# file pj2_1
from machine import Pin
import time

button1 = Pin(16, Pin.IN, Pin.PULL_UP)
button2 = Pin(27, Pin.IN, Pin.PULL_UP)

while True:
    btnVal1 = button1.value()  # Reads the value of button 1
    btnVal2 = button2.value()
    print("button1 =",btnVal1)  #Print it out in the shell
    print("button2 =",btnVal2)
    time.sleep(0.1) #delay 0.1s

# file pj2_2
from machine import Pin
import time

button1 = Pin(16, Pin.IN, Pin.PULL_UP)
led = Pin(12, Pin.OUT)
count = 0

while True:
    btnVal1 = button1.value()  # Reads the value of button 1
    #print("button1 =",btnVal1)  #Print it out in the shell
    if(btnVal1 == 0):
        time.sleep(0.01)
        while(btnVal1 == 0):
            btnVal1 = button1.value()
            if(btnVal1 == 1):
                count = count + 1
                print(count)
    val = count % 2
    if(val == 1):
        led.value(1)
    else:
        led.value(0)
    time.sleep(0.1) #delay 0.1s
    


# file pj3_1
from machine import Pin
import time

PIR = Pin(14, Pin.IN)
while True:
    value = PIR.value()
    print(value, end = " ")
    if value == 1:
        print("Some body is in this area!")
    else:
        print("No one!")
    time.sleep(0.1)

# file pj3_2
from machine import Pin
import time

PIR = Pin(14, Pin.IN)
led = Pin(12, Pin.OUT)

while True:
    value = PIR.value()
    print(value)
    if value == 1:
        led.value(1)# turn on led
    else:
        led.value(0)
    time.sleep(0.1)


# file pj4_1
from machine import Pin, PWM
from time import sleep
buzzer = PWM(Pin(25))

buzzer.duty(1000) 

# Happy birthday
buzzer.freq(294)
sleep(0.25)
buzzer.freq(440)
sleep(0.25)
buzzer.freq(392)
sleep(0.25)
buzzer.freq(532)
sleep(0.25)
buzzer.freq(494)
sleep(0.25)
buzzer.freq(392)
sleep(0.25)
buzzer.freq(440)
sleep(0.25)
buzzer.freq(392)
sleep(0.25)
buzzer.freq(587)
sleep(0.25)
buzzer.freq(532)
sleep(0.25)
buzzer.freq(392)
sleep(0.25)
buzzer.freq(784)
sleep(0.25)
buzzer.freq(659)
sleep(0.25)
buzzer.freq(532)
sleep(0.25)
buzzer.freq(494)
sleep(0.25)
buzzer.freq(440)
sleep(0.25)
buzzer.freq(698)
sleep(0.25)
buzzer.freq(659)
sleep(0.25)
buzzer.freq(532)
sleep(0.25)
buzzer.freq(587)
sleep(0.25)
buzzer.freq(532)
sleep(0.5)
buzzer.duty(0)

# file pj5_1
from machine import Pin, PWM
import time
pwm = PWM(Pin(13))  
pwm.freq(50)

'''
Duty cycle corresponding to the Angle
0°----2.5%----25
45°----5%----51.2
90°----7.5%----77
135°----10%----102.4
180°----12.5%----128
'''
angle_0 = 25
angle_90 = 77
angle_180 = 128

while True:
    pwm.duty(angle_0)
    time.sleep(1)
    pwm.duty(angle_90)
    time.sleep(1)
    pwm.duty(angle_180)
    time.sleep(1)

# file pj5_2
# Import Pin, ADC and DAC modules.
from machine import ADC,Pin,DAC,PWM
import time
pwm = PWM(Pin(5))  
pwm.freq(50)

# Turn on and configure the ADC with the range of 0-3.3V 
adc=ADC(Pin(34))
adc.atten(ADC.ATTN_11DB)
adc.width(ADC.WIDTH_12BIT)

# Read ADC value once every 0.1seconds, convert ADC value to DAC value and output it,
# and print these data to “Shell”. 
try:
    while True:
        adcVal=adc.read()
        dacVal=adcVal//16
        voltage = adcVal / 4095.0 * 3.3
        print("ADC Val:",adcVal,"DACVal:",dacVal,"Voltage:",voltage,"V")
        if(voltage > 0.6):
            pwm.duty(46)
        else:
            pwm.duty(100)
        time.sleep(0.1)
except:
    pass

# file pj6_1
#Import Pin, neopiexl and time modules.
from machine import Pin
import neopixel
import time

#Define the number of pin and LEDs connected to neopixel.
pin = Pin(26, Pin.OUT)
np = neopixel.NeoPixel(pin, 4) 

#brightness :0-255
brightness=100                                
colors=[[brightness,0,0],                    #red
        [0,brightness,0],                    #green
        [0,0,brightness],                    #blue
        [brightness,brightness,brightness],  #white
        [0,0,0]]                             #close

#Nest two for loops to make the module repeatedly display five states of red, green, blue, white and OFF.    
while True:
    for i in range(0,5):
        for j in range(0,4):
            np[j]=colors[i]
            np.write()
            time.sleep_ms(50)
        time.sleep_ms(500)
    time.sleep_ms(500)

# file pj6_2
#Import Pin, neopiexl and time modules.
from machine import Pin
import neopixel
import time

button1 = Pin(16, Pin.IN, Pin.PULL_UP)
button2 = Pin(27, Pin.IN, Pin.PULL_UP)
count = 0

#Define the number of pin and LEDs connected to neopixel.
pin = Pin(26, Pin.OUT)
np = neopixel.NeoPixel(pin, 4) 

#brightness :0-255
brightness=100                                
colors=[[0,0,0],
        [brightness,0,0],                    #red
        [0,brightness,0],                    #green
        [0,0,brightness],                    #blue
        [brightness,brightness,brightness]  #white
        ]                             #close

def func_color(val):
    for j in range(0,4):
        np[j]=colors[val]
        np.write()
        time.sleep_ms(50)
        
#Nest two for loops to make the module repeatedly display five states of red, green, blue, white and OFF.    
while True:
    btnVal1 = button1.value()  # Reads the value of button 1
    #print("button1 =",btnVal1)  #Print it out in the shell
    if(btnVal1 == 0):
        time.sleep(0.01)
        while(btnVal1 == 0):
            btnVal1 = button1.value()
            if(btnVal1 == 1):
                count = count - 1
                print(count)
                if(count <= 0):
                    count = 0
                
    btnVal2 = button2.value()        
    if(btnVal2 == 0):
        time.sleep(0.01)
        while(btnVal2 == 0):
            btnVal2 = button2.value()
            if(btnVal2 == 1):
                count = count + 1
                print(count)
                if(count >= 4):
                    count = 4
    
    if(count == 0):
        func_color(0)
    elif(count == 1):
        func_color(1)
    elif(count == 2):
        func_color(2)
    elif(count == 3):
        func_color(3)
    elif(count == 4):
        func_color(4)



# file pj7_1
from machine import Pin,PWM
import time
#Two pins of the motor
INA =PWM(Pin(19,Pin.OUT),10000)#INA corresponds to IN+
INB =PWM(Pin(18,Pin.OUT),10000)#INB corresponds to IN- 

try:
    while True:
        #Counterclockwise 2s
        INA.duty(0) #The range of duty cycle is 0-1023
        INB.duty(700)
        time.sleep(2)
        #stop 1s
        INA.duty(0)
        INB.duty(0)
        time.sleep(1)
        #Turn clockwise for 2s
        INA.duty(600)
        INB.duty(0)
        time.sleep(2)
        #stop 1s
        INA.duty(0)
        INB.duty(0)
        time.sleep(1)
except:
    INA.duty(0)
    INB.duty(0)
    INA.deinit()
    INB.deinit()

# file pj7_2
from machine import Pin,PWM
import time
#Two pins of the motor
INA =PWM(Pin(19,Pin.OUT),10000)#INA corresponds to IN+
INB =PWM(Pin(18,Pin.OUT),10000)#INB corresponds to IN-
button1 = Pin(16, Pin.IN, Pin.PULL_UP)
count = 0

try:
    while True:
        btnVal1 = button1.value()  # Reads the value of button 1
        if(btnVal1 == 0):
            time.sleep(0.01)
            while(btnVal1 == 0):
                btnVal1 = button1.value()
                if(btnVal1 == 1):
                    count=count + 1
                    print(count)
        val = count % 2
        if(val == 1):
            INA.duty(0) #The range of duty cycle is 0-1023
            INB.duty(700)
        else:
            INA.duty(0)
            INB.duty(0)
except:
    INA.duty(0)
    INB.duty(0)
    INA.deinit()
    INB.deinit()

# file pj8_2
from time import sleep_ms, ticks_ms 
from machine import SoftI2C, Pin 
from i2c_lcd import I2cLcd 

DEFAULT_I2C_ADDR = 0x27

scl_pin = Pin(22, Pin.OUT, pull=Pin.PULL_UP)  # GPIO22 with internal pull-up enabled
sda_pin = Pin(21, Pin.OUT, pull=Pin.PULL_UP)  # GPIO21 with internal pull-up enabled

i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000) 
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

from machine import Pin
import time
gas = Pin(23, Pin.IN, Pin.PULL_UP)

while True:
    gasVal = gas.value()  # Reads the value of button 1
    print("gas =",gasVal)  #Print it out in the shell
    lcd.move_to(1, 1)
    lcd.putstr('val: {}'.format(gasVal))
    if(gasVal == 1):
        #lcd.clear()
        lcd.move_to(1, 0)
        lcd.putstr('Safety       ')
    else:
        lcd.move_to(1, 0)
        lcd.putstr('dangerous')
    time.sleep(0.1) #delay 0.1s

# file pj9_1

# Import machine, time and dht modules. 
import machine
import time
import dht
from time import sleep_ms, ticks_ms 
from machine import SoftI2C, Pin 
from i2c_lcd import I2cLcd 

#Associate DHT11 with Pin(17).
DHT = dht.DHT11(machine.Pin(17))

DEFAULT_I2C_ADDR = 0x27

i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000) 
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

while True:
    DHT.measure() # Start DHT11 to measure data once.
   # Call the built-in function of DHT to obtain temperature
   # and humidity data and print them in “Shell”.
    print('temperature:',DHT.temperature(),'℃','humidity:',DHT.humidity(),'%')
    lcd.move_to(1, 0)
    lcd.putstr('T= {}'.format(DHT.temperature()))
    lcd.move_to(1, 1)
    lcd.putstr('H= {}'.format(DHT.humidity()))
    time.sleep_ms(1000)

# file pj11_1
# Import machine, time and dht modules.
from machine import Pin, PWM
from time import sleep_ms, ticks_ms 
from machine import SoftI2C, Pin 
from i2c_lcd import I2cLcd 

DEFAULT_I2C_ADDR = 0x27

# Initialize SCL/SDA pins and enable internal pull-up
scl_pin = Pin(22, Pin.OUT, pull=Pin.PULL_UP)  # GPIO22 with internal pull-up
sda_pin = Pin(21, Pin.OUT, pull=Pin.PULL_UP)  # GPIO21 with internal pull-up

i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000) 
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

button1 = Pin(16, Pin.IN, Pin.PULL_UP)
button2 = Pin(27, Pin.IN, Pin.PULL_UP)
count = 0
time_count = 0
password = ""   # Input password
correct_password = "-.-"  # Correct password
lcd.putstr("Enter password")
pwm = PWM(Pin(13))  
pwm.freq(50)

while True:
    btnVal1 = button1.value()  # Reads the value of button 1
    if(btnVal1 == 0):
        sleep_ms(10)
        while(btnVal1 == 0):
            time_count = time_count + 1  # Start counting how long the button is pressed
            sleep_ms(200)                # Time accumulates in 200ms increments
            btnVal1 = button1.value()
            if(btnVal1 == 1):
                count = count + 1
                print(count)
                print(time_count)
                if(time_count > 3):      # If button pressed longer than 200*3ms, add "-" to password
                    lcd.clear()
                    #lcd.move_to(1, 1)
                    password = password + "-"
                else:
                    lcd.clear()
                    password = password + "."  # Otherwise add "."
                lcd.putstr('{}'.format(password)) 
                time_count = 0
                
    btnVal2 = button2.value()
    if(btnVal2 == 0):
        if(password == correct_password):  # If password is correct
            lcd.clear()
            lcd.putstr("open")
            pwm.duty(128)  # Open door
            password = ""  # Clear password
            sleep_ms(1000)
        else:              # If password is wrong
            lcd.clear()
            lcd.putstr("error")
            pwm.duty(25)  # Close door
            sleep_ms(2000)
            lcd.clear()
            lcd.putstr("enter again")
            password = ""  # Clear password

# file pj12_1
import time
import network #Import network module

#Enter correct router name and password
ssidRouter     = 'LieBaoWiFi359' #Enter the router name
passwordRouter = 'wmbd315931' #Enter the router password

def STA_Setup(ssidRouter,passwordRouter):
    print("Setup start")
    sta_if = network.WLAN(network.STA_IF) #Set ESP32 in Station mode
    if not sta_if.isconnected():
        print('connecting to',ssidRouter)
#Activate ESP32’s Station mode, initiate a connection request to the router
#and enter the password to connect.
        sta_if.active(True)
        sta_if.connect(ssidRouter,passwordRouter)
#Wait for ESP32 to connect to router until they connect to each other successfully.
        while not sta_if.isconnected():
            pass
#Print the IP address assigned to ESP32 in “Shell”.
    print('Connected, IP address:', sta_if.ifconfig())
    print("Setup End")

try:
    STA_Setup(ssidRouter,passwordRouter)
except:
    sta_if.disconnect()


# file rc_config

class Uid:
    size    = 0                  # Number of bytes in the UID. 4, 7 or 10.
    uidByte = [0,0,0,0,0,0,0,0,0,0]
    sak     = 0                  # The SAK (Select acknowledge) byte returned from the PICC after successful selection.
    

class mfrc522Config(Uid):
    # MFRC522 registers. Described in chapter 9 of the datasheet.
    # PCD_Register
    # Page 0: Command and status
    #                 0x00 #reserved for future use
    CommandReg      = 0x01 #starts and stops command execution
    ComIEnReg       = 0x02 #enable and disable interrupt request control bits
    DivIEnReg       = 0x03 #enable and disable interrupt request control bits
    ComIrqReg       = 0x04 #interrupt request bits
    DivIrqReg       = 0x05 #interrupt request bits
    ErrorReg        = 0x06 #error bits showing the error status of the last command executed
    Status1Reg      = 0x07 #communication status bits
    Status2Reg      = 0x08 #receiver and transmitter status bits
    FIFODataReg     = 0x09 #input and output of 64 byte FIFO buffer
    FIFOLevelReg    = 0x0A #number of bytes stored in the FIFO buffer
    WaterLevelReg   = 0x0B #level for FIFO underflow and overflow warning
    ControlReg      = 0x0C #miscellaneous control registers
    BitFramingReg   = 0x0D #adjustments for bit-oriented frames
    CollReg         = 0x0E #bit position of the first bit-collision detected on the RF interface
    #                 0x0F #reserved for future use

    # Page 1: Command
    #                 0x10 #reserved for future use
    ModeReg         = 0x11 #defines general modes for transmitting and receiving
    TxModeReg       = 0x12 #defines transmission data rate and framing
    RxModeReg       = 0x13 #defines reception data rate and framing
    TxControlReg    = 0x14 #controls the logical behavior of the antenna driver pins TX1 and TX2
    TxASKReg        = 0x15 #controls the setting of the transmission modulation
    TxSelReg        = 0x16 #elects the internal sources for the antenna driver
    RxSelReg        = 0x17 #selects internal receiver settings
    RxThresholdReg  = 0x18 #selects thresholds for the bit decoder
    DemodReg        = 0x19 #defines demodulator settings
    #                 0x1A #reserved for future use
    #                 0x1B #eserved for future use
    MfTxReg         = 0x1C #controls some MIFARE communication transmit parameters
    MfRxReg         = 0x1D #controls some MIFARE communication receive parameters
    #                 0x1E #reserved for future use
    SerialSpeedReg  = 0x1F #selects the speed of the serial UART interface

    # Page 2: Configuration
    #   0x20 reserved for future use
    CRCResultRegH   = 0x21 #shows the MSB and LSB values of the CRC calculation
    CRCResultRegL   = 0x22 #
    #                 0x23 #reserved for future use
    ModWidthReg     = 0x24 #controls the ModWidth setting?
    #                 0x25 #reserved for future use
    RFCfgReg        = 0x26 #onfigures the receiver gain
    GsNReg          = 0x27 #selects the conductance of the antenna driver pins TX1 and TX2 for modulation
    CWGsPReg        = 0x28 #defines the conductance of the p-driver output during periods of no modulation
    ModGsPReg       = 0x29 #defines the conductance of the p-driver output during periods of modulation
    TModeReg        = 0x2A #defines settings for the internal timer
    TPrescalerReg   = 0x2B #the lower 8 bits of the TPrescaler value. The 4 high bits are in TModeReg.
    TReloadRegH     = 0x2C #efines the 16-bit timer reload value
    TReloadRegL     = 0x2D #
    TCounterValueRegH   = 0x2E #shows the 16-bit timer value
    TCounterValueRegL   = 0x2F #

    # Page 3: Test Registers
    #                 0x30 #reserved for future use
    TestSel1Reg     = 0x31 #general test signal configuration
    TestSel2Reg     = 0x32 #eneral test signal configuration
    TestPinEnReg    = 0x33 #enables pin output driver on pins D1 to D7
    TestPinValueReg = 0x34 #defines the values for D1 to D7 when it is used as an I/O bus
    TestBusReg      = 0x35 #shows the status of the internal test bus
    AutoTestReg     = 0x36 #controls the digital self test
    VersionReg      = 0x37 #shows the software version
    AnalogTestReg   = 0x38 #controls the pins AUX1 and AUX2
    TestDAC1Reg     = 0x39 #defines the test value for TestDAC1
    TestDAC2Reg     = 0x3A #defines the test value for TestDAC2
    TestADCReg      = 0x3B #shows the value of ADC I and Q channels
    #                 0x3C #reserved for production tests
    #                 0x3D #reserved for production tests
    #                 0x3E #reserved for production tests
    #                 0x3F #reserved for production tests 
    
    # MFRC522 commands. Described in chapter 10 of the datasheet.
    # PCD_Command
    PCD_Idle             = 0x00 #no action, cancels current command execution
    PCD_Mem              = 0x01 #stores 25 bytes into the internal buffer
    PCD_GenerateRandomID = 0x02 #generates a 10-byte random ID number
    PCD_CalcCRC          = 0x03 #activates the CRC coprocessor or performs a self test
    PCD_Transmit         = 0x04 #transmits data from the FIFO buffer
    PCD_NoCmdChange      = 0x07 #no command change, can be used to modify the CommandReg register bits without affecting the command, for example, the PowerDown bit
    PCD_Receive          = 0x08 #activates the receiver circuits
    PCD_Transceive       = 0x0C #transmits data from FIFO buffer to antenna and automatically activates the receiver after transmission
    PCD_MFAuthent        = 0x0E #performs the MIFARE standard authentication as a reader
    PCD_SoftReset        = 0x0F #resets the MFRC522

    # MFRC522 RxGain[2:0] masks, defines the receiver's signal voltage gain factor (on the PCD).
    # Described in 9.3.3.6 / table 98 of the datasheet at http://www.nxp.com/documents/data_sheet/MFRC522.pdf
    # PCD_RxGain
    RxGain_18dB          = 0x00 << 4 #000b - 18 dB, minimum
    RxGain_23dB          = 0x01 << 4 #001b - 23 dB
    RxGain_18dB_2        = 0x02 << 4 #010b - 18 dB, it seems 010b is a duplicate for 000b
    RxGain_23dB_2        = 0x03 << 4 #011b - 23 dB, it seems 011b is a duplicate for 001b
    RxGain_33dB          = 0x04 << 4 #100b - 33 dB, average, and typical default
    RxGain_38dB          = 0x05 << 4 #101b - 38 dB
    RxGain_43dB          = 0x06 << 4 #110b - 43 dB
    RxGain_48dB          = 0x07 << 4 #111b - 48 dB, maximum
    RxGain_min           = 0x00 << 4 #000b - 18 dB, minimum, convenience for RxGain_18dB
    RxGain_avg           = 0x04 << 4 #100b - 33 dB, average, convenience for RxGain_33dB
    RxGain_max           = 0x07 << 4 #111b - 48 dB, maximum, convenience for RxGain_48dB    
    
    # Commands sent to the PICC.
    # The commands used by the PCD to manage communication with several PICCs (ISO 14443-3, Type A, section 6.4)
    PICC_CMD_REQA           = 0x26 #REQuest command, Type A. Invites PICCs in state IDLE to go to READY and prepare for anticollision or selection. 7 bit frame.
    PICC_CMD_WUPA           = 0x52 #Wake-UP command, Type A. Invites PICCs in state IDLE and HALT to go to READY(*) and prepare for anticollision or selection. 7 bit frame.
    PICC_CMD_CT             = 0x88 #Cascade Tag. Not really a command, but used during anti collision.
    PICC_CMD_SEL_CL1        = 0x93 #Anti collision/Select, Cascade Level 1
    PICC_CMD_SEL_CL2        = 0x95 #Anti collision/Select, Cascade Level 2
    PICC_CMD_SEL_CL3        = 0x97 #Anti collision/Select, Cascade Level 3
    PICC_CMD_HLTA           = 0x50 #HaLT command, Type A. Instructs an ACTIVE PICC to go to state HALT.
    # The commands used for MIFARE Classic (from http://www.nxp.com/documents/data_sheet/MF1S503x.pdf, Section 9)
    # Use PCD_MFAuthent to authenticate access to a sector, then use these commands to read/write/modify the blocks on the sector.
    # The read/write commands can also be used for MIFARE Ultralight.
    PICC_CMD_MF_AUTH_KEY_A  = 0x60 #Perform authentication with Key A
    PICC_CMD_MF_AUTH_KEY_B  = 0x61 #Perform authentication with Key B
    PICC_CMD_MF_READ        = 0x30 #Reads one 16 byte block from the authenticated sector of the PICC. Also used for MIFARE Ultralight.
    PICC_CMD_MF_WRITE       = 0xA0 #Writes one 16 byte block to the authenticated sector of the PICC. Called "COMPATIBILITY WRITE" for MIFARE Ultralight.
    PICC_CMD_MF_DECREMENT   = 0xC0 #Decrements the contents of a block and stores the result in the internal data register.
    PICC_CMD_MF_INCREMENT   = 0xC1 #Increments the contents of a block and stores the result in the internal data register.
    PICC_CMD_MF_RESTORE     = 0xC2 #Reads the contents of a block into the internal data register.
    PICC_CMD_MF_TRANSFER    = 0xB0 #Writes the contents of the internal data register to a block.
    # The commands used for MIFARE Ultralight (from http://www.nxp.com/documents/data_sheet/MF0ICU1.pdf, Section 8.6)
    # The PICC_CMD_MF_READ and PICC_CMD_MF_WRITE can also be used for MIFARE Ultralight.
    PICC_CMD_UL_WRITE       = 0xA2 #Writes one 4 byte page to the PICC.

    # MIFARE constants that does not fit anywhere else
    #  MIFARE_Misc
    MF_ACK                  = 0xA #The MIFARE Classic uses a 4 bit ACK/NAK. Any other value than 0xA is NAK.
    MF_KEY_SIZE             = 6   #A Mifare Crypto1 key is 6 bytes.
    
    # PICC types we can detect. Remember to update PICC_GetTypeName() if you add more.
    # PICC_Type
    PICC_TYPE_UNKNOWN       = 0
    PICC_TYPE_ISO_14443_4   = 1 #PICC compliant with ISO/IEC 14443-4
    PICC_TYPE_ISO_18092     = 2 #PICC compliant with ISO/IEC 18092 (NFC)
    PICC_TYPE_MIFARE_MINI   = 3 #MIFARE Classic protocol, 320 bytes
    PICC_TYPE_MIFARE_1K     = 4 #MIFARE Classic protocol, 1KB
    PICC_TYPE_MIFARE_4K     = 5 #MIFARE Classic protocol, 4KB
    PICC_TYPE_MIFARE_UL     = 6 #MIFARE Ultralight or Ultralight C
    PICC_TYPE_MIFARE_PLUS   = 7 #MIFARE Plus
    PICC_TYPE_TNP3XXX       = 8 #Only mentioned in NXP AN 10833 MIFARE Type Identification Procedure
    ICC_TYPE_NOT_COMPLETE   = 255 #SAK indicates UID is not complete.
    
    # Return codes from the functions in this class. Remember to update GetStatusCodeName() if you add more.
    # StatusCode
    STATUS_OK               = 1 #Success
    STATUS_ERROR            = 2 #Error in communication
    STATUS_COLLISION        = 3 #Collission detected
    STATUS_TIMEOUT          = 4 #Timeout in communication.
    STATUS_NO_ROOM          = 5 #A buffer is not big enough.
    STATUS_INTERNAL_ERROR   = 6 #Internal error in the code. Should not happen ;-)
    STATUS_INVALID          = 7 #Invalid argument.
    STATUS_CRC_WRONG        = 8 #The CRC_A does not match
    STATUS_MIFARE_NACK      = 9 #A MIFARE PICC responded with NAK.
    
    # Size of the MFRC522 FIFO
    FIFO_SIZE               = 64 #The FIFO is 64 bytes.
    
    uid = Uid
    
    
#file rc_i2c

from machine import Pin
import time
from mfrc522_config import mfrc522Config
from soft_iic import softIIC

class mfrc522(mfrc522Config,softIIC):
   
    def __init__(self, scl_, sda_, addr_):
        # Invoke the parent class's constructor
        softIIC.__init__(self, scl_, sda_, addr_)


    # Writes a byte to the specified register in the MFRC522 chip.
    # The interface is described in the datasheet section 8.1.2. 
    def PCD_WriteRegister(self,  
                          _reg,  #The register to write to. One of the PCD_Register enums.
                          _dat   #The value to write.
                          ):
        self.Write(self.addr, _reg, _dat)

    # Writes a number of bytes to the specified register in the MFRC522 chip.
    # The interface is described in the datasheet section 8.1.2.
    def PCD_WriteRegister_(self,  
                           reg,    #The register to write to. One of the PCD_Register enums.
                           count,  #The number of bytes to write to the register
                           lst     #The values to write. Byte array.
                           ):
        self.IIC_start()
        self.IIC_write_byte(self.addr<<1)
        self.IIC_slave_ack()
        
        self.IIC_write_byte(reg)
        self.IIC_slave_ack()
        
        for i in range(count):
            self.IIC_write_byte(lst[i])
            self.IIC_slave_ack()
        self.IIC_stop()
 

    # Reads a byte from the specified register in the MFRC522 chip.
    # The interface is described in the datasheet section 8.1.2.
    def PCD_ReadRegister(self, _reg):     # The register to read from. One of the PCD_Register enums.
        return self.Read(self.addr,_reg)
        # End PCD_ReadRegister()


    # Reads a number of bytes from the specified register in the MFRC522 chip.
    # The interface is described in the datasheet section 8.1.2.
    # self.PCD_ReadRegister_(self.FIFODataReg, n, backData, rxAlign)
    def PCD_ReadRegister_(self,
                          reg,       # The register to read from. One of the PCD_Register enums.
                          count,     # The number of bytes to read
                          values,    # Byte array to store the values in.
                          rxAlign = 0    # Only bit positions rxAlign..7 in values[0] are updated.
                          ):
        if count == 0:
            return
        self.IIC_start()
        self.IIC_write_byte(self.addr<<1)
        self.IIC_slave_ack()
        #print("--------------1")
        self.IIC_write_byte(reg)
        self.IIC_slave_ack()
        self.IIC_stop()
        #print("--------------2")
        self.IIC_start()
        self.IIC_write_byte((self.addr<<1)|1)
        self.IIC_slave_ack()
        #print("--------------3")
        
        for i in range(count):
            if i == 0 and rxAlign != 0:         # Only update bit positions rxAlign..7 in values[0]
                # Create bit mask for bit positions rxAlign..7
                mask = 0
                for i in range(rxAlign, 8):
                    mask |= (1<<i)
                # Read value and tell that we want to read the same address again.
                value = self.IIC_read_byte()
                # Apply mask to both current value of values[0] and the new data in value.
                values[0] = (values[i] & ~mask) | (value & mask)
            else:   # Normal case
                values[i] = self.IIC_read_byte()
            
            if i < count - 1:
                self.IIC_master_ack()
            else:
                self.IIC_master_notack()
                self.IIC_stop()
        #print(values)     
        # End PCD_ReadRegister()
        
        
    def PCD_Init(self):
        self.PCD_Reset()

        # When communicating with a PICC we need a timeout if something goes wrong.
        # f_timer = 13.56 MHz / (2*TPreScaler+1) where TPreScaler = [TPrescaler_Hi:TPrescaler_Lo].
        # TPrescaler_Hi are the four low bits in TModeReg. TPrescaler_Lo is TPrescalerReg.
        self.PCD_WriteRegister(self.TModeReg, 0x80)      # TAuto=1; timer starts automatically at the end of the transmission in all communication modes at all speeds
        self.PCD_WriteRegister(self.TPrescalerReg, 0xA9) # TPreScaler = TModeReg[3..0]:TPrescalerReg, ie 0x0A9 = 169 => f_timer=40kHz, ie a timer period of 25�s.
        self.PCD_WriteRegister(self.TReloadRegH, 0x03)   # Reload timer with 0x3E8 = 1000, ie 25ms before timeout.
        self.PCD_WriteRegister(self.TReloadRegL, 0xE8)   

        self.PCD_WriteRegister(self.TxASKReg, 0x40)      # Default 0x00. Force a 100 % ASK modulation independent of the ModGsPReg register setting
        self.PCD_WriteRegister(self.ModeReg, 0x3D)       # Default 0x3F. Set the preset value for the CRC coprocessor for the CalcCRC command to 0x6363 (ISO 14443-3 part 6.2.4)
        self.PCD_AntennaOn()                        # Enable the antenna driver pins TX1 and TX2 (they were disabled by the reset)
        # End PCD_Init()

        
    # Performs a soft reset on the MFRC522 chip and waits for it to be ready again.
    def PCD_Reset(self):
        # Issue the SoftReset command.
        self.PCD_WriteRegister(self.CommandReg, self.PCD_SoftReset)
        time.sleep(1)
        
        if self.PCD_ReadRegister(self.CommandReg) & (1<<4):
            print("Reset error!")


    # Turns the antenna on by enabling pins TX1 and TX2.
    # After a reset these pins are disabled.
    def PCD_AntennaOn(self):
        value = self.PCD_ReadRegister(self.TxControlReg)
        #print("AntennaOn data:" + str(value))
        if value & 0x03 != 0x03:
            self.PCD_WriteRegister(self.TxControlReg, value | 0x03)
        #End PCD_AntennaOn()
 
 
    # Turns the antenna off by disabling pins TX1 and TX2.
    def PCD_AntennaOff(self):
        self.PCD_ClearRegisterBitMask(self.TxControlReg, 0x03)

    
    # Sets the bits given in mask in register reg.
    def PCD_SetRegisterBitMask(self,
                               reg,              # The register to update. One of the PCD_Register enums.
                               mask              # The bits to set.
                               ):
        tmp = self.PCD_ReadRegister(reg)
        self.PCD_WriteRegister(reg, tmp | mask)  # set bit mask
        # End PCD_SetRegisterBitMask()
    
    
    # Clears the bits given in mask from register reg.
    def PCD_ClearRegisterBitMask(self,
                                 reg,   # The register to update. One of the PCD_Register enums.
                                 mask   # The bits to clear.
                                 ):
        tmp = self.PCD_ReadRegister(reg)
        self.PCD_WriteRegister(reg, tmp & (~mask))  #clear bit mask
        #  End PCD_ClearRegisterBitMask()
        
        
    # Use the CRC coprocessor in the MFRC522 to calculate a CRC_A.  
    #
    # @return STATUS_OK on success, STATUS_??? otherwise.
    def PCD_CalculateCRC(self,
                         data,   #In: Pointer to the data to transfer to the FIFO for CRC calculation.
                         length, #In: The number of bytes to transfer.
                         result  #Out: Pointer to result buffer. Result is written to result[0..1], low byte first.
                         ):
        self.PCD_WriteRegister(self.CommandReg, self.PCD_Idle)      # Stop any active command.
        self.PCD_WriteRegister(self.DivIrqReg, 0x04)                # Clear the CRCIRq interrupt request bit
        self.PCD_SetRegisterBitMask(self.FIFOLevelReg, 0x80)        # FlushBuffer = 1, FIFO initialization
        self.PCD_WriteRegister_(self.FIFODataReg, length, data)      # Write data to the FIFO
        self.PCD_WriteRegister(self.CommandReg, self.PCD_CalcCRC)   # Start the calculation
        # Wait for the CRC calculation to complete. Each iteration of the while-loop takes 17.73�s.
        while True:
            n = self.PCD_ReadRegister(self.DivIrqReg)    # DivIrqReg[7..0] bits are: Set2 reserved reserved MfinActIRq reserved CRCIRq reserved reserved
            if (n & 0x04):                               # CRCIRq bit set - calculation done
                break
            if (--i == 0):                               # The emergency break. We will eventually terminate on this one after 89ms. Communication with the MFRC522 might be down.
                return self.STATUS_TIMEOUT
        self.PCD_WriteRegister(self.CommandReg, self.PCD_Idle)     # Stop calculating CRC for new content in the FIFO. 
        
        # Transfer the result from the registers to the result buffer
        result[0] = self.PCD_ReadRegister(self.CRCResultRegL)
        result[1] = self.PCD_ReadRegister(self.CRCResultRegH)
        return self.STATUS_OK        
        # End PCD_CalculateCRC()


    # Executes the Transceive command.
    # CRC validation can only be done if backData and backLen are specified.
    # 
    # @return STATUS_OK on success, STATUS_??? otherwise.
    def PCD_TransceiveData(self,
                           sendData,   # Pointer to the data to transfer to the FIFO.
                           sendLen,    # Number of bytes to transfer to the FIFO.
                           backData,   # NULL or pointer to buffer if data should be read back after executing the command.
                           backLen,    # In: Max number of bytes to write to *backData. Out: The number of bytes returned.
                           validBits,  # In/Out: The number of valid bits in the last byte. 0 for 8 valid bits. Default NULL.
                           rxAlign,    # In: Defines the bit position in backData[0] for the first bit received. Default 0.
                           checkCRC    # In: True => The last two bytes of the response is assumed to be a CRC_A that must be validated.
                           ):
        waitIRq = 0x30
        return self.PCD_CommunicateWithPICC(self.PCD_Transceive, waitIRq, sendData, sendLen, backData, backLen, validBits, rxAlign, checkCRC)
        # End PCD_TransceiveData()
        
        
    # Transfers data to the MFRC522 FIFO, executes a command, waits for completion and transfers data back from the FIFO.
    # CRC validation can only be done if backData and backLen are specified.
    #
    # @return STATUS_OK on success, STATUS_??? otherwise.
    # result = self.PCD_TransceiveData(buffer, bufferUsed, responseBuffer, responseLength, tLB, rxAlign, 0)
    def PCD_CommunicateWithPICC(self,
                                command,        # The command to execute. One of the PCD_Command enums.
                                waitIRq,        # The bits in the ComIrqReg register that signals successful completion of the command.
                                sendData,       # Pointer to the data to transfer to the FIFO.
                                sendLen,        # Number of bytes to transfer to the FIFO.
                                backData,       # NULL or pointer to buffer if data should be read back after executing the command.
                                backLen,        # In: Max number of bytes to write to *backData. Out: The number of bytes returned.
                                validBits,      # In/Out: The number of valid bits in the last byte. 0 for 8 valid bits.
                                rxAlign,        # In: Defines the bit position in backData[0] for the first bit received. Default 0.
                                checkCRC        # In: True => The last two bytes of the response is assumed to be a CRC_A that must be validated.
                                ):
        txLastBits = validBits[0] if validBits != None else 0
        bitFraming = (rxAlign << 4) + txLastBits    # RxAlign = BitFramingReg[6..4]. TxLastBits = BitFramingReg[2..0]
        
        self.PCD_WriteRegister(self.CommandReg, self.PCD_Idle)        # Stop any active command.
        self.PCD_WriteRegister(self.ComIrqReg, 0x7F)                  # Clear all seven interrupt request bits
        self.PCD_SetRegisterBitMask(self.FIFOLevelReg, 0x80)          # FlushBuffer = 1, FIFO initialization
        self.PCD_WriteRegister_(self.FIFODataReg, sendLen, sendData)  # Write sendData to the FIFO
        self.PCD_WriteRegister(self.BitFramingReg, bitFraming)        # Bit adjustments
        self.PCD_WriteRegister(self.CommandReg, command)              # Execute the command
        if command == self.PCD_Transceive:
            self.PCD_SetRegisterBitMask(self.BitFramingReg, 0x80)     # StartSend=1, transmission of data starts

        # Wait for the command to complete.
        # In PCD_Init() we set the TAuto flag in TModeReg. This means the timer automatically starts when the PCD stops transmitting.
        # Each iteration of the do-while-loop takes 17.86�s.
        i = 2000
        while True:
            n = self.PCD_ReadRegister(self.ComIrqReg)    #ComIrqReg[7..0] bits are: Set1 TxIRq RxIRq IdleIRq HiAlertIRq LoAlertIRq ErrIRq TimerIRq
            if n & waitIRq:
                break
            if n & 0x01:
                return self.STATUS_TIMEOUT
            if --i == 0:
                return self.STATUS_TIMEOUT
        
        # Stop now if any errors except collisions were detected.
        errorRegValue = self.PCD_ReadRegister(self.ErrorReg)    # ErrorReg[7..0] bits are: WrErr TempErr reserved BufferOvfl CollErr CRCErr ParityErr ProtocolErr
        if errorRegValue & 0x13:                                # BufferOvfl ParityErr ProtocolErr
            return self.STATUS_ERROR
        
        # If the caller wants data back, get it from the MFRC522.
        if backData != None and backLen != None :
            n = self.PCD_ReadRegister(self.FIFOLevelReg)    # Number of bytes in the FIFO
            if n> backLen[0]:
                return self.STATUS_NO_ROOM
            backLen[0] = n                                     # Number of bytes returned
            # Note: Use list mutable types in Python
            self.PCD_ReadRegister_(self.FIFODataReg, n, backData, rxAlign)  # Get received data from FIFO
            #print("backData:")
            #print(backData)
            _validBits = self.PCD_ReadRegister(self.ControlReg) & 0x07  # RxLastBits[2:0] indicates the number of valid bits in the last received byte. If this value is 000b, the whole byte is valid.
            if validBits != None:
                validBits[0] = _validBits
                
        # Tell about collisions
        if errorRegValue & 0x08: # collErr
            return self.STATUS_COLLISION
        
        # Perform CRC_A validation if requested.
        if backData != None and  backLen != None  and checkCRC != 0:
            # In this case a MIFARE Classic NAK is not OK.
            if backLen[0] == 1 and _validBits[0] == 4:
                return self.STATUS_MIFARE_NACK
            # We need at least the CRC_A value and all 8 bits of the last byte must be received.
            if backLen[0] < 2 or _validBits != 0:
                return self.STATUS_CRC_WRONG
            # Verify CRC_A - do our own calculation and store the control in controlBuffer.
            controlBuffer = [0, 0]
            n = self.PCD_CalculateCRC(backData[0], backLen[0] - 2, controlBuffer[0])
            if n != self.STATUS_OK:
                return n
            if (backData[backLen[0] - 2] != controlBuffer[0]) or (backData[backLen[0] - 1] != controlBuffer[1]):
                return self.STATUS_CRC_WRONG
        return self.STATUS_OK;
        # End PCD_CommunicateWithPICC()
        
            
    # Transmits a REQuest command, Type A. Invites PICCs in state IDLE to go to READY and prepare for anticollision or selection. 7 bit frame.
    # Beware: When two PICCs are in the field at the same time I often get STATUS_TIMEOUT - probably due do bad antenna design.
    # 
    # @return STATUS_OK on success, STATUS_??? otherwise.
    def PICC_RequestA(self,
                      bufferATQA,  # The buffer to store the ATQA (Answer to request) in
                      bufferSize   # Buffer size, at least two bytes. Also number of bytes returned if STATUS_OK.
                      ):
        cmd    = [self.PICC_CMD_REQA]
        return self.PICC_REQA_or_WUPA(cmd, bufferATQA, bufferSize)
        # End PICC_RequestA()
        
 
    # Transmits REQA or WUPA commands.
    # Beware: When two PICCs are in the field at the same time I often get STATUS_TIMEOUT - probably due do bad antenna design.
    # 
    # @return STATUS_OK on success, STATUS_??? otherwise.
    def PICC_REQA_or_WUPA(self,
                          command,     # The command to send - PICC_CMD_REQA or PICC_CMD_WUPA
                          bufferATQA,  # The buffer to store the ATQA (Answer to request) in
                          bufferSize   # Buffer size, at least two bytes. Also number of bytes returned if STATUS_OK.
                          ):
        if bufferATQA == None or bufferSize[0] < 2:   # The ATQA response is 2 bytes long.
            return self.STATUS_NO_ROOM
        self.PCD_ClearRegisterBitMask(self.CollReg, 0x80) # ValuesAfterColl=1 => Bits received after collision are cleared.
        validBits = [7]  # For REQA and WUPA we need the short frame format - transmit only 7 bits of the last (and only) byte. TxLastBits = BitFramingReg[2..0]
        status = self.PCD_TransceiveData(command, 1, bufferATQA, bufferSize, validBits, 0, 0)
        if status != self.STATUS_OK:
            return status
        if bufferSize[0] != 2 or validBits[0] != 0:
            return self.STATUS_ERROR
        return self.STATUS_OK
        # End PICC_REQA_or_WUPA()
    

    # Transmits SELECT/ANTICOLLISION commands to select a single PICC.
    # Before calling this function the PICCs must be placed in the READY(*) state by calling PICC_RequestA() or PICC_WakeupA().
    # On success:
    #       - The chosen PICC is in state ACTIVE(*) and all other PICCs have returned to state IDLE/HALT. (Figure 7 of the ISO/IEC 14443-3 draft.)
    #       - The UID size and value of the chosen PICC is returned in *uid along with the SAK.
    # 
    # A PICC UID consists of 4, 7 or 10 bytes.
    # Only 4 bytes can be specified in a SELECT command, so for the longer UIDs two or three iterations are used:
    #       UID size    Number of UID bytes    Cascade levels    Example of PICC
    #       ========    ===================    ==============    ===============
    #       single               4                   1           MIFARE Classic
    #       double               7                   2           MIFARE Ultralight
    #       triple              10                   3           Not currently in use?
    # 
    # @return STATUS_OK on success, STATUS_??? otherwise.
    def PICC_Select(self,
                    uid,           # Pointer to Uid struct. Normally output, but can also be used to supply a known UID.
                    validBits      # The number of known UID bits supplied in *uid. Normally 0. If set you must also supply uid->size.
                    ):
        uidComplete = False
        selectDone = False
        useCascadeTag = False
        cascadeLevel = 1
        result = 0
        count = 0
        index = 0
        uidIndex = 0                     # The first index in uid->uidByte[] that is used in the current Cascade Level.
        currentLevelKnownBits = 0        # The number of known UID bits in the current Cascade Level.
        buffer = [0,0,0,0,0,0,0,0,0]     # The SELECT/ANTICOLLISION commands uses a 7 byte standard frame + 2 bytes CRC_A
        bufferUsed = 0                   # The number of bytes used in the buffer, ie the number of bytes to transfer to the FIFO.
        rxAlign = 0                      # Used in BitFramingReg. Defines the bit position for the first bit received.
        txLastBits = 0                   # Used in BitFramingReg. The number of valid bits in the last transmitted byte.
        responseBuffer = [0]
        responseLength = [0]
        # Description of buffer structure:
        #       Byte 0: SEL                 Indicates the Cascade Level: PICC_CMD_SEL_CL1, PICC_CMD_SEL_CL2 or PICC_CMD_SEL_CL3
        #       Byte 1: NVB                 Number of Valid Bits (in complete command, not just the UID): High nibble: complete bytes, Low nibble: Extra bits.
        #       Byte 2: UID-data or CT      See explanation below. CT means Cascade Tag.
        #       Byte 3: UID-data
        #       Byte 4: UID-data
        #       Byte 5: UID-data
        #       Byte 6: BCC                 Block Check Character - XOR of bytes 2-5
        #       Byte 7: CRC_A
        #       Byte 8: CRC_A
        #  The BCC and CRC_A is only transmitted if we know all the UID bits of the current Cascade Level.
        # 
        #  Description of bytes 2-5: (Section 6.5.4 of the ISO/IEC 14443-3 draft: UID contents and cascade levels)
        #       UID size    Cascade level   Byte2   Byte3   Byte4   Byte5
        #       ========    =============   =====  =====    =====   =====
        #        4 bytes        1           uid0    uid1    uid2    uid3
        #        7 bytes        1           CT      uid0    uid1    uid2
        #                       2           uid3    uid4    uid5    uid6
        #       10 bytes        1           CT      uid0    uid1    uid2
        #                       2           CT      uid3    uid4    uid5
        #                       3           uid6    uid7    uid8    uid9
    
        # Sanity checks
        if validBits > 80:
            return self.STATUS_INVALID
    
        # Prepare MFRC522
        self.PCD_ClearRegisterBitMask(self.CollReg, 0x80)    # ValuesAfterColl=1 => Bits received after collision are cleared.

        # Repeat Cascade Level loop until we have a complete UID.
        uidComplete = False
        while uidComplete == False:
            # Set the Cascade Level in the SEL byte, find out if we need to use the Cascade Tag in byte 2.    
            if cascadeLevel == 1:
                buffer[0] = self.PICC_CMD_SEL_CL1
                uidIndex = 0
                useCascadeTag = validBits and uid.size > 4    # When we know that the UID has more than 4 bytes
            elif cascadeLevel == 2:
                buffer[0] = self.PICC_CMD_SEL_CL2
                uidIndex = 3
                useCascadeTag = validBits and uid.size > 7    # When we know that the UID has more than 7 bytes
            elif cascadeLevel == 3:
                buffer[0] = self.PICC_CMD_SEL_CL3
                uidIndex = 6
                useCascadeTag = False                         # Never used in CL3.           
            else:
                return self.STATUS_INTERNAL_ERROR
    
            # How many UID bits are known in this Cascade Level?
            currentLevelKnownBits = validBits - (8 * uidIndex)
            if currentLevelKnownBits < 0:
                currentLevelKnownBits = 0
        
            # Copy the known bits from uid->uidByte[] to buffer[]
            index = 2  # destination index in buffer[]
            #print(useCascadeTag);
            if useCascadeTag:
                index = index+1
                buffer[index] = self.PICC_CMD_CT
            # The number of bytes needed to represent the known bits for this level.
            bytesToCopy = 1 if currentLevelKnownBits % 8 > 0 else 0 # (currentLevelKnownBits % 8 ? 1 : 0) 
            bytesToCopy = currentLevelKnownBits // 8 + bytesToCopy
            if bytesToCopy:
                maxBytes = 3 if useCascadeTag else 4  # maxBytes = useCascadeTag ? 3 : 4
                if bytesToCopy > maxBytes:
                    bytesToCopy = maxBytes
                for i in range(bytesToCopy):
                    index = index+1
                    buffer[index] = uid.uidByte[uidIndex + i]
            # Now that the data has been copied we need to include the 8 bits in CT in currentLevelKnownBits
            if useCascadeTag:
                currentLevelKnownBits = currentLevelKnownBits + 8
        
            # Repeat anti collision loop until we can transmit all UID bits + BCC and receive a SAK - max 32 iterations.
            selectDone = False            
            while selectDone == False:
                # Find out how many bits and bytes to send and receive. 
                if currentLevelKnownBits >= 32:  # All UID bits in this Cascade Level are known. This is a SELECT.
                    # Serial.print(F("SELECT: currentLevelKnownBits=")); Serial.println(currentLevelKnownBits, DEC);
                    buffer[1] = 0x70 # NVB - Number of Valid Bits: Seven whole bytes
                    # Calculate BCC - Block Check Character
                    buffer[6] = buffer[2] ^ buffer[3] ^ buffer[4] ^ buffer[5]
                    # Calculate CRC_A
                    tmpBuffer = [buffer[7], buffer[8]]
                    result = self.PCD_CalculateCRC(buffer, 7, tmpBuffer)
                    buffer[7] = tmpBuffer[0]
                    buffer[8] = tmpBuffer[1]
                    
                    if result != self.STATUS_OK:
                        return result
                    txLastBits  = 0   # 0 => All 8 bits are valid.
                    bufferUsed  = 9
                    # Store response in the last 3 bytes of buffer (BCC and CRC_A - not needed after tx)
                    responseBuffer = [0].copy()
                    responseBuffer[0] = buffer[6]
                    responseBuffer = responseBuffer + buffer[7:]
                    responseLength[0] = 3
                    bufferFlag = 6
                    
                else: # This is an ANTICOLLISION.
                    # Serial.print(F("ANTICOLLISION: currentLevelKnownBits=")); Serial.println(currentLevelKnownBits, DEC);
                    txLastBits      = currentLevelKnownBits % 8
                    count           = currentLevelKnownBits // 8      # Number of whole bytes in the UID part.
                    index           = 2 + count                           # Number of whole bytes: SEL + NVB + UIDs
                    buffer[1]       = (index << 4) + txLastBits           # NVB - Number of Valid Bits
                
                    bufferUsed      = 1 if txLastBits else 0
                    bufferUsed      = index + bufferUsed
                    
                    responseBuffer = [0].copy()
                    # Store response in the unused part of buffer
                    responseBuffer[0]  = buffer[index]
                    responseBuffer     = responseBuffer + buffer[index+1:]
                    responseLength[0]  = len(buffer) - index
                    bufferFlag = index

                # Set bit adjustments
                rxAlign = txLastBits              # Having a seperate variable is overkill. But it makes the next line easier to read.
                self.PCD_WriteRegister(self.BitFramingReg, (rxAlign << 4) + txLastBits)   # RxAlign = BitFramingReg[6..4]. TxLastBits = BitFramingReg[2..0]
    
                #Transmit the buffer and receive the response.
                tLB = [txLastBits]
                result = self.PCD_TransceiveData(buffer, bufferUsed, responseBuffer, responseLength, tLB, rxAlign, 0)
                for i in range(bufferFlag, bufferFlag+responseLength[0]):
                    buffer[i] = responseBuffer[i-bufferFlag]

                if result == self.STATUS_COLLISION:    # More than one PICC in the field => collision.
                    result = self.PCD_ReadRegister(CollReg) # CollReg[7..0] bits are: ValuesAfterColl reserved CollPosNotValid CollPos[4:0]
                    if result & 0x20:
                        return self.STATUS_COLLISION   # Without a valid collision position we cannot continue
                    collisionPos = result & 0x1F       # Values 0-31, 0 means bit 32.
                    if collisionPos == 0:
                        collisionPos = 32
                    if collisionPos <= currentLevelKnownBits:  # No progress - should not happen
                        return self.STATUS_INTERNAL_ERROR
                    # Choose the PICC with the bit set.
                    currentLevelKnownBits = collisionPos
                    count = (currentLevelKnownBits - 1) % 8    # The bit to modify
                    index = 1 if count else 0
                    index = 1 + (currentLevelKnownBits / 8) + index  # First byte is index 0.
                    buffer[index] = buffer[index] | (1 << count)
                elif result != self.STATUS_OK:
                    return result
                else: # STATUS_OK
                    if currentLevelKnownBits >= 32:  # This was a SELECT.
                        selectDone = True            # No more anticollision
                        # We continue below outside the while.
                    else:  # This was an ANTICOLLISION.
                        # We now have all 32 bits of the UID in this Cascade Level
                        currentLevelKnownBits = 32
                        # Run loop again to do the SELECT.
            # End of while (!selectDone)
    
            # We do not check the CBB - it was constructed by us above.
            # Copy the found UID bytes from buffer[] to uid->uidByte[]
            index = 3 if buffer[2] == self.PICC_CMD_CT else 2  # source index in buffer[]
            bytesToCopy = 3 if buffer[2] == self.PICC_CMD_CT else 4
            for i in range(bytesToCopy):
                uid.uidByte[uidIndex + i] = buffer[index]
                index = index+1
              
            # Check response SAK (Select Acknowledge)
            if responseLength[0] != 3 or txLastBits != 0: # SAK must be exactly 24 bits (1 byte + CRC_A).
                return self.STATUS_ERROR
            # Verify CRC_A - do our own calculation and store the control in buffer[2..3] - those bytes are not needed anymore.          
            CRCbuffer = [buffer[2]]
            CRCbuffer = CRCbuffer + buffer[3:]
            result = self.PCD_CalculateCRC(responseBuffer, 1, CRCbuffer)
            buffer[2] = CRCbuffer[0]
            buffer[3] = CRCbuffer[1]
            
            if result != self.STATUS_OK:
                return result
            
            if (buffer[2] != responseBuffer[1]) or (buffer[3] != responseBuffer[2]):
                return self.STATUS_CRC_WRONG
            if responseBuffer[0] & 0x04: # Cascade bit set - UID not complete yes
                cascadeLevel = cascadeLevel+1
            else:
                uidComplete = True
                uid.sak = responseBuffer[0] 
        # End of while (!uidComplete)
            
        # Set correct uid->size
        uid.size = 3 * cascadeLevel + 1       
        return self.STATUS_OK
        #  End PICC_Select()
                
                
    # Returns true if a PICC responds to PICC_CMD_REQA.
    # Only "new" cards in state IDLE are invited. Sleeping cards in state HALT are ignored.
    # 
    # @return bool
    def PICC_IsNewCardPresent(self):
        bufferATQA = [0, 0]
        bufferSize = [len(bufferATQA)]
        result = self.PICC_RequestA(bufferATQA, bufferSize)
        return result == self.STATUS_OK or result == self.STATUS_COLLISION
        #  End PICC_IsNewCardPresent()
        

    # Simple wrapper around PICC_Select.
    # Returns true if a UID could be read.
    # Remember to call PICC_IsNewCardPresent(), PICC_RequestA() or PICC_WakeupA() first.
    # The read UID is available in the class variable uid.
    # 
    # @return bool
    def PICC_ReadCardSerial(self):
        result = self.PICC_Select(self.uid, 0)
        return (result == self.STATUS_OK)
        # End PICC_ReadCardSerial()
        
        
    # Show details of PCD - MFRC522 Card Reader details.
    def ShowReaderDetails(self):
        v = self.PCD_ReadRegister(self.VersionReg)
        version = str(v)
        if v == 0x91:
            version = version + " = v1.0"
        elif v == 0x92:
            version = version + " = v2.0"
        else:
            version = version + "unknown"   
        print("MFRC522 Software Version:" + version)

#file rc rfid implementation


from machine import Pin, PWM,I2C, Pin
import time
from mfrc522_i2c import mfrc522

pwm = PWM(Pin(13))  
pwm.freq(50)
button1 = Pin(16, Pin.IN, Pin.PULL_UP)
#i2c config
addr = 0x28
scl = 22
sda = 21
    
rc522 = mfrc522(scl, sda, addr)
rc522.PCD_Init()
rc522.ShowReaderDetails()            # Show details of PCD - MFRC522 Card Reader details

data = 0

while True:
    if rc522.PICC_IsNewCardPresent():
        #print("Is new card present!")
        if rc522.PICC_ReadCardSerial() == True:
            print("Card UID:")
            #print(rc522.uid.uidByte[0 : rc522.uid.size])
            for i in rc522.uid.uidByte[0 : rc522.uid.size]:
                data = data + i
        print(data)
        if(data == 510):
            pwm.duty(128)
            print("open")
        else:
            print("error")
        data = 0
    btnVal1 = button1.value()
    if(btnVal1 == 0):
        pwm.duty(25)
        print("close")
    time.sleep(1)

# file soft_iic

from machine import Pin
import time

class softIIC:

    def __init__(self, scl_, sda_, addr_):
        self.addr = addr_
        self.scl  = scl_
        self.sda  = sda_
        
        
    def IIC_start(self):
        Pin_scl = Pin(self.scl, Pin.OUT, value=1)    # create output pin
        Pin_sda = Pin(self.sda, Pin.OUT, value=1)    # create output pin                   
        #Pin_sda.value(1)
        #Pin_scl.value(1)
        time.sleep_us(5)
        #time.sleep(1)
        Pin_sda.value(0)                    
        time.sleep_us(5)
        Pin_scl.value(0)         
        #time.sleep(1)
        

    def IIC_stop(self):
        Pin_scl = Pin(self.scl, Pin.OUT, value=0)    # create output pin
        Pin_sda = Pin(self.sda, Pin.OUT, value=0)    # create output pin
        #Pin_scl.value(0) 
        #Pin_sda.value(0)                  
        time.sleep_us(5)
        Pin_scl.value(1)
        Pin_sda.value(1)
        time.sleep_us(5)  


    def IIC_master_ack(self):
        Pin_scl = Pin(self.scl, Pin.OUT, value=0)    # create output pin
        Pin_sda = Pin(self.sda, Pin.OUT, value=0)    # create output pin
        #Pin_scl.value(0)
        #Pin_sda.value(0)
        time.sleep_us(5)
        
        Pin_scl.value(1)
        time.sleep_us(5)
        Pin_scl.value(0)
        #Pin_sda.value(1)                      


    def IIC_master_notack(self):
        Pin_scl = Pin(self.scl, Pin.OUT, value=0)    # create output pin
        Pin_sda = Pin(self.sda, Pin.OUT, value=1)    # create output pin
        #Pin_scl.value(0)
        #Pin_sda.value(1)
        time.sleep_us(5)
        Pin_scl.value(1)                  
        time.sleep_us(5)
        Pin_scl.value(0)


    def IIC_slave_ack(self):
        i=0
        Pin_scl = Pin(self.scl, Pin.OUT, value=0)    # create output pin
        Pin_sda = Pin(self.sda, Pin.IN, Pin.PULL_UP)     # create input pin       
        Pin_scl.value(1)
        time.sleep_us(5)
        while Pin_sda.value() == 1:
            time.sleep_us(1)
            i = i+1
            if i>20:
                while 1 :
                    print("IIC slave device not ack")
                    time.sleep(1)
                #return
                    

    def IIC_read_byte(self):
        dat = 0
        Pin_scl = Pin(self.scl, Pin.OUT, value=0)    # create input pin
        Pin_sda = Pin(self.sda, Pin.IN, Pin.PULL_UP)     # create input pin        
        for i in range(8):
            Pin_scl.value(0)
            time.sleep_us(3)
            Pin_scl.value(1)
            time.sleep_us(2)
            #print(Pin_sda.value())
            if Pin_sda.value() == 1:
                dat = dat<<1 | 1
            else:
                dat = dat<<1
            time.sleep_us(5)
        return dat


    def IIC_write_byte(self, dat):
        Pin_scl = Pin(self.scl, Pin.OUT, value=0)    # create output pin
        Pin_sda = Pin(self.sda, Pin.OUT, value=0)    # create output pin        
        for i in range(8):
            if 0x80 & dat == 0x80:
                Pin_sda.value(1)
                #print(1)
            else:
                Pin_sda.value(0)
                #print(0)
            Pin_scl.value(1)
            time.sleep_us(5)
            Pin_scl.value(0)
            time.sleep_us(5)
            dat = dat<<1
        #print("--------------------")
 
 
    def Read(self, _adr, _reg):
        self.IIC_start()
        self.IIC_write_byte(_adr<<1)
        self.IIC_slave_ack()
        #print("--------------1")
        self.IIC_write_byte(_reg)
        self.IIC_slave_ack()
        self.IIC_stop()
        #print("--------------2")
        self.IIC_start()
        self.IIC_write_byte((_adr<<1)|1)
        self.IIC_slave_ack()
        #print("--------------3")
        dat = self.IIC_read_byte()
        self.IIC_master_notack()
        self.IIC_stop()
        return dat


    def Write(self, _adr, _reg, _dat):
        self.IIC_start()
        self.IIC_write_byte(_adr<<1)
        self.IIC_slave_ack()
        
        self.IIC_write_byte(_reg)
        self.IIC_slave_ack()
 
        self.IIC_write_byte(_dat)
        self.IIC_slave_ack()
        self.IIC_stop()
        
        
#file i2c_lcd
"""Implements a HD44780 character LCD connected via PCF8574 on I2C. 
   This was tested with: https://www.wemos.cc/product/d1-mini.html""" 
from lcd_api import LcdApi 
from machine import SoftI2C 
from time import sleep_ms 
# The PCF8574 has a jumper selectable address: 0x20 - 0x27 
#DEFAULT_I2C_ADDR = 0x20 
# Defines shifts or masks for the various LCD line attached to the PCF8574 
MASK_RS = 0x01 
MASK_RW = 0x02 
MASK_E = 0x04 
SHIFT_BACKLIGHT = 3 
SHIFT_DATA = 4 
class I2cLcd(LcdApi): 
    """Implements a HD44780 character LCD connected via PCF8574 on I2C.""" 
    def __init__(self, i2c, i2c_addr, num_lines, num_columns): 
        self.i2c = i2c 
        self.i2c_addr = i2c_addr 
        self.i2c.writeto(self.i2c_addr, bytearray([0])) 
        sleep_ms(20)   # Allow LCD time to powerup 
        # Send reset 3 times 
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET) 
        sleep_ms(5)    # need to delay at least 4.1 msec 
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET) 
        sleep_ms(1) 
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET) 
        sleep_ms(1) 
        # Put LCD into 4 bit mode 
        self.hal_write_init_nibble(self.LCD_FUNCTION) 
        sleep_ms(1) 
        LcdApi.__init__(self, num_lines, num_columns) 
        cmd = self.LCD_FUNCTION 
        if num_lines > 1: 
            cmd |= self.LCD_FUNCTION_2LINES 
        self.hal_write_command(cmd) 
    def hal_write_init_nibble(self, nibble): 
        """Writes an initialization nibble to the LCD. 
        This particular function is only used during initialization. 
        """ 
        byte = ((nibble >> 4) & 0x0f) << SHIFT_DATA 
        self.i2c.writeto(self.i2c_addr, bytearray([byte | MASK_E])) 
        self.i2c.writeto(self.i2c_addr, bytearray([byte])) 
    def hal_backlight_on(self): 
        """Allows the hal layer to turn the backlight on.""" 
        self.i2c.writeto(self.i2c_addr, bytearray([1 << SHIFT_BACKLIGHT])) 
    def hal_backlight_off(self): 
        """Allows the hal layer to turn the backlight off.""" 
        self.i2c.writeto(self.i2c_addr, bytearray([0])) 
    def hal_write_command(self, cmd): 
        """Writes a command to the LCD. 
        Data is latched on the falling edge of E. 
        """ 
        byte = ((self.backlight << SHIFT_BACKLIGHT) | (((cmd >> 4) & 0x0f) << SHIFT_DATA)) 
        self.i2c.writeto(self.i2c_addr, bytearray([byte | MASK_E])) 
        self.i2c.writeto(self.i2c_addr, bytearray([byte])) 
        byte = ((self.backlight << SHIFT_BACKLIGHT) | ((cmd & 0x0f) << SHIFT_DATA)) 
        self.i2c.writeto(self.i2c_addr, bytearray([byte | MASK_E])) 
        self.i2c.writeto(self.i2c_addr, bytearray([byte])) 
        if cmd <= 3: 
            # The home and clear commands require a worst case delay of 4.1 msec 
            sleep_ms(5) 
    def hal_write_data(self, data): 
        """Write data to the LCD.""" 
        byte = (MASK_RS | (self.backlight << SHIFT_BACKLIGHT) | (((data >> 4) & 0x0f) << SHIFT_DATA)) 
        self.i2c.writeto(self.i2c_addr, bytearray([byte | MASK_E])) 
        self.i2c.writeto(self.i2c_addr, bytearray([byte])) 
        byte = (MASK_RS | (self.backlight << SHIFT_BACKLIGHT) | ((data & 0x0f) << SHIFT_DATA)) 
        self.i2c.writeto(self.i2c_addr, bytearray([byte | MASK_E])) 
        self.i2c.writeto(self.i2c_addr, bytearray([byte]))

# file lcd_api

"""Provides an API for talking to HD44780 compatible character LCDs.""" 
import time 
class LcdApi: 
    """Implements the API for talking with HD44780 compatible character LCDs. 
    This class only knows what commands to send to the LCD, and not how to get 
    them to the LCD. 
    It is expected that a derived class will implement the hal_xxx functions. 
    """ 
    # The following constant names were lifted from the avrlib lcd.h 
    # header file, however, I changed the definitions from bit numbers 
    # to bit masks. 
    # 
    # HD44780 LCD controller command set 
    LCD_CLR = 0x01              # DB0: clear display 
    LCD_HOME = 0x02             # DB1: return to home position 
    LCD_ENTRY_MODE = 0x04       # DB2: set entry mode 
    LCD_ENTRY_INC = 0x02        # --DB1: increment 
    LCD_ENTRY_SHIFT = 0x01      # --DB0: shift 
    LCD_ON_CTRL = 0x08          # DB3: turn lcd/cursor on 
    LCD_ON_DISPLAY = 0x04       # --DB2: turn display on 
    LCD_ON_CURSOR = 0x02        # --DB1: turn cursor on 
    LCD_ON_BLINK = 0x01         # --DB0: blinking cursor 
    LCD_MOVE = 0x10             # DB4: move cursor/display 
    LCD_MOVE_DISP = 0x08        # --DB3: move display (0-> move cursor) 
    LCD_MOVE_RIGHT = 0x04       # --DB2: move right (0-> left) 
    LCD_FUNCTION = 0x20         # DB5: function set 
    LCD_FUNCTION_8BIT = 0x10    # --DB4: set 8BIT mode (0->4BIT mode) 
    LCD_FUNCTION_2LINES = 0x08  # --DB3: two lines (0->one line) 
    LCD_FUNCTION_10DOTS = 0x04  # --DB2: 5x10 font (0->5x7 font) 
    LCD_FUNCTION_RESET = 0x30   # See "Initializing by Instruction" section 
    LCD_CGRAM = 0x40            # DB6: set CG RAM address 
    LCD_DDRAM = 0x80            # DB7: set DD RAM address 
    LCD_RS_CMD = 0 
    LCD_RS_DATA = 1 
    LCD_RW_WRITE = 0 
    LCD_RW_READ = 1 
    def __init__(self, num_lines, num_columns): 
        self.num_lines = num_lines 
        if self.num_lines > 4: 
            self.num_lines = 4 
        self.num_columns = num_columns 
        if self.num_columns > 40: 
            self.num_columns = 40 
        self.cursor_x = 0 
        self.cursor_y = 0 
        self.implied_newline = False 
        self.backlight = True 
        self.display_off() 
        self.backlight_on() 
        self.clear() 
        self.hal_write_command(self.LCD_ENTRY_MODE | self.LCD_ENTRY_INC) 
        self.hide_cursor() 
        self.display_on() 
    def clear(self): 
        """Clears the LCD display and moves the cursor to the top left 
        corner. 
        """ 
        self.hal_write_command(self.LCD_CLR) 
        self.hal_write_command(self.LCD_HOME) 
        self.cursor_x = 0 
        self.cursor_y = 0 
    def show_cursor(self): 
        """Causes the cursor to be made visible.""" 
        self.hal_write_command(self.LCD_ON_CTRL | self.LCD_ON_DISPLAY | 
                               self.LCD_ON_CURSOR) 
    def hide_cursor(self): 
        """Causes the cursor to be hidden.""" 
        self.hal_write_command(self.LCD_ON_CTRL | self.LCD_ON_DISPLAY) 
    def blink_cursor_on(self): 
        """Turns on the cursor, and makes it blink.""" 
        self.hal_write_command(self.LCD_ON_CTRL | self.LCD_ON_DISPLAY | 
                               self.LCD_ON_CURSOR | self.LCD_ON_BLINK) 
    def blink_cursor_off(self): 
        """Turns on the cursor, and makes it no blink (i.e. be solid).""" 
        self.hal_write_command(self.LCD_ON_CTRL | self.LCD_ON_DISPLAY | 
                               self.LCD_ON_CURSOR) 
    def display_on(self): 
        """Turns on (i.e. unblanks) the LCD.""" 
        self.hal_write_command(self.LCD_ON_CTRL | self.LCD_ON_DISPLAY) 
    def display_off(self): 
        """Turns off (i.e. blanks) the LCD.""" 
        self.hal_write_command(self.LCD_ON_CTRL) 
    def backlight_on(self): 
        """Turns the backlight on. 
        This isn't really an LCD command, but some modules have backlight 
        controls, so this allows the hal to pass through the command. 
        """ 
        self.backlight = True 
        self.hal_backlight_on() 
    def backlight_off(self): 
        """Turns the backlight off. 
        This isn't really an LCD command, but some modules have backlight 
        controls, so this allows the hal to pass through the command. 
        """ 
        self.backlight = False 
        self.hal_backlight_off() 
    def move_to(self, cursor_x, cursor_y): 
        """Moves the cursor position to the indicated position. The cursor 
        position is zero based (i.e. cursor_x == 0 indicates first column). 
        """ 
        self.cursor_x = cursor_x 
        self.cursor_y = cursor_y 
        addr = cursor_x & 0x3f 
        if cursor_y & 1: 
            addr += 0x40    # Lines 1 & 3 add 0x40 
        if cursor_y & 2:    # Lines 2 & 3 add number of columns 
            addr += self.num_columns 
        self.hal_write_command(self.LCD_DDRAM | addr) 
    def putchar(self, char): 
        """Writes the indicated character to the LCD at the current cursor 
        position, and advances the cursor by one position. 
        """ 
        if char == '\n': 
            if self.implied_newline: 
                # self.implied_newline means we advanced due to a wraparound, 
                # so if we get a newline right after that we ignore it. 
                pass 
            else: 
                self.cursor_x = self.num_columns 
        else: 
            self.hal_write_data(ord(char)) 
            self.cursor_x += 1 
        if self.cursor_x >= self.num_columns: 
            self.cursor_x = 0 
            self.cursor_y += 1 
            self.implied_newline = (char != '\n') 
        if self.cursor_y >= self.num_lines: 
            self.cursor_y = 0 
        self.move_to(self.cursor_x, self.cursor_y) 
    def putstr(self, string): 
        """Write the indicated string to the LCD at the current cursor 
        position and advances the cursor position appropriately. 
        """ 
        for char in string: 
            self.putchar(char) 
    def custom_char(self, location, charmap): 
        """Write a character to one of the 8 CGRAM locations, available 
        as chr(0) through chr(7). 
        """ 
        location &= 0x7 
        self.hal_write_command(self.LCD_CGRAM | (location << 3)) 
        self.hal_sleep_us(40) 
        for i in range(8): 
            self.hal_write_data(charmap[i]) 
            self.hal_sleep_us(40) 
        self.move_to(self.cursor_x, self.cursor_y)
        
    def hal_backlight_on(self): 
        """Allows the hal layer to turn the backlight on. 
        If desired, a derived HAL class will implement this function. 
        """ 
        pass 
    def hal_backlight_off(self): 
        """Allows the hal layer to turn the backlight off. 
        If desired, a derived HAL class will implement this function. 
        """ 
        pass 
    def hal_write_command(self, cmd): 
        """Write a command to the LCD. 
        It is expected that a derived HAL class will implement this 
        function. 
        """ 
        raise NotImplementedError 
    def hal_write_data(self, data): 
        """Write data to the LCD. 
        It is expected that a derived HAL class will implement this 
        function. 
        """ 
        raise NotImplementedError 
    def hal_sleep_us(self, usecs): 
        """Sleep for some time (given in microseconds).""" 
        time.sleep_us(usecs)

# file lcd_test

from time import sleep_ms, ticks_ms 
from machine import SoftI2C, Pin 
from i2c_lcd import I2cLcd 

DEFAULT_I2C_ADDR = 0x27

# 初始化 SCL/SDA 引脚并启用内部上拉
scl_pin = Pin(22, Pin.OUT, pull=Pin.PULL_UP)  # GPIO22 启用内部上拉
sda_pin = Pin(21, Pin.OUT, pull=Pin.PULL_UP)  # GPIO21 启用内部上拉

i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)

devices = i2c.scan()
if not devices:
    print("未检测到 I2C 设备！检查接线/供电/上拉电阻")
else:
    print("检测到设备地址：", [hex(addr) for addr in devices])  # 输出十六进制地址‌:ml-citation{ref="3,8" data="citationList"}

lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

lcd.move_to(1, 0)
lcd.putstr('Hello')
lcd.move_to(1, 1)
lcd.putstr('keyestudio')

# The following line of code should be tested
# using the REPL:

# 1. To print a string to the LCD:
#    lcd.putstr('Hello world')
# 2. To clear the display:
#lcd.clear()
# 3. To control the cursor position:
# lcd.move_to(2, 1)
# 4. To show the cursor:
# lcd.show_cursor()
# 5. To hide the cursor:
#lcd.hide_cursor()
# 6. To set the cursor to blink:
#lcd.blink_cursor_on()
# 7. To stop the cursor on blinking:
#lcd.blink_cursor_off()
# 8. To hide the currently displayed character:
#lcd.display_off()
# 9. To show the currently hidden character:
#lcd.display_on()
# 10. To turn off the backlight:
#lcd.backlight_off()
# 11. To turn ON the backlight:
#lcd.backlight_on()
# 12. To print a single character:
#lcd.putchar('x')
# 13. To print a custom character:
#happy_face = bytearray([0x00, 0x0A, 0x00, 0x04, 0x00, 0x11, 0x0E, 0x00])
#lcd.custom_char(0, happy_face)
#lcd.putchar(chr(0))