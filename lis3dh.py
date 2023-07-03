import smbus2

class LIS3DH:

    I2C_ADDRESS = 0x18

    # Ranges
    RANGE_2G  = 0b00 
    RANGE_4G  = 0b01
    RANGE_8G  = 0b10
    RANGE_16G = 0b11
    # default
    RANGE_DEFAULT = RANGE_2G

    # Refresh rates
    DATARATE_400HZ          = 0b0111  # 400Hz 
    DATARATE_200HZ          = 0b0110  # 200Hz
    DATARATE_100HZ          = 0b0101  # 100Hz
    DATARATE_50HZ           = 0b0100  # 50Hz
    DATARATE_25HZ           = 0b0011  # 25Hz
    DATARATE_10HZ           = 0b0010  # 10Hz
    DATARATE_1HZ            = 0b0001  # 1Hz
    DATARATE_POWERDOWN      = 0       # Power down
    DATARATE_LOWPOWER_1K6HZ = 0b1000  # Low power mode (1.6KHz)
    DATARATE_LOWPOWER_5KHZ  = 0b1001  # Low power mode (5KHz) / Normal power mode (1.25KHz)
    # default
    DATARATE_DEFAULT = DATARATE_400HZ

    # Registers
    REG_WHOAMI        = 0x0F  # Device identification register
    REG_TEMPCFG       = 0x1F
    REG_CTRL1         = 0x20  # For data rate selection, and enabling/disabling individual axis
    REG_CTRL2         = 0x21
    REG_CTRL3         = 0x22
    REG_CTRL4         = 0x23  # For BDU, scale selection, resolution selection and self-testing
    REG_CTRL5         = 0x24
    REG_CTRL6         = 0x25
    REG_OUT_X_L       = 0x28
    REG_OUT_Y_L       = 0x2A
    REG_OUT_Z_L       = 0x2C

    # Values
    DEVICE_ID  = 0x33

    AXIS_X = 0x00
    AXIS_Y = 0x01
    AXIS_Z = 0x02

    def __init__(self, address=I2C_ADDRESS, bus=1,
                g_range=RANGE_DEFAULT, datarate=DATARATE_DEFAULT,
                debug=False):
  
        self.isDebug = debug
        self.debug("Initialising LIS3DH")

        self.bus = smbus2.SMBus(1)
        self.address = address

        try:
            val = self.bus.read_byte_data(0x18,self.REG_WHOAMI)
            if val != self.DEVICE_ID:
                raise Exception(("Device ID incorrect - expected 0x{:x}, " +
                                 "got 0x{:x} at address 0x{:x}").format(
                                     self.DEVICE_ID, val, self.address))

            self.debug(("Successfully connected to LIS3DH " +
                        "at address 0x{:x}").format(self.address))
            
        except Exception as e:
            print("Error establishing connection with LIS3DH")
            print(e)

        # Enable all axis
        self.setAxisStatus(self.AXIS_X, True)
        self.setAxisStatus(self.AXIS_Y, True)
        self.setAxisStatus(self.AXIS_Z, True)
        
        self.setDataRate(datarate)

        self.setHighResolution()
        self.setBDU()

        self.setRange(g_range)

    def getX(self):
        return self.getAxis(self.AXIS_X)

    def getY(self):
        return self.getAxis(self.AXIS_Y)

    def getZ(self):
        return self.getAxis(self.AXIS_Z)

    def getAxis(self, axis):
        """Get a reading from the desired axis"""
		
        # Determine which register we need to read from (2 per axis)
        base = self.REG_OUT_X_L + (2 * axis)

        # Get lower bits
        low = self.bus.read_byte_data(0x18,base)
        
        # Get higher bits
        high = self.bus.read_byte_data(0x18,base + 1)
        
        # Combine the two components
        res = low | (high << 8)
        
        # Calculate the 2's complement 
        res = self.twosComp(res)

        g_range = self.getRange()
        divisor = 1
        if g_range == self.RANGE_2G:    divisor = 16380
        elif g_range == self.RANGE_4G:  divisor = 8190
        elif g_range == self.RANGE_8G:  divisor = 4096
        elif g_range == self.RANGE_16G: divisor = 1365.33

        return float(res) / divisor

    def getRange(self):
        """Get the range that the sensor is currently set to"""
        
        # Get value from register, remove lowest 4 bits and mask off 2 highest bits
        val = self.bus.read_byte_data(0x18,self.REG_CTRL4)
        val = (val >> 4)  
        val &= 0b0011  

        if val == self.RANGE_2G:   return self.RANGE_2G
        elif val == self.RANGE_4G: return self.RANGE_4G
        elif val == self.RANGE_8G: return self.RANGE_8G
        else:                      return self.RANGE_16G

    def setRange(self, g_range):
        """Set the range of the sensor (2G, 4G, 8G, 16G)"""
        
        if g_range < 0 or g_range > 3:
            raise Exception("Tried to set invalid range")

        # Get value from register, mask off lowest 4 bits and write back to reg
        val = self.bus.read_byte_data(0x18,self.REG_CTRL4)  
        val &= ~(0b110000)  
        val |= (g_range << 4) 
        self.writeRegister(self.REG_CTRL4, val)  

    def setAxisStatus(self, axis, enable):
        """Enable or disable an individual axis, read status from CTRL_REG1, then write back with appropriate status bit"""
        
        if axis < 0 or axis > 2:
            raise Exception("Tried to modify invalid axis")

        current = self.bus.read_byte_data(0x18,self.REG_CTRL1)
        status = 1 if enable else 0
        final = self.setBit(current, axis, status)
        self.writeRegister(self.REG_CTRL1, final)

    def setDataRate(self, dataRate):
        
        val = self.bus.read_byte_data(0x18,self.REG_CTRL1) 
        val &= 0b1111
        val |= (dataRate << 4)  
        self.writeRegister(self.REG_CTRL1, val)  

    def setHighResolution(self, highRes=True):
        
        val = self.bus.read_byte_data(0x18,self.REG_CTRL4)  
        status = 1 if highRes else 0
        final = self.setBit(val, 3, status)
        self.writeRegister(self.REG_CTRL4, final)


    def setBDU(self, bdu=True):
        """Set block data update"""
        
        val = self.bus.read_byte_data(0x18,self.REG_CTRL4)  
        status = 1 if bdu else 0

        # Block data update is bit 8 of REG_CTRL4
        final = self.setBit(val, 7, status)
        self.writeRegister(self.REG_CTRL4, final)

    def writeRegister(self, register, value):
        
        self.debug("WRT {} to register 0x{:x}".format(
            bin(value), register))
        self.bus.write_byte_data(0x18,register, value)

    def setBit(self, input, bit, value):
        """Set the bit at index 'bit' to 'value' on 'input' and return"""
        mask = 1 << bit
        input &= ~mask
        if value:
            input |= mask
        return input

    def twosComp(self, x):
        
        if (0x8000 & x):
            x = - (0x010000 - x)
        return x

    def debug(self, message):
        
        if not self.isDebug:
            return
        print(message)