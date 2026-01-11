from flask import Flask, session,request, render_template
import os
import swimclub

app = Flask(__name__)

app.secret_key = "b437Ar8jXdmeVTDZThgEZhLUmVL7EErRwna6Yfgwv"

@app.get("/")
def index():
    return render_template(
        "index.html", 
        title="Welcome to the Swimclub system", 
    )

@app.get("/swimmers")
def display_swimmers():
    populate_data()
    return render_template(
        "select.html",
        title="Select a swimmer",
        url="/showfiles",
        select_id ="swimmer",
        data = sorted(session["swimmers"])
    )

@app.post("/showfiles")
def display_swimmer_files():
    populate_data()
    name = request.form["swimmer"]    
    return render_template(
        "select.html",
        title="Select an event",
        url="/showbarchart",
        select_id="file",
        data = session["swimmers"][name]
    )


@app.get("/files/<swimmer>")
def get_swimmers_files(swimmer):
    populate_data()
    return str(session["swimmers"][swimmer])

@app.post("/showbarchart")
def show_bar_chart():
    file_id = request.form["file"]
    # Ensure the chart is written to the templates directory that lives
    # next to this module regardless of the current working directory.
    templates_dir = os.path.join(os.path.dirname(__file__), "templates") + os.sep
    location = swimclub.produce_bar_chart(file_id, templates_dir)
    return render_template(location.split("/")[-1])

def populate_data():
    if "swimmers" not in session:
        swim_files = os.listdir(swimclub.FOLDER)
        swim_files.remove('.DS_Store')
        session["swimmers"] = {}
        for file in swim_files:
            name, *_ = swimclub.read_swim_data(file)
            if name not in session["swimmers"]:
                session["swimmers"][name] = []      
            session["swimmers"][name].append(file)

if __name__ == "__main__":
    app.run(debug=True)
