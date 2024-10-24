from flask import Flask, jsonify, request, render_template
from graph import Graph, RoutePlanner

app = Flask(__name__)
graph = Graph()
planner = RoutePlanner(graph, vehicle_efficiency=25)  # Example vehicle efficiency

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_node', methods=['POST'])
def add_node():
    data = request.get_json()
    node = data.get('node')
    graph.add_node(node)
    return jsonify({'message': f'Node {node} added successfully!'})

@app.route('/add_edge', methods=['POST'])
def add_edge():
    data = request.get_json()
    graph.add_edge(data['from_node'], data['to_node'], data['distance'], data['speed_limit'], data['traffic_factor'])
    return jsonify({'message': f'Edge from {data["from_node"]} to {data["to_node"]} added successfully!'})

@app.route('/find_route', methods=['GET'])
def find_route():
    start = request.args.get('start')
    end = request.args.get('end')
    result = planner.find_most_efficient_route(start, end)
    
    if result:
        return jsonify({'time': result[0], 'fuel': result[1]})
    else:
        return jsonify({'error': 'No valid route found.'}), 404

@app.route('/get_nodes', methods=['GET'])
def get_nodes():
    nodes_list = list(graph.nodes)
    return jsonify({'nodes': nodes_list})

@app.route('/get_edges', methods=['GET'])
def get_edges():
    edges_list = []
    for from_node, edges in graph.edges.items():
        for edge in edges:
            edges_list.append({
                'from': from_node,
                'to': edge['to'],
                'distance': edge['distance'],
                'speed_limit': edge['speed_limit'],
                'traffic_factor': edge['traffic_factor']
            })
    return jsonify(edges_list)

if __name__ == '__main__':
    app.run(debug=True)
