OMP_NUM_THREADS ?= 17

CPPSEQ = g++ -Wall -pg -fno-omit-frame-pointer -Ofast -march=native
SRCS = main.cpp fluid_solver.cpp EventManager.cpp
CPPCUDA = nvcc -O2 -std=c++11 -arch=sm_35 -Wno-deprecated-gpu-targets --restrict --use_fast_math -Xptxas -O3 -Xcompiler -Ofast,-funroll-loops,-funsafe-math-optimizations
SRCSCUDA = main.cu fluid_solver.cu EventManager.cpp

all: phase3

phase3:
	$(CPPSEQ) $(SRCS) -o fluid_sim_seq
	$(CPPCUDA) $(SRCSCUDA) -o fluid_sim

Makefile:
	$(CPPSEQ) $(SRCS) -o fluid_sim_seq
	$(CPPCUDA) $(SRCSCUDA) -o fluid_sim

cuda:
	$(CPPCUDA) $(SRCSCUDA) -o fluid_sim_cuda

clean:
	@echo Cleaning up...
	@rm -f fluid_sim fluid_sim_seq fluid_sim_cuda
	@echo Done.

runseq:
	sbatch run3.sh

run:
	sbatch run.sh

prof:
	sbatch run2.sh
