#include "fluid_solver.h"
#include <cmath>
#include <iostream>
#include <omp.h>

#define IX(i, j, k) ((i) + (M + 2) * (j) + (M + 2) * (N + 2) * (k))
#define SWAP(x0, x)                                                            \
  {                                                                            \
    float *tmp = x0;                                                           \
    x0 = x;                                                                    \
    x = tmp;                                                                   \
  }
#define MAX(a, b) (((a) > (b)) ? (a) : (b))
#define LINEARSOLVERTIMES 20


__global__ void add_source_kernel(int size, float *x, const float *s, float dt) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < size) {
        x[idx] += dt * s[idx];
    }
}

// Add sources (density or velocity)
void add_source(int M, int N, int O, float *x, const float *s, float dt) {
    int size = ((M + 2) * (N + 2) * (O + 2));

    // Configure kernel launch parameters
    int threadsPerBlock = 256;
    int blocksPerGrid = (( size ) + threadsPerBlock - 1) / threadsPerBlock;

    // Launch the kernel
    add_source_kernel<<<blocksPerGrid, threadsPerBlock>>>(size,x,s, dt);
}

// Kernel for handling the faces of the cube
__global__
void set_bnd_faces_kernel_a(int M, int N, int O, int b, float* x) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x + 1; // Skip boundary (start at 1)
    int idy = blockIdx.y * blockDim.y + threadIdx.y + 1; // Skip boundary (start at 1)

    if (idx <= M && idy <= N) {
        x[IX(idx, idy, 0)] = b == 3 ? -x[IX(idx, idy, 1)] : x[IX(idx, idy, 1)];
        x[IX(idx, idy, O + 1)] = b == 3 ? -x[IX(idx, idy, O)] : x[IX(idx, idy, O)];
    }
}

__global__
void set_bnd_faces_kernel_b(int M, int N, int O, int b, float* x) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x + 1; // Skip boundary (start at 1)
    int idy = blockIdx.y * blockDim.y + threadIdx.y + 1; // Skip boundary (start at 1)

    if (idx <= N && idy <= O) {
        x[IX(0, idx, idy)] = b == 1 ? -x[IX(1, idx, idy)] : x[IX(1, idx, idy)];
        x[IX(M + 1, idx, idy)] = b == 1 ? -x[IX(M, idx, idy)] : x[IX(M, idx, idy)];
    }
}

__global__
void set_bnd_faces_kernel_c(int M, int N, int O, int b, float* x) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x + 1; // Skip boundary (start at 1)
    int idy = blockIdx.y * blockDim.y + threadIdx.y + 1; // Skip boundary (start at 1)

    if (idx <= M && idy <= O) {
        x[IX(idx, 0, idy)] = b == 2 ? -x[IX(idx, 1, idy)] : x[IX(idx, 1, idy)];
        x[IX(idx, N + 1, idy)] = b == 2 ? -x[IX(idx, N, idy)] : x[IX(idx, N, idy)];
    }
}

