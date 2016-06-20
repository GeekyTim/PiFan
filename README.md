# PiFan
Under desk Pi controlled fans to keep my NASs and Network Switch cool.

## Objective
Desk space in my study is at a premium, and I also wanted to put noisy (spinning disk) items out of the way to keep the noise down. I bought a glass stand that fitted under the desk in the corner of the room (desk is full width) and have put all my spinnies and my new network swicth under there. One small problem, though, is that there is little or no air circulation around the equipment so it gets a little warmer than I would like.

## Solution(s)
My solution was to install a small (10cm) USB desk fan.  I didn't want it running all the time as it would not be necessary, so I decided to use one of my Pi Zeros (https://www.raspberrypi.org/products/pi-zero/), a Slice of Relay (No longer available - http://cpc.farnell.com/wirelessthings/pirelay/slice-of-relay-relay-board-for/dp/SC13292) and a Dalas 18B20 1-wire thermometer (from the CamJam EduKit 2 - https://thepihut.com/collections/camjam-edukit/products/camjam-edukit-2-sensors) to control the fan.

Mk 1 worked well. The power for the fan was supplied from the 5v rail of the Pi. But due to the space under the desk, I was only able to cool one of the shelves at a time. The small fan kept the switch nice and cool, or it could keep the QNAP NAS nice and cool, or the WD MyBook nice and cool, but not all at the same time.  I therefore needed something more.  First thought was to get another USB fan and have one pointing to one shelf, and the other to the other. However, the fans are not the msot compact, and keeping them in place was difficult.

So along came Mk 2. Instead of using USB fans I would use a few of the old 80mm PC case fans instead. I had about a dozen of them in the garage from my old PC building days. There were a couple of problems that had to be overcome first, though.
1. The fans were 12v, not 5v, so the same power supply could not be used for both the Pi and the fans. I would need a second supply.
2. How would I fix them to the glass shelves? Easy - I have a 3D printer (hence space issues on the desk!) to build mounts for them.

So, using the knowledge gained from building Mk 1 I went around building Mk 2.

The fan mounts were partially a customised form of someone elses design on Thingiverse (http://www.thingiverse.com/thing:204007) and partially my own design (https://tinkercad.com/things/habAKhs4W3C). A 25mm M2.5 bolt holds them together an an adjustable angle.

The circuit was quickly drawn up in Fritzing.  A second thermometer was added so the fans could be controlled independantly for each shelf.

I reused the Mk 1 protoboard (although the soldering was terrible as I was using a brand new soldering iron and lead-free solder for the first time, but the board had enough space to fit the new circuit in.

The second thermometer was connected parallel to the first one. Being 1-wire each thermometer will have its own address, so you can use two or more in parallel easily.

Common power and ground rails were added for the 12v fans; the +12v was connected to the fan, and the ground connected to the fans via the relays.

## Software
The software was pretty simple, starting from the code that I had written for the CamJam EduKits to monitor the temperature. My checking the thermometer temperature every X seconds (I chose 10, which is more than frequent enough!) I was able to switch the relays when the temperature of the thermometers got about 25 degrees C. Switching the relay is as simple as taking the GPIO for that relay high or low.

## Preparing the SD Card
As the Pi would not be used for anythign else, decided to go minimal and installed Raspbian Jessie Lite onto a 2GB microSD card. I wanted to use Python 3 for no other reason than knowing this is the latest version. I therefore had to install python 3 onto the card as it does not come as standard on Lite to save space. I also followed my own EduKit instructions for setting up the 1-Wire interface. The final part was to start the python program on reboot as I would be running the Pi headerless and without a network interface. For that, I created a systemd service as described by the Raspberry Pi Spy (http://www.raspberrypi-spy.co.uk/2015/10/how-to-autorun-a-python-script-on-boot-using-systemd/). Remember that Jessie uses systemd for the boot sequence, not the old init.d.
