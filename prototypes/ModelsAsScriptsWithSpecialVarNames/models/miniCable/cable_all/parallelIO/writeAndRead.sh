rm "./datafile.contig"
#mpirun -n 4 ./parallel_write_test.py
cd src
make
cd ..
mpirun -n 4 ./src/parallel_write_test

mpirun -n 4 ./parallel_read_test.py
