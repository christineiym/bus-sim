import simpy


class Passenger(object):
    def __init__(self, env):
        self.env = env
        self.action = env.process(self.run())
    
    def run(self):
        while True:
            # Start riding
            print('Start riding at %d' % self.env.now)
            trip_duration = 2  # this is what we're trying to figure out
            yield self.env.timeout(trip_duration)


def main():
    print("hello!")
    env = simpy.Environment()
    bus = simpy.Resource(env, capacity=100)

if __name__ == "__main__":
    main()