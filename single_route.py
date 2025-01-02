import random
import plotly.graph_objects as go

class Passenger:
    def __init__(self, on_stop):
        self.on_stop = on_stop
        self.off_stop = "n/a"
    
    def set_off_stop(self, off_stop):
        self.off_stop = off_stop
    
    def trip_info(self) -> str:
        trip_info_string = f"{self.on_stop} - {self.off_stop}"
        return trip_info_string

def main():
    # ons = [3, 2, 4, 0]
    # offs = [0, 2, 2, 5]  # is this a valid set of ons/offs?
    # stops = ["s1", "s2", "s3", "s4"]

    stops = ['BRADDOCK AVE AT 2ND ST', 'BRADDOCK AVE AT 4TH ST', 'BRADDOCK AVE AT COREY AVE', 'BRADDOCK AVE AT LINE AVE', '7TH ST AT BRADDOCK AVE', '6TH ST AT MARGARETTA ST', '6TH ST AT BRADDOCK AVE', 'YOST BLVD AT BRINTON RD FS', 'BRADDOCK AVE AT GREENDALE AVE FS', 'BRADDOCK AVE AT HUTCHINSON ST', 'BRADDOCK AVE AT SANDERS ST', 'BRADDOCK AVE OPP CHARLESTON AVE', '6TH ST AT BALDRIDGE AVE', 'YOST BLVD OPP MAIN ST', 'BRADDOCK AVE AT BIDDLE AVE', 'BRADDOCK AVE AT HENRIETTA ST', 'BRADDOCK AVE AT GUTHRIE ST', 'FIFTH AVE AT KIRKPATRICK ST FS', 'FIFTH AVE AT MOULTRIE ST FS', 'FIFTH AVE AT WYANDOTTE ST', 'FIFTH AVE OPP SENECA ST', 'FIFTH AVE AT DINWIDDIE ST', 'FIFTH AVE OPP VAN BRAAM ST', 'NORTH SIDE STATION', 'FIFTH AVE OPP GIST ST', 'FIFTH AVE AT MAGEE ST', 'FIFTH AVE AT WASHINGTON PL', 'FIFTH AVE OPP DIAMOND ST', 'SIXTH AVE AT BIGELOW BLVD', 'SIXTH AVE AT SMITHFIELD ST', 'SIXTH AVE AT WOOD ST', 'SIXTH AVE AT CENTRE AVE', 'FORBES AVE AT BRADDOCK AVE FS', 'FORBES AVE AT DALLAS AVE', 'FORBES AVE AT BEECHWOOD BLVD', 'FORBES AVE AT BEELER ST', 'FORBES AVE BTW DENNISTON ST & SHADY AVE', 'FORBES AVE AT MURDOCH ST', 'FORBES AVE AT MURRAY AVE FS', 'FORBES AVE AT NORTHUMBERLAND ST FS', 'FORBES AVE AT PLAINFIELD ST', 'FORBES AVE AT WIGHTMAN ST', 'FORBES AVE OPP MARGARET MORRISON ST', 'RANKIN BLVD AT HAWKINS AVE', 'RANKIN BLVD AT KENMAWR AVE FS', 'MONONGAHELA AVE AT CHURCH ST', 'MONONGAHELA AVE AT IRVINE ST', 'MONONGAHELA AVE OPP WHIPPLE ST (#1641)', 'BRADDOCK AVE AT OVERTON ST']
    ons = [379.0, 445.0, 686.0, 284.0, 40.0, 11.0, 109.0, 71.0, 243.0, 599.0, 187.0, 321.0, 144.0, 10.0, 354.0, 204.0, 127.0, 32.0, 20.0, 159.0, 44.0, 114.0, 38.0, 491.0, 40.0, 67.0, 136.0, 57.0, 22.0, 737.0, 1032.0, 52.0, 750.0, 293.0, 190.0, 193.0, 1345.0, 632.0, 2959.0, 128.0, 99.0, 1595.0, 335.0, 244.0, 163.0, 801.0, 128.0, 393.0, 291.0]
    offs = [38.0, 56.0, 36.0, 37.0, 7.0, 17.0, 49.0, 14.0, 8.0, 50.0, 46.0, 17.0, 127.0, 3.0, 21.0, 23.0, 26.0, 34.0, 49.0, 92.0, 88.0, 136.0, 44.0, 803.0, 59.0, 118.0, 306.0, 123.0, 276.0, 2727.0, 2545.0, 1925.0, 91.0, 20.0, 16.0, 141.0, 431.0, 37.0, 1093.0, 14.0, 21.0, 61.0, 455.0, 111.0, 61.0, 324.0, 42.0, 34.0, 0.0]
    
    bus = []
    completed_trips = []

    times_to_simulate = 100
    trip_summaries = {}

    for x in range(times_to_simulate):
        # Simulate the trip
        i = 0
        while i < len(stops):
            # offs
            j = 0
            while j < offs[i]:
                if len(bus) > 0:
                    random_index = random.randint(0, len(bus) - 1)
                    exited_passenger: Passenger = bus.pop(random_index)
                    exited_passenger.set_off_stop(stops[i])
                    completed_trips.append(exited_passenger)
                j += 1

            # ons
            k = 0
            while k < ons[i]:
                bus.append(Passenger(stops[i]))
                k += 1
            i += 1
        
        # Compile trip info
        trip_summary = bus_trips_summary(completed_trips)
        if trip_summary in trip_summaries:
            trip_summaries[trip_summary] += 1
        else:
            trip_summaries[trip_summary] = 1
        
        bus = []
        completed_trips = []
    
    # for item in trip_summaries:
    #     print(str(item) + " occurred " + str(trip_summaries[item]) + " times.")

    # show sankey
    max_value = max(trip_summaries.values())
    keys_with_highest_value = [key for key, value in trip_summaries.items() if value == max_value]
    random_key = random.choice(keys_with_highest_value)
    pairs = random_key.split(", ")
    print(pairs)
    origin_dest = [pair.split(": ")[0] for pair in pairs]
    origin = [origin_dest_pair.split(" - ")[0] for origin_dest_pair in origin_dest]
    dest = [origin_dest_pair.split(" - ")[1] for origin_dest_pair in origin_dest]
    origin_index = [stops.index(curr_origin) + 1 for curr_origin in origin]
    dest_index = [stops.index(curr_dest) + 1 for curr_dest in dest]
    values = [int(pair.split(": ")[1]) for pair in pairs]

    fig = go.Figure(data=[go.Sankey(
        node = dict(
        pad = 15,
        thickness = 10,
        line = dict(color = "black", width = 0.5),
        label = stops,
        color = "blue"
        ),
        link = dict(
        source = origin_index,
        target = dest_index,
        value = values
    ))])

    fig.update_layout(title_text="Passenger Flow Between Stops", font_size=10)
    fig.show()


def bus_trips_summary(passengers: list[Passenger]):
    trip_summary = {}
    for passenger in passengers:
        curr_passenger = passenger.trip_info()
        if curr_passenger in trip_summary:
            trip_summary[curr_passenger] += 1
        else:
            trip_summary[curr_passenger] = 1
    trip_summary_strings = [str(key) + ": " + str(trip_summary[key]) for key in trip_summary]
    trip_summary_strings.sort()
    trip_summary_string = ", ".join(trip_summary_strings)
    return trip_summary_string


if __name__ == "__main__":
    main()