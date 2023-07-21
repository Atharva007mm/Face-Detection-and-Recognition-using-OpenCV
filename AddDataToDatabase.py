import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceidrealtime-default-rtdb.firebaseio.com/"
})


ref = db.reference('Students')

data = {
    "321654":
        {
            "name": "Sparsh Teli",
            "major": "B/101 Silver Avenue,Santacruz(E),Mumbai",
            "starting_year":2021,
            "total_attendance":1,
            "standing":"O-",
            "year":400098,
            "last_attendance_time": "2024-12-12 00:54:34"
        },
    "852741":
        {
            "name": "Atharva Mhaishalkar",
            "major": "A/401 Sky View,Thane(E),Mumbai",
            "starting_year":1995,
            "total_attendance":2,
            "standing":"O+",
            "year":400604,
            "last_attendance_time": "2024-12-12 00:54:34"
        },
    "963852":
        {
            "name": "Kasustubh Toraskar",
            "major": "C/303 Golden Square,Kalayan(E),Mumbai",
            "starting_year":2020,
            "total_attendance":3,
            "standing":"O+",
            "year":421301,
            "last_attendance_time": "2024-12-12 00:54:34"
        },
}

for key,value in data.items():
    ref.child(key).set(value)