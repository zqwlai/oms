#coding: UTF-8 -*-

items = {
    'mysql':{
        'Sent Received':['MySQL.bytes.received', 'MySQL.bytes.sent'],
        'Com operations': ['Com.select', 'Com.insert', 'Com.update', 'Com.delete', 'Com.replace'],
        #'Innodb rows operations':['Innodb_rows_deleted', 'Innodb_rows_inserted', 'Innodb_rows_read', 'Innodb_rows_updated'],
        'Slow Queries':['Slow.queries'],
        'QPS/TPS': ['MySQL.QPS', 'MySQL.TPS'],
        'Connections':['MySQL.Connections']
    },

    'redis':{
        'Memory': ['redis.used.memory', 'redis.used.memory.rss'],
        'Connections': ['redis.connected.clients', 'redis.blocked.clients', 'redis.rejected.connections'],
        'KeyStatus': ['redis.expired.keys', 'redis.evicted.keys', 'redis.keyspace.hits', 'redis.keyspace.misses', 'redis.keys.num']
    },

    'zookeeper':{
        'Sent Received':['zookeeper.stat.received', 'zookeeper.stat.sent'],
        'Status':[
            'zookeeper.stat.connections',
            'zookeeper.stat.outstanding',
            'zookeeper.stat.nodecount',
            'zookeeper.wchs.connections',
            'zookeeper.wchs.watchingpaths',
            'zookeeper.wchs.totalwatches'
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
        'Used Percent':['rabbitmq.mem.used.percent', 'rabbitmq.proc.used.percent'],
        'Message Number': ['rabbitmq.messages.total', 'rabbitmq.messages.ready', 'rabbitmq.messages.unacknowledged'],
        'Global Counts':['rabbitmq,channels', 'rabbitmq.connections', 'rabbitmq.consumers', 'rabbitmq.exchanges', 'rabbitmq.queues']
    },
    'elasticsearch':{
        'nodes count': ['es.nodes.count.data', 'es.nodes.count.master', 'es.nodes.count.total'],
        'indices count': ['es.indices.count'],
        'docs.count': ['es.docs.count'],
        'shards': ['es.shards.total', 'es.shards.primaries'],
        'mem.used.percent': ['es.mem.used.percent'],
        'fs.used.percent': ['es.fs.used.percent'],
        'cpu.percent': ['es.nodes.cpu.percent']
    },
    'docker':{
        'cpu.usage': ['cpu.busy', 'cpu.user', 'cpu.system'],
        'mem.usage': ['mem.memused','mem.memused.hot', 'mem.memtotal'],
        'mem.used.percent': ['mem.memused.percent'],
        'disk.io': ['disk.io.read_bytes', 'disk.io.write_bytes'],
        'net.if':['net.if.in.bytes', 'net.if.out.bytes']
    },
    'jmx':{
        'parnew.gc.avg.time': ['parnew.gc.avg.time'],
        'parnew.gc.count': ['parnew.gc.count'],
        'gc.throughput': ['gc.throughput'],
        'new.gen.promotion': ['new.gen.promotion'],
        'new.gen.avg.promotion': ['new.gen.avg.promotion'],
        'old.gen.mem.used': ['old.gen.mem.used'],
        'old.gen.mem.ratio': ['old.gen.mem.ratio'],
        'thread.active.count': ['thread.active.count'],
        'thread.peak.count': ['thread.peak.count']
    }
}


