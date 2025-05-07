#include "fluid_solver.h"
#include <cmath>

#define IX(i, j, k) ((i) + (M + 2) * (j) + (M + 2) * (N + 2) * (k))
#define SWAP(x0, x)                                                            \
  {                                                                            \
    float *tmp = x0;                                                           \
    x0 = x;                                                                    \
    x = tmp;                                                                   \
  }
#define MAX(a, b) (((a) > (b)) ? (a) : (b))
#define LINEARSOLVERTIMES 20
#define BLOCK_SIZE 4

// Add sources (density or velocity)
void add_source(int M, int N, int O, float *x, float *s, float dt) {
  int size = (M + 2) * (N + 2) * (O + 2);
  for (int i = 0; i < size; i++) {
    x[i] += dt * s[i];
  }
}

// Set boundary conditions
void set_bnd(int M, int N, int O, int b, float *x) {
  int i, j;

  // Set boundary on faces
  for (j = 1; j <= M; j++) {
    for (i = 1; i <= N; i++) {
      x[IX(i, j, 0)] = b == 3 ? -x[IX(i, j, 1)] : x[IX(i, j, 1)];
      x[IX(i, j, O + 1)] = b == 3 ? -x[IX(i, j, O)] : x[IX(i, j, O)];
    }
  }
  for (j = 1; j <= N; j++) {
    for (i = 1; i <= O; i++) {
      x[IX(0, i, j)] = b == 1 ? -x[IX(1, i, j)] : x[IX(1, i, j)];
      x[IX(M + 1, i, j)] = b == 1 ? -x[IX(M, i, j)] : x[IX(M, i, j)];
    }
  }
  for (j = 1; j <= M; j++) {
    for (i = 1; i <= O; i++) {
      x[IX(i, 0, j)] = b == 2 ? -x[IX(i, 1, j)] : x[IX(i, 1, j)];
      x[IX(i, N + 1, j)] = b == 2 ? -x[IX(i, N, j)] : x[IX(i, N, j)];
    }
  }

  // Set corners
  x[IX(0, 0, 0)] = 0.33f * (x[IX(1, 0, 0)] + x[IX(0, 1, 0)] + x[IX(0, 0, 1)]);
  x[IX(M + 1, 0, 0)] =
      0.33f * (x[IX(M, 0, 0)] + x[IX(M + 1, 1, 0)] + x[IX(M + 1, 0, 1)]);
  x[IX(0, N + 1, 0)] =
      0.33f * (x[IX(1, N + 1, 0)] + x[IX(0, N, 0)] + x[IX(0, N + 1, 1)]);
  x[IX(M + 1, N + 1, 0)] = 0.33f * (x[IX(M, N + 1, 0)] + x[IX(M + 1, N, 0)] +
                                    x[IX(M + 1, N + 1, 1)]);
}

// Linear solve for implicit methods (diffusion)
void lin_solve(int M, int N, int O, int b, float *x, float *x0, float a, float c) {
    for (int l = 0; l < LINEARSOLVERTIMES; l++) {
        for (int k = 1; k <= O; k +=2) {
            for (int j = 1; j <= N; j +=2) {
                for (int i = 1; i <= M; i ++) {
                  int aux = IX(i, j, k);
                  int aux2 = IX(i, j + 1, k);
                  int aux3 = IX(i, j, k + 1);
                  int aux4 = IX(i, j + 1, k + 1);

                  float sum_neighbors = x[IX(i - 1, j, k)] + x[IX(i + 1, j, k)] +   
                                        x[IX(i, j - 1, k)] + x[aux2] +               
                                        x[IX(i, j, k - 1)] + x[aux3];    

                  x[aux] = (x0[aux] + a * sum_neighbors) / c;

                  sum_neighbors = x[IX(i - 1, j + 1, k)] + x[IX(i + 1, j + 1, k)] +   
                                  x[aux] +         x[IX(i, j + 2, k)] +                  
                                  x[IX(i, j + 1, k - 1)] + x[aux4];  
                                                    
                  x[aux2] = (x0[aux2] + a * sum_neighbors) / c;

                  sum_neighbors = x[IX(i - 1, j, k + 1)] + x[IX(i + 1, j, k + 1)] + 
                                  x[IX(i, j - 1, k + 1)] + x[aux4] +
                                  x[aux] + x[IX(i, j, k + 2)];                 
                  
                  x[aux3] = (x0[aux3] + a * sum_neighbors) / c;

                  sum_neighbors = x[IX(i - 1, j + 1, k + 1)] + x[IX(i + 1, j + 1, k + 1)] + 
                                  x[aux3] +  x[IX(i, j + 2, k + 1)] +                     
                                  x[aux2] + x[IX(i, j + 1, k + 2)];       
                                                 
                  x[aux4] = (x0[aux4] + a * sum_neighbors) / c;
                }  
            }
        }   
    set_bnd(M, N, O, b, x);
    }
}

