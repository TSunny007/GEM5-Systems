from m5.objects import Cache
# This BaseCache will serve as the framework for our chache structure
# Underneath the hood, these python abstractions will be passed to the C++ implementation of the object

# here we will be extending a BaseCache object provided to us by creating caches with specified parameters
class L1Cache(Cache):
        assoc = 2 # associativity: how many ways each index in "tag" array has
        data_latency = 2 # hit time

        tag_latency = 1 # Tag lookup latency
        data_latency = 1 # Data access latency
        response_latency = 0 # Latency for the rturn path on a miss

        mshrs = 4 # number of MSHRS (max outstanfing requests)
        tgts_per_mshr = 20 # numbers of accesses per MSHR
        # This is to connect to a CPU: Objects extending L1 cache have to adhere to this
        def connectCPU(self, cpu):
                raise NotImplementedError
        # This is to connect the CPU to connect the cache to a bus
        def connectBus(self, bus):
                self.mem_side = bus.slave
# extensions of L1 cache: i and d cache
class L1ICache(L1Cache):
        size = '16kB'

        def connectCPU(self, icache_port):
                self.cpu_side = icache_port

class L1DCache(L1Cache):
        size = '64kB'

        def connectCPU(self, dcache_port):
                self.cpu_side = dcache_port

# Now we create an L2 cache with reasonable attributes
class L2Cache(Cache):
        size = '256kB' # We would naturally expect larger size than L1 cache
        assoc = 8 # 8-ways

        tag_latency = 5 # Naturally take longer to 'hit' than L1
        data_latency = 10
        response_latency = 0

        mshrs = 20
        tgts_per_mshr = 12 # Max number of acceses per MSHR

        def connectCPUSideBus(self, bus):
                """"Connect this cache to a cpu-side bus"""
                self.cpu_side = bus.master

        def connectMemSideBus(self, bus):
                """"Connect this cache to a memory-side bus"""
                self.mem_side = bus.slave

# Now we create an L3 cache with reasonable attributes
class L3Cache(Cache):
        size = '1024kB' # Much bigger than L2
        assoc = 16 #16-ways

	tag_latency = 15 # Tag lookup latency
        data_latency = 20 # Latency for the return path on a miss
        response_latency = 0

        mshrs= 60
        tgts_per_mshr = 16 # Max number of access per MSHR

        def connectCPUSideBus(self, bus):
                """Connect this cache to a cpu-side bus"""
                self.cpu_side = bus.master
        def connectMemSideBus(self, bus):
                """Connect this cache to a memory-side bus"""
                self.mem_side = bus.slave
