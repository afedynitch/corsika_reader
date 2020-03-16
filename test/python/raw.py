
import unittest
import sys, os
sys.path.append('')
try:
    import icecube
    with_icecube = True
except:
    with_icecube = False

if with_icecube: from icecube import corsika
else: import corsika

import numpy

# this is the first particle block in DAT000002-32
reference = numpy.array([[7.653100e+04,  -1.160752e+01,   9.754623e-01,   3.125265e+01,   5.020117e+05,  -4.068420e+04,   1.693577e+06],
                         [6.531000e+03,  -1.087171e+01,   1.039457e+00,   2.943657e+01,  -1.545890e+04,   5.227068e+03,   3.900454e+05],
                         [7.553100e+04,  -4.463568e+00,   6.004802e-01,   1.268876e+01,   6.457018e+05,  -5.141263e+04,   2.078663e+06],
                         [5.531000e+03,  -3.956338e+00,   4.497687e-01,   1.085382e+01,   1.392930e+04,   2.606024e+04,   3.897382e+05],
                         [7.653100e+04,  -7.739039e+00,   4.498707e-01,   2.073167e+01,   6.464204e+05,  -5.252401e+04,   2.082826e+06],
                         [6.531000e+03,  -7.116247e+00,   5.290348e-01,   1.881782e+01,  -2.019043e+04,  -6.502461e+03,   3.900905e+05],
                         [7.553100e+04,  -2.936366e+00,   4.294271e-01,   8.352021e+00,   6.479938e+05,  -5.158130e+04,   2.084938e+06],
                         [5.531000e+03,  -2.318731e+00,   2.003050e-01,   6.652174e+00,   2.352265e+04,   2.057402e+04,   3.896284e+05],
                         [1.031000e+03,  -1.725379e-03,  -2.931793e-03,   1.306867e-02,   1.988874e+04,  -3.902078e+04,   3.896666e+05],
                         [7.653100e+04,  -2.268032e+00,   2.081946e-01,   6.387280e+00,   6.516310e+05,  -5.258580e+04,   2.095815e+06],
                         [6.531000e+03,  -1.611050e+00,   2.499403e-01,   4.729528e+00,   1.848695e+04,   2.736930e+04,   3.896988e+05],
                         [1.041000e+03,  -1.564030e-02,   1.300719e-03,   4.189749e-02,  -7.959271e+03,  -6.586376e+03,   3.899531e+05],
                         [1.041000e+03,  -1.247883e-02,   6.140986e-04,   1.476106e-02,  -6.973791e+04,  -1.212312e+04,   3.910042e+05],
                         [1.041000e+03,  -1.333058e-03,  -1.133893e-03,   5.166197e-03,   7.278466e+04,  -8.492829e+04,   3.894892e+05],
                         [1.041000e+03,  -3.347514e-03,   5.537451e-04,   8.855162e-03,  -2.752351e+02,   1.202439e+04,   3.898840e+05],
                         [1.041000e+03,  -4.733688e-04,   8.769854e-04,   5.182052e-03,   4.202239e+04,  -1.063180e+04,   3.895250e+05],
                         [1.031000e+03,   1.964041e-04,  -7.783927e-04,   3.638319e-03,   6.965433e+03,   1.265137e+04,   3.899183e+05],
                         [1.031000e+03,  -2.668779e-03,   6.648803e-04,   7.966751e-03,  -4.925089e+03,   2.172775e+04,   3.899537e+05],
                         [1.031000e+03,  -7.432477e-03,   3.296045e-03,   2.452547e-02,   2.624084e+04,   2.459691e+04,   3.896442e+05],
                         [1.031000e+03,  -3.912949e-03,  -6.114519e-04,   1.278255e-02,   2.022540e+04,  -3.192709e+04,   3.896571e+05],
                         [1.031000e+03,  -1.648791e-03,   1.469409e-03,   3.038753e-03,   4.212864e+04,   4.107050e+03,   3.895630e+05],
                         [1.031000e+03,  -1.432775e-05,  -1.728450e-03,   4.266012e-03,   8.584550e+04,  -1.026377e+05,   3.896261e+05],
                         [1.031000e+03,  -2.488682e-03,  -2.061639e-04,   4.778565e-03,  -9.762608e+03,  -2.742279e+04,   3.899777e+05],
                         [1.031000e+03,  -1.375893e-02,  -1.614325e-03,   3.753648e-02,  -5.393840e+03,  -2.790427e+04,   3.899197e+05],
                         [1.031000e+03,  -8.375580e-03,  -6.250086e-04,   2.780546e-02,  -2.543298e+03,  -2.700768e+04,   3.898886e+05],
                         [1.031000e+03,  -4.375622e-03,   3.091448e-03,   1.382103e-02,   1.132764e+04,   4.763318e+04,   3.899416e+05],
                         [1.031000e+03,  -2.516706e-03,   9.142131e-04,   3.997427e-03,  -4.083734e+04,   3.007651e+04,   3.905636e+05],
                         [1.031000e+03,  -4.986919e-03,   6.268335e-04,   1.243869e-02,  -2.358840e+04,   9.931502e+03,   3.901526e+05],
                         [1.031000e+03,  -2.642127e-03,   1.295410e-03,   1.039560e-02,   4.148849e+04,   3.692167e+04,   3.895540e+05],
                         [1.031000e+03,  -1.269272e-02,  -4.891594e-04,   1.780412e-02,  -4.243151e+04,  -2.337998e+04,   3.904591e+05],
                         [1.031000e+03,  -5.939803e-03,  -3.975095e-03,   2.157654e-02,  -2.163859e+04,  -3.072372e+04,   3.901811e+05],
                         [1.031000e+03,  -2.721590e-03,   6.066738e-05,   7.431211e-03,  -1.791433e+03,  -7.490848e+03,   3.898781e+05],
                         [1.031000e+03,  -1.548318e-02,   1.736608e-03,   4.597299e-02,   7.738070e+02,  -2.807805e+03,   3.898520e+05],
                         [1.031000e+03,  -2.128421e-03,   1.313241e-03,   4.351867e-03,  -4.161184e+03,   5.975480e+03,   3.899586e+05],
                         [1.031000e+03,  -2.059251e-02,   3.230299e-03,   7.312713e-02,   2.793879e+03,  -2.614119e+03,   3.898324e+05],
                         [1.031000e+03,  -1.941226e-02,   9.551847e-04,   5.466710e-02,  -1.093945e+02,  -3.545782e+03,   3.898611e+05],
                         [1.031000e+03,  -2.395986e-03,   6.569585e-04,   6.099525e-03,  -5.977234e+02,  -1.699365e+03,   3.898702e+05],
                         [1.031000e+03,  -2.047075e-02,   5.394848e-03,   5.156138e-02,  -6.481782e+02,  -1.726373e+03,   3.898707e+05],
                         [1.031000e+03,  -2.477210e-03,   5.616519e-04,   7.321044e-03,  -2.029909e+02,  -2.003557e+03,   3.898648e+05]])

