#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField
from wtforms.validators import DataRequired, URL
import pandas as pd

# custom paths
scans_folder = os.path.join(os.getcwd(), "scans")
domain_list = os.path.join(os.getcwd(),"domains.txt")
ignore_list = os.path.join(os.getcwd(),"ignore.txt")

app = Flask(__name__)
#app.config['']

class DomainForm(FlaskForm):
    """Jump to domain form"""
    domain = StringField('Website', validators=[URL()])
    submit = SubmitField('Submit')

def clean_csv(csv_file):
    cdata = open(csv_file, 'r')
    lines = cdata.readlines()
    lines[0] = lines[0].replace('-','_')
    with open(csv_file, 'w') as f:
        for line in lines:
            f.write(line)

def get_csv(csv_file):
    clean_csv(csv_file)
    ignored = open(ignore_list, 'r')
    #data = pd.read_csv(csv_file, index_col="domain_name")
    data = pd.read_csv(csv_file)
    clean_data = data.set_index("domain_name", drop=False)
    for domain in ignored:
        try:
            clean_data.drop(domain.rstrip(), inplace=True)
        except:
            continue
    return clean_data

@app.route('/')
def index():
    domains = open(domain_list, 'r').readlines()
    return render_template("index.html", len=len(domains), domains=domains)

@app.route('/jump/', methods=['GET'])
def jump():
    domain = request.args.get('domain')
    return redirect("../results/"+domain+"/")


@app.route('/results/<domain>/')
def domain(domain):
    try:
        dnsdata = get_csv(os.path.join(scans_folder, domain+".csv"))
        dnsdata = list(dnsdata.values)
        return render_template("table.html", title=domain, dnsdata=dnsdata)
    except:
        return render_template("scan404.html", domain=domain)

@app.route("/add/<domain>/")
def add(domain):
    domains = open(domain_list, 'r')
    if domain in domains.read():
        return "Domain already exists!"
    else:
        with open(domain_list, 'a') as f:
            f.write(domain+"\n")
        return "Domain added."

@app.route("/delete/<domain>/")
def delete(domain):
    domain = domain + "\n"
    domains = open(domain_list, 'r').readlines()
    if domain in domains:
        domains.remove(domain)
        with open(domain_list, 'wt') as f:
            for domain in domains:
                f.write(domain)
        return "Removed domain from monitoring."
    else:
        return "Domain not monitored."

@app.route("/ignore/<domain>/")
def ignore(domain):
    domains = open(ignore_list, 'r')
    if domain in domains.read():
        if "http://localhost" in request.referrer:
            return redirect(request.referrer)
        else:
            return "Domain already ignored."
    else:
        with open(ignore_list, 'a') as f:
            f.write(domain+"\n")
        if "http://localhost" in request.referrer:
            return redirect(request.referrer)
        else:
            return "Domain ignored."

if __name__ == "__main__":
    Bootstrap(app)
    app.run(debug=True)