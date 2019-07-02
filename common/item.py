#coding: UTF-8 -*-

items = {
    'mysql':{
        'Sent Received':['Bytes_received', 'Bytes_sent'],
        'Com operations': ['Com_select', 'Com_insert', 'Com_update', 'Com_delete', 'Com_replace'],
        'Innodb rows operations':['Innodb_rows_deleted', 'Innodb_rows_inserted', 'Innodb_rows_read', 'Innodb_rows_updated'],
        'Status': ['Slow_queries', 'MySQL_QPS', 'MySQL_TPS', 'Connections']
    },

    'redis':{
        'Memory': ['redis.used_memory', 'redis.used_memory_rss'],
        'Connections': ['redis.connected_clients', 'redis.blocked_clients', 'redis.rejected_connections'],
        'KeyStatus': ['redis.expired_keys', 'redis.evicted_keys', 'redis.keyspace_hits', 'redis.keyspace_misses', 'redis.keys_num']
    },

    'zookeeper':{
        'Sent Received':['zookeeper_stat_received', 'zookeeper_stat_sent'],
        'Status':[
            'zookeeper_stat_connections',
            'zookeeper_stat_outstanding',
            'zookeeper_stat_nodecount',
            'zookeeper_wchs_connections',
            'zookeeper_wchs_watchingpaths',
            'zookeeper_wchs_totalwatches'
        ]
    },
    'nginx':{
        'Status': [
            'nginx.status.active',
            'nginx.status.reading',
            'nginx.status.requests',
            'nginx.status.handled',
            'nginx.status.accepts',
            'nginx.status.waiting',
            'nginx.status.writing'
        ]
    },
    'rabbitmq':{
        'Mem Usage': ['rabbitmq.mem_used'],
        'Used Rate':['rabbitmq.mem_used_rate', 'rabbitmq.proc_used_rate'],
        'Message Number': ['rabbitmq.messages_total', 'rabbitmq.messages_ready', 'rabbitmq.messages_unacknowledged'],
        'Global Counts':['rabbitmq,channels', 'rabbitmq.connections', 'rabbitmq.consumers', 'rabbitmq.exchanges', 'rabbitmq.queues']
    }
}


