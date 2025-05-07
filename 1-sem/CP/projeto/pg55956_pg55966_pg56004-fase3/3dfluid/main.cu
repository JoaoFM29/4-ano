#include "EventManager.h"
#include "fluid_solver.h"
#include <iostream>
#include <vector>

#define SIZE 168

#define IX(i, j, k) ((i) + (M + 2) * (j) + (M + 2) * (N + 2) * (k))

// Globals for the grid size
static int M = SIZE;
static int N = SIZE;
static int O = SIZE;
static float dt = 0.1f;      // Time delta
static float diff = 0.0001f; // Diffusion constant
static float visc = 0.0001f; // Viscosity constant

// Fluid simulation arrays
static float *dens;

// Fluid simulation on cuda

static float *d_u, *d_v, *d_w, *d_u_prev, *d_v_prev, *d_w_prev;
static float *d_dens, *d_dens_prev;

// Function to allocate simulation data
int allocate_data() {
  int size = (M + 2) * (N + 2) * (O + 2);
  dens = new float[size];
  cudaMalloc((void **)&d_u, size * sizeof(float));
  cudaMalloc((void **)&d_v, size * sizeof(float));
  cudaMalloc((void **)&d_w, size * sizeof(float));
  cudaMalloc((void **)&d_u_prev, size * sizeof(float));
  cudaMalloc((void **)&d_v_prev, size * sizeof(float));
  cudaMalloc((void **)&d_w_prev, size * sizeof(float));
  cudaMalloc((void **)&d_dens, size * sizeof(float));
  cudaMalloc((void **)&d_dens_prev, size * sizeof(float));
  
  cudaError_t err = cudaGetLastError();
  if (err != cudaSuccess) {
      printf("CUDA Error after Malloc: %s\n", cudaGetErrorString(err));
      return 0;
  }

  if (!dens) {
    std::cerr << "Cannot allocate memory" << std::endl;
    return 0;
  }
  return 1;
}

// Function to clear the data (set all to zero)
void clear_data() {
  int size = (M + 2) * (N + 2) * (O + 2);

  cudaMemset(d_dens, 0, size);
  cudaMemset(d_dens_prev, 0, size);
  cudaMemset(d_u, 0, size);
  cudaMemset(d_v, 0, size);
  cudaMemset(d_w, 0, size);
  cudaMemset(d_u_prev, 0, size);
  cudaMemset(d_v_prev, 0, size);
  cudaMemset(d_w_prev, 0, size);

}

// Free allocated memory
void free_data() {

  delete[] dens;
  cudaFree(d_u);
  cudaFree(d_v);
  cudaFree(d_w);
  cudaFree(d_u_prev);
  cudaFree(d_v_prev);
  cudaFree(d_w_prev);
  cudaFree(d_dens);
  cudaFree(d_dens_prev);
}


__global__
void apply_events_kernel(int M,int N,int O,float *u,float *v,float *w,float *dens,Event event){


  int i = M / 2, j = N / 2, k = O / 2; // Assume all events affect the center
    int idx = IX(i, j, k);

        if (event.type == ADD_SOURCE) {
            // Add density source
            dens[idx] = event.density;
        } else if (event.type == APPLY_FORCE) {
            // Apply force vector
            u[idx] = event.force.x;
            v[idx] = event.force.y;
            w[idx] = event.force.z;
        }
    

}
// Apply events (source or force) for the current timestep
void apply_events(const std::vector<Event> &events) {


  for (const auto &event : events) {
    dim3 threadsPerBlock(32);
    dim3 numBlocks(1); 
    apply_events_kernel<<<numBlocks, threadsPerBlock>>>(M,N,O,d_u, d_v, d_w, d_dens, event);
  }

}

/*
__global__ void sum_density_kernel(float* d_dens, float* d_partial_sums, int size) {
    extern __shared__ float sdata[];

    int tid = threadIdx.x + blockIdx.x * blockDim.x;
    int local_tid = threadIdx.x;

    // Load data into shared memory
    sdata[local_tid] = (tid < size) ? d_dens[tid] : 0.0f;
    __syncthreads();

    // Perform reduction within the block
    for (int stride = blockDim.x / 2; stride > 0; stride /= 2) {
        if (local_tid < stride) {
            sdata[local_tid] += sdata[local_tid + stride];
        }
        __syncthreads();
    }

    // Write block's partial sum to global memory
    if (local_tid == 0) {
        d_partial_sums[blockIdx.x] = sdata[0];
    }
}


float sum_density() {
    int size = (M + 2) * (N + 2) * (O + 2);
    int threads_per_block = 256;
    int num_blocks = (size + threads_per_block - 1) / threads_per_block;

    // Allocate memory for partial sums on the GPU
    float* d_partial_sums;
    cudaMalloc(&d_partial_sums, num_blocks * sizeof(float));

    // Launch reduction kernel
    sum_density_kernel<<<num_blocks, threads_per_block, threads_per_block * sizeof(float)>>>(d_dens, d_partial_sums, size);

    // Copy partial sums back to the host
    std::vector<float> partial_sums(num_blocks);
    cudaMemcpy(partial_sums.data(), d_partial_sums, num_blocks * sizeof(float), cudaMemcpyDeviceToHost);

    // Perform final summation on the host
    float total_density = 0.0f;
    for (float partial : partial_sums) {
        total_density += partial;
    }

    // Free GPU memory for partial sums
    cudaFree(d_partial_sums);

    return total_density;
}
*/

float sum_density() {

  float total_density = 0.0f;
  int size = (M + 2) * (N + 2) * (O + 2);
  cudaMemcpy(dens,d_dens, sizeof(float) * size, cudaMemcpyDeviceToHost);
  for (int i = 0; i < size; i++) {
    total_density += dens[i];
  }
  return total_density;
}

// Simulation loop
void simulate(EventManager &eventManager, int timesteps) {
  for (int t = 0; t < timesteps; t++) {
    // Get the events for the current timestep
    std::vector<Event> events = eventManager.get_events_at_timestamp(t);

    // Apply events to the simulation
    apply_events(events);

    // Perform the simulation steps
    vel_step(M, N, O, d_u, d_v, d_w, d_u_prev, d_v_prev, d_w_prev, visc, dt);
    dens_step(M, N, O,d_dens, d_dens_prev, d_u, d_v, d_w, diff, dt);
  }
}

int main() {
  // Initialize EventManager
  EventManager eventManager;
  eventManager.read_events("events.txt");

  // Get the total number of timesteps from the event file
  int timesteps = eventManager.get_total_timesteps();

  // Allocate and clear data
  if (!allocate_data())
    return -1;
  clear_data();

  // Run simulation with events
  simulate(eventManager, timesteps);

  // Print total density at the end of simulation
  float total_density = sum_density();
  std::cout << "Total density after " << timesteps
            << " timesteps: " << total_density << std::endl;

  // Free memory
  free_data();

  return 0;
}