import json
import re
from typing import Dict, Tuple, Union

# Configuration schema
config_schema = {
    "max_wal_senders": {"step": 1, "type": "integer", "default": 10.0, "min": 0.0, "max": 50},
    "autovacuum_max_workers": {"step": 1, "type": "integer", "default": 3.0, "min": 1.0, "max": 200},
    "max_connections": {"step": 1, "type": "integer", "default": 100.0, "min": 50.0, "max": 3000},
    "wal_buffers": {"step": 1, "type": "integer", "default": -1, "min": -1.0, "max": 131072},
    "shared_buffers": {"step": 1, "type": "integer", "default": 1024.0, "min": 16.0, "max": 4194304},
    "autovacuum_analyze_scale_factor": {"max": 100, "min": 0, "type": "float", "default": 0.1, "step": 1},
    "autovacuum_analyze_threshold": {"max": 2147483647, "min": 0, "type": "integer", "default": 50.0, "step": 50},
    "autovacuum_naptime": {"max": 2147483, "min": 1, "type": "integer", "default": 60.0, "step": 60},
    "autovacuum_vacuum_cost_delay": {"max": 100, "min": -1, "type": "integer", "default": 2, "step": 1},
    "autovacuum_vacuum_cost_limit": {"max": 10000, "min": -1, "type": "integer", "default": -1.0, "step": 1},
    "autovacuum_vacuum_scale_factor": {"max": 100, "min": 0, "type": "float", "default": 0.2, "step": 1},
    "autovacuum_vacuum_threshold": {"max": 2147483647, "min": 0, "type": "integer", "default": 50.0, "step": 50},
    "backend_flush_after": {"max": 256, "min": 0, "type": "integer", "default": 0.0, "step": 1},
    "bgwriter_delay": {"max": 10000, "min": 10, "type": "integer", "default": 200.0, "step": 10},
    "bgwriter_flush_after": {"max": 256, "min": 0, "type": "integer", "default": 64.0, "step": 1},
    "bgwriter_lru_maxpages": {"max": 1000, "min": 0, "type": "integer", "default": 2, "step": 10},
    "bgwriter_lru_multiplier": {"max": 10, "min": 0, "type": "integer", "default": 2.0, "step": 1},
    "checkpoint_completion_target": {"max": 1, "min": 0, "type": "float", "default": 0.9, "step": 0.1},
    "checkpoint_flush_after": {"max": 256, "min": 0, "type": "integer", "default": 32.0, "step": 2},
    "checkpoint_timeout": {"max": 3600, "min": 30, "type": "integer", "default": 300.0, "step": 10},
    "commit_delay": {"max": 100000, "min": 0, "type": "integer", "default": 0.0, "step": 10},
    "commit_siblings": {"max": 1000, "min": 0, "type": "integer", "default": 5.0, "step": 5},
    "cursor_tuple_fraction": {"max": 1, "min": 0, "type": "float", "default": 0.1, "step": 0.1},
    "deadlock_timeout": {"max": 2147483647, "min": 1, "type": "integer", "default": 1000.0, "step": 10},
    "default_statistics_target": {"max": 10000, "min": 1, "type": "integer", "default": 100.0, "step": 10},
    "effective_cache_size": {"max": 2147483647, "min": 1, "type": "integer", "default": 524288.0, "step": 64},
    "effective_io_concurrency": {"max": 1000, "min": 0, "type": "integer", "default": 1.0, "step": 1},
    "from_collapse_limit": {"max": 2147483647, "min": 1, "type": "integer", "default": 8.0, "step": 8},
    "geqo_effort": {"max": 10, "min": 1, "type": "integer", "default": 5.0, "step": 1},
    "geqo_generations": {"max": 2147483647, "min": 0, "type": "integer", "default": 0.0, "step": 8},
    "geqo_pool_size": {"max": 2147483647, "min": 0, "type": "integer", "default": 0.0, "step": 8},
    "geqo_seed": {"max": 1, "min": 0, "type": "float", "default": 0.0, "step": 0.1},
    "geqo_threshold": {"max": 2147483647, "min": 2, "type": "integer", "default": 12.0, "step": 12},
    "join_collapse_limit": {"max": 2147483647, "min": 1, "type": "integer", "default": 8.0, "step": 8},
    "maintenance_work_mem": {"max": 2147483647, "min": 1024, "type": "integer", "default": 65536.0, "step": 128},
    "temp_buffers": {"max": 1073741823, "min": 100, "type": "integer", "default": 1024.0, "step": 32},
    "temp_file_limit": {"max": 2147483647, "min": -1, "type": "integer", "default": -1.0, "step": 32},
    "vacuum_cost_delay": {"max": 100, "min": 0, "type": "integer", "default": 0.0, "step": 1},
    "vacuum_cost_limit": {"max": 10000, "min": 1, "type": "integer", "default": 200.0, "step": 10},
    "vacuum_cost_page_dirty": {"max": 10000, "min": 0, "type": "integer", "default": 20.0, "step": 5},
    "vacuum_cost_page_hit": {"max": 10000, "min": 0, "type": "integer", "default": 1.0, "step": 1},
    "vacuum_cost_page_miss": {"max": 10000, "min": 0, "type": "integer", "default": 2.0, "step": 5},
    "wal_writer_delay": {"max": 10000, "min": 1, "type": "integer", "default": 200.0, "step": 5},
    "work_mem": {"max": 2147483647, "min": 64, "type": "integer", "default": 4096.0, "step": 64}
}

