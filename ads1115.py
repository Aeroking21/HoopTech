import time
import smbus2

I2C_DEFAULT_ADDRESS            = 0x48

# Registers and other configuration:
CONVERSION_REGISTER            = 0x00
CONFIG_REGISTER                = 0x01

ADS1115_CONFIG_OS_SINGLE       = 0x8000
ADS1115_CONFIG_MUX_OFFSET      = 12

# Maping of gain values to config register values
ADS1115_CONFIG_GAIN = {
	2/3: 0x0000,
	1:   0x0200,
	2:   0x0400,
	4:   0x0600,
	8:   0x0800,
	16:  0x0A00
}
ADS1115_CONFIG_MODE_CONTINUOUS  = 0x0000
ADS1115_CONFIG_MODE_SINGLE      = 0x0100

# Mapping of data/sample rate to config register values
ADS1115_CONFIG_DR = {

    8:    0x0000,
    16:   0x0020,
    32:   0x0040,
    64:   0x0060,
    128:  0x0080,
    250:  0x00A0,
    475:  0x00C0,
    860:  0x00E0
}

ADS1115_CONFIG_COMP_QUE_DISABLE = 0x0003

	8:    0x0000,
	16:   0x0020,
	32:   0x0040,
	64:   0x0060,
	128:  0x0080,
	250:  0x00A0,
	475:  0x00C0,
	860:  0x00E0
}


ADS1115_CONFIG_COMP_QUE_DISABLE = 0x0003

class ADS1115(object):


    def __init__(self, address=I2C_DEFAULT_ADDRESS, **kwargs):
        self._bus = smbus2.SMBus(1)

    def _data_rate_default(self):
        # Default from datasheet page 28, config register DR bit default.
        return 128

    def _data_rate_config(self, data_rate):
        if data_rate not in ADS1115_CONFIG_DR:
            raise ValueError('Data rate must be one of: 8, 16, 32, 64, 128, 250, 475, 860')
        return ADS1115_CONFIG_DR[data_rate]

    def _conversion_value(self, low, high):
        # Convert to 16-bit signed value.
        value = ((high & 0xFF) << 8) | (low & 0xFF)
        # Check for sign bit and turn into a negative value if set.
        if value & 0x8000 != 0:
            value -= 1 << 16
        return value

    def _read(self, mux, gain, data_rate, mode):
        config = ADS1115_CONFIG_OS_SINGLE  # Go out of power-down mode for conversion.
        # Specify mux value.
        config |= (mux & 0x07) << ADS1115_CONFIG_MUX_OFFSET
        # Validate the passed in gain and then set it in the config.
        if gain not in ADS1115_CONFIG_GAIN:
            raise ValueError('Gain must be one of: 2/3, 1, 2, 4, 8, 16')
        config |= ADS1115_CONFIG_GAIN[gain]
        # Set the mode (continuous or single shot).
        config |= mode
        # Get the default data rate if none is specified (default differs between
        # ADS1015 and ADS1115).
        if data_rate is None:
            data_rate = self._data_rate_default()
        # Set the data rate (this is controlled by the subclass as it differs
        # between ADS1015 and ADS1115).
        config |= self._data_rate_config(data_rate)
        config |= ADS1115_CONFIG_COMP_QUE_DISABLE  # Disble comparator mode.
        # Send the config value to start the ADC conversion.
        # Explicitly break the 16-bit value down to a big endian pair of bytes.

        self._bus.write_i2c_block_data(I2C_DEFAULT_ADDRESS, CONFIG_REGISTER, [(config >> 8) & 0xFF, config & 0xFF])
        # Wait for the ADC sample to finish based on the sample rate plus a
        # small offset to be sure (0.1 millisecond).
        time.sleep(1.0/data_rate+0.0001)
        # Retrieve the result.
        result = self._bus.read_i2c_block_data(I2C_DEFAULT_ADDRESS, CONVERSION_REGISTER, 2)
        return self._conversion_value(result[1], result[0])

    def read_adc(self, channel, gain=1, data_rate=None):
        """Read a single ADC channel and return the ADC value as a signed integer
        result.  Channel must be a value within 0-3.
        """
        assert 0 <= channel <= 3, 'Channel must be a value within 0-3!'
        # Perform a single shot read and set the mux value to the channel plus
        # the highest bit (bit 3) set.
        return self._read(channel + 0x04, gain, data_rate, ADS1115_CONFIG_MODE_SINGLE)

	def __init__(self, address=I2C_DEFAULT_ADDRESS, **kwargs):
		self._bus = smbus2.SMBus(1)

	def _data_rate_default(self):
		return 128

	def _data_rate_config(self, data_rate):
		if data_rate not in ADS1115_CONFIG_DR:
			raise ValueError('Data rate must be one of: 8, 16, 32, 64, 128, 250, 475, 860')
		return ADS1115_CONFIG_DR[data_rate]

	def _conversion_value(self, low, high):
		"""Convert to 16-bit signed value."""
  
		value = ((high & 0xFF) << 8) | (low & 0xFF)
  
		# Check for sign bit and turn into a negative value if set.
		if value & 0x8000 != 0:
			value -= 1 << 16
		return value

	def _read(self, mux, gain, data_rate, mode):
		
		# Go out of power-down mode
		config = ADS1115_CONFIG_OS_SINGLE  
  
		# Specify mux value and set gain
		config |= (mux & 0x07) << ADS1115_CONFIG_MUX_OFFSET
		if gain not in ADS1115_CONFIG_GAIN:
			raise ValueError('Gain must be one of: 2/3, 1, 2, 4, 8, 16')
		config |= ADS1115_CONFIG_GAIN[gain]
  
		# Set the mode 
		config |= mode
  
		# Set data rate
		if data_rate is None:
			data_rate = self._data_rate_default()
		config |= self._data_rate_config(data_rate)
  
		# Disble comparator mode.
		config |= ADS1115_CONFIG_COMP_QUE_DISABLE  
  
		# Send the config value to start the ADC conversion.
		# Explicitly break the 16-bit value down to a big endian pair of bytes.
		self._bus.write_i2c_block_data(I2C_DEFAULT_ADDRESS, CONFIG_REGISTER, [(config >> 8) & 0xFF, config & 0xFF])
  
		# Wait for the ADC sample to finish based on the sample rate plus a
		# small offset to be sure (0.1 millisecond)
		time.sleep(1.0/data_rate+0.0001)
  
		# Retrieve the result
		result = self._bus.read_i2c_block_data(I2C_DEFAULT_ADDRESS, CONVERSION_REGISTER, 2)
		return self._conversion_value(result[1], result[0])

	def read_adc(self, channel, gain=1, data_rate=None):
		"""Read a single ADC channel and return the ADC value as a signed integer
		result.  Channel must be a value within 0-3.
		"""
  
		assert 0 <= channel <= 3, 'Channel must be a value within 0-3!'
  
		# Perform a single shot read and set the mux value to the channel plus
		# the highest bit (bit 3) set.
		return self._read(channel + 0x04, gain, data_rate, ADS1115_CONFIG_MODE_SINGLE)

