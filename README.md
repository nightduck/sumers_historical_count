# Flask/MySQL Docker Template

This is meant to be a reference for anyone who wants to dockerize a Flask app with a MySQL database attached. It also comes with a simple web app that you can reference.

To run it as is, just enter

    docker-compose up -d

You can verify the app is running by typing `localhost:5000` in your browser's address bar

## Getting Started

An example application has been provided in `app/app.py`. Modify the values in the config dictionary, and replace the methods as you will. `templates/` and `app/static/` can be used for blueprints, templates, or any static content.

### Password

You can set the password for your database in the `db/password.txt` file. It will be loaded into your docker containers after running the docker-compose command. Keeping it as a separate file means that you can source control the `docker-compose.yml` file without committing your password to a public repo. You can make sure git ignores changes to the password file with

    git update-index --assume-unchanged db/password.txt

### Initialization

When your app first starts, you'll probably want to initialize some tables. This is done in `db/init.sql`, which specifies schema that should be run when the app is created. You can create users and tables, populate preliminary data, and assign permissions.

Note this initialization happens only when the container is created. Any changes to the file will not be observed until the previous container instance is deleted. `docker-compose down` alone will not do, as `docker-compose up` will re-use existing containers when available.

### Volumes

Some (most) people prefer their data to be persistent across container reboots. While not enabled by default in this template, you'll see some commented-out lines in docker-compose.yml.

If you want to have a docker-managed persistent volume, uncomment lines 2, 3, and 16. This volume will survive the container if stopped or even deleted. Simply make it again and it'll reattach.

If you'd rather mount a custom folder on your filesystem instead, then uncomment line 17 (only line 17) and edit appropriately. This is useful when you have a large external disk that you want to store your data on.

### Debugging

 If you need direct access to the database, the MySQL container is exposed by default on the host network at port 28019. You can use that to connect to the database directly from your favorite IDE. Open a query console to send commands straight to the database, bypassing your ostensibly buggy python code.

## Learning Resources

### Flask Examples

Flask allows you to create a simple webserver from a python script. Visiting URLs will trigger different methods in your script. You can use this to serve content or create a REST API. I've included 3 examples you can use as reference: home_page, greet_user, and create_user. The last one only accepts POST commannds, so you can't view it in a browser. Trigger it from the commandline with

    curl -X POST http://website.com/create_user/Fake/Name/1980-06-20

This will extract arguments from the URL, connect to your database, and create row for your new user in the birthdays table. You can see an example of reading the database in the greet_user method. Trigger it with

    curl -X GET http://website.com/greet_user/1

Since this is a GET call, you can also put this url in your browser. When creating users, the user_id argument starts at 1 and increments for each user you add.

### Static Content

For complex web apps, there are dedicated folders, `app/static/` and `app/templates/`, where you can provide [blueprints](https://flask.palletsprojects.com/en/2.0.x/tutorial/views/), [templates](https://flask.palletsprojects.com/en/2.0.x/tutorial/templates/), and [static files](https://flask.palletsprojects.com/en/2.0.x/tutorial/static/). I have not provided examples in this repo, but you can follow the links for more in depth tutorials on Flask, and wrap it all together with this [final tutorial](https://flask.palletsprojects.com/en/2.0.x/tutorial/blog/).

### MySQL

Flask has many libraries for interfacing with MySQL. In this template, we use MySQL Connector. Queries are typically assembled with string formatting. You can see examples for the most common queries, SELECT and INSERT, in `app/app.py`. See [here](https://www.w3schools.com/sql/) for tutorials on other MySQL syntax.