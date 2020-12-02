./build/ARM/gem5.opt -d zeusmp configs/spec2k6/run.py -b zeusmp --maxinsts=500000 --cpu-type=DerivO3CPU --caches --l2cache --l1d_assoc=2 --l1i_assoc=2 --l2_assoc=8 --l1d_size=32kB --l1i_size=32kB --l2_size=2MB

./build/ARM/gem5.opt -d test_run/zeusmp configs/spec2k6/run.py -b zeusmp\
 --maxinsts=500000 --cpu-type=DerivO3CPU --caches --l2cache --l1d_assoc=2 --l1i_assoc=2 --l2_assoc=8\
 --l1d_size=64kB --l1i_size=64kB --l2_size=4MB


 dealII
 gamess
 gromacs
 perlbench
 soplex
 specrand_f
 specrand_i
 sphinx3
 tonto
 zeusmp