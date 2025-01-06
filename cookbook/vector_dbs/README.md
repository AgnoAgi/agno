## Vector DBs
Vector databases enable us to store information as embeddings and search for “results similar” to our input query using cosine similarity or full text search.

## Setup

### Create a virtual environment

```shell
python3 -m venv ~/.venvs/aienv
source ~/.venvs/aienv/bin/activate
```

### Install libraries

```shell
pip install -U qdrant-client pypdf openai phidata
```

## Test your VectorDB

### ChromaDB

```shell
python cookbook/vector_dbs/chroma_db.py
```

### LanceDB

```shell
python cookbook/vector_dbs/lance_db.py
```

### PgVector

> Install [docker desktop](https://docs.docker.com/desktop/install/mac-install/) first.

- Run using a helper script

```shell
./cookbook/run_pgvector.sh
```

- OR run using the docker run command

```shell
docker run -d \
  -e POSTGRES_DB=ai \
  -e POSTGRES_USER=ai \
  -e POSTGRES_PASSWORD=ai \
  -e PGDATA=/var/lib/postgresql/data/pgdata \
  -v pgvolume:/var/lib/postgresql/data \
  -p 5532:5432 \
  --name pgvector \
  phidata/pgvector:16
```

```shell
python cookbook/vector_dbs/pg_vector.py
```

### Mem0

```shell
python cookbook/vector_dbs/mem0.py
```

### Milvus

```shell
python cookbook/vector_dbs/milvus.py
```

### Pinecone DB

```shell
python cookbook/vector_dbs/pinecone_db.py
```

### Singlestore

> Install [docker desktop](https://docs.docker.com/desktop/install/mac-install/) first.

#### Run the docker container
```shell
docker run \
    -d --name singlestoredb-dev \
    -e ROOT_PASSWORD="admin" \
    -p 3306:3306 -p 8080:8080 -p 9000:9000 \
    --platform linux/amd64 \
    ghcr.io/singlestore-labs/singlestoredb-dev:latest
```

#### Create the database

- Visit http://localhost:8080 and login with `root` and `admin`
- Create the database with your choice of name

#### Add credentials

- For SingleStore

```shell
export SINGLESTORE_HOST="localhost"
export SINGLESTORE_PORT="3306"
export SINGLESTORE_USERNAME="root"
export SINGLESTORE_PASSWORD="admin"
export SINGLESTORE_DATABASE="your_database_name"
export SINGLESTORE_SSL_CA=".certs/singlestore_bundle.pem"
```

- Set your OPENAI_API_KEY

```shell
export OPENAI_API_KEY="sk-..."
```

#### Run Agent

```shell
python cookbook/vector_dbs/singlestore.py
```


### Qdrant

```shell
docker run -p 6333:6333 -p 6334:6334 -v $(pwd)/qdrant_storage:/qdrant/storage:z qdrant/qdrant
```

```shell
python cookbook/vector_dbs/qdrant_db.py
```