# Percentage input
percentage_input = {
    "max_wal_senders": "10% to 20%",
    "autovacuum_max_workers": "40% to 50%",
    "max_connections": "50% to 60%",
    "wal_buffers": "80% to 90%",
    "shared_buffers": "00% to 10%",
    "autovacuum_analyze_scale_factor": "40% to 50%",
    "autovacuum_analyze_threshold": "70% to 80%",
    "autovacuum_naptime": "40% to 50%",
    "autovacuum_vacuum_cost_delay": "90% to 100%",
    "autovacuum_vacuum_cost_limit": "60% to 70%",
    "autovacuum_vacuum_scale_factor": "20% to 30%",
    "autovacuum_vacuum_threshold": "70% to 80%",
    "backend_flush_after": "30% to 40%",
    "bgwriter_delay": "90% to 100%",
    "bgwriter_flush_after": "20% to 30%",
    "bgwriter_lru_maxpages": "70% to 80%",
    "bgwriter_lru_multiplier": "10% to 20%",
    "checkpoint_completion_target": "90% to 100%",
    "checkpoint_flush_after": "70% to 80%",
    "checkpoint_timeout": "60% to 70%",
    "commit_delay": "90% to 100%",
    "commit_siblings": "90% to 100%",
    "cursor_tuple_fraction": "00% to 10%",
    "deadlock_timeout": "70% to 80%",
    "default_statistics_target": "80% to 90%",
    "effective_cache_size": "60% to 70%",
    "effective_io_concurrency": "10% to 20%",
    "from_collapse_limit": "40% to 50%",
    "geqo_effort": "70% to 80%",
    "geqo_generations": "70% to 80%",
    "geqo_pool_size": "90% to 100%",
    "geqo_seed": "90% to 100%",
    "geqo_threshold": "60% to 70%",
    "join_collapse_limit": "50% to 60%",
    "maintenance_work_mem": "10% to 20%",
    "temp_buffers": "10% to 20%",
    "temp_file_limit": "middle",
    "vacuum_cost_delay": "40% to 50%",
    "vacuum_cost_limit": "80% to 90%",
    "vacuum_cost_page_dirty": "30% to 40%",
    "vacuum_cost_page_hit": "50% to 60%",
    "vacuum_cost_page_miss": "90% to 100%",
    "wal_writer_delay": "60% to 70%",
    "work_mem": "60% to 70%"
}