void launch_set_bnd_faces_kernels(int M, int N, int O, int b, float* d_x) {
    // Define block and grid dimensions for all kernels
    dim3 blockDim(16, 16); // Adjust as necessary based on GPU resources

    dim3 gridDim_a((M + 2+ blockDim.x - 1) / blockDim.x, (N + 2 + blockDim.y - 1) / blockDim.y);
    set_bnd_faces_kernel_a<<<gridDim_a, blockDim>>>(M, N, O, b, d_x);


    dim3 gridDim_b((N + 2 + blockDim.x - 1) / blockDim.x, (O  + 2+ blockDim.y - 1) / blockDim.y);
    set_bnd_faces_kernel_b<<<gridDim_b, blockDim>>>(M, N, O, b, d_x);


    dim3 gridDim_c((M + 2 + blockDim.x - 1) / blockDim.x, (O + 2 + blockDim.y - 1) / blockDim.y);
    set_bnd_faces_kernel_c<<<gridDim_c, blockDim>>>(M, N, O, b, d_x);

}
// Kernel for handling the corners
__global__ void set_bnd_corners_kernel(int M, int N, int O, float* x) {

    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx == 0) {
        x[IX(0, 0, 0)] = 0.33f * (x[IX(1, 0, 0)] + x[IX(0, 1, 0)] + x[IX(0, 0, 1)]);
        x[IX(M + 1, 0, 0)] = 0.33f * (x[IX(M, 0, 0)] + x[IX(M + 1, 1, 0)] + x[IX(M + 1, 0, 1)]);
        x[IX(0, N + 1, 0)] = 0.33f * (x[IX(1, N + 1, 0)] + x[IX(0, N, 0)] + x[IX(0, N + 1, 1)]);
        x[IX(M + 1, N + 1, 0)] = 0.33f * (x[IX(M, N + 1, 0)] + x[IX(M + 1, N, 0)] + x[IX(M + 1, N + 1, 1)]);
    }
}
// Main function to set boundary conditions
void set_bnd_cuda(int M, int N, int O, int b, float* d_x) {
   
    launch_set_bnd_faces_kernels(M,N,O,b,d_x);
    // Configuration for corners kernel (single block with single thread is sufficient)
    dim3 cornerThreads(32, 1, 1);  
    dim3 cornerBlocks(1, 1, 1);
  
    set_bnd_corners_kernel<<<cornerBlocks, cornerThreads>>>(M, N, O, d_x);
}

__device__ int getGlobalBlockId() {
    return blockIdx.x + 
           blockIdx.y * gridDim.x + 
           blockIdx.z * gridDim.x * gridDim.y;
}

template<int BLOCK_SIZE>
__global__ void red_phase_kernel(int M, int N, int O, float *x, float *x0, float a, float c, float *max_change) {
    extern __shared__ float block_changes[];  // Dynamic shared memory

    // Calculate linear thread ID
    int lid = threadIdx.x + threadIdx.y * blockDim.x + threadIdx.z * blockDim.x * blockDim.y;
    
    // Calculate 3D indices
    int i = blockIdx.x * blockDim.x + threadIdx.x + 1;
    int j = blockIdx.y * blockDim.y + threadIdx.y + 1;
    int k = blockIdx.z * blockDim.z + threadIdx.z + 1;
    
    // Compute change
    float change = 0.0f;
    if (i <= M && j <= N && k <= O && (i + j + k) % 2 == 0) {
        int idx = IX(i, j, k);
        float old_x = x[idx];
        x[idx] = (x0[idx] + 
                    a * (x[IX(i - 1, j, k)] + x[IX(i + 1, j, k)] +
                        x[IX(i, j - 1, k)] + x[IX(i, j + 1, k)] +
                        x[IX(i, j, k - 1)] + x[IX(i, j, k + 1)])) / c;
        change = fabs(x[idx] - old_x);
    }
    
    // Store in shared memory
    block_changes[lid] = change;
    __syncthreads();
    
    // Reduction optimized for 1024 threads
    if ( BLOCK_SIZE >= 1024) {
        if (lid < 512) {
            block_changes[lid] = fmaxf(block_changes[lid], block_changes[lid + 512]);
        }
        __syncthreads();
    }

    if ( BLOCK_SIZE >= 512) {
    if (lid < 256) {
        block_changes[lid] = fmaxf(block_changes[lid], block_changes[lid + 256]);
    }
    __syncthreads();
     }
    if ( BLOCK_SIZE >= 256) {
    if (lid < 128) {
        block_changes[lid] = fmaxf(block_changes[lid], block_changes[lid + 128]);
    }
    __syncthreads();
     }
     if ( BLOCK_SIZE >= 128) {
    if (lid < 64) {
        block_changes[lid] = fmaxf(block_changes[lid], block_changes[lid + 64]);
    }
    __syncthreads();
    }    
    // Last 64 elements
    if (lid < 32) {
        volatile float* smem = block_changes;
        smem[lid] = fmaxf(smem[lid], smem[lid + 32]);
        smem[lid] = fmaxf(smem[lid], smem[lid + 16]);
        smem[lid] = fmaxf(smem[lid], smem[lid + 8]);
        smem[lid] = fmaxf(smem[lid], smem[lid + 4]);
        smem[lid] = fmaxf(smem[lid], smem[lid + 2]);
        smem[lid] = fmaxf(smem[lid], smem[lid + 1]);
    }
    __syncthreads();
    // Write result
    if (lid == 0)  max_change[getGlobalBlockId()] = block_changes[0];
    
}

