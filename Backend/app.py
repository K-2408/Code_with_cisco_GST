# from flask import Flask, request, jsonify
# import networkx as nx
# import matplotlib.pyplot as plt
# import io
# import base64

# from flask import Flask, request, jsonify
# import networkx as nx
# import matplotlib.pyplot as plt
# from flask_cors import CORS


# app = Flask(__name__)
# CORS(app)



# class NetworkDesigner:
#     def __init__(self):
#         self.graph = nx.Graph()
#         self.router_status = {}
#         self.router_specs = {'Type1': {'100G_ports': 8, '400G_ports': 2, 'power': 250},
#                              'Type2': {'100G_ports': 0, '400G_ports': 8, 'power': 350}}
#         self.city_customers = {}
#         self.city_connections = []
#         self.bandwidth_patterns = []

#     def add_city(self, city_name, num_customers):
#         self.graph.add_node(city_name, customers=num_customers, type='city')
#         self.city_customers[city_name] = num_customers

#     def add_connection(self, city1, city2, upload_peak, download_peak):
#         self.city_connections.append((city1, city2, upload_peak, download_peak))
#         port_number = 0
#         capacity = max(upload_peak, download_peak) * 1000  # Convert Tb to Gb
#         self.graph.add_edge(city1, city2, capacity=capacity, used_capacity=0, port=port_number)

#     def add_bandwidth_pattern(self, start_time, end_time, city1, city2, upload, download):
#         self.bandwidth_patterns.append((start_time, end_time, city1, city2, upload, download))

#     def calculate_ports(self, num_customers):
#         return (num_customers + self.router_specs['Type1']['100G_ports'] - 1) // self.router_specs['Type1']['100G_ports']

#     def calculate_type2_routers(self, type1_routers):
#         return (type1_routers // 7) + 1

#     def place_routers(self):
#         for city, num_customers in self.city_customers.items():
#             required_type1_routers = self.calculate_ports(num_customers)
#             required_type2_routers = self.calculate_type2_routers(required_type1_routers)
#             self.graph.nodes[city]['type1_routers'] = required_type1_routers
#             self.graph.nodes[city]['type2_routers'] = required_type2_routers
#             for i in range(required_type1_routers):
#                 router_name = f"{city}Type1_router{i+1}"
#                 self.graph.add_node(router_name, type='router', router_type='Type1')
#                 self.graph.add_edge(city, router_name, capacity=0, used_capacity=0, port=i)
#             for i in range(required_type2_routers):
#                 router_name = f"{city}Type2_router{i+1}"
#                 self.graph.add_node(router_name, type='router', router_type='Type2')
#                 self.graph.add_edge(city, router_name, capacity=0, used_capacity=0, port=i)

#     def connect_type2_routers_ring(self):
#         cities = list(self.city_customers.keys())
#         n = len(cities)
#         for i in range(n):
#             city1 = cities[i]
#             city2 = cities[(i + 1) % n]
#             router1 = f"{city1}Type2_router1"
#             router2 = f"{city2}Type2_router1"
#             self.graph.add_edge(router1, router2, capacity=400 * 8, used_capacity=0, port=0)  # 400G ports * 8

#     def connect_cities(self):
#         for city1, city2, upload_peak, download_peak in self.city_connections:
#             capacity = max(upload_peak, download_peak) * 1000  # Convert Tb to Gb
#             type1_routers_city1 = [node for node in self.graph.neighbors(city1) if self.graph.nodes[node]['router_type'] == 'Type1']
#             type1_routers_city2 = [node for node in self.graph.neighbors(city2) if self.graph.nodes[node]['router_type'] == 'Type1']
#             for i, (router1, router2) in enumerate(zip(type1_routers_city1, type1_routers_city2)):
#                 self.graph.add_edge(router1, router2, capacity=capacity, used_capacity=0, port=i)

#     def route_traffic(self, source, target, traffic):
#         paths = list(nx.all_simple_paths(self.graph, source=source, target=target))
#         best_path = None
#         min_used_capacity = float('inf')

#         for path in paths:
#             max_used_capacity = max(self.graph.edges[path[i], path[i + 1]]['used_capacity'] for i in range(len(path) - 1))
#             if max_used_capacity < min_used_capacity:
#                 min_used_capacity = max_used_capacity
#                 best_path = path

#         if best_path:
#             for i in range(len(best_path) - 1):
#                 self.graph.edges[best_path[i], best_path[i + 1]]['used_capacity'] += traffic

#     def manage_power(self):
#         total_power = 0
#         for city, data in self.graph.nodes(data=True):
#             type1_routers = data.get('type1_routers', 0)
#             type2_routers = data.get('type2_routers', 0)
#             for i in range(type1_routers):
#                 total_power += self.router_specs['Type1']['power']
#             for i in range(type2_routers):
#                 total_power += self.router_specs['Type2']['power']
#         return total_power

#     def simulate(self):
#         for time, city1, city2, upload, download in self.bandwidth_patterns:
#             self.route_traffic(city1, city2, upload * 1000)
#             self.route_traffic(city2, city1, download * 1000)
#         total_power = self.manage_power()
#         img_data = self.visualize_network()
#         connections_summary = self.summarize_connections()
#         return total_power, img_data, connections_summary

