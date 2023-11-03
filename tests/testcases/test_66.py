from py3gpp import nrPDSCHDMRSIndices, nrPDSCHConfig, nrCarrierConfig

def test_issue_66():
  cfg = nrPDSCHConfig()
  carrier = nrCarrierConfig()
  dmrsIndices = nrPDSCHDMRSIndices(carrier, cfg)
