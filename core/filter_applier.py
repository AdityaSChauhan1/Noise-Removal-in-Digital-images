# # core/filter_applier.py

# class FilterApplier:
#     def __init__(self):
#         pass

#     def arithmetic_mean(self, image, kernel_size=3):
#         return self._apply_filter(image, kernel_size, lambda window: sum(window) // len(window))

#     def geometric_mean(self, image, kernel_size=3):
#         def geometric(window):
#             product = 1.0
#             for val in window:
#                 product *= max(val, 1)  # avoid log(0)
#             return int(product ** (1.0 / len(window)))
#         return self._apply_filter(image, kernel_size, geometric)

#     def harmonic_mean(self, image, kernel_size=3):
#         def harmonic(window):
#             denom = sum(1.0 / max(val, 1) for val in window)  # avoid division by 0
#             return int(len(window) / denom)
#         return self._apply_filter(image, kernel_size, harmonic)

#     def contraharmonic(self, image, kernel_size=3, Q=1.5):
#         def contraharmonic(window):
#             num = sum(val ** (Q + 1) for val in window)
#             denom = sum(val ** Q for val in window)
#             return int(num / denom) if denom != 0 else 0
#         return self._apply_filter(image, kernel_size, contraharmonic)

#     def median_filter(self, image, kernel_size=3):
#         return self._apply_filter(image, kernel_size, lambda window: sorted(window)[len(window) // 2])

#     def max_filter(self, image, kernel_size=3):
#         return self._apply_filter(image, kernel_size, lambda window: max(window))

#     def min_filter(self, image, kernel_size=3):
#         return self._apply_filter(image, kernel_size, lambda window: min(window))

#     def midpoint_filter(self, image, kernel_size=3):
#         return self._apply_filter(image, kernel_size, lambda window: (max(window) + min(window)) // 2)

#     def alpha_trimmed(self, image, kernel_size=3, d=2):
#         def alpha(window):
#             trimmed = sorted(window)[d//2:len(window)-d//2]
#             return sum(trimmed) // len(trimmed) if trimmed else 0
#         return self._apply_filter(image, kernel_size, alpha)

#     def adaptive_median(self, image, max_kernel=7):
#         padded_image = self._pad_image(image, max_kernel // 2)
#         height = len(image)
#         width = len(image[0])
#         result = [[0]*width for _ in range(height)]

#         for y in range(height):
#             for x in range(width):
#                 k = 3
#                 while k <= max_kernel:
#                     window = self._get_window(padded_image, x + max_kernel // 2, y + max_kernel // 2, k)
#                     z_min = min(window)
#                     z_max = max(window)
#                     z_med = sorted(window)[len(window)//2]
#                     z_xy = padded_image[y + max_kernel // 2][x + max_kernel // 2]

#                     if z_min < z_med < z_max:
#                         if z_min < z_xy < z_max:
#                             result[y][x] = z_xy
#                         else:
#                             result[y][x] = z_med
#                         break
#                     else:
#                         k += 2
#                 if k > max_kernel:
#                     result[y][x] = z_med
#         return result

#     # ---------- Internal helpers ----------

#     def _apply_filter(self, image, kernel_size, func):
#         pad = kernel_size // 2
#         padded = self._pad_image(image, pad)
#         height = len(image)
#         width = len(image[0])
#         output = [[0]*width for _ in range(height)]

#         for y in range(height):
#             for x in range(width):
#                 window = self._get_window(padded, x + pad, y + pad, kernel_size)
#                 output[y][x] = self._clip(func(window))
#         return output

#     def _get_window(self, image, cx, cy, size):
#         half = size // 2
#         window = []
#         for y in range(cy - half, cy + half + 1):
#             for x in range(cx - half, cx + half + 1):
#                 window.append(image[y][x])
#         return window

#     def _pad_image(self, image, pad):
#         height = len(image)
#         width = len(image[0])
#         padded = [[0] * (width + 2*pad) for _ in range(height + 2*pad)]
#         for y in range(height):
#             for x in range(width):
#                 padded[y + pad][x + pad] = image[y][x]
#         return padded

#     def _clip(self, val):
#         return max(0, min(255, int(val)))



# core/filter_applier.py
import numpy as np
from scipy.ndimage import generic_filter, median_filter, maximum_filter, minimum_filter