#     def visualize_network(self):
#         plt.figure(figsize=(20, 15))
#         pos = nx.spring_layout(self.graph)  # positions for all nodes
#         capacities = nx.get_edge_attributes(self.graph, 'capacity')
#         used_capacities = nx.get_edge_attributes(self.graph, 'used_capacity')

#         # Get node colors and labels based on their type
#         node_colors = []
#         labels = {}
#         for node, data in self.graph.nodes(data=True):
#             if data['type'] == 'city':
#                 node_colors.append('blue')
#                 labels[node] = f"{node}\nUsers: {data['customers']}"
#             elif data['type'] == 'router':
#                 node_colors.append('green' if data['router_type'] == 'Type1' else 'red')
#                 labels[node] = f"Router ({data['router_type']})"

#         # Draw the nodes
#         nx.draw_networkx_nodes(self.graph, pos, node_size=700, node_color=node_colors)

#         # Draw the edges
#         nx.draw_networkx_edges(self.graph, pos, width=2)

#         # Draw the labels
#         nx.draw_networkx_labels(self.graph, pos, labels, font_size=10, font_family="sans-serif")

#         # Draw edge labels
#         edge_labels = {(u, v): f"{used}/{cap}" for (u, v), used, cap in zip(used_capacities.keys(), used_capacities.values(), capacities.values())}
#         nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, font_size=8)

#         plt.title("Network Graph")

#         img = io.BytesIO()
#         plt.savefig(img, format='png')
#         img.seek(0)
#         img_data = base64.b64encode(img.read()).decode('utf-8')
#         plt.close()
#         return img_data

#     def summarize_connections(self):
#         summary = "\nInter-city Connections Summary:\n"
#         for city1, city2, _, _ in self.city_connections:
#             type1_routers_city1 = [node for node in self.graph.neighbors(city1) if self.graph.nodes[node]['router_type'] == 'Type1']
#             type1_routers_city2 = [node for node in self.graph.neighbors(city2) if self.graph.nodes[node]['router_type'] == 'Type1']
#             type2_routers_city1 = [node for node in self.graph.neighbors(city1) if self.graph.nodes[node]['router_type'] == 'Type2']
#             type2_routers_city2 = [node for node in self.graph.neighbors(city2) if self.graph.nodes[node]['router_type'] == 'Type2']

#             if type1_routers_city1 and type1_routers_city2:
#                 for router1, router2 in zip(type1_routers_city1, type1_routers_city2):
#                     used_capacity = self.graph[router1][router2]['used_capacity']
#                     total_capacity = self.graph[router1][router2]['capacity']
#                     summary += f"{router1} <--> {router2}: {used_capacity}/{total_capacity} Gbps used\n"

#             if type2_routers_city1 and type2_routers_city2:
#                 for router1, router2 in zip(type2_routers_city1, type2_routers_city2):
#                     used_capacity = self.graph[router1][router2]['used_capacity']
#                     total_capacity = self.graph[router1][router2]['capacity']
#                     summary += f"{router1} <--> {router2}: {used_capacity}/{total_capacity} Gbps used\n"

#         return summary

# @app.route('/submit', methods=['POST'])
# def design_network():
#     data = request.json
#     print(data)

#     nd = NetworkDesigner()

#     for city in data['cityUsers']:
#         nd.add_city(city['cityName'], int(city['numOfUsers']))

#     for connection in data['cityTraffic']:
#         nd.add_connection(connection['city1'], connection['city2'], float(connection['uploadPeak']), float(connection['downloadPeak']))

#     for pattern in data['timeRangeTraffic']:
#         nd.add_bandwidth_pattern(pattern['startTime'], pattern['endTime'], pattern['city1'], pattern['city2'], float(pattern['uploadPeak']), float(pattern['downloadPeak']))

#     nd.place_routers()
#     nd.connect_type2_routers_ring()
#     nd.connect_cities()

#     total_power, img_data, connections_summary = nd.simulate()

#     return jsonify({
#         'total_power': total_power,
#         'network_graph': img_data,
#         'connections_summary': connections_summary
#     })


# if __name__ == '__main__':
#     app.run(debug=True)


# import io
# import base64
# from flask import Flask, request, jsonify
# import networkx as nx
# import matplotlib.pyplot as plt
# from flask_cors import CORS


# app = Flask(__name__)
# CORS(app)

# class NetworkDesigner:
#     def __init__(self):
#         self.graph = nx.Graph()
#         self.router_status = {}
#         self.router_specs = {'Type1': {'100G_ports': 8, '400G_ports': 2, 'power': 250},
#                              'Type2': {'100G_ports': 0, '400G_ports': 8, 'power': 350}}
#         self.city_customers = {}
#         self.city_connections = []
#         self.bandwidth_patterns = []

#     def add_city(self, city_name, num_customers):
#         self.graph.add_node(city_name, customers=num_customers, type='city')
#         self.city_customers[city_name] = num_customers

#     def add_connection(self, city1, city2, upload_peak, download_peak):
#         self.city_connections.append((city1, city2, upload_peak, download_peak))

#     def add_bandwidth_pattern(self, time, city1, city2, upload, download):
#         self.bandwidth_patterns.append((time, city1, city2, upload, download))

#     def calculate_ports(self, num_customers):
#         return (num_customers + self.router_specs['Type1']['100G_ports'] - 1) // self.router_specs['Type1']['100G_ports']

