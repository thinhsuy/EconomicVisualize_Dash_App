from preprocessing import *
from layout import *
from callback import *

app.layout = getLayout(app)

app.run_server(debug=True, 
               use_reloader=False
            #    host="172.16.4.193",
               # port="8000"
               )