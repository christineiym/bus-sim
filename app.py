from flask import Flask, render_template, g, request, url_for, flash, redirect
import plotly.graph_objects as go
import plotly.io as pio
import random
import json
import sqlite3
import os

# port = process.env.PORT | 5000

app = Flask(__name__, template_folder='./')

DATABASE = './bus_data.db'

DEMO_ROUTE_SCHEDULE = """
    SELECT stop_name, direction, total_ons, total_offs
               FROM Stop_Usage S
               WHERE route_name = "1"
                AND serviceday = "Sat"
                AND datekey = 201909
                AND direction = "Both"
            ORDER BY direction;
"""
ROUTE_SCHEDULE = """
    SELECT stop_name, direction, total_ons, total_offs
               FROM Stop_Usage S
               WHERE route_name = ?
                AND serviceday = ?
                AND datekey = ?
                AND direction = ?
            ORDER BY direction;
"""

# how to validate?
MENU_ROUTE = """
    SELECT DISTINCT route_name FROM Stop_Usage S ORDER BY route_name;
"""
MENU_SERVICE_DAY = """
    SELECT DISTINCT serviceday FROM Stop_Usage S ORDER BY serviceday;
"""
MENU_DATE = """
    SELECT DISTINCT datekey FROM Stop_Usage S ORDER BY datekey;
"""
MENU_DIRECTION = """
    SELECT DISTINCT direction FROM Stop_Usage S ORDER BY direction;
"""

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

class Passenger:
    def __init__(self, on_stop):
        self.on_stop = on_stop
        self.off_stop = "n/a"
    
    def set_off_stop(self, off_stop):
        self.off_stop = off_stop
    
    def trip_info(self) -> str:
        trip_info_string = f"{self.on_stop} --- {self.off_stop}"
        return trip_info_string

@app.route('/', methods=('GET', 'POST'))
def index():
    # ons = [3, 2, 4, 0]
    # offs = [0, 2, 2, 5]  # is this a valid set of ons/offs?
    # stops = ["s1", "s2", "s3", "s4"]

    cursor = get_db().cursor()

    cursor.execute(MENU_ROUTE)
    result = cursor.fetchall()
    menu_route_list = [item[0] for item in result]

    cursor.execute(MENU_SERVICE_DAY)
    result = cursor.fetchall()
    menu_service_day_list = [item[0] for item in result]

    cursor.execute(MENU_DATE)
    result = cursor.fetchall()
    menu_date_list = [item[0] for item in result]

    cursor.execute(MENU_DIRECTION)
    result = cursor.fetchall()
    menu_direction_list = [item[0] for item in result]

    route_name = "1"
    service_day = "Weekday"
    date = "202001"
    direction = "Inbound"

    cursor.execute(ROUTE_SCHEDULE, (route_name, service_day, date, direction,))
    result = cursor.fetchall()
    stops = [item[0] for item in result]
    ons = [item[2] for item in result]
    offs = [item[3] for item in result]
    # print(stops)

    if request.method == 'POST':
        route_name = request.form['route_name']
        service_day = request.form['service_day']
        date = request.form['date']
        direction = request.form['direction']

        if not route_name:
            flash('Route name is required!')
        elif not service_day:
            flash('Service day is required!')
        elif not date:
            flash('Date is required!')
        elif not direction:
            flash('Direction is required!')
        else:
            # messages.append({'title': title, 'content': content})
            # return redirect(url_for('index'))
            cursor.execute(ROUTE_SCHEDULE, (route_name, service_day, date, direction,))
            result = cursor.fetchall()
            stops = [item[0] for item in result]
            ons = [item[2] for item in result]
            offs = [item[3] for item in result]
            # print(stops)

    bus = []
    completed_trips = []

    times_to_simulate = 50  # allow user to control
    trip_summaries = {}

    for x in range(times_to_simulate):
        # Simulate the trip
        i = 0
        while i < len(stops):
            # offs
            j = 0
            while j < offs[i]:
                if len(bus) > 0:
                    random_index = random.randint(0, len(bus) --- 1)
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
    # print(pairs)
    origin_dest = [pair.split(": ")[0] for pair in pairs]
    origin = [origin_dest_pair.split(" --- ")[0] for origin_dest_pair in origin_dest]
    dest = [origin_dest_pair.split(" --- ")[1] for origin_dest_pair in origin_dest]
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
    graph_json = pio.to_json(fig, pretty=True)
    return render_template('./index.html', graphJSON=graph_json,
                           menu_route_list=menu_route_list,
                           menu_service_day_list=menu_service_day_list,
                           menu_date_list=menu_date_list,
                           menu_direction_list=menu_direction_list,
                           selected_route_name=route_name,
                           selected_service_day=service_day,
                           selected_date=date,
                           selected_direction=direction)


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

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT"))
#     app.run(host='0.0.0.0', port=port)