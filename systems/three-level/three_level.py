# the m5 (gem5) library was created when gem5 was built
import m5
# import all of the SimObjects
from m5.objects import *
# import the caches which we made
from caches import *

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

# Adding our caches to this system
system.cpu.icache = L1ICache()
system.cpu.dcache = L1DCache()

# connecting the caches to our CPU ports
system.cpu.icache.connectCPU(system.cpu.icache_port)
system.cpu.dcache.connectCPU(system.cpu.dcache_port)

# We can't directly connect the L1 caches to the L2 cache since the L2 cache only expects a single port to connect to it.
# Therefore, we need to create an L2 bus toconnect out L1 caches to the L2 cache. Then we can use our helper function to connect the L1 caches to the L2 bus.
system.l2bus = L2XBar()
system.l3bus = L2XBar()

# Hook up the CPU ports up to the l2bus
system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)

# create our l2 cache and connect it to the L2 bus
system.l2cache = L2Cache()
system.l2cache.connectCPUSideBus(system.l2bus)

# create out l3 cache and connect it to the L3 bus and the memory bus
system.l3cache = L3Cache()
system.l3cache.connectCPUSideBus(system.l3bus)

# Create a memory bus
system.membus = SystemXBar()

# Connect the L2 cache to l3bus
system.l2cache.connectMemSideBus(system.l3bus)
# Connect the L3 cache to the membus
system.l3cache.connectMemSideBus(system.membus)

# create the interrupt controller for the CPU and connect to the membus
# Note: these directly connected to the memory bus and are not cached
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.master
system.cpu.interrupts[0].int_master = system.membus.slave
system.cpu.interrupts[0].int_slave = system.membus.master

# Connect the system to the membus
system.system_port = system.membus.slave

# Connectiong the memory controller to the membus. We'll use a DDR3 controller
system.mem_ctrl = DDR3_1600_8x8()
system.mem_ctrl.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.master

# Now we set up the process we want the CPU to execute. we will be executing in syscall emulation mode.
# we have to create the process, then set the processes command to the command we want to run. 
process = Process()
process.cmd = ['programs/c/a.out']
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