template<int BLOCK_SIZE>
__global__ void black_phase_kernel(int M, int N, int O, float *x, float *x0, float a, float c, float *max_change) {
    extern __shared__ float block_changes[];  // Dynamic shared memory

    // Calculate linear thread ID
    int lid = threadIdx.x + threadIdx.y * blockDim.x + threadIdx.z * blockDim.x * blockDim.y;
    
    // Calculate 3D indices
    int i = blockIdx.x * blockDim.x + threadIdx.x + 1;
    int j = blockIdx.y * blockDim.y + threadIdx.y + 1;
    int k = blockIdx.z * blockDim.z + threadIdx.z + 1;
    
    // Compute change
    float change = 0.0f;
    if (i <= M && j <= N && k <= O && (i + j + k) % 2 == 1) {
        int idx = IX(i, j, k);
        float old_x = x[idx];
        x[idx] = (x0[idx] + 
                    a * (x[IX(i - 1, j, k)] + x[IX(i + 1, j, k)] +
                        x[IX(i, j - 1, k)] + x[IX(i, j + 1, k)] +
                        x[IX(i, j, k - 1)] + x[IX(i, j, k + 1)])) / c;
        change = fabs(x[idx] - old_x);
    }
    
    // Store in shared memory
    block_changes[lid] = change;
    __syncthreads();
    
  // Reduction optimized for 1024 threads
 if ( BLOCK_SIZE >= 1024) {
    if (lid < 512) {
        block_changes[lid] = fmaxf(block_changes[lid], block_changes[lid + 512]);
    }
    __syncthreads();
 }

    if ( BLOCK_SIZE >= 512) {
    if (lid < 256) {
        block_changes[lid] = fmaxf(block_changes[lid], block_changes[lid + 256]);
    }
    __syncthreads();
     }
    if ( BLOCK_SIZE >= 256) {
    if (lid < 128) {
        block_changes[lid] = fmaxf(block_changes[lid], block_changes[lid + 128]);
    }
    __syncthreads();
     }
     if ( BLOCK_SIZE >= 128) {
    if (lid < 64) {
        block_changes[lid] = fmaxf(block_changes[lid], block_changes[lid + 64]);
    }
    __syncthreads();
    }    
    // Last 64 elements
    if (lid < 32) {
        volatile float* smem = block_changes;
        smem[lid] = fmaxf(smem[lid], smem[lid + 32]);
        smem[lid] = fmaxf(smem[lid], smem[lid + 16]);
        smem[lid] = fmaxf(smem[lid], smem[lid + 8]);
        smem[lid] = fmaxf(smem[lid], smem[lid + 4]);
        smem[lid] = fmaxf(smem[lid], smem[lid + 2]);
        smem[lid] = fmaxf(smem[lid], smem[lid + 1]);
    }
    __syncthreads();

    if (lid == 0) max_change[getGlobalBlockId()] = block_changes[0];
}