#     def calculate_type2_routers(self, type1_routers):
#         return (type1_routers // 7) + 1

#     def place_routers(self):
#         for city, num_customers in self.city_customers.items():
#             required_type1_routers = self.calculate_ports(num_customers)
#             required_type2_routers = self.calculate_type2_routers(required_type1_routers)
#             self.graph.nodes[city]['type1_routers'] = required_type1_routers
#             self.graph.nodes[city]['type2_routers'] = required_type2_routers
#             for i in range(required_type1_routers):
#                 router_name = f"{city}Type1_router{i+1}"
#                 self.graph.add_node(router_name, type='router', router_type='Type1')
#                 self.graph.add_edge(city, router_name, capacity=0, used_capacity=0, ports='100G')
#             for i in range(required_type2_routers):
#                 router_name = f"{city}Type2_router{i+1}"
#                 self.graph.add_node(router_name, type='router', router_type='Type2')
#                 self.graph.add_edge(city, router_name, capacity=0, used_capacity=0, ports='400G')

#     def connect_type2_routers_ring(self):
#         cities = list(self.city_customers.keys())
#         n = len(cities)
#         for i in range(n):
#             city1 = cities[i]
#             city2 = cities[(i + 1) % n]
#             router1 = f"{city1}Type2_router1"
#             router2 = f"{city2}Type2_router1"
#             self.graph.add_edge(router1, router2, capacity=400 * 8, used_capacity=0, ports='400G')

#     def connect_cities(self):
#         for city1, city2, upload_peak, download_peak in self.city_connections:
#             capacity = max(upload_peak, download_peak) * 1000  # Convert Tb to Gb
#             type1_routers_city1 = [node for node in self.graph.neighbors(city1) if self.graph.nodes[node]['router_type'] == 'Type1']
#             type1_routers_city2 = [node for node in self.graph.neighbors(city2) if self.graph.nodes[node]['router_type'] == 'Type1']
#             for router1, router2 in zip(type1_routers_city1, type1_routers_city2):
#                 self.graph.add_edge(router1, router2, capacity=capacity, used_capacity=0, ports='400G')

#     def route_traffic(self, source, target, traffic):
#         paths = list(nx.all_simple_paths(self.graph, source=source, target=target))
#         best_path = None
#         min_used_capacity = float('inf')

#         for path in paths:
#             max_used_capacity = max(self.graph.edges[path[i], path[i + 1]]['used_capacity'] for i in range(len(path) - 1))
#             if max_used_capacity < min_used_capacity:
#                 min_used_capacity = max_used_capacity
#                 best_path = path

#         if best_path:
#             for i in range(len(best_path) - 1):
#                 self.graph.edges[best_path[i], best_path[i + 1]]['used_capacity'] += traffic

#     # def manage_power(self):
#     #     total_power = 0
#     #     for city, data in self.graph.nodes(data=True):
#     #         type1_routers = data.get('type1_routers', 0)
#     #         type2_routers = data.get('type2_routers', 0)
#     #         for i in range(type1_routers):
#     #             total_power += self.router_specs['Type1']['power']
#     #         for i in range(type2_routers):
#     #             total_power += self.router_specs['Type2']['power']
#     #     print(f"Total Power Consumption: {total_power}W")

#     # def simulate(self):
#     #     for time, city1, city2, upload, download in self.bandwidth_patterns:
#     #         self.route_traffic(city1, city2, upload * 1000)
#     #         self.route_traffic(city2, city1, download * 1000)
#     #     self.manage_power()
#     #     self.visualize_network()
#     #     self.summarize_connections()

#     def manage_power(self):
#         total_power = 0
#         for city, data in self.graph.nodes(data=True):
#             type1_routers = data.get('type1_routers', 0)
#             type2_routers = data.get('type2_routers', 0)
#             for i in range(type1_routers):
#                 total_power += self.router_specs['Type1']['power']
#             for i in range(type2_routers):
#                 total_power += self.router_specs['Type2']['power']
#         return total_power

#     def simulate(self):
#         for time, city1, city2, upload, download in self.bandwidth_patterns:
#             self.route_traffic(city1, city2, upload * 1000)
#             self.route_traffic(city2, city1, download * 1000)
#         total_power = self.manage_power()
#         img_data = self.visualize_network()
#         connections_summary = self.summarize_connections()
#         return total_power, img_data, connections_summary

#     def visualize_network(self):
#         plt.figure(figsize=(20, 15))
#         pos = nx.spring_layout(self.graph)  # positions for all nodes
#         capacities = nx.get_edge_attributes(self.graph, 'capacity')
#         used_capacities = nx.get_edge_attributes(self.graph, 'used_capacity')
#         ports = nx.get_edge_attributes(self.graph, 'ports')

#         # Get node colors and labels based on their type
#         node_colors = []
#         labels = {}
#         for node, data in self.graph.nodes(data=True):
#             if data['type'] == 'city':
#                 node_colors.append('blue')
#                 labels[node] = f"{node}\nUsers: {data['customers']}"
#             elif data['type'] == 'router':
#                 node_colors.append('green' if data['router_type'] == 'Type1' else 'red')
#                 labels[node] = f"Router ({data['router_type']})"