def parse_percentage(percent_str: str) -> Tuple[float, float]:
    """Parse percentage string to get min and max percentages."""
    if percent_str.lower() == "middle":
        return (50.0, 50.0)
    
    match = re.match(r'(\d+)%\s*to\s*(\d+)%', percent_str)
    if match:
        return (float(match.group(1)), float(match.group(2)))
    
    raise ValueError(f"Invalid percentage format: {percent_str}")


def calculate_value(config: Dict, percent_min: float, percent_max: float) -> Dict[str, Union[int, float]]:
    """Calculate actual values from percentage ranges."""
    value_range = config['max'] - config['min']
    min_val = config['min'] + (value_range * percent_min / 100)
    max_val = config['min'] + (value_range * percent_max / 100)
    
    if config['type'] == 'integer':
        return {
            'min': round(min_val),
            'max': round(max_val)
        }
    else:  # float
        return {
            'min': round(min_val, 2),
            'max': round(max_val, 2)
        }


def map_percentage_to_values(config_schema: Dict, percentage_input: Dict) -> Dict:
    """Map all percentage ranges to actual configuration values."""
    results = {}
    
    for key, percent_str in percentage_input.items():
        if key not in config_schema:
            print(f"Warning: {key} not found in config schema")
            continue
        
        config = config_schema[key]
        
        try:
            percent_min, percent_max = parse_percentage(percent_str)
            values = calculate_value(config, percent_min, percent_max)
            
            results[key] = {
                'percentage_range': percent_str,
                'value_range': f"{values['min']} to {values['max']}",
                'min': values['min'],
                'max': values['max'],
                'default': config['default'],
                'config_min': config['min'],
                'config_max': config['max'],
                'type': config['type']
            }
        except Exception as e:
            print(f"Error processing {key}: {e}")
    
    return results


def print_results(results: Dict, detailed: bool = True):
    """Print the mapping results in a readable format."""
    print("\n" + "="*80)
    print("PostgreSQL Configuration Mapping: Percentage Ranges to Actual Values")
    print("="*80 + "\n")
    
    for key, data in sorted(results.items()):
        print(f"Parameter: {key}")
        print(f"  Percentage Range: {data['percentage_range']}")
        print(f"  Actual Value Range: {data['value_range']}")
        
        if detailed:
            print(f"  Min Value: {data['min']}")
            print(f"  Max Value: {data['max']}")
            print(f"  Default: {data['default']}")
            print(f"  Config Bounds: {data['config_min']} to {data['config_max']}")
            print(f"  Type: {data['type']}")
        
        print()


def export_to_json(results: Dict, filename: str = 'postgres_config_ranges.json'):
    """Export results to JSON file."""
    export_data = {}
    for key, data in results.items():
        export_data[key] = {
            'range': data['value_range'],
            'min': data['min'],
            'max': data['max'],
            'percentage': data['percentage_range']
        }
    
    with open(filename, 'w') as f:
        json.dump(export_data, f, indent=2)
    
    print(f"Results exported to {filename}")


def get_value_for_parameter(results: Dict, param_name: str) -> Dict:
    """Get the mapped values for a specific parameter."""
    if param_name in results:
        return results[param_name]
    else:
        return None


# Main execution
if __name__ == "__main__":
    # Map percentage ranges to actual values
    mapped_values = map_percentage_to_values(config_schema, percentage_input)
    
    # Print results
    print_results(mapped_values, detailed=True)
    
    # Export to JSON
    export_to_json(mapped_values)
    
    # # Example: Get specific parameter
    # print("\n" + "="*80)
    # print("Example: Looking up specific parameter")
    # print("="*80)
    # param = "max_connections"
    # value = get_value_for_parameter(mapped_values, param)
    # if value:
    #     print(f"\n{param}:")
    #     print(f"  Range: {value['value_range']}")
    #     print(f"  Min: {value['min']}, Max: {value['max']}")