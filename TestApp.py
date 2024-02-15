import pytest
from bottle import Bottle, template, TEMPLATE_PATH
import requests
from requests import get, post
from FileUpload import login
import os
import sqlite3

base_url = 'http://localhost:8082'
TEMPLATE_PATH.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "Views")))

def test_login():
    url = base_url+'/login'
    response = requests.get(url)
    assert response.status_code == 200
    assert response.text == template('Login.tpl', register=False, retry=False, register_success=False, logout=False)

    query_params = {'register': 'true'}
    response = requests.get(url, params=query_params)
    assert response.status_code == 200
    assert response.text == template('Login.tpl', register=True, retry=False, register_success=False, logout=False)

    query_params = {'retry': 'true'}
    response = requests.get(url, params=query_params)
    assert response.status_code == 200
    assert response.text == template('Login.tpl', register=False, retry=True, register_success=False, logout=False)

    query_params = {'register_success': 'true'}
    response = requests.get(url, params=query_params)
    assert response.status_code == 200
    assert response.text == template('Login.tpl', register=False, retry=False, register_success=True, logout=False)

    query_params = {'logout': 'true'}
    response = requests.get(url, params=query_params)
    assert response.status_code == 200
    assert response.text == template('Login.tpl', register=False, retry=False, register_success=False, logout=True)


def test_register():
    url = base_url+'/register'
    response = requests.get(url)
    assert response.status_code == 200
    assert response.text == template('Register.tpl', register=True, user_exists=False)


def test_register_reply():
    url = base_url+'/register'

    # Passwords do not match
    response = requests.post(url, data={'username': 'testuser1', 'firstname': 'Will', 'lastname': 'Smith', 'password_1': 'WillSmith23', 'password_2': 'willsmith23'})
    assert response.status_code == 200
    assert response.text == template('Register.tpl', register=False, user_exists=False)

    # Successful registration
    response = requests.post(url, data={'username': 'testuser1', 'firstname': 'Will', 'lastname': 'Smith', 'password_1': 'WillSmith23', 'password_2': 'WillSmith23'})
    assert response.status_code == 200
    assert response.text == template('login.tpl', register=False, retry=False, register_success=True, logout=False)

    # username already exists
    response = requests.post(url, data={'username': 'testuser1', 'firstname': 'Will', 'lastname': 'Smith', 'password_1': 'WillSmith23', 'password_2': 'WillSmith23'})
    assert response.status_code == 200
    assert response.text == template('Register.tpl', register=False, user_exists=True, user='testuser1')


def test_login_reply():
    url = base_url+'/login'

    # Test user does not exist, register
    response = requests.post(url, data={'username': 'testuser2', 'password': 'aaaaaaaaa'})
    assert response.status_code == 200
    assert response.text == template('Login.tpl', register=True, retry=False, register_success=False, logout=False)

    # Test incorrect password
    response = requests.post(url, data={'username': 'testuser1', 'password': 'aaaaaaaaa'})
    assert response.status_code == 200
    assert response.text == template('Login.tpl', register=False, retry=True, register_success=False, logout=False)

    # Login successful
    response = requests.post(url, data={'username': 'testuser1', 'password': 'WillSmith23'})
    assert response.status_code == 200
    assert response.text == template('DropFiles.tpl', welcome=True, user='Will')


def test_upload_page():
    url = base_url+'/upload/Will'
    response = requests.get(url)
    assert response.status_code == 200
    assert response.text == template('DropFiles.tpl', welcome=True, user='Will')


def test_drop_files():
    url = base_url+'/upload/Will'

    # File upload successful
    files = {'upload': open('testfile.txt', 'rb')}
    response = requests.post(url, files=files)
    cwd = os.getcwd()
    folder_path = cwd+"/Files"
    assert response.status_code == 200
    assert response.text == template('DropFiles.tpl', welcome=False, file_success=True, user='Will', folder_name=folder_path)

    # File exists
    response = requests.post(url, files=files)
    cwd = os.getcwd()
    folder_path = cwd+"/Files"
    error = "File already exists! Delete file and re-upload to overwrite"
    assert response.status_code == 200
    assert response.text == template('DropFiles.tpl', welcome=False, file_success=False, file_fail=True, user='Will', error_message=error)


def test_delete():
    url = base_url+'/delete/Will'

    # File delete successful
    filename = 'testfile.txt'
    response = requests.post(url, data={'filename':filename})
    cwd = os.getcwd()
    folder_path = cwd+"/Files"
    assert response.status_code == 200
    assert response.text == template('DropFiles.tpl', welcome=False, file_success=False, file_fail=False, folder_success=False, folder_fail=False, delete_success=True, user='Will', folder_name=folder_path)

    # File not found
    response = requests.post(url, data={'filename':filename})
    error = "File not found!"
    assert response.status_code == 200
    assert response.text == template('DropFiles.tpl', welcome=False, file_success=False, file_fail=False, folder_success=False, folder_fail=False, delete_success=False, delete_fail=True, user='Will', error_message=error)

    # Folder delete
    folder_path = cwd+"/Files/test"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    response = requests.post(url, data={'filename':'test'})
    error = "Cannot delete folders! Please enter a filename!"
    assert response.status_code == 200
    assert response.text == template('DropFiles.tpl', welcome=False, file_success=False, file_fail=False, folder_success=False, folder_fail=False, delete_success=False, delete_fail=True, user='Will', error_message=error)


def test_logout():
    url = base_url+'/logout/Will'
    response = requests.post(url)
    assert response.status_code == 200
    assert response.text == template('Login.tpl', register=False, retry=False, register_success=False, logout=True)
    
    # Delete the user
    user="testuser1"
    connection = sqlite3.connect("Users.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM UserAuthentication where username=?", (user,))
    connection.commit()
    connection.close()

    # shutdown the server to stop the test thread
    response = requests.get(base_url+'/shutdown')