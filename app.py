from placementportalcode import create_app
from placementportalcode import db
from flask_cors import CORS



app=create_app()

CORS(app,
     supports_credentials=True,
     origins="http://localhost:5173")


with app.app_context():
    db.create_all()
    

if(__name__=="__main__"):
    app.run(debug=True)