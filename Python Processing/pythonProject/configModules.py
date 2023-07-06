def select_mode():
    mode_list = ['Experiment Configuration', 'Manual Operation']
    mode_selected = False
    print("\nSelect Mode:")
    for index, mode in enumerate(mode_list):
        print(f"{index + 1}. {mode}")
    while not mode_selected:
        try:
            mode_selection = int(input())
            if 0 < mode_selection <= (len(mode_list)):
                mode_selection = mode_list[mode_selection - 1]
                mode_selected = True
                return mode_selection
        except ValueError:
            mode_selected = False

def select_platform():
    platform_list = ['GHK AKS-74U']
    platform_selected = False
    print("\nSelect Platform:")
    for index, platform in enumerate(platform_list):
        print(f"{index + 1}. {platform}")
    while not platform_selected:
        try:
            platform_selection = int(input())
            if 0 < platform_selection <= (len(platform_list)):
                platform_selection = platform_list[platform_selection - 1]
                platform_selected = True
                return platform_selection
        except ValueError:
            platform_selected = False

def select_propellant():
    propellant_list = ['Propane', 'Propylene', 'CO2', 'HPA']
    propellant_selected = False
    print("\nSelect propellant:")
    for index, propellant in enumerate(propellant_list):
        print(f"{index + 1}. {propellant}")
    while not propellant_selected:
        try:
            propellant_selection = int(input())
            if 0 < propellant_selection <= (len(propellant_list)):
                propellant_selection = propellant_list[propellant_selection - 1]
                propellant_selected = True
                return propellant_selection
        except ValueError:
            propellant_selected = False

def select_mass():
    mass_selected = False
    print("\nSelect Mass of Propellant (g):")
    while not mass_selected:
        try:
            mass_selection = int(input())
            if 0 < mass_selection <= 30:
                mass_selected = True
                return mass_selection
        except ValueError:
            mass_selected = False

def select_interval():
    interval_selected = False
    print("\nSelect Cycling Interval (ms):")
    while not interval_selected:
        try:
            interval_selection = int(input())
            if 300 < interval_selection <= 2000:
                interval_selected = True
                return interval_selection
        except ValueError:
            interval_selected = False


