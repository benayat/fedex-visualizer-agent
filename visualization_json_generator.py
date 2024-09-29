import json


def generate_visualization_call(analysis_result):
    measure_type = analysis_result['measure_type']
    params = construct_params(analysis_result)

    visualization_call = {
        'measure_type': measure_type,
        'parameters': params
    }

    # Convert to JSON string
    visualization_json = json.dumps(visualization_call, indent=4)
    return visualization_json


def construct_params(analysis_result):
    measure_type = analysis_result['measure_type']
    if measure_type == 'Exceptionality':
        # Construct parameters for ExceptionalityMeasure
        params = {
            'x': ['Value1', 'Value2', 'Value3'],
            'y': [10, 20, 5],
            'items_to_bold': [analysis_result['max_value']],
            'xname': analysis_result['col_name'],
            'yname': 'Frequency'
        }
    elif measure_type == 'Diversity':
        # Construct parameters for DiversityMeasure
        params = {
            'x': ['Category A', 'Category B', 'Category C'],
            'y': [0.3, 0.5, 0.2],
            'avg_line': 0.4,
            'items_to_bold': [analysis_result['max_value']],
            'xname': analysis_result['col_name'],
            'yname': 'Proportion'
        }
    elif measure_type == 'Shapley':
        # Construct parameters for ShapleyMeasure
        params = {
            'x': ['Feature1', 'Feature2', 'Feature3'],
            'y': [0.1, 0.6, 0.3],
            'items_to_bold': [analysis_result['max_value']],
            'xname': analysis_result['col_name'],
            'yname': 'Shapley Value'
        }
    else:
        raise ValueError(f"Unsupported measure type: {measure_type}")

    return params