#         # Draw the nodes
#         nx.draw_networkx_nodes(self.graph, pos, node_size=700, node_color=node_colors)

#         # Draw the edges
#         nx.draw_networkx_edges(self.graph, pos, width=2)

#         # Draw the labels
#         nx.draw_networkx_labels(self.graph, pos, labels, font_size=10, font_family="sans-serif")

#         # Draw edge labels
#         edge_labels = {(u, v): f"{used}/{cap} ({ports[(u, v)]})" for (u, v), used, cap in zip(used_capacities.keys(), used_capacities.values(), capacities.values())}
#         nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, font_size=8)

#         plt.title("Network Graph")
                

#         img = io.BytesIO()
#         plt.savefig(img, format='png')
#         img.seek(0)
#         img_data = base64.b64encode(img.read()).decode('utf-8')
#         plt.close()
#         return img_data

        

#     def summarize_connections(self):
#         summary = "\nInter-city Connections Summary:\n"
#         for city1, city2, _, _ in self.city_connections:
#             type1_routers_city1 = [node for node in self.graph.neighbors(city1) if self.graph.nodes[node]['router_type'] == 'Type1']
#             type1_routers_city2 = [node for node in self.graph.neighbors(city2) if self.graph.nodes[node]['router_type'] == 'Type1']
#             type2_routers_city1 = [node for node in self.graph.neighbors(city1) if self.graph.nodes[node]['router_type'] == 'Type2']
#             type2_routers_city2 = [node for node in self.graph.neighbors(city2) if self.graph.nodes[node]['router_type'] == 'Type2']

#             if type1_routers_city1 and type1_routers_city2:
#                 for router1, router2 in zip(type1_routers_city1, type1_routers_city2):
#                     used_capacity = self.graph[router1][router2]['used_capacity']
#                     total_capacity = self.graph[router1][router2]['capacity']
#                     summary += f"{router1} <--> {router2}: {used_capacity}/{total_capacity} Gbps used\n"

#             if type2_routers_city1 and type2_routers_city2:
#                 for router1, router2 in zip(type2_routers_city1, type2_routers_city2):
#                     used_capacity = self.graph[router1][router2]['used_capacity']
#                     total_capacity = self.graph[router1][router2]['capacity']
#                     summary += f"{router1} <--> {router2}: {used_capacity}/{total_capacity} Gbps used\n"

#         return summary
    
# network_designer = NetworkDesigner()

# @app.route('/submit', methods=['POST'])
# def submit():
#     data = request.get_json()
#     print(data)
#     cities = data.get('cities', [])
#     connections = data.get('connections', [])
#     bandwidth_patterns = data.get('bandwidth_patterns', [])

#     for city in cities:
#         network_designer.add_city(city['name'], city['customers'])

#     for connection in connections:
#         network_designer.add_connection(connection['city1'], connection['city2'], connection['upload_peak'], connection['download_peak'])

#     for pattern in bandwidth_patterns:
#         network_designer.add_bandwidth_pattern(pattern['time'], pattern['city1'], pattern['city2'], pattern['upload'], pattern['download'])

#     network_designer.place_routers()
#     network_designer.connect_type2_routers_ring()
#     network_designer.connect_cities()
#     # network_designer.simulate()

#     # return jsonify({"message": "Network simulation completed"}), 200
#     total_power, img_data, connections_summary = network_designer.simulate()

#     return jsonify({
#         'total_power': total_power,
#         'network_graph': img_data,
#         'connections_summary': connections_summary
#     })

# if __name__ == '__main__':
#     app.run(debug=True)


# from flask import Flask, request, jsonify
# import networkx as nx
# import matplotlib.pyplot as plt
# import io
# import base64

# from flask import Flask, request, jsonify
# import networkx as nx
# import matplotlib.pyplot as plt
# from flask_cors import CORS


# app = Flask(__name__)
# CORS(app)



# class NetworkDesigner:
#     def __init__(self):
#         self.graph = nx.Graph()
#         self.router_status = {}
#         self.router_specs = {'Type1': {'100G_ports': 8, '400G_ports': 2, 'power': 250},
#                              'Type2': {'100G_ports': 0, '400G_ports': 8, 'power': 350}}
#         self.city_customers = {}
#         self.city_connections = []
#         self.bandwidth_patterns = []

#     def add_city(self, city_name, num_customers):
#         self.graph.add_node(city_name, customers=num_customers, type='city')
#         self.city_customers[city_name] = num_customers

#     def add_connection(self, city1, city2, upload_peak, download_peak):
#         self.city_connections.append((city1, city2, upload_peak, download_peak))
#         port_number = 0
#         capacity = max(upload_peak, download_peak) * 1000  # Convert Tb to Gb
#         self.graph.add_edge(city1, city2, capacity=capacity, used_capacity=0, port=port_number)

#     def add_bandwidth_pattern(self, start_time, end_time, city1, city2, upload, download):
#         self.bandwidth_patterns.append((start_time, end_time, city1, city2, upload, download))

#     def calculate_ports(self, num_customers):
#         return (num_customers + self.router_specs['Type1']['100G_ports'] - 1) // self.router_specs['Type1']['100G_ports']

#     def calculate_type2_routers(self, type1_routers):
#         return (type1_routers // 7) + 1

