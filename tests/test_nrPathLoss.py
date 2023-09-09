import numpy as np
from py3gpp.nrPathLoss import nrPathLoss
from py3gpp.configs.nrPathLossConfig import nrPathLossConfig

def test_nrPathLoss():
    pathlossconf = nrPathLossConfig()
    pathlossconf.Scenario = "RMa"
    pathlossconf.BuildingHeight = 7
    pathlossconf.StreetWidth = 25
    freq = 3.5e9
    los = True
    bs = np.array([0, 0, 30])
    ue = np.array([1000, 1000, 1.5])
    pathloss, shadowfading = nrPathLoss(pathlossconf, freq, los, bs, ue)
    print("Path Loss:", pathloss)
    print("Shadow Fading:", shadowfading)
    assert np.round(pathloss, 4) == 110.1615
    assert shadowfading == 4

if __name__ == '__main__':
    test_nrPathLoss()
