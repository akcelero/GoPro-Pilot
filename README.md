# GoPro-Pilot
Open source pilot for gopro hero 4 based on unofficial http api.

# ---> PROJECT HAS BUG <---<br />READ IT BEFORE START

Bug is in eagle project in schematic. There is no connection between pin CH_PD and Vcc!
You need to put small wire to connect these two pins.

## Prepare board

TODO: describe how to prepare own PCB board

## Instalation

1. Put micropython into ESP<br />
`# esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 LATEST_MICROPYTHON.bin`
2. Put credentials and main program<br />
`# ampy --port /dev/ttyUSB0 put main.py /main.py`<br />
`# ampy --port /dev/ttyUSB0 put credentials.config /credentials.config`
3. If pilot does not work, pls check debug output<br />
`# screen /dev/ttyUSB0 115200`

## Sources:

1. List of instructions in api (congrats for this project)<br />
https://github.com/KonradIT/goprowifihack/blob/master/HERO4/WifiCommands.md
2. Micropython<br />
http://micropython.org/download#esp8266
3. Tutorial for micropython in ESP8266<br />
https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html

## License
Apache License 2.0v
