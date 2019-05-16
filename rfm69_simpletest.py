# Simple example to send a message and then wait indefinitely for messages
# to be received.  This uses the default RadioHead compatible GFSK_Rb250_Fd250
# modulation and packet format for the radio.
# Author: Tony DiCola
import board
import busio
import digitalio
import time
import adafruit_rfm69


# Define radio parameters.
RADIO_FREQ_MHZ = 433.0  # Frequency of the radio in Mhz. Must match your
                        # module! Can be a value like 915.0, 433.0, etc.

# Define pins connected to the chip, use these if wiring up the breakout according to the guide:
CS = digitalio.DigitalInOut(board.D7)
RESET = digitalio.DigitalInOut(board.D5)
# Or uncomment and instead use these if using a Feather M0 RFM69 board
# and the appropriate CircuitPython build:
#CS = digitalio.DigitalInOut(board.RFM69_CS)
#RESET = digitalio.DigitalInOut(board.RFM69_RST)

# Define the onboard LED
LED = digitalio.DigitalInOut(board.D13)
LED.direction = digitalio.Direction.OUTPUT
LED.value = True

# Initialize SPI bus.
print("Init spi")
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Initialze RFM radio
print("Init rfm")
rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, 433.0)
print("Rfm initiated")
LED.value = False

# Optionally set an encryption key (16 byte AES key). MUST match both
# on the transmitter and receiver (or be set to None to disable/the default).
rfm69.encryption_key = b'\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08'
print("Encription initiated")
# Print out some chip state:
# Send a packet.  Note you can only send a packet up to 60 bytes in length.
# This is a limitation of the radio packet size, so if you need to send larger
# amounts of data you will need to break it into smaller send calls.  Each send
# call will wait for the previous one to finish before continuing.
print('Temperature: {0}C'.format(rfm69.temperature))
print('Frequency: {0}mhz'.format(rfm69.frequency_mhz))
print('Bit rate: {0}kbit/s'.format(rfm69.bitrate/1000))
print('Frequency deviation: {0}hz'.format(rfm69.frequency_deviation))

while False:
	LED.value = True
	rfm69.send(bytes('Hello world!\r\n',"utf-8"))
	LED.value = False
	print('Sent hello world message!')
	time.sleep(0.1)

# Wait to receive packets.  Note that this library can't receive data at a fast
# rate, in fact it can only receive and process one 60 byte packet at a time.
# This means you should only use this for low bandwidth scenarios, like sending
# and receiving a single message at a time.
print('Waiting for packets...')
while True:
    packet = rfm69.receive(timeout=2.0)
    print("Command executed")
    # Optionally change the receive timeout from its default of 0.5 seconds:
    #packet = rfm69.receive(timeout=5.0)
    # If no packet was received during the timeout then None is returned.
    if packet is None:
        # Packet has not been received
        LED.value = False
        print('Received nothing! Listening again...')
    else:
        LED.value = True
        # Received a packet!
        # Print out the raw bytes of the packet:
        print('Received (raw bytes): {0}'.format(packet))
        # And decode to ASCII text and print it too.  Note that you always
        # receive raw bytes and need to convert to a text format like ASCII
        # if you intend to do string processing on your data.  Make sure the
        # sending side is sending ASCII data before you try to decode!
        packet_text = str(packet, 'ascii')
        print('Received (ASCII): {0}'.format(packet_text))
