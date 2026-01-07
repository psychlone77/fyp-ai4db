import re
import json
from typing import List, Dict, Any
from pathlib import Path

class WorkloadFeatureGenerator:
    """
    Analyzes SQL workloads and generates feature summaries including:
    - Workload statistics (size, ratios, query characteristics)
    """
    
    def __init__(self):
        self.queries = []
        
    def parse_queries(self, query_list: List[str]) -> None:
        """Parse and store queries for analysis"""
        self.queries = [q.strip() for q in query_list if q.strip()]
    
    def load_queries_from_file(self, file_path: str) -> None:
        """Load queries from SQL file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split by semicolon to get individual queries
        queries = [q.strip() for q in content.split(';') if q.strip()]
        self.parse_queries(queries)
    
    def analyze_workload_features(self) -> Dict[str, Any]:
        """Extract workload-level features from queries"""
        features = {
            'size': len(self.queries),
            'read_ratio': 0.0,
            'group_by_ratio': 0.0,
            'order_by_ratio': 0.0,
            'avg_query_length': 0.0,
            'avg_joins': 0.0,
            'filter_ratio': 0.0
        }
        
        if not self.queries:
            return features
        
        read_count = 0
        group_by_count = 0
        order_by_count = 0
        total_length = 0
        total_joins = 0
        filter_count = 0
        
        for query in self.queries:
            query_upper = query.upper()
            
            # Count SELECT queries (reads)
            if 'SELECT' in query_upper and not any(kw in query_upper for kw in ['INSERT', 'UPDATE', 'DELETE']):
                read_count += 1
            
            # Count GROUP BY
            if 'GROUP BY' in query_upper:
                group_by_count += 1
            
            # Count ORDER BY
            if 'ORDER BY' in query_upper:
                order_by_count += 1
            
            # Query length (character count)
            total_length += len(query)
            
            # Count JOINs
            join_count = len(re.findall(r'\bJOIN\b', query_upper))
            total_joins += join_count
            
            # Count WHERE clauses (filters)
            if 'WHERE' in query_upper:
                filter_count += 1
        
        num_queries = len(self.queries)
        features['read_ratio'] = round(read_count / num_queries, 2)
        features['group_by_ratio'] = round(group_by_count / num_queries, 2)
        features['order_by_ratio'] = round(order_by_count / num_queries, 2)
        features['avg_query_length'] = round(total_length / num_queries, 1)
        features['avg_joins'] = round(total_joins / num_queries, 1)
        features['filter_ratio'] = round(filter_count / num_queries, 2)
        
        return features
    
    def generate_feature_string(self) -> str:
        """Generate the complete feature string in the required format"""
        workload_features = self.analyze_workload_features()
        
        # Format workload features
        workload_str = (
            f"workload features: size of workload: {workload_features['size']}; "
            f"read ratio: {workload_features['read_ratio']}; "
            f"group by ratio: {workload_features['group_by_ratio']}; "
            f"order by ratio: {workload_features['order_by_ratio']}; "
            f"avg query length: {workload_features['avg_query_length']}; "
            f"number of joins: {workload_features['avg_joins']}; "
            f"filter ratio: {workload_features['filter_ratio']};"
        )
        
        return workload_str
    
    def save_to_json(self, output_path: str) -> None:
        """Save workload features to JSON file"""
        workload_features = self.analyze_workload_features()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(workload_features, f, indent=2)
        
        print(f"Workload features saved to: {output_path}")


# Example usage
if __name__ == "__main__":
    # Get script directory
    script_dir = Path(__file__).parent.parent
    
    # Path to SQL workload file
    workload_file = script_dir / 'olap_input_files' / 'job_0_workload.sql'
    
    # Output JSON file path
    output_json = script_dir / 'olap_input_files' / 'workload_features.json'
    
    # Check if file exists
    if not workload_file.exists():
        print(f"Error: File not found at {workload_file}")
        exit(1)
    
    print(f"Loading queries from: {workload_file}\n")
    
    # Generate features
    generator = WorkloadFeatureGenerator()
    generator.load_queries_from_file(str(workload_file))
    
    print(f"Loaded {len(generator.queries)} queries\n")
    
    # Generate and display feature string
    input_features = generator.generate_feature_string()
    print(input_features)
    print("\n" + "="*80 + "\n")
    
    # Display individual components
    print("Workload Features:")
    workload_features = generator.analyze_workload_features()
    print(workload_features)
    print("\n" + "="*80 + "\n")
    
    # Save to JSON
    generator.save_to_json(str(output_json))