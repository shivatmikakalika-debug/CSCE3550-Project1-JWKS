

\# Basic JWKS Server



\*\*Student:\*\* Shivatmika Kalika  

\*\*Project:\*\* Project 1 - Implementing a Basic JWKS Server



\## Project Description



This project implements a basic JSON Web Key Set (JWKS) server using Python and Flask.



The server generates RSA key pairs, assigns unique Key IDs (kid), and manages key expiration. It provides public keys for JWT verification and supports issuing both valid and expired JWTs.



This project is for educational purposes and uses mock authentication.



\## Technologies Used



\- Python

\- Flask

\- PyJWT

\- Cryptography

\- Pytest

\- pytest-cov

\- Ruff



\## Features



\- Generates 2048-bit RSA key pairs.

\- Assigns a unique kid to each key.

\- Stores an expiration timestamp for each key.

\- Provides public keys in JWKS format.

\- Excludes expired keys from the JWKS endpoint.

\- Generates signed JWTs using RS256.

\- Supports expired JWT generation.

\- Runs on port 8080.



\## API Endpoints



\### GET /.well-known/jwks.json



Returns public keys that have not expired.



Example:



http://localhost:8080/.well-known/jwks.json



\### POST /auth



Generates a valid signed JWT for a mock user.



Example:



curl -X POST http://localhost:8080/auth



\### POST /auth?expired



Generates a JWT signed with an expired key and an expired expiration timestamp.



Example:



curl -X POST "http://localhost:8080/auth?expired"



\## Installation



Install the required packages:



```bash

python -m pip install flask pyjwt cryptography pytest pytest-cov ruff

```



\## Running the Server



Start the server using:



```bash

python app.py

```



The server runs at:



http://localhost:8080



\## Running Tests



Run the test suite and measure coverage:



```bash

python -m pytest --cov=app --cov-report=term-missing

```



Test results:



\- 12 tests passed.

\- 97% code coverage.

\- Required coverage: over 80%.



\## Code Quality



Check the code using Ruff:



```bash

python -m ruff check app.py test\_app.py

```



Result:



All checks passed!



\## Official Test Client



The project was tested using the CSCE3550 Project 1 grading client.



Official grading result: 98.93%.



All six functional grading checks received full points.



\## Project Files



\- app.py - JWKS server implementation.

\- test\_app.py - Automated test suite.

\- README.md - Project documentation.



\## Security Note



This project uses mock authentication and generates RSA keys in memory. It is intended for educational use rather than production deployment.

