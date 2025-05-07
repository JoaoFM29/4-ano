#include<stdio.h>
#include<stdlib.h>

#ifndef size
#define size 512
#endif

double *A, *B, *C;

// Complexidade de ordem 1 (tempo fisico)
void alloc() {
    A = (double *) malloc(size*size*sizeof(double));
    B = (double *) malloc(size*size*sizeof(double));
    C = (double *) malloc(size*size*sizeof(double));
}

// Complexidade de ordem N^2
void init() {
    for(int i=0; i<size; i++) {
        for(int j=0; j<size; j++) {
            A[i*size+j] = rand();
            B[i*size+j] = rand();
            C[i*size+j] = 0;
        }
    }
}

// Complexidade de ordem N^3 (aumentando para 2N o algoritmo aumenta 8x o tempo de execução)
void mmult() {
    for(int i=0; i<size; i++) {
        for(int j=0; j<size; j++) {
            for(int k=0; k<size; k++) {
                C[i*size+j] += A[i*size+k] * B[k*size+j];
            }
        }
    }
}

int main() {
    alloc();
    init();
    mmult();

    printf("%f\n", C[size/2+5]);
}
