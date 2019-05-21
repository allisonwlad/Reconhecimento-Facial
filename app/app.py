import connexion
from connexion.resolver import RestyResolver

options={"swagger_ui":False}
app = connexion.FlaskApp(__name__, specification_dir='swagger/', options=options)
app.add_api('facial_api.yaml', resolver=RestyResolver('api'))
app.run(port=8080)