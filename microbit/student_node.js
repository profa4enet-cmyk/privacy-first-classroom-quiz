/**
 * BBC micro:bit Student Node (MakeCode JavaScript / TypeScript)
 * Change "ID05" and display string "5" for each student board (ID01 - ID05).
 */

// Button A pressed (Answer: YES / A)
input.onButtonPressed(Button.A, function () {
    // Send student identifier and answer on Radio Group 2
    radio.sendString("ID05_ANS:A")
    // Visual confirmation on the student's LED matrix
    basic.showIcon(IconNames.Yes)
    basic.pause(600)
    // Return to displaying the device ID number
    basic.showString("5")
})

// Button B pressed (Answer: NO / B)
input.onButtonPressed(Button.B, function () {
    // Send student identifier and answer on Radio Group 2
    radio.sendString("ID05_ANS:B")
    // Visual confirmation on the student's LED matrix
    basic.showIcon(IconNames.No)
    basic.pause(600)
    // Return to displaying the device ID number
    basic.showString("5")
})

// Set dedicated quiz radio group
radio.setGroup(2)

// Initial device ID display on startup
basic.showString("5")
