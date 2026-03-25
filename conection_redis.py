from redis import Redis

r = Redis(host='localhost', port=6379)

print(r.ping())

r.set("jedi2", "Luke Skywalker")
print(r.get("jedi"))

r.lpush("jedis", "Yoda", "Obi-wan", "Mace Windu")
print(r.lrange("jedis", 0, -1))