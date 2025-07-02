#!/usr/bin/env python3
"""
Main application entry point for User Service API
"""
import os
import logging
import logging.config
import connexion
from flask_cors import CORS
from prometheus_flask_exporter import ConnexionPrometheusMetrics

from my_config.logging_config import LOGGING_CONFIG
from db.database import db_session, init_db

# Create Connexion application instance
connex_app = connexion.FlaskApp(__name__, specification_dir='./')

# Add API definition
connex_app.add_api('./inventory.yaml', name='inventory', validate_responses=True, pythonic_params=True)
# connex_app.add_api('./user-service.yaml', name='users', validate_responses=True, pythonic_params=True)

# Get Flask application instance
app = connex_app.app

# Configure the application
app.config.from_object('my_config.config.Config')
logging.config.dictConfig(LOGGING_CONFIG)

# Enable CORS
CORS(app)

# Set Prometheus Client
metrics = ConnexionPrometheusMetrics(connex_app)

# Register DB session cleanup
@app.teardown_appcontext
def shutdown_session(exception=None):
    if exception:
        logging.error(f'shutdown_session : {exception}')
    db_session.remove()


# Initialize the database
init_db()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    connex_app.run(host='0.0.0.0', port=port)
