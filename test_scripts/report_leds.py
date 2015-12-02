import mraa

leds = [[35,'GP131 - battery red'],[26,'GP130 - battery green'],[25,'GP129 - battery blue'],[31,'GP44 - server red'],[45,'GP45 - server green'],[32,'GP46 - server blue']]

for led in leds:
	pin = mraa.Gpio(led[0])
	print led[1] + ': ' + str(pin.read())
