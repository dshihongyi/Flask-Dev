from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
# from data import Templates
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
import sys
import pyperclip


app = Flask(__name__)

#Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'daniel'
app.config['MYSQL_PASSWORD'] = '324DanS'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

# init MySQL
mysql = MySQL(app)


# Templates = Templates()

# index
@app.route('/')
def index():
    return render_template('home.html')

# Router Page
@app.route('/router')
def router():
    return render_template('router.html')

# Switch Templates
@app.route('/switch')
def switches():
        # Create Cursor
        cur = mysql.connection.cursor()

        # Get Switch templates
        result = cur.execute("SELECT * FROM sw_templates")

        sw_templates = cur.fetchall()
        if result > 0:
            return render_template('switch.html',switches=sw_templates)
        else:
            msg = "No Templates Found"
            return render_template('switch.html', msg=msg)

        # Close connection
        cur.close()

    # return render_template('switch.html', templates = Templates)

# Single Switch Template
@app.route('/sw_template/<string:id>')
def sw_template(id):

    # Create Cursor
    cur = mysql.connection.cursor()

    # Get Switch templates
    result = cur.execute("SELECT * FROM sw_templates WHERE id = %s", [id])

    sw_template = cur.fetchone()

    return render_template('sw_template.html', sw_template=sw_template)

# Register Form Class
# https://flask.palletsprojects.com/en/1.1.x/patterns/wtforms/
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
      validators.DataRequired(),
      validators.EqualTo('confirm', message='Password do not match')
    ])
    confirm = PasswordField('Confirm Password')

