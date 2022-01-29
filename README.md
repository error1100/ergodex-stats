# ergodex-stats

A set of docker containers that leverages the ErgoDEX backend to scan the Ergo blockchain and dump swap/pool/amm statistics into a database.


## Quick Start

If docker and docker-compose v2 are setup then:

<br>`docker compose up -d`</br>

To check if everything is working properly login to the Postgres database:

<br>`psql -U ergodex -h localhost -d ergodex -p 5432`</br>

Default password: <br>`ergodex`</br>


Then fetch the latest global index:

<br>`select max(gindex) from pools;`</br>
