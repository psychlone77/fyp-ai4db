First run
```bash
sudo apt-get update
```

## Install Postgres
```bash
sudo apt install -y postgresql-common ca-certificates
```

```bash
sudo /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh
```

```bash
sudo apt install postgresql-12
```

create user
```bash
# Switch to the postgres user
sudo -i -u postgres

# Create a user named 'root' (or whatever your SSH user is) with Superuser privileges
createuser --interactive --pwprompt
# > Enter name of role to add: azureuser
# > Enter password for new role: <Type a strong password> databasefyp
# > Shall the new role be a superuser? (y/n) y

# Exit the postgres user session
exit
```

test connection
```bash
psql -U root -d postgres
```

Run this to ensure the user table is created.
```bash
psql -h localhost
```
## Install JOB Benchmark (IMDb)
https://github.com/danolivo/jo-bench

```bash
git clone https://github.com/danolivo/jo-bench.git
```

```bash
psql -d postgres -c "CREATE DATABASE imdb;"
```
Navigate to the repo folder
```bash
psql -f schema.sql -d imdb
```

Run this to ensure tables have been created
```bash
psql -d imdb -c "\dt"
```

Ensure permissions are given to the CSV files
```bash
sudo chmod +x csv/*
```

```bash
psql -vdatadir="'$HOME/localfiles/job/jo-bench'" -f copy.sql -d imdb
```
## Setup E2ETune repo

```bash
git clone https://github.com/psychlone77/E2ETune-AI4DB.git
```

Create virtual environment
```
python -m venv venv
```

Activate venv
```
source venv/bin/activate
```

```
pip install -r requirements.txt
```
