from scipy.optimize import linprog
import matplotlib.pyplot as plt

def battery_charging(initial_charge: float, capacity: float, discharge_limit: float, charge_limit: float, prices: list[float]) -> list[float]:
    raise NotImplementedError # TODO: Optimize using `linprog`

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Battery charging problem solver")
    parser.add_argument("--file", required=True, help="CSV input file")
    file_name = parser.parse_args().file
 
    capacity = None
    c_rating = None
    initial_charge = None
    prices = None
    with open(file_name, "r") as file:
        lines = file.readlines()
        capacity, c_rating, initial_charge = map(float, lines[0].split(","))
        prices = list(map(float, lines[1:]))
    
    discharge_limit = -capacity * c_rating
    charge_limit = capacity * c_rating
    charging_decisions = battery_charging(initial_charge, capacity, discharge_limit, charge_limit, prices)

    state_of_charge = [initial_charge]
    for charge_decision in charging_decisions:
        state_of_charge.append(state_of_charge[-1] + charge_decision)
    state_of_charge = state_of_charge[1:]
    state_of_charge = [100*charge/capacity for charge in state_of_charge]

    figure,axis = plt.subplots(3,1)
    axis[0].plot(charging_decisions)
    axis[0].plot([discharge_limit for _ in prices])
    axis[0].plot([charge_limit for _ in prices])
    axis[0].set_title('Charging decisions (kWh)')

    axis[1].plot(state_of_charge)
    axis[1].plot([0 for _ in prices])
    axis[1].plot([100 for _ in prices])
    axis[1].set_title('State of charge (%)')

    axis[2].plot(prices)
    axis[2].plot([0 for _ in prices])
    axis[2].set_title('Prices (€/kWh)')

    plt.tight_layout() # Ensure titles don't overlap
    plt.show()
