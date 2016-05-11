
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

#https://twistedmatrix.com/pipermail/twisted-python/2013-October/027579.html
from twisted.internet import reactor, protocol
from twisted.protocols.basic import LineReceiver
from twisted.internet.serialport import SerialPort



class Echo(LineReceiver):
    def dataReceived(self, data):
        print('data recv: %s' % (data))

    def lineReceived(self, line):
        print('recv: %s' % (line))



def main():
    factory = protocol.ServerFactory()
    factory.protocol = Echo
    s = SerialPort(Echo(), 
            '/dev/serial/by-id/usb-FTDI_FT231X_USB_UART_DN01A79Z-if00-port0',
            reactor, 
            baudrate=9600)

    reactor.run()

if __name__ == '__main__':
    main()
