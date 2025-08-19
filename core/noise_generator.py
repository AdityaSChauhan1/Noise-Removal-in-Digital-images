# core/noise_generator.py

import random
import math

class NoiseGenerator:
    def __init__(self, seed=None):
        if seed is not None:
            random.seed(seed)

    def add_gaussian(self, image, mean=0, stddev=40):
        noisy = []
        for row in image:
            noisy_row = []
            for pixel in row:
                noise = self._gaussian_noise(mean, stddev)
                noisy_pixel = self._clip(pixel + noise)
                noisy_row.append(noisy_pixel)
            noisy.append(noisy_row)
        return noisy

    def add_rayleigh(self, image, scale=60):
        noisy = []
        for row in image:
            noisy_row = []
            for pixel in row:
                noise = self._rayleigh_noise(scale)
                noisy_pixel = self._clip(pixel + noise - scale // 2)  # Center around 0
                noisy_row.append(noisy_pixel)
            noisy.append(noisy_row)
        return noisy

    def add_erlang(self, image, k=5, lam=0.2):
        noisy = []
        for row in image:
            noisy_row = []
            for pixel in row:
                noise = self._erlang_noise(k, lam)
                noisy_pixel = self._clip(pixel + noise - (k / lam / 2))  # Centered
                noisy_row.append(noisy_pixel)
            noisy.append(noisy_row)
        return noisy

    def add_exponential(self, image, lam=0.1):
        noisy = []
        for row in image:
            noisy_row = []
            for pixel in row:
                noise = self._exponential_noise(lam)
                noisy_pixel = self._clip(pixel + noise - (1 / lam / 2))  # Center
                noisy_row.append(noisy_pixel)
            noisy.append(noisy_row)
        return noisy

    def add_uniform(self, image, low=-60, high=60):
        noisy = []
        for row in image:
            noisy_row = []
            for pixel in row:
                noise = random.uniform(low, high)
                noisy_pixel = self._clip(pixel + noise)
                noisy_row.append(noisy_pixel)
            noisy.append(noisy_row)
        return noisy

    def add_impulse(self, image, prob=0.25):
        noisy = []
        for row in image:
            noisy_row = []
            for pixel in row:
                r = random.random()
                if r < prob / 2:
                    noisy_pixel = 0       # pepper
                elif r < prob:
                    noisy_pixel = 255     # salt
                else:
                    noisy_pixel = pixel
                noisy_row.append(noisy_pixel)
            noisy.append(noisy_row)
        return noisy

    # ----------- Noise Generators ------------

    def _gaussian_noise(self, mean, stddev):
        # Box-Muller transform
        u1 = random.random()
        u2 = random.random()
        z1 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
        return int(mean + stddev * z1)

    def _rayleigh_noise(self, scale):
        u = random.random()
        return int(scale * math.sqrt(-2 * math.log(1 - u)))

    def _erlang_noise(self, k, lam):
        total = 0
        for _ in range(k):
            u = random.random()
            total += -math.log(u) / lam
        return int(total)

    def _exponential_noise(self, lam):
        u = random.random()
        return int(-math.log(1 - u) / lam)

    def _clip(self, val):
        return max(0, min(255, int(val)))
