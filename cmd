run: 
uvicorn src.main:app --reload

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

test:
pytest --log-cli-level=INFO -s   


makemigration: 
alembic revision --autogenerate -m ""

migrate: 
alembic upgrade head