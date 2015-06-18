# Introduction #

A quick-guide for the tool will be described below.

This project implements a humble RS232-ELM327 device simulator based on OBD (On Board Diagnostics) protocol, useful to check code developments without having to afford an expensive physical Electronic Control Unit.

For further information about what we are working on currently, check [karmind.com](http://www.karmind.com).

# Details #

Let´s do it work step by step.

**_Build a virtual COM port pair_**
  * Firstly, let´s get started with building a virtual COM port pair. Get com0com [here](http://sourceforge.net/projects/com0com/).
  * Configure a virtual COM port pair so that you can connect your code development in one side of the virtual link, and this RS232-OBD-SIM in the other. For example, link virtual COM ports CNCA0 and CNCB0.

**_SVN checkout_**
  * Perform a checkout from the SVN in Downloads tab, and install it.

**_Execute rs232-obd-sim_**
  * Run the simulator (COM port according to the previous COM configuration):
> > > python rs232-obd-sim.py //./CNCB0

**_Run your own code_**
  * Run your development code to be tested, and that´s it. You should get answers from the sim for the most common PIDs.
  * Type help in the simulator to modify some parameters.

Any doubt, improvement or bug to report, let us know, please, hereby or at [karmind.com](http://www.karmind.com).

Good day!