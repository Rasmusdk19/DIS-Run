

# Python virtual environment
Lav et virtual environment og install de 3 pakker

python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux

pip install flask
pip install psycopg2-binary
pip install psycopg2

# Pithon filen db.py 
Ændre user og password til postgres, til det du bruger i postgres:

conn = psycopg2.connect(
    dbname="runapp",
    user="postgres",          
    password="",  
    host=""
)

# Postgres
Gå in i Postgres og start en database op og derefter til kan man kopiere det nedenunder.
Man skal erstatte postgres med sit eget brugernavn
createdb -U postgres runapp
psql -U postgres -d runapp -f schema.sql

psql -U postgres -d runapp -f insert_sample_data.sql

psql -U postgres -d runapp


# I terminalen i mappen
export FLASK_APP=app.py
flask run --debug

# Brug aff webappen/hjemmeside
Dette hjemmeside er til en lokal løbeklub, hvor de mangler et sted at indsætte alle deres tider og løb.
Man starter på den side hvor man kan Registrere sig, med fornavn og efternavn og startdato.
Når man tilføjer en løber, kommer man ind på registrerede løbere, hvor der vil være eksempler på løbere som er i insert_sample_data.sql.
Derfra kan man trykke på opret et løb, hvor man på den side kan oprette et løb, med dato, løber, Distance, Varighed og Temperatur, hvor Temperatur behøves ikke at blive tilføjet.
Når man man lavet et løb, kommer man ind på alle løb, hvor der er en liste over løbene, derfra kan man bruge filter søgningen, hvor man søge efter løb en specifik dato, minimum og maks distance eller tid.

# forbedringer/videreudvikling

Man kan ikke logind, så man kan selv vælge sit løb bliver Registreret til en anden løber.