template<int BLOCK_SIZE>
__global__ void reduceMaxKernel(float* input, float* output, int size) {
    extern __shared__ float sdata[];

    unsigned int tid = threadIdx.x;
    unsigned int i = blockIdx.x * (2 * blockDim.x) + threadIdx.x;

    // Load data into shared memory
    sdata[tid] = (i < size) ? input[i] : -INFINITY;
    if (i + blockDim.x < size) {
        sdata[tid] = fmaxf(sdata[tid], input[i + blockDim.x]);
    }
    __syncthreads();

     if ( BLOCK_SIZE >= 1024) {
    if (tid < 512) {
         sdata[tid] = fmaxf( sdata[tid],  sdata[tid + 512]);
    }
    __syncthreads();
 }

    if ( BLOCK_SIZE >= 512) {
    if (tid < 256) {
         sdata[tid ] = fmaxf( sdata[tid ],  sdata[tid + 256]);
    }
    __syncthreads();
     }
    if ( BLOCK_SIZE >= 256) {
    if (tid  < 128) {
         sdata[tid ] = fmaxf( sdata[tid],  sdata[tid + 128]);
    }
    __syncthreads();
     }
     if ( BLOCK_SIZE >= 128) {
    if (tid < 64) {
         sdata[tid] = fmaxf( sdata[tid],  sdata[tid + 64]);
    }
    __syncthreads();
    }    
    // Last 64 elements
    if (tid < 32) {
        volatile float* smem =  sdata;
        smem[tid] = fmaxf(smem[tid], smem[tid + 32]);
        smem[tid] = fmaxf(smem[tid], smem[tid + 16]);
        smem[tid] = fmaxf(smem[tid], smem[tid + 8]);
        smem[tid] = fmaxf(smem[tid], smem[tid + 4]);
        smem[tid] = fmaxf(smem[tid], smem[tid + 2]);
        smem[tid] = fmaxf(smem[tid], smem[tid + 1]);
    }
    __syncthreads();
    // Write the maximum for this block to global memory
    if (tid == 0) output[blockIdx.x] = sdata[0];
}

__global__ void compareMaxChangesKernel(float* redChanges, float* blackChanges, int size) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < size) {
        redChanges[idx] = fmaxf(redChanges[idx], blackChanges[idx]);
    }
}

int getTotalBlocks(const dim3& numBlocks) {
    return numBlocks.x * numBlocks.y * numBlocks.z;
}

int getTotalThreadsPerBlock(const dim3& threadsPerBlock){
    return threadsPerBlock.x * threadsPerBlock.y * threadsPerBlock.z;
}

void lin_solve(int M, int N, int O, int b, float *x, float *x0, float a, float c) {
    float tol = 1e-7;
    float *d_max_change_red,*d_max_change_black, *d_final_max;
    float max_change;
    
    dim3 threadsPerBlock(16, 16, 1);
    dim3 numBlocks(
        (M  + 15) / 16,
        (N + 15) / 16,
        (O)
    );
    int totalBlocks = getTotalBlocks(numBlocks);
    int l = 0;
    
    cudaMalloc((void**) &d_max_change_red, sizeof(float) * totalBlocks);
    cudaMalloc((void**) &d_max_change_black, sizeof(float) * totalBlocks);
    cudaMalloc((void**) &d_final_max, sizeof(float));

    const int REDUCE_THREADS = 256;
    int reduceBlocks = (totalBlocks + REDUCE_THREADS - 1) / REDUCE_THREADS;
    const int tt = 256;

    do {
        max_change = 0.0f;

        red_phase_kernel<tt><<<numBlocks, threadsPerBlock,tt * sizeof(float)>>>(M, N, O, x, x0, a, c, d_max_change_red);

        black_phase_kernel<tt><<<numBlocks, threadsPerBlock,tt * sizeof(float)>>>(M, N, O, x, x0, a, c, d_max_change_black);

        compareMaxChangesKernel<<<reduceBlocks, REDUCE_THREADS>>>(d_max_change_red, d_max_change_black, totalBlocks);

        reduceMaxKernel<REDUCE_THREADS><<<reduceBlocks, REDUCE_THREADS, REDUCE_THREADS * sizeof(float)>>>
            (d_max_change_red, d_final_max, totalBlocks);

        int currentBlocks = reduceBlocks;
        while (currentBlocks > 1) {
            int nextBlocks = (currentBlocks + REDUCE_THREADS - 1) / REDUCE_THREADS;
            reduceMaxKernel<REDUCE_THREADS><<<nextBlocks, REDUCE_THREADS, REDUCE_THREADS * sizeof(float)>>>
                (d_final_max, d_final_max, currentBlocks);

            currentBlocks = nextBlocks;
        }
        
        set_bnd_cuda(M, N, O, b, x);
        cudaDeviceSynchronize();
        cudaMemcpy(&max_change, d_final_max, sizeof(float), cudaMemcpyDeviceToHost);
    
    } while (max_change > tol && ++l < 20);

    cudaFree(d_max_change_red);
    cudaFree(d_max_change_black);
    cudaFree(d_final_max);
}
// Diffusion step (uses implicit method)
void diffuse(int M, int N, int O, int b, float *x, float *x0, float diff,
             float dt) {
  int max = MAX(MAX(M, N), O);
  float a = dt * diff * max * max;
  lin_solve(M, N, O, b, x, x0, a, 1 + 6 * a);
}

