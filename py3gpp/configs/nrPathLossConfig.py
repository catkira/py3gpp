# Ref: https://www.mathworks.com/help/5g/ref/nrpathlossconfig.html

import numpy as np

def nrPathLossConfig(
    Scenario='UMa',
    BuildingHeight=5,
    StreetWidth=20,
    EnvironmentHeight=1,
    OptionalModel=0
):
    # Check dependencies
    if Scenario == 'RMa':
        BuildingHeight = max(5, min(50, BuildingHeight))
        StreetWidth = max(5, min(50, StreetWidth))
    elif Scenario in ['UMa', 'UMi']:
        if isinstance(EnvironmentHeight, (int, float)):
            EnvironmentHeight = max(0, EnvironmentHeight)
        elif isinstance(EnvironmentHeight, (list, np.ndarray)):
            EnvironmentHeight = np.maximum(0, EnvironmentHeight)
    else:
        raise ValueError(
            "Invalid Scenario. Supported values: 'UMa', 'UMi', 'RMa'")

    OptionalModel = bool(OptionalModel)

    #TODO Indoor path loss model related configuration  - currently not defined in MATLAB docs

    # Return the configured parameters
    return {
        'Scenario': Scenario,
        'BuildingHeight': BuildingHeight,
        'StreetWidth': StreetWidth,
        'EnvironmentHeight': EnvironmentHeight,
        'OptionalModel': OptionalModel
    }

