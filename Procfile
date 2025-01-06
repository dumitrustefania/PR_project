web: bash deploy.sh && gunicorn --worker-class eventlet -w 1 --chdir ./gym-attendance-backend/ -b 0.0.0.0:5000 app:app