// Diffusion step (uses implicit method)
void diffuse(int M, int N, int O, int b, float *x, float *x0, float diff,
             float dt) {
  int max = std::max(std::max(M,N),O);
  float a = dt * diff * max * max;
  lin_solve(M, N, O, b, x, x0, a, 1 + 6 * a);
}

// Advection step (uses velocity field to move quantities)
void advect(int M, int N, int O, int b, float *d, float *d0, float *u, float *v,
            float *w, float dt) {
  float dtX = dt * M, dtY = dt * N, dtZ = dt * O;


  for (int kk = 1; kk <= O; kk += BLOCK_SIZE) {
    for (int jj = 1; jj <= N; jj += BLOCK_SIZE) {
      for (int ii = 1; ii <= M; ii += BLOCK_SIZE) {
        int k_max = std::min(kk + BLOCK_SIZE - 1, O);
        int j_max = std::min(jj + BLOCK_SIZE - 1, N);
        int i_max = std::min(ii + BLOCK_SIZE - 1, M);

        for (int k = kk; k <= k_max; k++) {
          for (int j = jj; j <= j_max; j++) {
            for (int i = ii; i <= i_max; i++) {
              int idx = IX(i, j, k);
              float x = i - dtX * u[idx];
              float y = j - dtY * v[idx];
              float z = k - dtZ * w[idx];

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

              d[idx] =
                  s0 * (t0 * (u0 * d0[IX(i0, j0, k0)] + u1 * d0[IX(i0, j0, k1)]) +
                        t1 * (u0 * d0[IX(i0, j1, k0)] + u1 * d0[IX(i0, j1, k1)])) +
                  s1 * (t0 * (u0 * d0[IX(i1, j0, k0)] + u1 * d0[IX(i1, j0, k1)]) +
                        t1 * (u0 * d0[IX(i1, j1, k0)] + u1 * d0[IX(i1, j1, k1)]));
            }
          }
        }
      }
    }
  }

  set_bnd(M, N, O, b, d);
}

// Projection step to ensure incompressibility (make the velocity field
// divergence-free)
void project(int M, int N, int O, float *u, float *v, float *w, float *p,
             float *div) {


  // First step: calculate divergence and reset pressure
  for (int kk = 1; kk <= O; kk += BLOCK_SIZE) {
    for (int jj = 1; jj <= N; jj += BLOCK_SIZE) {
      for (int ii = 1; ii <= M; ii += BLOCK_SIZE) {
        int k_max = std::min(kk + BLOCK_SIZE - 1, O);
        int j_max = std::min(jj + BLOCK_SIZE - 1, N);
        int i_max = std::min(ii + BLOCK_SIZE - 1, M);

        for (int k = kk; k <= k_max; k++) {
          for (int j = jj; j <= j_max; j++) {
            for (int i = ii; i <= i_max; i++) {
              int idx = IX(i, j, k);
              div[idx] =
                  -0.5f *
                  (u[IX(i + 1, j, k)] - u[IX(i - 1, j, k)] +
                   v[IX(i, j + 1, k)] - v[IX(i, j - 1, k)] +
                   w[IX(i, j, k + 1)] - w[IX(i, j, k - 1)]) /
                  std::max(std::max(M,N),O);
              p[idx] = 0;
            }
          }
        }
      }
    }
  }

  set_bnd(M, N, O, 0, div);
  set_bnd(M, N, O, 0, p);
  lin_solve(M, N, O, 0, p, div, 1, 6);

  // Second step: subtract gradient of pressure from velocity field
  for (int kk = 1; kk <= O; kk += BLOCK_SIZE) {
    for (int jj = 1; jj <= N; jj += BLOCK_SIZE) {
      for (int ii = 1; ii <= M; ii += BLOCK_SIZE) {
        int k_max = std::min(kk + BLOCK_SIZE - 1, O);
        int j_max = std::min(jj + BLOCK_SIZE - 1, N);
        int i_max = std::min(ii + BLOCK_SIZE - 1, M);

        for (int k = kk; k <= k_max; k++) {
          for (int j = jj; j <= j_max; j++) {
            for (int i = ii; i <= i_max; i++) {
              int idx = IX(i, j, k);
              u[idx] -= 0.5f * (p[IX(i + 1, j, k)] - p[IX(i - 1, j, k)]);
              v[idx] -= 0.5f * (p[IX(i, j + 1, k)] - p[IX(i, j - 1, k)]);
              w[idx] -= 0.5f * (p[IX(i, j, k + 1)] - p[IX(i, j, k - 1)]);
            }
          }
        }
      }
    }
  }

  set_bnd(M, N, O, 1, u);
  set_bnd(M, N, O, 2, v);
  set_bnd(M, N, O, 3, w);
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
