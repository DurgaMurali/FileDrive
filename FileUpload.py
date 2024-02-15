from bottle import route, run, request, template, redirect, TEMPLATE_PATH
import sqlite3
import os
import sys


# Login page
@route('/login')
def login():
    is_register = request.query.get('register') == 'true'
    is_retry = request.query.get('retry') == 'true'
    is_register_success = request.query.get('register_success') == 'true'
    is_logout = request.query.get('logout') == 'true'
    return template('Login.tpl', register=is_register, retry=is_retry, register_success=is_register_success, logout=is_logout)


# Login POST
@route('/login', method='POST')
def login_reply():
    user = request.forms.get('username')
    password = request.forms.get('password')
    cursor.execute("SELECT firstname, password from UserAuthentication where username=?", (user,))
    rows = cursor.fetchone()

    # User does not exist
    if(rows == None):
        return template('Login.tpl', register=True, retry=False, register_success=False)
    # User exists and password matches
    elif(rows[1] == password):
        print("Login success")
        url = '/upload?username='
        redirect('/upload/{}'.format(rows[0]))
    # Incorrect password
    elif(rows[1] != password):
        print("Login Failed")
        return template('Login.tpl', register=False, retry=True, register_success=False)


# File upload Page redirect
@route('/upload/<username>')
def upload_page(username):
    return template('DropFiles.tpl', welcome=True, user=username.title())


# File upload
@route('/upload/<username>', method='POST')
def drop_files(username):
    upload = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    cwd = os.getcwd()
    folder_path = cwd+"/Files"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = "{path}/{file}".format(path=folder_path, file=upload.filename)
    try:
        upload.save(file_path)
    except IOError as e:
        print(e)
        error = "File already exists! Delete file and re-upload to overwrite"
        return template('DropFiles.tpl', welcome=False, file_success=False, file_fail=True, user=username, error_message=error)

    return template('DropFiles.tpl', welcome=False, file_success=True, user=username, folder_name=folder_path)


# File delete
@route('/delete/<username>', method='POST')
def delete(username):
    filename = request.forms.get('filename')
    cwd = os.getcwd()
    folder_path = cwd+"/Files"
    file_path = "{path}/{file}".format(path=folder_path, file=filename)

    try:
        os.remove(file_path)
    except FileNotFoundError as e:
        print(e)
        error = "File not found!"
        return template('DropFiles.tpl', welcome=False, file_success=False, file_fail=False, folder_success=False, folder_fail=False, delete_success=False, delete_fail=True, user=username, error_message=error)
    except OSError as e:
        print(e)
        error = "Cannot delete folders! Please enter a filename!"
        return template('DropFiles.tpl', welcome=False, file_success=False, file_fail=False, folder_success=False, folder_fail=False, delete_success=False, delete_fail=True, user=username, error_message=error)
    
    return template('DropFiles.tpl', welcome=False, file_success=False, file_fail=False, folder_success=False, folder_fail=False, delete_success=True, user=username, folder_name=folder_path)


# Create Folder
@route('/newfolder/<username>', method='POST')
def createFolder(username):
    folder = request.forms.get('folder')

    # if folder is empty -- handle this case
    cwd = os.getcwd()
    folder_path = cwd+"/Files/"+folder

    try:
        os.makedirs(folder_path)
        return template('DropFiles.tpl', welcome=False, file_success=False, file_fail=False, folder_success=True, user=username, folder_name=folder_path)
    except OSError as e:
        return template('DropFiles.tpl', welcome=False, file_success=False, file_fail=False, folder_success=False, folder_fail=True, user=username, error_message=e)


# Register Page
@route('/register')
def register():
    return template('Register.tpl', register=True, user_exists=False)


# Register POST
@route('/register', method='POST')
def register_reply():
    user = request.forms.get('username')
    firstname = request.forms.get('firstname')
    lastname = request.forms.get('lastname')
    password_1 = request.forms.get('password_1')
    password_2 = request.forms.get('password_2')

    # Password and re-entered password do not match
    if(password_1 != password_2):
        return template('Register.tpl', register=False, user_exists=False)
    
    # Check if username already exists
    cursor.execute("SELECT username, password from UserAuthentication where username=?", (user,))
    rows = cursor.fetchone()

    # User does not exist, create new user
    if(rows == None):
        cursor.execute("INSERT INTO UserAuthentication(firstname, lastname, username, password) VALUES(?, ?, ?, ?)", (firstname, lastname, user, password_1))
        connection.commit()
        redirect('/login?register=false&retry=false&register_success=true&logout=false')
    # User already exists, re-register
    else:
        return template('Register.tpl', register=False, user_exists=True, user=user)


@route('/logout/<username>', method='POST')
def logout(username):
    redirect('/login?register=false&retry=false&register_success=false&logout=true')

@route('/shutdown')
def shutdown():
    sys.stderr.close()


if __name__ == '__main__':
    connection = sqlite3.connect("Users.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS UserAuthentication(firstname text NOT NULL, lastname text NOT NULL, username text NOT NULL, password text NOT NULL)")
    print(os.path.dirname(__file__))
    print(os.path.join(os.path.dirname(__file__), "Views"))
    print(os.path.abspath(os.path.join(os.path.dirname(__file__), "Views")))

    # Set TEMPLATE_PATH to make this work in container environment
    TEMPLATE_PATH.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "Views")))

    run(host='0.0.0.0', port='8082')
    connection.close()