OMP_NUM_THREADS ?= 17

CPP = g++ -Wall -pg -fopenmp -fno-omit-frame-pointer -Ofast -march=native
CPPSEQ = g++ -Wall -pg -fno-omit-frame-pointer -Ofast -march=native
SRCS = main.cpp fluid_solver.cpp EventManager.cpp

all: phase2

phase2:
	$(CPP) $(SRCS) -o fluid_sim
	$(CPPSEQ) $(SRCS) -o fluid_sim_seq

clean:
	@echo Cleaning up...
	@rm -f fluid_sim fluid_sim_seq
	@echo Done.

runseq:
	OMP_NUM_THREADS=1 ./fluid_sim_seq

runpar:
	OMP_NUM_THREADS=$(OMP_NUM_THREADS) ./fluid_sim