#     def place_routers(self):
#         for city, num_customers in self.city_customers.items():
#             required_type1_routers = self.calculate_ports(num_customers)
#             required_type2_routers = self.calculate_type2_routers(required_type1_routers)
#             self.graph.nodes[city]['type1_routers'] = required_type1_routers
#             self.graph.nodes[city]['type2_routers'] = required_type2_routers
#             for i in range(required_type1_routers):
#                 router_name = f"{city}Type1_router{i+1}"
#                 self.graph.add_node(router_name, type='router', router_type='Type1')
#                 self.graph.add_edge(city, router_name, capacity=0, used_capacity=0, port=i)
#             for i in range(required_type2_routers):
#                 router_name = f"{city}Type2_router{i+1}"
#                 self.graph.add_node(router_name, type='router', router_type='Type2')
#                 self.graph.add_edge(city, router_name, capacity=0, used_capacity=0, port=i)

#     def connect_type2_routers_ring(self):
#         cities = list(self.city_customers.keys())
#         n = len(cities)
#         for i in range(n):
#             city1 = cities[i]
#             city2 = cities[(i + 1) % n]
#             router1 = f"{city1}Type2_router1"
#             router2 = f"{city2}Type2_router1"
#             self.graph.add_edge(router1, router2, capacity=400 * 8, used_capacity=0, port=0)  # 400G ports * 8

#     def connect_cities(self):
#         for city1, city2, upload_peak, download_peak in self.city_connections:
#             capacity = max(upload_peak, download_peak) * 1000  # Convert Tb to Gb
#             type1_routers_city1 = [node for node in self.graph.neighbors(city1) if self.graph.nodes[node]['router_type'] == 'Type1']
#             type1_routers_city2 = [node for node in self.graph.neighbors(city2) if self.graph.nodes[node]['router_type'] == 'Type1']
#             for i, (router1, router2) in enumerate(zip(type1_routers_city1, type1_routers_city2)):
#                 self.graph.add_edge(router1, router2, capacity=capacity, used_capacity=0, port=i)

#     def route_traffic(self, source, target, traffic):
#         paths = list(nx.all_simple_paths(self.graph, source=source, target=target))
#         best_path = None
#         min_used_capacity = float('inf')

#         for path in paths:
#             max_used_capacity = max(self.graph.edges[path[i], path[i + 1]]['used_capacity'] for i in range(len(path) - 1))
#             if max_used_capacity < min_used_capacity:
#                 min_used_capacity = max_used_capacity
#                 best_path = path

#         if best_path:
#             for i in range(len(best_path) - 1):
#                 self.graph.edges[best_path[i], best_path[i + 1]]['used_capacity'] += traffic

#     def manage_power(self):
#         total_power = 0
#         for city, data in self.graph.nodes(data=True):
#             type1_routers = data.get('type1_routers', 0)
#             type2_routers = data.get('type2_routers', 0)
#             for i in range(type1_routers):
#                 total_power += self.router_specs['Type1']['power']
#             for i in range(type2_routers):
#                 total_power += self.router_specs['Type2']['power']
#         return total_power

#     def simulate(self):
#         for time, city1, city2, upload, download in self.bandwidth_patterns:
#             self.route_traffic(city1, city2, upload * 1000)
#             self.route_traffic(city2, city1, download * 1000)
#         total_power = self.manage_power()
#         img_data = self.visualize_network()
#         connections_summary = self.summarize_connections()
#         return total_power, img_data, connections_summary

#     def visualize_network(self):
#         plt.figure(figsize=(20, 15))
#         pos = nx.spring_layout(self.graph)  # positions for all nodes
#         capacities = nx.get_edge_attributes(self.graph, 'capacity')
#         used_capacities = nx.get_edge_attributes(self.graph, 'used_capacity')

#         # Get node colors and labels based on their type
#         node_colors = []
#         labels = {}
#         for node, data in self.graph.nodes(data=True):
#             if data['type'] == 'city':
#                 node_colors.append('blue')
#                 labels[node] = f"{node}\nUsers: {data['customers']}"
#             elif data['type'] == 'router':
#                 node_colors.append('green' if data['router_type'] == 'Type1' else 'red')
#                 labels[node] = f"Router ({data['router_type']})"

#         # Draw the nodes
#         nx.draw_networkx_nodes(self.graph, pos, node_size=700, node_color=node_colors)

#         # Draw the edges
#         nx.draw_networkx_edges(self.graph, pos, width=2)

#         # Draw the labels
#         nx.draw_networkx_labels(self.graph, pos, labels, font_size=10, font_family="sans-serif")

#         # Draw edge labels
#         edge_labels = {(u, v): f"{used}/{cap}" for (u, v), used, cap in zip(used_capacities.keys(), used_capacities.values(), capacities.values())}
#         nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, font_size=8)

#         plt.title("Network Graph")

#         img = io.BytesIO()
#         plt.savefig(img, format='png')
#         img.seek(0)
#         img_data = base64.b64encode(img.read()).decode('utf-8')
#         plt.close()
#         return img_data

