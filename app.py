from flask import Flask, render_template, request, redirect
from db import (
    add_runner,
    get_all_runners,
    get_all_events,
    add_run_event_and_participation
)
import re 

app = Flask(__name__)  # Opret Flask applikationen

# Standardrute – viderestiller til tilføjelse af løber
@app.route('/')
def index():
    return redirect('/add-runner')

# Rute til at tilføje en ny løber
@app.route('/add-runner', methods=['GET', 'POST'])
def add_runner_route():
    if request.method == 'POST':
        # Hent brugerinput fra HTML-formular
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        joined_date = request.form['joined_date']

        # REGEX-validering: Kun tilladte tegn i navne (bogstaver, mellemrum, bindestreg, æøå)
        if not re.match(r'^[A-Za-zÆØÅæøå\- ]+$', first_name):
            return "Ugyldigt fornavn: kun bogstaver og mellemrum tilladt", 400
        if not re.match(r'^[A-Za-zÆØÅæøå\- ]+$', last_name):
            return "Ugyldigt efternavn: kun bogstaver og mellemrum tilladt", 400

        name = f"{first_name} {last_name}"

        # Kald databasefunktion til at gemme løberen
        add_runner(name, joined_date)
        return redirect('/runners')  

    return render_template('add_runner.html')  

# Vis alle løbere
@app.route('/runners')
def show_runners():
    runners = get_all_runners()  # Hent løbere fra databasen
    return render_template('runners.html', runners=runners)

# Rute til at tilføje et løb og registrere deltagelse
@app.route('/add-event', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        # Hent og formater input
        date = request.form['date']
        hours = int(request.form['hours'])
        minutes = int(request.form['minutes'])
        seconds = int(request.form['seconds'])
        milliseconds = int(request.form['milliseconds'])
        distance = request.form['distance'].replace(',', '.')
        temperature = request.form['temperature']
        runner_id = int(request.form['runner'])

        # Kombiner tid til interval-format
        duration = f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"

        # Temperatur kan være valgfri
        temperature = int(temperature) if temperature.strip() else None

        # Gem løb og deltagelse i databasen
        add_run_event_and_participation(date, duration, temperature, distance, runner_id)
        return redirect('/events')  # Efter oprettelse, vis alle løb

    runners = get_all_runners()  
    return render_template('add_run_event.html', runners=runners)

# Rute til at vise alle løb med filtreringsmuligheder
@app.route('/events')
def show_events():
    # Hent filterparametre fra query string 
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')
    min_distance = request.args.get('min_distance')
    max_distance = request.args.get('max_distance')
    min_duration = request.args.get('min_duration')
    max_duration = request.args.get('max_duration')

    # Hent løb fra databasen med eventuelle filtre
    events = get_all_events(
        from_date, to_date,
        min_distance, max_distance,
        min_duration, max_duration
    )
    return render_template('events.html', events=events)  

# Starter appen i debug-tilstand (kun til udvikling)
if __name__ == '__main__':
    app.run(debug=True)



