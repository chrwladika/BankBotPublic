"""
Bankbot Database Initialization

This module contains code for initializing the database tables using PyDAL.

"""

from pydal import DAL, Field
import os
import datetime

from pydal.validators import IS_IN_SET

from models.enum import Roles

# PyDAL Database configuration
db_folder = os.path.abspath("db")
os.makedirs(db_folder, exist_ok=True)
db = DAL("sqlite://{}/bankbot.db".format(db_folder), folder=db_folder)

# Define the 'user' table
db.define_table("user",
                Field("email",
                      "string",
                      unique=True,
                      notnull=True),
                Field("first_name",
                      type="string",
                      required=True),
                Field("last_name",
                      type="string",
                      required=True)
)

# Define the 'csrequests' table
db.define_table("csrequests",
                Field("request",
                      type='string',
                      required=True,
                      label='Request'),
                Field("telephone",
                      type='string',
                      required=True,
                      label='Telephone'),
                Field("user_ref",
                      type="reference user",
                      label='Requestor'),
                Field("category",
                      type='string',
                      label='Category'),
                Field("timestamp",
                      type="datetime",
                      default=datetime.datetime.now(),
                      notnull=True)
                )

# Check if a user with id 1 exists and insert sample data if not
if db(db.user.id == 1).select(db.user.ALL).first() is None:
    u1 = db.user.insert(email="max.mustermann@example.com", first_name="Max", last_name="Mustermann")
    u2 = db.user.insert(email="maxi.mustermann@example.com", first_name="Maxime", last_name="Musterfrau")
    db.csrequests.insert(request="Ich möchte einen Betrugsfall melden!", user_ref=u1, category="Card", telephone="0664826328836")