filename = None

class RawTest(unittest.TestCase):
    def test(self):
        global filename
        if filename is None: filename = corsika.example_data_dir + '/DAT000002-32'
        assert os.path.exists(filename)

        raw = corsika.RawStream(filename)
        block = corsika.Block()

        # get the run header, event header and first particle block
        raw.get_next_block(block)
        assert block.ID == 'RUNH'
        raw.get_next_block(block)
        assert block.ID == 'EVTH'
        raw.get_next_block(block)
        assert numpy.all(numpy.isclose(reference, block.data.reshape((-1,7))))
        n_blocks = 3
        while raw.get_next_block(block):
            n_blocks += 1

        # check total number of blocks
        assert n_blocks == 4725
        raw.close()

        # check particle iteration
        raw = corsika.RawStream(filename)
        raw.get_next_block(block)
        raw.get_next_block(block)
        particles = raw.particles() # this works because it is positioned right before the particle block
        for i,p in enumerate(raw.particles()):
            if i >= reference.shape[0]: break
            assert numpy.all(numpy.isclose([p.px, p.py, p.pz, p.x, p.y, p.t_or_z], reference[i][1:], 3))

if __name__ == '__main__':
    # unittest uses sys.argv, so in order to pass arguments we read them first and set sys.argv so it is k for unittest
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='Input file')
    parser.add_argument('unittest_args', nargs='*')

    args = parser.parse_args()
    if args.input: filename = args.input

    sys.argv[1:] = args.unittest_args
    unittest.main()