__global__ void advect_kernel(int M, int N, int O, int b, float *d, float *d0, float *u, float *v,
            float *w, float dt) {

  float dtX = dt * M, dtY = dt * N, dtZ = dt * O;
  int i = blockIdx.x * blockDim.x + threadIdx.x + 1;
  int j = blockIdx.y * blockDim.y + threadIdx.y + 1;
  int k = blockIdx.z * blockDim.z + threadIdx.z + 1;
  if ( k > O || j > N || i > M) return;


        float x = i - dtX * u[IX(i, j, k)];
        float y = j - dtY * v[IX(i, j, k)];
        float z = k - dtZ * w[IX(i, j, k)];

        // Clamp to grid boundaries
        if (x < 0.5f)
          x = 0.5f;
        if (x > M + 0.5f)
          x = M + 0.5f;
        if (y < 0.5f)
          y = 0.5f;
        if (y > N + 0.5f)
          y = N + 0.5f;
        if (z < 0.5f)
          z = 0.5f;
        if (z > O + 0.5f)
          z = O + 0.5f;

        int i0 = (int)x, i1 = i0 + 1;
        int j0 = (int)y, j1 = j0 + 1;
        int k0 = (int)z, k1 = k0 + 1;

        float s1 = x - i0, s0 = 1 - s1;
        float t1 = y - j0, t0 = 1 - t1;
        float u1 = z - k0, u0 = 1 - u1;

        d[IX(i, j, k)] =
            s0 * (t0 * (u0 * d0[IX(i0, j0, k0)] + u1 * d0[IX(i0, j0, k1)]) +
                  t1 * (u0 * d0[IX(i0, j1, k0)] + u1 * d0[IX(i0, j1, k1)])) +
            s1 * (t0 * (u0 * d0[IX(i1, j0, k0)] + u1 * d0[IX(i1, j0, k1)]) +
                  t1 * (u0 * d0[IX(i1, j1, k0)] + u1 * d0[IX(i1, j1, k1)]));
 
}

// Advection step (uses velocity field to move quantities)
void advect(int M, int N, int O, int b, float *d, float *d0, float *u, float *v,
            float *w, float dt) {
  
    // Configure kernel launch parameters
    dim3 threadsPerBlock(16, 16, 1);  // 256 threads per block
    dim3 numBlocks(
        (M + 15 ) / 16,
        (N + 15 ) / 16,
        (O)
    );

    // Launch the kernel
    advect_kernel<<<numBlocks, threadsPerBlock>>>(M, N, O,b,d,d0,u,v,w, dt);
    set_bnd_cuda(M, N, O, b, d);


}

