CPP = g++ -Wall -O3 -march=native -funroll-loops -ffast-math -flto
SRCS = main.cpp fluid_solver.cpp EventManager.cpp

all:
	$(CPP) $(SRCS) -o fluid_sim

asm:
	$(CPP) -fverbose-asm -masm=intel -S $(SRCS)

clean:
	@echo Cleaning up...
	@rm fluid_sim
	@rm gmon.out
	@echo Done.