# User Register
@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create DictCursor
        cur = mysql.connection.cursor()

        # Excute query
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        # Commit to DB
        mysql.connection.commit()

        # Close Connection
        cur.close()

        flash("You are now registed and can log in", 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# User login
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        # Get From Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by Username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # app.logger.info('PASSWORD MATCHED')
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                # app.logger.info('PASSWORD NOT MATCHED')
                error = 'Invalid Password'
                return render_template('login.html', error=error)
                # Close Connection
                cur.close()

        else:
            # app.logger.info('NO USER')
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Check if user logged if __name__ == '__main__':
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    # Create Cursor
    cur = mysql.connection.cursor()

    # Get Switch templates
    # result = cur.execute("SELECT * FROM sw_templates")

    sw_templates = cur.fetchall()
    if result > 0:
        return render_template('dashboard.html',sw_templates=sw_templates)
    else:
        msg = "No Templates Found"
        return render_template('dashboard.html', msg=msg)

    # Close connection
    cur.close()


# Templates Form Class
class TemplateForm(Form):
    # brand = StringField('Brand', [validators.Length(min=1, max=50)])
    # type = StringField('Type', [validators.Length(min=4, max=50)])
    # model = StringField('Model', [validators.Length(min=1, max=50)])
    # ios = StringField('IOS', [validators.Length(min=4, max=25)])
    # agency = StringField('Agent', [validators.Length(min=1, max=50)])
    # site = StringField('Site Code', [validators.Length(min=2, max=5)])
    # ci_name = StringField('CI_Name', [validators.Length(min=1, max=50)])
    isp = StringField('Supplier', [validators.Length(min=1, max=20)])
    ide = StringField('ID', [validators.Length(min=1, max=50)])
    desc = StringField('Description', [validators.Length(min=1, max=50)])
    ip = StringField('IP Address', [validators.Length(min=1, max=50)])
    prefix = StringField('Sub-Mask', [validators.Length(min=1, max=25)])
    config = TextAreaField('Config', [validators.Length(min=0)])

# Add Switch Templates
@app.route('/add_sw_template', methods=['GET','POST'])
@is_logged_in
def add_sw_template():
    form = TemplateForm(request.form)
        
    if request.method == 'POST' and form.validate() and form.isp.data == 'FEENIX':
        # brand = request.form['brand']
        # brand = form.brand.data
        # type = form.type.data
        # model = form.model.data
        # ios = form.ios.data
        # agency = form.agency.data
        # site = form.site.data
        # ci_name = form.ci_name.data
        Feenix_Template = open("/home/daniel/Desktop/Web-Template/ISP_Template/Feenix.txt").read()

        ide = form.ide.data
        desc = form.desc.data
        ip = form.ip.data
        prefix = form.prefix.data
        configs = form.config.data

        Parsed_Feenix_Template = Feenix_Template.format(ide = ide, desc = desc, ip = ip, prefix = prefix)
        
       
        # return 'Successfully load value'
        flash('Template Created','success')

        return redirect(url_for('Feenix_template', result_data=Parsed_Feenix_Template))
        # return render_template('add_sw_template.html', result=form.config.data)

    elif request.method == 'POST' and form.validate() and form.isp.data == 'SPARK':

        Spark_Template = open("/home/daniel/Desktop/Web-Template/ISP_Template/Spark.txt").read()

        ide = form.ide.data
        desc = form.desc.data
        ip = form.ip.data
        prefix = form.prefix.data
        configs = form.config.data

        Parsed_Spark_Template = Spark_Template.format(ide = ide, desc = desc, ip = ip, prefix = prefix)
        
       
        # return 'Successfully load value'
        flash('Template Created','success')

        return redirect(url_for('Spark_template', result_data=Parsed_Spark_Template))
        # return render_template('add_sw_template.html', result=form.config.data)


        # # Create Cursor
        # cur = mysql.connection.cursor()

        # # Execute
        # cur.execute("INSERT INTO sw_templates(brand, type, model, IOS, agency, site, ci_name, config, last_editor) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", (brand, type, model, ios, agency, site, ci_name, config, session['username']))


        # # Commit to # DEBUG:
        # mysql.connection.commit()

        # # Close connection
        # cur.close()

        # flash('Template Created','success')

        # return redirect(url_for('dashboard'))

    return render_template('add_sw_template.html', form=form)

@app.route('/Feenix_template', methods=['POST', 'GET'])
def Feenix_template():
    result_data = request.args.get('result_data', None)

    if request.method == 'POST':
        print(request.form["text_area"])
        pyperclip.copy(request.form["text_area"])

    return render_template('Feenix_template.html', result_data=result_data)


@app.route('/Spark_template', methods=['POST', 'GET'])
def Spark_template():
    result_data = request.args.get('result_data', None)

    if request.method == 'POST':
        print(request.form["text_area"])
        pyperclip.copy(request.form["text_area"])

    return render_template('Spark_template.html', result_data=result_data)


# Edit Switch Templates
@app.route('/edit_sw_template/<string:id>', methods=['GET','POST'])
@is_logged_in
def edit_sw_template(id):
    # Create Cursor
    cur = mysql.connection.cursor()

    # Get user by id
    result = cur.execute("SELECT * FROM sw_templates WHERE id = %s", [id])

    template = cur.fetchone()

    # Get from
    form = TemplateForm(request.form)

    # Populate template form Fields
    form.brand.data = template['brand']
    form.type.data = template['type']
    form.model.data = template['model']
    form.ios.data = template['IOS']
    form.agency.data = template['agency']
    form.site.data = template['site']
    form.ci_name.data = template['ci_name']
    form.config.data = template['config']


    if request.method == 'POST' and form.validate():
        # brand = request.form['brand']
        brand = request.form['brand']
        type = request.form['type']
        model = request.form['model']
        ios = request.form['ios']
        agency = request.form['agency']
        site = request.form['site']
        ci_name = request.form['ci_name']
        config = request.form['config']

        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute
        cur.execute("UPDATE sw_templates SET brand=%s, type=%s, model=%s, IOS=%s, agency=%s, site=%s, ci_name=%s, config=%s, last_editor=%s WHERE id = %s", (brand, type, model, ios, agency, site, ci_name, config, session['username'],id))


        # Commit to # DEBUG:
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('Template Updated','success')

        return redirect(url_for('dashboard'))

    return render_template('edit_sw_template.html', form=form)

# Delete switch Template
@app.route('/delete_switch/<string:id>', methods=['POST'])
@is_logged_in
def delete_switch(id):
    #Create cursor
    cur = mysql.connection.cursor()

    # Execute Delte
    cur.execute("DELETE FROM sw_templates WHERE id = %s", [id])

    # Commit to # DEBUG:
    mysql.connection.commit()

    # Close connection
    cur.close()

    flash('Template Deleted','success')

    return redirect(url_for('dashboard'))

# # Deltetest Page
# @app.route('/deteletest')
# def router():
#     return render_template('deletetest.html')


if __name__ == '__main__':
    app.secret_key='secure123'
    app.run(host="0.0.0.0", debug=True)
