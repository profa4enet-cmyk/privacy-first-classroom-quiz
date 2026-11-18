/**
 * BBC micro:bit Receiver Gateway (MakeCode JavaScript / TypeScript)
 * Listens on Radio Group 2 and forwards incoming student answers over USB Serial (115200 baud).
 */
radio.onReceivedString(function (receivedString) {
    // Forward the received radio packet directly to the USB serial port
    serial.writeLine(receivedString)
    // Visual confirmation of packet reception on the center LED
    led.toggle(2, 2)
})

// Dedicated radio group for classroom quiz / student voting
radio.setGroup(2)

// Standard serial communication over USB (115200 baud)
serial.redirectToUSB()

// Indicate that the Gateway is ready ('G')
basic.showString("G")
