# Ref: https://www.mathworks.com/help/5g/ref/nrpathlossconfig.html

class nrPathLossConfig:
    def __init__(
        self,
        Scenario='UMa',
        BuildingHeight=5,
        StreetWidth=20,
        EnvironmentHeight=1,
        OptionalModel=0
    ):
        
        # Set the attributes
        self.Scenario = Scenario
        self.BuildingHeight = BuildingHeight
        self.StreetWidth = StreetWidth
        self.EnvironmentHeight = EnvironmentHeight
        self.OptionalModel = OptionalModel


# # Example usage
# pathlossconf = nrPathLossConfig()
# print(f'Scenario: ', pathlossconf.Scenario)
# print(f'BuildingHeight: ', pathlossconf.BuildingHeight)
# print(f'StreetWidth: ', pathlossconf.StreetWidth)
# print(f'EnvironmentHeight: ', pathlossconf.EnvironmentHeight)
# print(f'OptionalModel: ', pathlossconf.OptionalModel)
