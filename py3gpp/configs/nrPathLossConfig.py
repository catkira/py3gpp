# Ref: https://www.mathworks.com/help/5g/ref/nrpathlossconfig.html

class nrPathLossConfig():
    def __init__(self):
        self._Scenario = 'UMa'
        self._BuildingHeight = 5
        self._StreetWidth = 20
        self._EnvironmentHeight = 1
        self._OptionalModel = 0

    @property
    def Scenario(self):
        return self._Scenario

    @Scenario.setter
    def Scenario(self, Scenario):
        assert Scenario in ['UMa', 'UMi', 'RMa', 'InH', 'InF-SL', 'InF-DL', 'InF-SH', 'InF-DH',
                            'InF-HH'], "The value must be in 'UMa', 'UMi', 'RMa', 'InH', 'InF-SL', 'InF-DL', 'InF-SH', 'InF-DH', or 'InF-HH'"
        self._Scenario = Scenario

    @property
    def BuildingHeight(self):
        return self._BuildingHeight

    @BuildingHeight.setter
    def BuildingHeight(self, BuildingHeight):
        assert BuildingHeight >= 5 and BuildingHeight <= 50, "The value must be 5..50"
        self._BuildingHeight = BuildingHeight

    @property
    def StreetWidth(self):
        return self._StreetWidth

    @StreetWidth.setter
    def StreetWidth(self, StreetWidth):
        assert StreetWidth >= 5 and StreetWidth <= 50, "The value must be 5..50"
        self._StreetWidth = StreetWidth

    @property
    def EnvironmentHeight(self):
        return self._EnvironmentHeight

    @EnvironmentHeight.setter
    def EnvironmentHeight(self, EnvironmentHeight):
        self._EnvironmentHeight = EnvironmentHeight

    @property
    def OptionalModel(self):
        return self._OptionalModel

    @OptionalModel.setter
    def OptionalModel(self, OptionalModel):
        assert OptionalModel in [0, 1, True, False], "The value must be 0 / False or 1 / True"
        self._OptionalModel = OptionalModel


# # Example usage
# pathlossconf = nrPathLossConfig()
# print(f'Scenario: ', pathlossconf.Scenario)
# print(f'BuildingHeight: ', pathlossconf.BuildingHeight)
# print(f'StreetWidth: ', pathlossconf.StreetWidth)
# print(f'EnvironmentHeight: ', pathlossconf.EnvironmentHeight)
# print(f'OptionalModel: ', pathlossconf.OptionalModel)
