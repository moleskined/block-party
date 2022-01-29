# Block Party Realty—a Proof-of-concept, Blockchain-based Real Estate App

<figure>
	<img src="https://user-images.githubusercontent.com/10587575/151504027-dd02042b-3d44-4bbc-8040-6339b2e8b635.png" width="100%">
</figure>

*Block Party Realty* demonstrates using a blockchain to maintain a trusted record of transactions between sellers, authorities, buyers and banks.

## Setting Up

### Requirements

To run the app, you will need:

* Python > 3.6[^1].
* The ability to use a [Python virtual environment (venv)](https://docs.python.org/3/tutorial/venv.html).
* A releatively recent version of Safari (>=14), Firefox (>=78), Chrome (>=78) or Edge (>=91).
* A working internet connection.

Optional: to build the GUI from scratch:

* Node.js (>=v17.4.0) and NPM (>=8.3.1).

### Step 1: Install & Activate the Virtual Environment

Open a terminal and navigate to the directory you downloaded or pulled from git. Open the directory (usually `block-party`) in a terminal.

Create a directory to store your virtual environment. These instructions assume `./venv` will be the directory, and has been added to `.gitignore`.

```bash
$ mkdir ./venv
```

Next, initialise the virtual environment.

```bash
$ python3 -m venv venv
```

Finally, activate the environment.

```
$ source venv/bin/activate
```

### Step 2: Install Dependencies & Initialise the Database

The application has a small number of dependencies. To install them, run the following command (see appendix for notes about running with an older version of Python).

```bash
$ pip install --upgrade pip && pip install -r requirements.txt
```

Next, initialise the database. This will setup the schema and test users.

```bash
$ flask db upgrade
```
```bash
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 40d1da15458a, empty message
INFO  [alembic.runtime.migration] Running upgrade 40d1da15458a -> e4400a2d48d8, empty message
```

Verify that the database `app.db` has been created:

```bash
$ file app.db

app.db: SQLite 3.x database, last written using SQLite version 3037002
```

```bash
$ sqlite3 app.db "SELECT * FROM sqlite_master WHERE type='table';"

table|alembic_version|alembic_version|2|CREATE TABLE alembic_version (
		version_num VARCHAR(32) NOT NULL, 
		CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
)
table|block|block|4|CREATE TABLE block (
		hash VARCHAR(50) NOT NULL, 
		"index" INTEGER, 
		timestamp DATETIME NOT NULL, 
		previous_hash VARCHAR(50), 
		data TEXT, 
		PRIMARY KEY (hash)
)
table|user|user|8|CREATE TABLE user (
		id INTEGER NOT NULL, 
		username VARCHAR(64), 
		password_hash VARCHAR(128), 
		role INTEGER, 
		PRIMARY KEY (id)
)
```

### Step 3: Running the Application

*Block Party** uses [Flask](https://palletsprojects.com/p/flask/) to host the webapp and API. Most interactions will be through this interface, but Flask needs to be running to accept connections.

Run the following:

```bash
$ flask run

 * Serving Flask app 'block_party.py' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

Then, open a browser window to [http://127.0.0.1:5000](http://127.0.0.1:5000/) and you should see a login prompt.

#### Optional: Logging

*Block Party* is quite verbose. Creation and verification of blocks are printed to `stdout`, so it could be useful to save this output to a logfile. For example:

```bash
$ flask run > activity.log
```

## Dev Dependencies

- [Python](https://www.python.org)
- [Flask](https://github.com/pallets/flask)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [React](https://reactjs.org)
- [MUI](https://mui.com)
- [Babel](https://babeljs.io)
- [Webpack](https://webpack.js.org)
- [Sass](https://sass-lang.com)


[^1]: Setting `WTForms==3.0.1` in `requirements.txt` to `WTForms==3.0.0` allows the program to install for Python 3.6.