#     def summarize_connections(self):
#         summary = "\nInter-city Connections Summary:\n"
#         for city1, city2, _, _ in self.city_connections:
#             type1_routers_city1 = [node for node in self.graph.neighbors(city1) if self.graph.nodes[node]['router_type'] == 'Type1']
#             type1_routers_city2 = [node for node in self.graph.neighbors(city2) if self.graph.nodes[node]['router_type'] == 'Type1']
#             type2_routers_city1 = [node for node in self.graph.neighbors(city1) if self.graph.nodes[node]['router_type'] == 'Type2']
#             type2_routers_city2 = [node for node in self.graph.neighbors(city2) if self.graph.nodes[node]['router_type'] == 'Type2']

#             if type1_routers_city1 and type1_routers_city2:
#                 for router1, router2 in zip(type1_routers_city1, type1_routers_city2):
#                     used_capacity = self.graph[router1][router2]['used_capacity']
#                     total_capacity = self.graph[router1][router2]['capacity']
#                     summary += f"{router1} <--> {router2}: {used_capacity}/{total_capacity} Gbps used\n"

#             if type2_routers_city1 and type2_routers_city2:
#                 for router1, router2 in zip(type2_routers_city1, type2_routers_city2):
#                     used_capacity = self.graph[router1][router2]['used_capacity']
#                     total_capacity = self.graph[router1][router2]['capacity']
#                     summary += f"{router1} <--> {router2}: {used_capacity}/{total_capacity} Gbps used\n"

#         return summary

# @app.route('/submit', methods=['POST'])
# def design_network():
#     data = request.json
#     print(data)

#     nd = NetworkDesigner()

#     for city in data['cityUsers']:
#         nd.add_city(city['cityName'], int(city['numOfUsers']))

#     for connection in data['cityTraffic']:
#         nd.add_connection(connection['city1'], connection['city2'], float(connection['uploadPeak']), float(connection['downloadPeak']))

#     for pattern in data['timeRangeTraffic']:
#         nd.add_bandwidth_pattern(pattern['startTime'], pattern['endTime'], pattern['city1'], pattern['city2'], float(pattern['uploadPeak']), float(pattern['downloadPeak']))

#     nd.place_routers()
#     nd.connect_type2_routers_ring()
#     nd.connect_cities()

#     total_power, img_data, connections_summary = nd.simulate()

#     return jsonify({
#         'total_power': total_power,
#         'network_graph': img_data,
#         'connections_summary': connections_summary
#     })


# if __name__ == '__main__':
#     app.run(debug=True)


import io
import base64
from flask import Flask, request, jsonify
import networkx as nx
import matplotlib.pyplot as plt
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

