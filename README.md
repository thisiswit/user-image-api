# FastAPI User Image guide
## All the API test was run on : http://localhost:8000/docs

## First of all we need to activate the venv environment:
### Windows: .\venv\Script\activate
### Linux: source venv/bin/activate

## After that we need to build the docker:
### docker-compose up --build

## You can see the MongoDB database with Mongo compass, download the link below:
https://www.mongodb.com/try/download/compass

## To run the application locally you need to use the following command:
### uvicorn main:app --host localhost --reload
