workload_features = {
        "size": 9,
        "read_ratio": 1.0,
        "group_by_ratio": 0.89,
        "order_by_ratio": 0.89,
        "avg_query_length": 281.9,
        "avg_joins": 1.2,
        "filter_ratio": 0.89,
    }

query_plans = [
        "Merge Join(cost=1915.8)(Index Scan(cost=1016.9); Index Scan(cost=1066.1))",
        "Aggregate(cost=1004.1)(Seq Scan(cost=698.5))",
        "Hash Join(cost=2827.2)(Seq Scan(cost=896.0); Seq Scan(cost=1116.4))",
    ]

inner_metrics = {
        "buffer_hit_ratio": 0.96,
        "avg_response_time": 166.5,
        "lock_wait": 0.02,
        "rows_returned": 1408,
        "deadlocks": 0,
    }

    