class NetworkDesigner:
    def __init__(self):
        self.graph = nx.Graph()
        self.router_status = {}
        self.router_specs = {'Type1': {'100G_ports': 8, '400G_ports': 2, 'power': 250},
                             'Type2': {'100G_ports': 0, '400G_ports': 8, 'power': 350}}
        self.city_customers = {}
        self.city_connections = []
        self.bandwidth_patterns = []

    def add_city(self, city_name, num_customers):
        self.graph.add_node(city_name, customers=num_customers, type='city')
        self.city_customers[city_name] = num_customers

    def add_connection(self, city1, city2, upload_peak, download_peak):
        self.city_connections.append((city1, city2, upload_peak, download_peak))

    def add_bandwidth_pattern(self, time, city1, city2, upload, download):
        self.bandwidth_patterns.append((time, city1, city2, upload, download))

    def calculate_ports(self, num_customers):
        return (num_customers + self.router_specs['Type1']['100G_ports'] - 1) // self.router_specs['Type1']['100G_ports']

    def calculate_type2_routers(self, type1_routers):
        return (type1_routers // 7) + 1

    def place_routers(self):
        for city, num_customers in self.city_customers.items():
            required_type1_routers = self.calculate_ports(num_customers)
            required_type2_routers = self.calculate_type2_routers(required_type1_routers)
            self.graph.nodes[city]['type1_routers'] = required_type1_routers
            self.graph.nodes[city]['type2_routers'] = required_type2_routers
            for i in range(required_type1_routers):
                router_name = f"{city}Type1_router{i+1}"
                self.graph.add_node(router_name, type='router', router_type='Type1')
                self.graph.add_edge(city, router_name, capacity=0, used_capacity=0, ports='100G')
            for i in range(required_type2_routers):
                router_name = f"{city}Type2_router{i+1}"
                self.graph.add_node(router_name, type='router', router_type='Type2')
                self.graph.add_edge(city, router_name, capacity=0, used_capacity=0, ports='400G')

    def connect_type2_routers_ring(self):
        cities = list(self.city_customers.keys())
        n = len(cities)
        for i in range(n):
            city1 = cities[i]
            city2 = cities[(i + 1) % n]
            router1 = f"{city1}Type2_router1"
            router2 = f"{city2}Type2_router1"
            self.graph.add_edge(router1, router2, capacity=400 * 8, used_capacity=0, ports='400G')

    def connect_cities(self):
        for city1, city2, upload_peak, download_peak in self.city_connections:
            capacity = max(upload_peak, download_peak) * 1000  # Convert Tb to Gb
            type1_routers_city1 = [node for node in self.graph.neighbors(city1) if self.graph.nodes[node]['router_type'] == 'Type1']
            type1_routers_city2 = [node for node in self.graph.neighbors(city2) if self.graph.nodes[node]['router_type'] == 'Type1']
            for router1, router2 in zip(type1_routers_city1, type1_routers_city2):
                self.graph.add_edge(router1, router2, capacity=capacity, used_capacity=0, ports='400G')

    def route_traffic(self, source, target, traffic):
        paths = list(nx.all_simple_paths(self.graph, source=source, target=target))
        best_path = None
        min_used_capacity = float('inf')

        for path in paths:
            max_used_capacity = max(self.graph.edges[path[i], path[i + 1]]['used_capacity'] for i in range(len(path) - 1))
            if max_used_capacity < min_used_capacity:
                min_used_capacity = max_used_capacity
                best_path = path

        if best_path:
            for i in range(len(best_path) - 1):
                self.graph.edges[best_path[i], best_path[i + 1]]['used_capacity'] += traffic

    # def manage_power(self):
    #     total_power = 0
    #     for city, data in self.graph.nodes(data=True):
    #         type1_routers = data.get('type1_routers', 0)
    #         type2_routers = data.get('type2_routers', 0)
    #         for i in range(type1_routers):
    #             total_power += self.router_specs['Type1']['power']
    #         for i in range(type2_routers):
    #             total_power += self.router_specs['Type2']['power']
    #     print(f"Total Power Consumption: {total_power}W")

    # def simulate(self):
    #     for time, city1, city2, upload, download in self.bandwidth_patterns:
    #         self.route_traffic(city1, city2, upload * 1000)
    #         self.route_traffic(city2, city1, download * 1000)
    #     self.manage_power()
    #     self.visualize_network()
    #     self.summarize_connections()

    def manage_power(self):
        total_power = 0
        for city, data in self.graph.nodes(data=True):
            type1_routers = data.get('type1_routers', 0)
            type2_routers = data.get('type2_routers', 0)
            for i in range(type1_routers):
                total_power += self.router_specs['Type1']['power']
            for i in range(type2_routers):
                total_power += self.router_specs['Type2']['power']
        return total_power

    def simulate(self):
        for time, city1, city2, upload, download in self.bandwidth_patterns:
            self.route_traffic(city1, city2, upload * 1000)
            self.route_traffic(city2, city1, download * 1000)
        total_power = self.manage_power()
        img_data = self.visualize_network()
        connections_summary = self.summarize_connections()
        return total_power, img_data, connections_summary

    def visualize_network(self):
        plt.figure(figsize=(20, 15))
        pos = nx.spring_layout(self.graph)  # positions for all nodes
        capacities = nx.get_edge_attributes(self.graph, 'capacity')
        used_capacities = nx.get_edge_attributes(self.graph, 'used_capacity')
        ports = nx.get_edge_attributes(self.graph, 'ports')

        # Get node colors and labels based on their type
        node_colors = []
        labels = {}
        for node, data in self.graph.nodes(data=True):
            if data['type'] == 'city':
                node_colors.append('blue')
                labels[node] = f"{node}\nUsers: {data['customers']}"
            elif data['type'] == 'router':
                node_colors.append('green' if data['router_type'] == 'Type1' else 'red')
                labels[node] = f"Router ({data['router_type']})"

        # Draw the nodes
        nx.draw_networkx_nodes(self.graph, pos, node_size=700, node_color=node_colors)

        # Draw the edges
        nx.draw_networkx_edges(self.graph, pos, width=2)

        # Draw the labels
        nx.draw_networkx_labels(self.graph, pos, labels, font_size=10, font_family="sans-serif")

        # Draw edge labels
        edge_labels = {(u, v): f"{used}/{cap} ({ports[(u, v)]})" for (u, v), used, cap in zip(used_capacities.keys(), used_capacities.values(), capacities.values())}
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, font_size=8)

        plt.title("Network Graph")
        # plt.show()

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        img_data = base64.b64encode(img.read()).decode('utf-8')
        plt.close()
        return img_data

    def summarize_connections(self):
        summary = "\nInter-city Connections Summary:\n"
        print("\nInter-city Connections Summary:")
        for city1, city2, _, _ in self.city_connections:
            type1_routers_city1 = [node for node in self.graph.neighbors(city1) if self.graph.nodes[node]['router_type'] == 'Type1']
            type1_routers_city2 = [node for node in self.graph.neighbors(city2) if self.graph.nodes[node]['router_type'] == 'Type1']
            type2_routers_city1 = [node for node in self.graph.neighbors(city1) if self.graph.nodes[node]['router_type'] == 'Type2']
            type2_routers_city2 = [node for node in self.graph.neighbors(city2) if self.graph.nodes[node]['router_type'] == 'Type2']

            print(f"\nConnection between {city1} and {city2}:")

            if type1_routers_city1 and type1_routers_city2:
                for router1, router2 in zip(type1_routers_city1, type1_routers_city2):
                    if self.graph.has_edge(router1, router2):
                        edge_data = self.graph.edges[router1, router2]
                        capacity = edge_data['capacity']
                        used_capacity = edge_data['used_capacity']
                        port = edge_data.get('port', 'N/A')
                        print(f"  Type1 Router: {router1} <-> {router2} with capacity {capacity} Gb, used capacity {used_capacity} Gb, port {port}")

            if type2_routers_city1 and type2_routers_city2:
                for router1, router2 in zip(type2_routers_city1, type2_routers_city2):
                    if self.graph.has_edge(router1, router2):
                        edge_data = self.graph.edges[router1, router2]
                        capacity = edge_data['capacity']
                        used_capacity = edge_data['used_capacity']
                        port = edge_data.get('port', 'N/A')
                        print(f"  Type2 Router: {router1} <-> {router2} with capacity {capacity} Gb, used capacity {used_capacity} Gb, port {port}")
        return summary

    # def summarize_connections(self):
    #     summary = "\nInter-city Connections Summary:\n"
    #     for city1, city2, _, _ in self.city_connections:
    #         type1_routers_city1 = [node for node in self.graph.neighbors(city1) if self.graph.nodes[node]['router_type'] == 'Type1']
    #         type1_routers_city2 = [node for node in self.graph.neighbors(city2) if self.graph.nodes[node]['router_type'] == 'Type1']
    #         type2_routers_city1 = [node for node in self.graph.neighbors(city1) if self.graph.nodes[node]['router_type'] == 'Type2']
    #         type2_routers_city2 = [node for node in self.graph.neighbors(city2) if self.graph.nodes[node]['router_type'] == 'Type2']

    #         if type1_routers_city1 and type1_routers_city2:
    #             for router1, router2 in zip(type1_routers_city1, type1_routers_city2):
    #                 used_capacity = self.graph[router1][router2]['used_capacity']
    #                 total_capacity = self.graph[router1][router2]['capacity']
    #                 summary += f"{router1} <--> {router2}: {used_capacity}/{total_capacity} Gbps used\n"

    #         if type2_routers_city1 and type2_routers_city2:
    #             for router1, router2 in zip(type2_routers_city1, type2_routers_city2):
    #                 used_capacity = self.graph[router1][router2]['used_capacity']
    #                 total_capacity = self.graph[router1][router2]['capacity']
    #                 summary += f"{router1} <--> {router2}: {used_capacity}/{total_capacity} Gbps used\n"

    #     return summary
    
