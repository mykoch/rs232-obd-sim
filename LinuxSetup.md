This is a recipe to setup rs232-obd-sim.py on Linux.

## Prerequisites ##

It uses [virtualenv](http://www.virtualenv.org) to install an specific environment for the simulator.

```
$ sudo apt-get install python-virtualenv
```

It needs [socat](http://www.dest-unreach.org/socat/doc/socat.html) to establish a kind of null model between 2 pseudo terminals.

```
$ sudo apt-get install socat
```

## Set up ##

1. Create a folder to install rs232-obd-sim and python virtual environment.

```
$ cd ~
$ mkdir karmind-simulator
$ cd karmind-simulator
```

2. Create a virtual environment and install pyserial

```
$ virtualenv env
$ source env/bin/activate
(env) $ pip install pyserial
```

3. Download simulator source code and run

```
(env) $ svn checkout http://rs232-obd-sim.googlecode.com/svn/trunk/ rs232-obd-sim-read-only
(env) $ cd rs232-obd-sim-read-only
```


4. The _magic_ is to use **socat** to create a virtual port (kind of null modem) to connect the OBD application.

From other terminal:

```
$ socat -v -x -d -d PTY: PTY:
2010/11/01 00:00:01 socat[7561] N PTY is /dev/pts/5
2010/11/01 00:00:01 socat[7561] N PTY is /dev/pts/6
2010/11/01 00:00:01 socat[7561] N starting data transfer loop with FDs [3,3] and [5,5]
```

Return to your original terminal and launch the simulator:

```
(env) $ python rs232-obd-sim.py /dev/pts/5
```


Now you can connect your OBD application (for example [Karmind OBD app](http://code.google.com/p/karmind-obd-application/)) to port /dev/pts/6.