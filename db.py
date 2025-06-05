import psycopg2

# Forbind til PostgreSQL
conn = psycopg2.connect(
    dbname="runapp",
    user="postgres",          
    password="",  
    host=""
)

# Funktion til at tilføje en løber
def add_runner(name, joined_date):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO Runner (Name, Joined_date) VALUES (%s, %s)",
            (name, joined_date)
        )
        conn.commit()

# Funktion til at hente alle løbere
def get_all_runners():
    with conn.cursor() as cur:
        cur.execute("SELECT Runner_ID, Name, Joined_date FROM Runner")
        return cur.fetchall()


def add_run_event_and_participation(date, duration, temperature, distance, runner_id):
    with conn.cursor() as cur:
        # Opret selve løbet
        cur.execute(
            "INSERT INTO Run_event (Date, Duration, Temperature, Distance) VALUES (%s, %s, %s, %s) RETURNING Run_event_ID",
            (date, duration, temperature, distance)
        )
        run_event_id = cur.fetchone()[0]

        # Registrer deltagelse
        cur.execute(
            "INSERT INTO Participation (Runner_ID, Run_event_ID, Run_Distance, Run_Time) VALUES (%s, %s, %s, %s)",
            (runner_id, run_event_id, distance, duration)
        )

        conn.commit()

    

def add_run_event(date, duration, temperature, distance):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO Run_event (Date, Duration, Temperature) VALUES (%s, %s, %s)",
            (date, duration, temperature)
        )
        conn.commit()


def get_all_events(from_date=None, to_date=None, min_distance=None, max_distance=None, min_duration=None, max_duration=None):
    query = """
        SELECT e.Date, r.Name, p.Run_Distance, p.Run_Time, e.Temperature
        FROM Run_event e
        JOIN Participation p ON e.Run_event_ID = p.Run_event_ID
        JOIN Runner r ON p.Runner_ID = r.Runner_ID
    """
    conditions = []
    params = []

    #Dato
    if from_date:
        conditions.append("e.Date >= %s")
        params.append(from_date)
    if to_date:
        conditions.append("e.Date <= %s")
        params.append(to_date)

    #Distance
    if min_distance:
        conditions.append("p.Run_Distance >= %s")
        params.append(min_distance)
    if max_distance:
        conditions.append("p.Run_Distance <= %s")
        params.append(max_distance)

    #Varighed
    if min_duration:
        conditions.append("p.Run_Time >= %s::interval")
        params.append(min_duration)
    if max_duration:
        conditions.append("p.Run_Time <= %s::interval")
        params.append(max_duration)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY e.Date DESC"

    with conn.cursor() as cur:
        cur.execute(query, params)
        return cur.fetchall()