network_designer = NetworkDesigner()

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    print(data)
    cities = data.get('cityUsers', [])
    connections = data.get('cityTraffic', [])
    bandwidth_patterns = data.get('timeRangeTrafficData', [])

    for city in cities:
        network_designer.add_city(city['cityName'], int(city['numOfUsers']))

    for connection in connections:
        network_designer.add_connection(connection['city1'], connection['city2'], float(connection['uploadPeak']), float(connection['downloadPeak']))

    for pattern in bandwidth_patterns:
        network_designer.add_bandwidth_pattern(pattern['startTime'], pattern['city1'], pattern['city2'], float(pattern['uploadPeak']), float(pattern['downloadPeak']))

    network_designer.place_routers()
    network_designer.connect_type2_routers_ring()
    network_designer.connect_cities()
    # network_designer.simulate()

    # return jsonify({"message": "Network simulation completed"}), 200
    total_power, img_data, connections_summary = network_designer.simulate()

    return jsonify({
        'total_power': total_power,
        'network_graph': img_data,
        'connections_summary': connections_summary
    })
    # network = NetworkDesigner()

    # # Add cities and number of customers
    # network.add_city("Bengaluru", 64)
    # network.add_city("Hyderabad", 32)
    # network.add_city("Mysuru", 16)
    # network.add_city("Tumkur", 8)

    # # Add connections with peak bandwidths in Tb
    # network.add_connection("Bengaluru", "Hyderabad", 6.4, 3.2)
    # network.add_connection("Bengaluru", "Mysuru", 3.2, 2.4)
    # network.add_connection("Mysuru", "Tumkur", 1.6, 0.8)

    # # Place routers and connect cities
    # network.place_routers()
    # network.connect_type2_routers_ring()
    # network.connect_cities()

    # # Add bandwidth patterns
    # network.add_bandwidth_pattern(1, "Bengaluru", "Hyderabad", 5.0, 2.0)
    # network.add_bandwidth_pattern(2, "Bengaluru", "Mysuru", 2.5, 1.0)
    # network.add_bandwidth_pattern(3, "Mysuru", "Tumkur", 1.0, 0.5)

    # # Simulate network and visualize
    # total_power, img_data, connections_summary = network.simulate()

    # return jsonify({
    #     'total_power':1,
    #     'network_graph': img_data,
    #     'connections_summary': "connections_summary"
    # })
# Example usage
# network = NetworkDesigner()

# # Add cities and number of customers
# network.add_city("Bengaluru", 64)
# network.add_city("Hyderabad", 32)
# network.add_city("Mysuru", 16)
# network.add_city("Tumkur", 8)

# # Add connections with peak bandwidths in Tb
# network.add_connection("Bengaluru", "Hyderabad", 6.4, 3.2)
# network.add_connection("Bengaluru", "Mysuru", 3.2, 2.4)
# network.add_connection("Mysuru", "Tumkur", 1.6, 0.8)

# # Place routers and connect cities
# network.place_routers()
# network.connect_type2_routers_ring()
# network.connect_cities()

# # Add bandwidth patterns
# network.add_bandwidth_pattern(1, "Bengaluru", "Hyderabad", 5.0, 2.0)
# network.add_bandwidth_pattern(2, "Bengaluru", "Mysuru", 2.5, 1.0)
# network.add_bandwidth_pattern(3, "Mysuru", "Tumkur", 1.0, 0.5)

# # Simulate network and visualize
# network.simulate()

if __name__ == '__main__':

    app.run(debug=True)
