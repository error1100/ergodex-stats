# ergodex-stats

A set of docker containers that leverages the ErgoDEX backend to scan and dump swap/pool/blockchain statistics into a database.


## Quick Start

If docker and docker-compose v2 are setup then:  
`docker compose up -d`

To check if everything is working properly login to the Postgres database:  
`psql -U ergodex -h localhost -d ergodex -p 5432`

Default password: `ergodex`

Then fetch the latest global index:  
`select max(gindex) from pools;`
