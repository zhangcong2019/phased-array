import numpy as np
import math
from matplotlib import pyplot as plt


class PhasedArray:
    def __init__(self, emitter_num, emitter_space, phase_shift, wave_length=800e-9, mesh_n=201, mesh_space=1):
        self.mesh_n = mesh_n
        self.mesh_space = mesh_space
        self.emitter_num = emitter_num
        self.emitter_space = emitter_space
        self.phase_shift = phase_shift
        self.wave_length = wave_length
        self.mesh_length = (mesh_n - 1) * mesh_space

        # initialize E and amplitude
        self.E = np.zeros([mesh_n, mesh_n], dtype=complex)
        self.sub_E = np.ones([emitter_num, mesh_n, mesh_n], dtype=complex)
        self.electric_amplitude = np.zeros([mesh_n, mesh_n], dtype=float)

        # coordinates& distances
        self.emitter_coordinates_x = np.linspace(-(emitter_num // 2) * emitter_space,
                                                 (emitter_num - (emitter_num // 2) - 1) * emitter_space, emitter_num) + 0.5
        self.emitter_coordinates_y = np.zeros([emitter_num], dtype=float) + 0.5

        coordinates_x = np.linspace(-self.mesh_length / 2, self.mesh_length / 2, mesh_n)
        coordinates_y = np.linspace(0, self.mesh_length, mesh_n) - 20

        self.mesh_coordinates_x, self.mesh_coordinates_y = np.meshgrid(coordinates_x, coordinates_y)

        self.mesh_distance_x = np.zeros(shape=[emitter_num, mesh_n, mesh_n], dtype=float)
        self.mesh_distance_y = np.zeros(shape=[emitter_num, mesh_n, mesh_n], dtype=float)
        self.mesh_distance = np.zeros(shape=[emitter_num, mesh_n, mesh_n], dtype=float)

        for i_emitter in range(emitter_num):
            self.mesh_distance_y[i_emitter] = self.mesh_coordinates_y - self.emitter_coordinates_y[i_emitter]
            self.mesh_distance_x[i_emitter] = self.mesh_coordinates_x[i_emitter] - self.emitter_coordinates_x[i_emitter]
            self.mesh_distance[i_emitter] = np.sqrt(np.square(self.mesh_distance_y[i_emitter]) + \
                                            np.square(self.mesh_distance_x[i_emitter]))

        # calculate sub electric field E
        for i_emitter in range(emitter_num):
            phase_distance = 2 * math.pi * self.mesh_distance[i_emitter]
            phase_emitter = 2 * math.pi * phase_shift * i_emitter
            E_emitter = np.exp(-1j * phase_emitter)
            complex_phase = np.exp(-1j * phase_distance) * E_emitter
            sub_E = np.divide(complex_phase, self.mesh_distance[i_emitter])
            self.sub_E[i_emitter] = sub_E
            self.E += self.sub_E[i_emitter]

        self.electric_amplitude = np.absolute(self.E)

        self.electric_amplitude[0:40]

        print("construct finished")

    def amplitude(self):
        return self.electric_amplitude

def main():
    print("this is main")

    for i in range(10000):
        array = PhasedArray(emitter_num=51, emitter_space=0.25, phase_shift=0.025*(i % 21 - 10))

        plt.imshow(array.amplitude())
        plt.show()

if __name__ == '__main__':
    main()
