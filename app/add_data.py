import sqlite3
from pathlib import Path

# Define the path to the app directory and database
app_path = Path(__file__).parent
db_path = app_path / 'venues.db'

# Connect to the database
conn = sqlite3.connect(db_path, check_same_thread=False)
cursor = conn.cursor()

# SQL command to create the 'venues' table if it doesn't exist
create_table_sql = """
CREATE TABLE IF NOT EXISTS venues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    address TEXT,
    photo_url TEXT,
    playground TEXT,
    fenced TEXT,
    quiet_zones TEXT,
    colors INTEGER,
    smells INTEGER,
    food_own TEXT,
    defined_duration TEXT,
    quiet INTEGER,
    crowdedness INTEGER,
    food_variey INTEGER,
    reviews_count INTEGER

) """

# Execute the SQL command
cursor.execute(create_table_sql)


# SQL commands to insert sample data
insert_data_sql = """
INSERT INTO venues (name, address, photo_url, playground, fenced, quiet_zones, colors, smells, food_own, defined_duration, quiet, crowdedness, food_variey, reviews_count)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

# Sample data
sample_data = [
    ('Open Air Museum Massing - Freilichtmuseum Massing', 'Steinbüchl 1, 84323 Massing', 'https://lh3.googleusercontent.com/p/AF1QipNVEepOh6IuGFYhWJ-KmE8ZyPFSQ6UPi2Hn6EbF=s1360-w1360-h1020', "NO", "NO", "YES", 1, 3, "YES", "NO", 1, 1, 2, 0),
    ('Old town hall Pfarrkirchen', 'Stadtpl. 1, 84347 Pfarrkirchen', 'https://lh3.googleusercontent.com/p/AF1QipOU-nZCzrodrJR6GfHrEJvc_AfRWrryrfhUlpqn=s1360-w1360-h1020', "NO", "NO", "YES", 2, 2, "YES", "NO", 3, 3, 1, 0),
    ('Hans-Reiffenstuel House, Pfarrkirchen', 'St.-Rémy-Platz 1. 84347 Pfarrkirchen', 'https://pfarrkirchen.de/tl_files/images/content/stadtfuehrer/HRH.png', "NO", "NO", "YES", 1, 1, "NO", "NO", 2, 2, 1, 0),
    ('Pfarrkirchen Glass House', 'Ringstraße 9, 84347 Pfarrkirchen', 'https://img.pnp.de/ezplatform/images/_aliases/detail_teaser_item_image_variation/2/7/9/4/233464972-1-ger-DE/e7127d8f3098-29-107114533.jpg', "NO", "NO", "YES", 2, 1, "NO", "NO", 1, 1, 1, 0),
    ('Simbach am Inn Museum of local history', 'Innstraße 21, 84359 Simbach am Inn', 'https://le-cdn.website-editor.net/s/4dda15a888ca49a9a636d53b1a28fa1c/dms3rep/multi/opt/MuseumVorderansicht-576w.jpg?Expires=1720408204&Signature=mnLUhyom8oTUJovgKfdjF~iZ6kjG-sw8tcIKj8JL5qoHoAbm5OnCIh94b-4cK-aeR3WJx5NtdHrAjLVj7-k8KLSpjTRw845aJ0Tn6gFaRa5bglfxGA4tzy6TYBZFy3dj8--wyYjlUk8SGk7sCz8UBt8U~zIH8bctLCemBiQOiSF-WdQb-vFvIIYHf1fm8qv6yEMaucLrnyOBpCL5Bv8ImkY73qk2r9yqagiwba8x0aLqy-seVShOqp3bXdzFFyM4iVik5SsaZpsy-d8wRelyQpJpqDujObqeWYr3CMlf7pVkZawabE3OMpTfwV9WJ7FXRMRYMtGNC0fTTPgDGGCcPQ__&Key-Pair-Id=K2NXBXLF010TJW', "NO", "NO", "YES", 3, 1, "NO", "NO", 1, 1, 1, 0),
    ('Simbach am Inn Customs House Museum', 'Innstraße 14 84359 Simbach am Inn', 'https://fotos.verwaltungsportal.de/mandate/fotos/562007_113716_zollhaus.jpg', "NO", "NO", "YES", 2, 2, "NO", "NO", 2, 1, 1, 0),
    ('Showroom K3 gallery for contemporary art', 'Kottigstelzham 3, 84359 Simbach am Inn', 'https://schauraumk3.com/wp-content/uploads/2024/04/A-4JPEG.jpg', "NO", "NO", "YES", 1, 2, "NO", "NO", 4, 4, 1, 0),
    ('Alt-Arnstorf-House', 'Vorderer Berg 2, 94424 Arnstorf', 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/16/Vorderer_Berg_2_%28Arnstorf%29.jpg/2560px-Vorderer_Berg_2_%28Arnstorf%29.jpg', "NO", "NO", "YES", 2, 3, "NO", "NO", 2, 2, 1, 0),
    ('Heimathaus Hirschhorn', 'Dorfplatz 7, 84329 Wurmannsquick', 'https://wurmannsquick.dahoam-in-niederbayern.de/fileadmin/user_upload/vereinslogos/_processed_/b/1/csm_Wappen_06_64a7eb4b93.jpg', "NO", "NO", "YES", 2, 2, "YES", "NO", 2, 3, 1, 0),
    ('Adventure park Voglsam', 'Voglsam 1, 84337 Schönau', 'https://mein.toubiz.de/api/v1/article/a760f478-bec7-487d-b93c-dcb393ae0716/mainImage?format=image/jpeg&width=1900', "YES", "YES", "NO", 2, 2, "YES", "NO", 2, 2, 3, 0),
    ('Rottaler Golf Club', 'Fischgartl 2, 84389 Hebertsfelden', 'https://rottaler-gc.de/fileadmin/user_upload/Clubhaus.png', "NO", "NO", "YES", 3, 1, "YES", "YES", 2, 3, 1, 0),
    ('Bella Vista Golf Park', 'Bella Vista Allee 1, 84364 Bad Birnbach', 'https://www.badbirnbach.de/extension/portal-birnbach/var/storage/images/media/bibliothek/bella-vista-golfpark/bella-vista-treffpunkt-mit-cartflotte/57631-1-ger-DE/bella-vista-treffpunkt-mit-cartflotte_front_small.jpg', "NO", "NO", "YES", 3, 1, "NO", "YES", 2, 3, 1, 0),
    ('Bowling Center in Pfarrkirchen', 'Bahnweg 11 A, 84347 Pfarrkirchen', 'https://lh3.googleusercontent.com/p/AF1QipP_n0INeFD0o1i_jn9EpST5GfJ1OYyM00ImM3mc=s1360-w1360-h1020', "YES", "YES", "NO", 4, 2, "NO", "YES", 4, 4, 2, 0),
    ('Erlebnisbad Pfarrkirchen', 'Böhmerwaldweg 19, 84347 Pfarrkirchen', 'https://www.swpan.de/fileadmin/user_upload/Erlebnisbad/Erlebnisbad-Pfarrkirchen.jpg', "YES", "YES", "YES", 3, 3, "YES", "NO", 3, 3, 3, 0),
    ('Freibad Simbach am Inn', 'Gollinger Str. 2, 84359 Simbach am Inn', 'https://fotos.verwaltungsportal.de/mandate/logo/fe21f829becda46462f054d3a10a86fd_freibad-simbach_1.jpg', "YES", "YES", "YES", 2, 3, "YES", "NO", 2, 1, 3, 0),
    ('Erlebnisbad Eggenfelden', 'Taufkirchener Str. 1, 84307 Eggenfelden', 'https://img0.oastatic.com/img2/52827521/max/variant.jpg', "YES", "YES", "NO", 3, 3, "NO", "YES", 3, 3, 2, 0),
    ('Hallenbad Burghausen', 'Franz-Alexander-Straße 25, 84489 Burghausen', 'https://www.baeder-burghausen.de/content/images/temp/Erlebnisbadewelt/Lauer-Lebock/2009-11-_DSC1085-bad_burghausen.jpg', "YES", "YES", "NO", 3, 3, "YES", "YES", 4, 3, 2, 0),
    ('Hallenbad Massing', 'Wolfsegger Str. 33, 84323 Massing', 'https://www.xperbike.de/img_up/size4/4f91202fc8e60HallenbadMassinginnen.jpg', "NO", "NO", "YES", 1, 3, "YES", "NO", 2, 1, 1, 0),
    ('Berta-Hummel-Museum im Hummelhaus', 'Berta-Hummel-Straße 2, 84323 Massing', 'https://lh3.googleusercontent.com/p/AF1QipNsIffHKnorICMmO5XAtKNvKY3u2_XYlQVkM3_P=s1360-w1360-h1020', "NO", "NO", "NO", 2, 1, "NO", "NO", 1, 2, 1, 0),
    ('Sudetendeutsche Stuben – Schlesierstube', 'Marktplatz 20, Obergeschoss, 84323 Massing', 'https://www.rottalermuseumsstrasse.de/images/content/rms/massing-gal-sudeten1.jpg', "NO", "NO", "YES", 1, 2, "NO", "NO", 2, 2, 1, 0),
    ('Lanzmuseum Leo Speer', 'Rattenbacher Str. 10, 84326 Rimbach', 'https://www.rottalermuseumsstrasse.de/images/content/rms/rimbach-gal-lanz1.jpg', "NO", "NO", "YES", 1, 3, "YES", "NO", 1, 1, 1, 0),
    ('Meterstabmuseum Sallach', 'Mecklweg 3, 84326 Rimbach-Sallach', 'https://www.rottalermuseumsstrasse.de/images/content/rms/rimbach-gal-meterstab1.jpg', "NO", "NO", "NO", 2, 1, "YES", "NO", 2, 1, 1, 0),
    ('Prühmühle an der Rott', 'Prühmühle 1, 84307 Eggenfelden', 'https://www.rottalermuseumsstrasse.de/images/content/cities/Pruehmuehle_3.jpg', "NO", "NO", "YES", 4, 1, "NO", "YES", 4, 4, 2, 0),
    ('SchlossÖkonomie Gern', 'Hofmark, 84307 Eggenfelden', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQAmXdYtxRuYeYMXSyDZsKPChR15I67k90aUw&s', "NO", "NO", "YES", 3, 2, "NO", "YES", 4, 4, 2, 0),
    ('Artrium', 'Kurallee 7, 84364 Bad Birnbach', 'https://mein.toubiz.de/api/v1/article/1f153ea0-a5d3-4403-8220-4ff95e00df12/mainImage?format=image/jpeg&width=1900', "NO", "NO", "YES", 3, 2, "NO", "YES", 4, 4, 2, 0),
    ('Kirchenburg, Wallfahrtsstätte & Museum', 'Marktpl. 35, 94149 Kößlarn', 'https://www.rottalermuseumsstrasse.de/images/content/rms/koesslarn-gal-kirchenburg5.jpg', "NO", "NO", "YES", 2, 3, "YES", "NO", 2, 3, 1, 0),
    ('Feuerwehrmuseum', 'Rottfelling 2, 94094 Rotthalmünster', 'https://www.rottalermuseumsstrasse.de/images/content/rms/rotthalmuenster-gal-feuerwehrmuseum1.jpg', "YES", "YES", "NO", 3, 3, "YES", "YES", 3, 2, 1, 0),
    ('Bulldog-Museum', 'Altasbach 5, 94094 Rotthalmünster', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSM6axaUowHSHlgt8iTYgYVkzgtYl_gzuhM8g&s', "NO", "NO", "NO", 2, 2, "YES", "YES", 4, 2, 1, 0),
    ('Heimatmuseum', 'Kirchpl. 5, 94094 Rotthalmünster', 'https://www.rotthalmuenster.de/fileadmin/_processed_/3/7/csm_rotthalmuenster-event-heimatmuseum_993496452e.jpg', "NO", "NO", "YES", 2, 3, "NO", "NO", 2, 3, 1, 0),
    ('Leonhardi Museum', 'Penninger Weg 7, 94072 Bad Füssing', 'https://mein.toubiz.de/api/v1/media/6e70cbb0-a283-4bd3-ac5d-64fa20816507/view', "NO", "NO", "NO", 2, 1, "NO", "NO", 3, 3, 1, 0),
    ('Drehscheibe Pocking', 'Simbacher Straße 9, 94060 Pocking', 'https://www.rottalermuseumsstrasse.de/images/content/rms/pocking-gal-drehscheibe2.jpg', "YES", "NO", "YES", 3, 1, "NO", "NO", 2, 2, 1, 0),
    ('Rottauer Museum für Fahrzeuge, Wehrtechnik und Zeitgeschichte', 'Rottau 11a, 94060 Pocking', 'https://live.staticflickr.com/65535/49658496128_d6274023e8_b.jpg', "NO", "NO", "YES", 2, 3, "NO", "NO", 2, 2, 1, 0),
    ('Siebenschläferkirche', 'Rotthof 16, 94099 Ruhstorf an der Rott', 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/Siebenschl%C3%A4ferkirche_in_Rotthof_%28Ruhstorf_an_der_Rott%29_Ansicht_von_S%C3%BCdosten.png/798px-Siebenschl%C3%A4ferkirche_in_Rotthof_%28Ruhstorf_an_der_Rott%29_Ansicht_von_S%C3%BCdosten.png', "NO", "NO", "YES", 3, 3, "YES", "NO", 4, 1, 1, 0),
    ('historischer Ortsteil Mittich', 'Neuhaus am Inn', 'https://www.rottalermuseumsstrasse.de/images/content/rms/neuhaus-gal-mittich1.jpg', "YES", "NO", "YES", 2, 2, "YES", "NO", 3, 2, 1, 0),
    ('Klosterkirche Neuhaus', 'Schloss 1, 94152 Neuhaus a. Inn', 'https://media.tourdata.at/display/original/4032346458782f34994a9f24410edaec.jpg', "NO", "NO", "YES", 2, 3, "YES", "YES", 2, 2, 1, 0),
    ('Klosterkirche Vornbach', 'Maria am Sand 4, 94152 Neuhaus am Inn', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcStsCVjbkJha4tr564lK938LaEg0tNPkaKehA&s', "NO", "NO", "YES", 2, 2, "YES", "YES", 1, 1, 1, 0)
]


# Insert the sample data into the database

for entry in sample_data:
    if create_table_sql:
        cursor.execute(insert_data_sql, entry)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Sample data inserted successfully.")