class FilterApplier:
    def __init__(self):
        pass

    def _convert_to_array(self, image):
        """Convert list of lists to numpy array if needed"""
        if isinstance(image, list):
            return np.array(image, dtype='float32')
        return image

    def _convert_to_list(self, image):
        """Convert numpy array back to list of lists"""
        return image.astype('uint8').tolist()

    def arithmetic_mean(self, image, kernel_size=3):
        array = self._convert_to_array(image)
        kernel = np.ones((kernel_size, kernel_size)) / (kernel_size**2)
        result = generic_filter(array, np.mean, footprint=kernel, mode='reflect')
        return self._convert_to_list(result)

    def geometric_mean(self, image, kernel_size=3):
        def geo_func(window):
            window = np.maximum(window, 1e-6)  # avoid log(0)
            return np.exp(np.mean(np.log(window)))
        
        array = self._convert_to_array(image)
        result = generic_filter(array, geo_func, size=kernel_size, mode='reflect')
        return self._convert_to_list(result)

    def harmonic_mean(self, image, kernel_size=3):
        def harm_func(window):
            window = np.maximum(window, 1e-6)  # avoid division by 0
            return window.size / np.sum(1.0 / window)
        
        array = self._convert_to_array(image)
        result = generic_filter(array, harm_func, size=kernel_size, mode='reflect')
        return self._convert_to_list(result)

    def contraharmonic(self, image, kernel_size=3, Q=1.5):
        def contra_func(window):
            window = np.maximum(window, 1e-6)  # avoid division by 0
            numerator = np.sum(window ** (Q + 1))
            denominator = np.sum(window ** Q)
            return numerator / denominator if denominator != 0 else 0
            
        array = self._convert_to_array(image)
        result = generic_filter(array, contra_func, size=kernel_size, mode='reflect')
        return self._convert_to_list(np.clip(result, 0, 255))

    def median_filter(self, image, kernel_size=3):
        array = self._convert_to_array(image)
        result = median_filter(array, size=kernel_size, mode='reflect')
        return self._convert_to_list(result)

    def max_filter(self, image, kernel_size=3):
        array = self._convert_to_array(image)
        result = maximum_filter(array, size=kernel_size, mode='reflect')
        return self._convert_to_list(result)

    def min_filter(self, image, kernel_size=3):
        array = self._convert_to_array(image)
        result = minimum_filter(array, size=kernel_size, mode='reflect')
        return self._convert_to_list(result)

    def midpoint_filter(self, image, kernel_size=3):
        array = self._convert_to_array(image)
        min_img = minimum_filter(array, size=kernel_size, mode='reflect')
        max_img = maximum_filter(array, size=kernel_size, mode='reflect')
        result = (min_img + max_img) / 2
        return self._convert_to_list(result)

    def alpha_trimmed(self, image, kernel_size=3, d=2):
        def alpha_func(window):
            window = np.sort(window.flatten())
            trimmed = window[d//2 : len(window)-d//2]
            return np.mean(trimmed) if len(trimmed) > 0 else 0
            
        array = self._convert_to_array(image)
        result = generic_filter(array, alpha_func, size=kernel_size, mode='reflect')
        return self._convert_to_list(result)

    # def adaptive_median(self, image, max_kernel=7):
    #     array = self._convert_to_array(image)
    #     height, width = array.shape
    #     result = np.zeros_like(array)
    #     pad = max_kernel // 2
    #     padded = np.pad(array, pad, mode='reflect')
        
    #     for y in range(height):
    #         for x in range(width):
    #             k = 3
    #             while k <= max_kernel:
    #                 half = k // 2
    #                 window = padded[y:y+2*half+1, x:x+2*half+1]
    #                 z_min, z_med, z_max = np.min(window), np.median(window), np.max(window)
    #                 z_xy = array[y, x]
                    
    #                 if z_min < z_med < z_max:
    #                     if z_min < z_xy < z_max:
    #                         result[y, x] = z_xy
    #                     else:
    #                         result[y, x] = z_med
    #                     break
    #                 k += 2
    #             else:
    #                 result[y, x] = z_med
    #     return self._convert_to_list(result)

    def adaptive_median(self, image, max_kernel=7):
        array = self._convert_to_array(image)
        height, width = array.shape
        result = np.zeros_like(array)
        pad = max_kernel // 2

        # better border handling for impulse noise
        padded = np.pad(array, pad, mode='edge')  

        for y in range(height):
            for x in range(width):
                k = 3
                pixel_set = False
                while k <= max_kernel:
                    half = k // 2
                    window = padded[y+pad-half:y+pad+half+1, x+pad-half:x+pad+half+1]
                    z_min, z_med, z_max = np.min(window), np.median(window), np.max(window)
                    z_xy = array[y, x]

                    # ---------- Stage A ----------
                    if z_min < z_med < z_max:
                        # ---------- Stage B ----------
                        if z_min < z_xy < z_max:
                            result[y, x] = z_xy
                        else:
                            result[y, x] = z_med
                        pixel_set = True
                        break
                    else:
                        k += 2

                # if no valid window found, assign median of largest window
                if not pixel_set:
                    result[y, x] = z_med  

        return self._convert_to_list(result)
