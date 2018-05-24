import m5
from m5.objects import *
# import these libraries which we've already compiled.
# to create a system SimObject, we simply instantiate it like a normal python class:
system = System()
# This is where we can set the clock on the system. We don't care about the system power right now, so we can 
# just use the default options for the voltage.
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()
# Let's also set up how memory will be simulated. We will use the timing mode for the memory simulation
system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('8192MB')]
# Create a CPU. 
system.cpu = TimingSimpleCPU()
# System wide memory bus
system.membus = SystemXBar()
# This system doesn't have any cache, so we will directly connect the cache ports to the membus.
system.cpu.icache_port = system.membus.slave
system.cpu.dcache_port = system.membus.slave
# These port connections will make sure that our system will function correctly.
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.master
system.cpu.interrupts[0].int_master = system.membus.slave
system.cpu.interrupts[0].int_slave = system.membus.master

system.system_port = system.membus.slave
# Connectiong the memory controller to the membus. We'll use a simple DDR3 controller
system.mem_ctrl = DDR3_1600_8x8()
system.mem_ctrl.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.master

# Now we set up the process we want hte CPU to execute. we will be executing in syscall emulation mode.
# we have to create the process, then set the processes commang to the command we want to run. 
process = Process()
process.cmd = ['tests/test-progs/hello/bin/x86/linux/hello']
system.cpu.workload = process
system.cpu.createThreads()
# Instantiation goes through all the SimObjects we've created in python and creates the c++ equivalents.
root = Root(full_system = False, system = system)
m5.instantiate()
# Now we can kick off the simulation
print('Beginning simulation!')
exit_event = m5.simulate()
# Once this simulation finishes, we can inspect the state of the system
print('Exiting @ tick {} because {}'
      .format(m5.curTick(), exit_event.getCause()))
# Parameters in this configuration file can be changed and the results should be different.
# For instance, if you double the system clock, the simulation should finish faster. 
# If you change the DDR controller to DDR4, the performance should be better
# If you change the model to MinorCPU, it would model an in-order CPU, Deriv03CPU to model an out-of-order CPU
