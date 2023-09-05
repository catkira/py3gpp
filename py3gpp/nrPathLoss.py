# Ref: https://www.mathworks.com/help/5g/ref/nrpathloss.html#d124e18391
# Ref: TR 38.901 Section 7.4.1

import numpy as np
import math
from configs.nrPathLossConfig import nrPathLossConfig

pathlossconf = nrPathLossConfig()


def nrPathLoss(pathlossconf, freq, los, bs, ue):

    # Check the input types
    if not isinstance(freq, (int, float)):
        raise TypeError('freq must be a positive numeric scalar')

    if not isinstance(los, (bool, int, np.ndarray)):
        raise TypeError('los must be true, false, 1, 0, or a logical matrix')

    if not isinstance(bs, np.ndarray) or not isinstance(ue, np.ndarray):
        raise TypeError('bs and ue must be numeric matrices')

    # Path loss equation
    if pathlossconf.Scenario == 'RMa':

        if not isinstance(los, (bool, int)):
            # TODO Multiple BSs and UEs
            raise TypeError('Multiple BSs and UEs not yet supported.')

        else:
            c = 3e8  # Speed of light (m/s)
            dist_bp = 2 * math.pi * bs[2] * ue[2] * freq / c
            dist_2d = np.sqrt((ue[0] - bs[0])**2 + (ue[1] - bs[1])**2)
            dist_3d = np.sqrt((dist_2d)**2 + (bs[2] - ue[2])**2)

            pathloss_one = 0
            pathloss_two = 0
            shadowfading_one = 0
            shadowfading_two = 0

            pathloss_one += 20 * \
                math.log10(40 * math.pi * dist_3d * (freq/1e9) / 3)
            pathloss_one += min((0.03 * pathlossconf.BuildingHeight)
                                ** 1.72, 10) * math.log10(dist_3d)
            pathloss_one += - \
                min((0.044 * pathlossconf.BuildingHeight)**1.72, 14.77)
            pathloss_one += 0.002 * \
                math.log10(pathlossconf.BuildingHeight * dist_3d)

            if dist_2d <= dist_bp:
                shadowfading_one = 4

            else:
                pathloss_two += 10 * \
                    math.log10((10**(pathloss_one / 10)) * dist_bp)
                pathloss_two += 40 * math.log10(dist_3d / dist_bp)
                shadowfading_two = 6

            pathloss_los = pathloss_one + pathloss_two + shadowfading_one + shadowfading_two
            shadowfading_los = shadowfading_one + shadowfading_two

            if los in [True, 1]:  # LOS case

                pathloss = pathloss_los
                shadowfading = shadowfading_los

            elif los in [False, 0]:  # NLOS case

                pathloss_nlos_ = 0
                pathloss_nlos_ += 161.04
                pathloss_nlos_ += - \
                    (7.11 * math.log10(pathlossconf.StreetWidth))
                pathloss_nlos_ += 7.5 * math.log10(pathlossconf.BuildingHeight)
                pathloss_nlos_ += - \
                    (24.37 - (3.7*(pathlossconf.BuildingHeight /
                     bs[2])**2)) * math.log10(bs[2])
                pathloss_nlos_ += (43.42 - (3.1 *
                                   math.log10(bs[2]))) * ((math.log10(dist_3d)) - 3)
                pathloss_nlos_ += (20 * math.log10(freq/1e9)) - \
                    (3.2 * (math.log10(11.75 * ue[2])))**2 - 4.97

                shadowfading_nlos = 8

                pathloss_nlos = max(pathloss_los, pathloss_nlos_)

                pathloss = pathloss_nlos + shadowfading_nlos
                shadowfading = shadowfading_nlos

            else:

                raise TypeError(
                    'los for single bs-ue link must be true, false, 1, 0')

    return pathloss, shadowfading


# Example usage
# pathlossconf.Scenario = "RMa"
# pathlossconf.BuildingHeight = 7
# pathlossconf.StreetWidth = 25
# freq = 3.5e9
# los = True
# bs = np.array([0, 0, 30])
# ue = np.array([1000, 1000, 1.5])
# pathloss, shadowfading = nrPathLoss(pathlossconf, freq, los, bs, ue)
# print("Path Loss:", pathloss)
# print("Shadow Fading:", shadowfading)
