from flask import Flask, session,request, render_template
import data_utils
import convert_utils

app = Flask(__name__)

app.secret_key = "b437Ar8jXdmeVTDZThgEZhLUmVL7EErRwna6Yfgwv"

@app.get("/")
def index():
    return render_template(
        "index.html", 
        title="Welcome to Swimclub", 
    )

@app.get("/swims")
def display_swim_sessions():
    data = data_utils.get_swim_sessions()
    dates = [d[0].split(" ")[0] for d in data]
    return render_template(
        "select.html",
        title="Select a swim session",
        url="/swimmers",
        select_id="chosen_date",
        data=dates
    )

@app.post("/swimmers")
def display_swimmers():
    session["chosen_date"] = request.form["chosen_date"]   
    data = data_utils.get_session_swimmers(session["chosen_date"])   
    return render_template(
        "select.html",
        title="Select a swimmer",
        url="/showevents",
        select_id ="swimmer",
        data = sorted([f"{name}-{age}" for name, age in data])
    )

@app.post("/showevents")
def display_swimmer_files():
    session["swimmer"], session["age"] = request.form["swimmer"].split("-")
    data = data_utils.get_swimmers_events(session["swimmer"], session["age"], session["chosen_date"])
    
    return render_template(
        "select.html",
        title="Select an event",
        url="/showbarchart",
        select_id="event",
        data = [f"{distance} {stroke}" for distance, stroke in data]
    )


@app.get("/files/<swimmer>")
def get_swimmers_files(swimmer):
    return str(session["swimmers"][swimmer])

@app.post("/showbarchart")
def show_bar_chart():
    distance, stroke = request.form["event"].split(" ")
    data = data_utils.get_swimmers_times(
        session["swimmer"],
        session["age"],
        distance,
        stroke,
        session["chosen_date"]
    )
    
    times = [time[0] for time in data]

    average_str, times_reversed, scaled = convert_utils.perform_conversions(times)
    world_records = convert_utils.get_worlds(distance, stroke)
    header = f"{session["swimmer"]} (Under {session['age']}) {distance} {stroke} - {session['chosen_date']}"
    return render_template(
        "chart.html",
        title=header,
        data=list(zip(times_reversed, scaled)),
        average=average_str,
        worlds=world_records
    )


if __name__ == "__main__":
    app.run(debug=True)
