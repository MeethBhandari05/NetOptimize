import random
import os
import math
import matplotlib.pyplot as plt
import numpy as np

def tlbo_main(G_SIZE, SR_SIZE, S_SIZE, T_SIZE, IP_SIZE, QJ_SIZE, EC_SIZE, TARGET_COORDINATES):
    def initialize_network_lifetime():
        network = {
            'targets': TARGET_COORDINATES,
            'sensors': [],
            'coverage': [0] * T_SIZE,
            'matrix': [],
            'upper_bound': [],
            'qj': QJ_SIZE,
            'ip': IP_SIZE,
            'ec': EC_SIZE,
            'bi': IP_SIZE / EC_SIZE,
            'sr': SR_SIZE,
            'network_lifetime': 0
        }
        return network

    def initialize_sensors(network):
        for _ in range(S_SIZE):
            random1 = random.randint(0, G_SIZE)
            random2 = random.randint(0, G_SIZE)
            network['sensors'].append((random1, random2))

    def calculate_distance(network):
        sr_squared = network['sr'] ** 2
        sensors = network['sensors']
        targets = network['targets']
        coverage = network['coverage']
        matrix = network['matrix']
        
        for i, (tx, ty) in enumerate(targets):
            temp = []
            for sx, sy in sensors:
                dist_squared = (tx - sx) ** 2 + (ty - sy) ** 2
                if dist_squared < sr_squared:
                    temp.append(1)
                    coverage[i] += 1
                else:
                    temp.append(0)
            matrix.append(temp)

    def check_network_lifetime(network):
        for i in range(T_SIZE):
            if network['coverage'][i] < network['qj']:
                return False
        calculate_network_lifetime(network)
        return True

    def calculate_network_lifetime(network):
        for i in range(len(network['matrix'])):
            sum_ = sum(network['matrix'][i])
            ut = sum_ * network['bi'] / network['qj']
            network['upper_bound'].append(ut)
        network['upper_bound'].sort()
        network['network_lifetime'] = network['upper_bound'][0]

    def initialize_tlbo():
        tlbo = {
            'targets': TARGET_COORDINATES,
            'sensor': [],
            'nl': 0,
            'coverage': [0] * T_SIZE,
            'qj': QJ_SIZE,
            'ip': IP_SIZE,
            'ec': EC_SIZE,
            'bi': IP_SIZE / EC_SIZE,
            'sr': SR_SIZE,
            'upper_bound': [],
            'matrix': []
        }
        return tlbo

    import math

    def calculate_distance_tlbo(tlbo):
        sr_squared = tlbo['sr'] ** 2
        sensors = tlbo['sensor']
        targets = tlbo['targets']
        coverage = tlbo['coverage']
        matrix = tlbo['matrix']
        
        for i, (tx, ty) in enumerate(targets):
            temp = []
            for sx, sy in sensors:
                dist_squared = (tx - sx) ** 2 + (ty - sy) ** 2
                if dist_squared < sr_squared:
                    temp.append(1)
                    coverage[i] += 1
                else:
                    temp.append(0)
            matrix.append(temp)

    def calculate_network_lifetime_tlbo(tlbo):
        for i in range(len(tlbo['matrix'])):
            sum_ = sum(tlbo['matrix'][i])
            ut = sum_ * tlbo['bi'] / tlbo['qj']
            tlbo['upper_bound'].append(ut)
        tlbo['upper_bound'].sort()
        tlbo['nl'] = tlbo['upper_bound'][0]

    def check_network_lifetime_tlbo(tlbo):
        for i in range(T_SIZE):
            if tlbo['coverage'][i] < tlbo['qj']:
                return False
        calculate_network_lifetime_tlbo(tlbo)
        return True

    import matplotlib.pyplot as plt

    def plot_sensors_and_targets(target_coordinates, sensors,output_path,title):
        os.makedirs("static",exist_ok=True)
        # Extract sensor and target coordinates
        sensor_x = [sensor[0] for sensor in sensors]  
        sensor_y = [sensor[1] for sensor in sensors]  
        target_x = [target[0] for target in target_coordinates]  
        target_y = [target[1] for target in target_coordinates]  

        plt.figure(figsize=(12, 10))

        # Plot sensors
        plt.scatter(sensor_x, sensor_y, color='blue', label="Sensors", marker='o', s=100, edgecolors='black', linewidth=1.2)

        # Plot target locations
        plt.scatter(target_x, target_y, color='red', label="Target Coordinates", marker='x', s=120, linewidth=2)

        # Labels & Customization
        plt.xlabel("X Coordinate", fontsize=14)
        plt.ylabel("Y Coordinate", fontsize=14)
        plt.title(title, fontsize=16, fontweight='bold')
        plt.legend(fontsize=12, loc="upper right")
        plt.grid(True, linestyle="--", alpha=0.6)

        # Set limits (optional: ensures better spacing)
        plt.xlim(min(target_x + sensor_x) - 50, max(target_x + sensor_x) + 50)
        plt.ylim(min(target_y + sensor_y) - 50, max(target_y + sensor_y) + 50)

        # Save the plot
        plt.savefig(output_path, dpi=300)
        plt.close()  # Close to prevent memory leaks

    def remove_idle_sensors(tlbo):
        sensors = tlbo['sensor']
        targets = tlbo['targets']

        # Step 2: Compute Coverage Matrix
        num_sensors = len(sensors)
        num_targets = len(targets)
        coverage_matrix = np.zeros((num_sensors, num_targets), dtype=int)

        for i, (sx, sy) in enumerate(sensors):
            for j, (tx, ty) in enumerate(targets):
                distance_squared = (sx - tx) ** 2 + (sy - ty) ** 2
                if distance_squared <= SR_SIZE ** 2:  # If target is within sensor radius
                    coverage_matrix[i, j] = 1

        # Identify idle sensors (sensors with no targets in their radius)
        idle_sensors = set()
        for i in range(num_sensors):
            if np.all(coverage_matrix[i, :] == 0):  # No targets covered by this sensor
                idle_sensors.add(i)
        
        # Remove idle sensors
        required_sensors = set(range(num_sensors)) - idle_sensors
        
        return required_sensors



    random.seed(0)
    flag = False
    k = 30
    networks = [initialize_network_lifetime() for _ in range(k * 100)]
    tlbo_list = [initialize_tlbo() for _ in range(k)]
    t1, t2, t3 = initialize_tlbo(), initialize_tlbo(), initialize_tlbo()
    x, i = 0, 0
    graph_lifetime = []
    random_deployment_index = []

    while x != k:
        initialize_sensors(networks[i])
        calculate_distance(networks[i])
        flag = check_network_lifetime(networks[i])
        if flag:
            tlbo_list[x]['sensor'] = networks[i]['sensors'][:]
            tlbo_list[x]['nl'] = networks[i]['network_lifetime']
            x += 1
        i += 1

    print("\nBefore TLBO")
    for i in range(k):
        print(f"Set no:{i+1}\tNL: {tlbo_list[i]['nl']}")
    total_iteration = 30
    iteration = 0
    while iteration != total_iteration:
        max_nl = 0
        teacher_index = 0
        for i in range(k):
            if tlbo_list[i]['nl'] > max_nl:
                max_nl = tlbo_list[i]['nl']
                teacher_index = i
        
        if iteration == 0:
            first_sensors = tlbo_list[teacher_index]['sensor']
            plot_sensors_and_targets(TARGET_COORDINATES,first_sensors,"ui_integration/static/images/random_sensor_plot.png","Random Sensor Locations")

        for i in range(k):
            if i != teacher_index:
                swap_count = random.randint(0, S_SIZE)
                t1['sensor'] = tlbo_list[i]['sensor'][:]
                t1['nl'] = tlbo_list[i]['nl']
                for j in range(swap_count):
                    swap_index = random.randint(0, S_SIZE - 1)
                    tlbo_list[i]['sensor'][swap_index] = tlbo_list[teacher_index]['sensor'][swap_index]
                calculate_distance_tlbo(tlbo_list[i])
                check_network_lifetime_tlbo(tlbo_list[i])
                if t1['nl'] > tlbo_list[i]['nl']:
                    tlbo_list[i]['sensor'] = t1['sensor'][:]
                    tlbo_list[i]['nl'] = t1['nl']
                tlbo_list[i]['upper_bound'].clear()
                tlbo_list[i]['matrix'].clear()
                tlbo_list[i]['coverage'] = [0] * T_SIZE

        t1['sensor'] = tlbo_list[teacher_index]['sensor'][:]
        t1['nl'] = tlbo_list[teacher_index]['nl']
        calculate_distance_tlbo(tlbo_list[teacher_index])
        check_network_lifetime_tlbo(tlbo_list[teacher_index])
        if t1['nl'] > tlbo_list[teacher_index]['nl']:
            tlbo_list[teacher_index]['sensor'] = t1['sensor'][:]
            tlbo_list[teacher_index]['nl'] = t1['nl']
        tlbo_list[teacher_index]['upper_bound'].clear()
        tlbo_list[teacher_index]['matrix'].clear()
        tlbo_list[teacher_index]['coverage'] = [0] * T_SIZE
        num_learning_pairs = int(k * 2.5)  # 2.5 times the number of networks
        learning_pairs = [(random.randint(0, k - 1), random.randint(0, k - 1)) for _ in range(num_learning_pairs)]
        for x, y in learning_pairs:
            if tlbo_list[x]['nl'] > tlbo_list[y]['nl']:
                t2['sensor'] = tlbo_list[y]['sensor'][:]
                t2['nl'] = tlbo_list[y]['nl']
                tlbo_list[y]['upper_bound'].clear()
                tlbo_list[y]['matrix'].clear()
                tlbo_list[y]['coverage'] = [0] * T_SIZE
                swap_count = random.randint(0, S_SIZE - 1)
                for j in range(swap_count):
                    swap_index = random.randint(0, S_SIZE - 1)
                    tlbo_list[y]['sensor'][swap_index] = tlbo_list[x]['sensor'][swap_index]
                calculate_distance_tlbo(tlbo_list[y])
                check_network_lifetime_tlbo(tlbo_list[y])
                if t2['nl'] > tlbo_list[y]['nl']:
                    tlbo_list[y]['sensor'] = t2['sensor'][:]
                    tlbo_list[y]['nl'] = t2['nl']
                tlbo_list[y]['upper_bound'].clear()
                tlbo_list[y]['matrix'].clear()
                tlbo_list[y]['coverage'] = [0] * T_SIZE
            else:
                t3['sensor'] = tlbo_list[x]['sensor'][:]
                t3['nl'] = tlbo_list[x]['nl']
                tlbo_list[x]['upper_bound'].clear()
                tlbo_list[x]['matrix'].clear()
                tlbo_list[x]['coverage'] = [0] * T_SIZE
                swap_count = random.randint(0, S_SIZE - 1)
                for j in range(swap_count):
                    swap_index = random.randint(0, S_SIZE - 1)
                    tlbo_list[x]['sensor'][swap_index] = tlbo_list[y]['sensor'][swap_index]
                calculate_distance_tlbo(tlbo_list[x])
                check_network_lifetime_tlbo(tlbo_list[x])
                if t3['nl'] > tlbo_list[x]['nl']:
                    tlbo_list[x]['sensor'] = t3['sensor'][:]
                    tlbo_list[x]['nl'] = t3['nl']
                tlbo_list[x]['upper_bound'].clear()
                tlbo_list[x]['matrix'].clear()
                tlbo_list[x]['coverage'] = [0] * T_SIZE

        maximum_network_lifetime, max_index = max(
            (tlbo_list[i]['nl'], i) for i in range(k)
        ) 
        
        graph_lifetime.append(maximum_network_lifetime)
        random_deployment_index.append(max_index)
        iteration += 1

    print("\nAfter TLBO")
    for i in range(k):
        print(f"Set no:{i+1}\tNL: {tlbo_list[i]['nl']}")

    print("\nMaximum network lifetime of", iteration, "Iterations")
    for lifetime in graph_lifetime:
        print(f"Networklifetime: {lifetime}")
    
    for i in random_deployment_index:
        print(i,", ")
    
        
    last_sensors = tlbo_list[random_deployment_index[k-1]]['sensor']
    
    # Call this function with your data
    plot_sensors_and_targets(TARGET_COORDINATES,last_sensors,"ui_integration/static/images/optimal_sensor_plot.png","Optimal Sensor Locations")
    optimized_sensor_indices = remove_idle_sensors(tlbo_list[random_deployment_index[k-1]])
    print(len(optimized_sensor_indices))
    optimized_sensors = [tlbo_list[random_deployment_index[k-1]]['sensor'][i] for i in optimized_sensor_indices]
    plot_sensors_and_targets(TARGET_COORDINATES,optimized_sensors,"ui_integration/static/images/removed_idle_sensor_plot.png","Removed Idle Sensor Locations")

def run_tlbo(params):
    return tlbo_main(
        params["grid_size"], params["sensor_radius"], params["num_sensors"],
        params["num_targets"], params["initial_power"], params["qj_coverage"],
        params["energy_rate"], params["target_coordinates"]
    )