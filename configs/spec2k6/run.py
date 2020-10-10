# Copyright (c) 2020 Purdue University
# All rights reserved.
#
# Redistribution and use in source and binary forms, with o without
# modification, are permitted provided that the following coditions are
# met: redistributions of source code must retain the above cpyright
# notice, this list of conditions and the following disclaimer
# redistributions in binary form must reproduce the above copyrght
# notice, this list of conditions and the following disclaimer i the
# documentation and/or other materials provided with the distribuion;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived fom
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors: Malek Musleh, modified by Tim Rogers to work with gem5 20.x
### The following file was referenced from the following site:
### http://www.m5sim.org/SPEC_CPU2006_benchmarks
###
### and subsequent changes were made

from __future__ import print_function
from __future__ import absolute_import


# import the m5 (gem5) library created when gem5 is built
import m5
# import all of the SimObjects
from m5.objects import *

m5.util.addToPath('../')

from common import Options
import optparse
import spec2k6


# Get paths we might need.  It's expected this file is in m5/configs/example.
config_path = os.path.dirname(os.path.abspath(__file__))
print(config_path)
config_root = os.path.dirname(config_path)
print(config_root)
m5_root = os.path.dirname(config_root)
print(m5_root)

parser = optparse.OptionParser()
Options.addCommonOptions(parser)
Options.addSEOptions(parser)

# Benchmark options

parser.add_option("-b", "--benchmark", default="",
                 help="The benchmark to be loaded.")


(options, args) = parser.parse_args()

if args:
    print("Error: script doesn't take any positional arguments")
    sys.exit(1)

if options.benchmark == 'perlbench':
   process = spec2k6.perlbench
elif options.benchmark == 'bzip2':
   process = spec2k6.bzip2
elif options.benchmark == 'gcc':
   process = spec2k6.gcc
elif options.benchmark == 'bwaves':
   process = spec2k6.bwaves
elif options.benchmark == 'gamess':
   process = spec2k6.gamess
elif options.benchmark == 'mcf':
   process = spec2k6.mcf
elif options.benchmark == 'milc':
   process = spec2k6.milc
elif options.benchmark == 'zeusmp':
   process = spec2k6.zeusmp
elif options.benchmark == 'gromacs':
   process = spec2k6.gromacs
elif options.benchmark == 'cactusADM':
   process = spec2k6.cactusADM
elif options.benchmark == 'leslie3d':
   process = spec2k6.leslie3d
elif options.benchmark == 'namd':
   process = spec2k6.namd
elif options.benchmark == 'gobmk':
   process = spec2k6.gobmk;
elif options.benchmark == 'dealII':
   process = spec2k6.dealII
elif options.benchmark == 'soplex':
   process = spec2k6.soplex
elif options.benchmark == 'povray':
   process = spec2k6.povray
elif options.benchmark == 'calculix':
   process = spec2k6.calculix
elif options.benchmark == 'hmmer':
   process = spec2k6.hmmer
elif options.benchmark == 'sjeng':
   process = spec2k6.sjeng
elif options.benchmark == 'GemsFDTD':
   process = spec2k6.GemsFDTD
elif options.benchmark == 'libquantum':
   process = spec2k6.libquantum
elif options.benchmark == 'h264ref':
   process = spec2k6.h264ref
elif options.benchmark == 'tonto':
   process = spec2k6.tonto
elif options.benchmark == 'lbm':
   process = spec2k6.lbm
elif options.benchmark == 'omnetpp':
   process = spec2k6.omnetpp
elif options.benchmark == 'astar':
   process = spec2k6.astar
elif options.benchmark == 'wrf':
   process = spec2k6.wrf
elif options.benchmark == 'sphinx3':
   process = spec2k6.sphinx3
elif options.benchmark == 'xalancbmk':
   process = spec2k6.xalancbmk
elif options.benchmark == 'specrand_i':
   process = spec2k6.specrand_i
elif options.benchmark == 'specrand_f':
   process = spec2k6.specrand_f

# import the m5 (gem5) library created when gem5 is built
import m5
# import all of the SimObjects
from m5.objects import *

# create the system we are going to simulate
system = System()

# Set the clock fequency of the system (and all of its children)
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

# Set up the system
system.mem_mode = 'timing'               # Use timing accesses
system.mem_ranges = [AddrRange('512MB')] # Create an address range

# Create a simple CPU
system.cpu = TimingSimpleCPU()

# Create a memory bus, a system crossbar, in this case
system.membus = SystemXBar()

# Hook the CPU ports up to the membus
system.cpu.icache_port = system.membus.slave
system.cpu.dcache_port = system.membus.slave

# create the interrupt controller for the CPU and connect to the membus
system.cpu.createInterruptController()

print(m5.defines.buildEnv)
print(m5.defines.buildEnv['TARGET_ISA'])

# For x86 only, make sure the interrupts are connected to the memory
# Note: these are directly connected to the memory bus and are not cached
if m5.defines.buildEnv['TARGET_ISA'] == "x86":
    system.cpu.interrupts[0].pio = system.membus.master
    system.cpu.interrupts[0].int_master = system.membus.slave
    system.cpu.interrupts[0].int_slave = system.membus.master

# Set the cpu to use the process as its workload and create thread contexts
system.cpu.workload = process
system.cpu.createThreads()

# Create a DDR3 memory controller and connect it to the membus
system.mem_ctrl = DDR3_1600_8x8()
system.mem_ctrl.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.master

# Connect the system up to the membus
system.system_port = system.membus.slave

# set up the root SimObject and start the simulation
root = Root(full_system = False, system = system)
# instantiate all of the objects we've created above
m5.instantiate()

print("Beginning simulation!")
exit_event = m5.simulate()
print('Exiting @ tick %i because %s' % (m5.curTick(), exit_event.getCause()))