// Projection step to ensure incompressibility (make the velocity field
// divergence-free)
__global__ void project_kernel_a(int M, int N, int O, float *u, float *v, float *w, float *p,
             float *div) {
    
    int i = blockIdx.x * blockDim.x + threadIdx.x + 1;
    int j = blockIdx.y * blockDim.y + threadIdx.y + 1;
    int k = blockIdx.z * blockDim.z + threadIdx.z + 1;
    if ( k > O || j > N || i > M) return;

    div[IX(i, j, k)] =
        -0.5f *
        (u[IX(i + 1, j, k)] - u[IX(i - 1, j, k)] + v[IX(i, j + 1, k)] -
          v[IX(i, j - 1, k)] + w[IX(i, j, k + 1)] - w[IX(i, j, k - 1)]) /
        MAX(M, MAX(N, O));
    p[IX(i, j, k)] = 0;

}

__global__ void project_kernel_b(int M, int N, int O, float *u, float *v, float *w, float *p,
             float *div) {

        int i = blockIdx.x * blockDim.x + threadIdx.x + 1;
        int j = blockIdx.y * blockDim.y + threadIdx.y + 1;
        int k = blockIdx.z * blockDim.z + threadIdx.z + 1;
        if ( k > O || j > N || i > M) return;

        u[IX(i, j, k)] -= 0.5f * (p[IX(i + 1, j, k)] - p[IX(i - 1, j, k)]);
        v[IX(i, j, k)] -= 0.5f * (p[IX(i, j + 1, k)] - p[IX(i, j - 1, k)]);
        w[IX(i, j, k)] -= 0.5f * (p[IX(i, j, k + 1)] - p[IX(i, j, k - 1)]);
}

void project(int M, int N, int O, float *u, float *v, float *w, float *p,
             float *div) {

  // Configure kernel launch parameters
    dim3 threadsPerBlock(16, 16, 1);  // 512 threads per block
    dim3 numBlocks(
        (M + 15 ) / 16,
        (N + 15  ) / 16,
        (O)
    );

    // Launch the kernel
    project_kernel_a<<<numBlocks, threadsPerBlock>>>(M, N, O,u,v,w,p,div);


    set_bnd_cuda(M, N, O, 0,div);
    set_bnd_cuda(M, N, O, 0,p);

    lin_solve(M, N, O, 0, p, div, 1, 6);


    project_kernel_b<<<numBlocks, threadsPerBlock>>>(M, N, O,u,v,w,p,div);
      
    set_bnd_cuda(M, N, O, 1,u);
    set_bnd_cuda(M, N, O, 2,v);
    set_bnd_cuda(M, N, O, 3,w);

}

// Step function for density
void dens_step(int M, int N, int O, float *x, float *x0, float *u, float *v,
               float *w, float diff, float dt) {
  add_source(M, N, O, x, x0, dt);
  SWAP(x0, x);
  diffuse(M, N, O, 0, x, x0, diff, dt);
  SWAP(x0, x);
  advect(M, N, O, 0, x, x0, u, v, w, dt);
}

// Step function for velocity
void vel_step(int M, int N, int O, float *u, float *v, float *w, float *u0,
              float *v0, float *w0, float visc, float dt) {
  add_source(M, N, O, u, u0, dt);
  add_source(M, N, O, v, v0, dt);
  add_source(M, N, O, w, w0, dt);
  SWAP(u0, u);
  diffuse(M, N, O, 1, u, u0, visc, dt);
  SWAP(v0, v);
  diffuse(M, N, O, 2, v, v0, visc, dt);
  SWAP(w0, w);
  diffuse(M, N, O, 3, w, w0, visc, dt);
  project(M, N, O, u, v, w, u0, v0);
  SWAP(u0, u);
  SWAP(v0, v);
  SWAP(w0, w);
  advect(M, N, O, 1, u, u0, u0, v0, w0, dt);
  advect(M, N, O, 2, v, v0, u0, v0, w0, dt);
  advect(M, N, O, 3, w, w0, u0, v0, w0, dt);
  project(M, N, O, u, v, w, u0, v0);
}