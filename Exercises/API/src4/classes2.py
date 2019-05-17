class Flight:

    def __init__(self, origin, destination, duration):
        self.origin = origin
        self.destination = destination
        self.duration = duration

    def __str__(self):
        return("Flight origin:"+self.origin)
        


def main():

    f1 = Flight(origin="New York", destination="Paris", duration=540)
    print(f1)
    f2 = Flight(origin="Tokyo", destination="Shanghai", duration=185)
    print(f2)

if __name__ == "__main__":
    main()
