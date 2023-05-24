import json
import consul

consul_client = consul.Consul()

consul_client.kv.put("hazelcast-cluster-members", json.dumps(["127.0.0.1"]))
consul_client.kv.put("hazelcast-cluster-name", "dev")
