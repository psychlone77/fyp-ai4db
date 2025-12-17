import re
from typing import List, Dict, Any
import random

class WorkloadFeatureGenerator:
    """
    Analyzes SQL workloads and generates feature summaries including:
    - Workload statistics (size, ratios, query characteristics)
    - Query plan summaries
    - Performance metrics
    """
    
    def __init__(self):
        self.queries = []
        
    def parse_queries(self, query_list: List[str]) -> None:
        """Parse and store queries for analysis"""
        self.queries = [q.strip() for q in query_list if q.strip()]
    
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
    
    def generate_query_plans(self) -> List[str]:
        """
        Generate simplified query plan representations
        In production, you'd get these from EXPLAIN ANALYZE
        """
        plans = []
        plan_templates = [
            "Aggregate(cost={agg_cost})(Seq Scan(cost={scan_cost}))",
            "Nested Loop(cost={nl_cost})(Index Scan(cost={idx_cost}); Seq Scan(cost={seq_cost}))",
            "Hash Join(cost={hj_cost})(Seq Scan(cost={s1_cost}); Seq Scan(cost={s2_cost}))",
            "Sort(cost={sort_cost})(Aggregate(cost={agg_cost})(Seq Scan(cost={scan_cost})))",
            "Merge Join(cost={mj_cost})(Index Scan(cost={i1_cost}); Index Scan(cost={i2_cost}))"
        ]
        
        # Generate 2-3 representative plans
        num_plans = min(3, max(2, len(self.queries) // 3))
        
        for _ in range(num_plans):
            template = random.choice(plan_templates)
            # Generate realistic costs
            costs = {
                'agg_cost': round(random.uniform(800, 1500), 1),
                'scan_cost': round(random.uniform(500, 800), 1),
                'nl_cost': round(random.uniform(1500, 2500), 1),
                'idx_cost': round(random.uniform(1000, 1500), 1),
                'seq_cost': round(random.uniform(600, 1000), 1),
                'hj_cost': round(random.uniform(2000, 3000), 1),
                's1_cost': round(random.uniform(800, 1200), 1),
                's2_cost': round(random.uniform(800, 1200), 1),
                'sort_cost': round(random.uniform(1200, 1800), 1),
                'mj_cost': round(random.uniform(1800, 2800), 1),
                'i1_cost': round(random.uniform(900, 1400), 1),
                'i2_cost': round(random.uniform(900, 1400), 1)
            }
            plans.append(template.format(**costs))
        
        return plans
    
    def generate_inner_metrics(self) -> Dict[str, Any]:
        """
        Generate database performance metrics
        In production, these would come from database monitoring
        """
        return {
            'buffer_hit_ratio': round(random.uniform(0.95, 0.99), 2),
            'avg_response_time': round(random.uniform(80, 200), 1),
            'lock_wait': round(random.uniform(0.01, 0.05), 2),
            'rows_returned': random.randint(500, 2000),
            'deadlocks': random.randint(0, 2)
        }
    
    def generate_feature_string(self) -> str:
        """Generate the complete feature string in the required format"""
        workload_features = self.analyze_workload_features()
        query_plans = self.generate_query_plans()
        inner_metrics = self.generate_inner_metrics()
        
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
        
        # Format query plans
        plans_str = "query plans in workload: " + "; ".join(query_plans) + ";"
        
        # Format inner metrics
        metrics_str = (
            f"inner metrics: buffer hit ratio: {inner_metrics['buffer_hit_ratio']}; "
            f"average response time: {inner_metrics['avg_response_time']}ms; "
            f"lock wait: {inner_metrics['lock_wait']}; "
            f"rows returned: {inner_metrics['rows_returned']}; "
            f"deadlocks: {inner_metrics['deadlocks']};"
        )
        
        return f"{workload_str}\n{plans_str}\n{metrics_str}"


# Example usage
if __name__ == "__main__":
    # Your workload queries
    queries = [
        """SELECT t.title, COUNT(c.movie_id) AS num_cast_members 
           FROM title AS t JOIN cast_info AS c ON t.id = c.movie_id 
           WHERE t.production_year BETWEEN 2000 AND 2020 
           GROUP BY t.title HAVING COUNT(c.movie_id) > 10 
           ORDER BY num_cast_members DESC;""",
        
        """SELECT k.keyword, COUNT(mk.movie_id) AS num_movies 
           FROM keyword AS k JOIN movie_keyword AS mk ON k.id = mk.keyword_id 
           GROUP BY k.keyword HAVING COUNT(mk.movie_id) > 100 
           ORDER BY num_movies DESC;""",
        
        """SELECT n.name, COUNT(ci.person_id) AS num_roles 
           FROM name AS n JOIN cast_info AS ci ON n.id = ci.person_id 
           WHERE ci.role_id IN (1, 2) GROUP BY n.name 
           HAVING COUNT(ci.person_id) > 50 ORDER BY num_roles DESC;""",
        
        """SELECT t.title, AVG(mi.info::integer) AS average_rating 
           FROM title AS t JOIN movie_info AS mi ON t.id = mi.movie_id 
           WHERE mi.info_type_id = 101 AND t.production_year BETWEEN 2000 AND 2020 
           GROUP BY t.title HAVING AVG(mi.info::integer) > 7 
           ORDER BY average_rating DESC;""",
        
        """SELECT t1.title AS movie1, t2.title AS movie2, lt.link 
           FROM movie_link AS ml JOIN title AS t1 ON ml.movie_id = t1.id 
           JOIN title AS t2 ON ml.linked_movie_id = t2.id 
           JOIN link_type AS lt ON ml.link_type_id = lt.id 
           WHERE ml.link_type_id IN (9, 10, 12) 
           AND t1.production_year BETWEEN 2000 AND 2020;""",
        
        """SELECT t.title, COUNT(mc.company_id) AS num_companies 
           FROM title AS t JOIN movie_companies AS mc ON t.id = mc.movie_id 
           WHERE t.production_year BETWEEN 2000 AND 2020 
           GROUP BY t.title HAVING COUNT(mc.company_id) > 5 
           ORDER BY num_companies DESC;""",
        
        """SELECT t.title, COUNT(mk.keyword_id) AS num_keywords 
           FROM title AS t JOIN movie_keyword AS mk ON t.id = mk.movie_id 
           WHERE t.production_year BETWEEN 2000 AND 2020 
           GROUP BY t.title HAVING COUNT(mk.keyword_id) > 20 
           ORDER BY num_keywords DESC;""",
        
        """SELECT n.name, COUNT(pi.person_id) AS num_facts 
           FROM name AS n JOIN person_info AS pi ON n.id = pi.person_id 
           WHERE pi.info_type_id IN (2, 3, 4) GROUP BY n.name 
           HAVING COUNT(pi.person_id) > 10 ORDER BY num_facts DESC;""",
        
        """SELECT t.title, COUNT(mi.movie_id) AS num_movie_info 
           FROM title AS t JOIN movie_info AS mi ON t.id = mi.movie_id 
           WHERE t.production_year BETWEEN 2000 AND 2020 
           GROUP BY t.title HAVING COUNT(mi.movie_id) > 15 
           ORDER BY num_movie_info DESC;"""
    ]
    
    # Generate features
    generator = WorkloadFeatureGenerator()
    generator.parse_queries(queries)
    
    input_features = generator.generate_feature_string()
    print(input_features)
    print("\n" + "="*80 + "\n")
    
    # Display individual components
    print("Workload Features:")
    print(generator.analyze_workload_features())
    print("\nQuery Plans:")
    for plan in generator.generate_query_plans():
        print(f"  - {plan}")
    print("\nInner Metrics:")
    print(generator.generate_inner_metrics())