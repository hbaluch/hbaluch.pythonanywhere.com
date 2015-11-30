from flask import Flask, request, render_template, redirect, url_for, flash
from db_operations import UrlStorageUtility
from base62coder import Base62Coder
from urllib.parse import urlparse
import re

app = Flask(__name__)
db = UrlStorageUtility()

#
# Home page
#
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':

        #Get Url from form
        original_url    = request.form.get('original_url')

        #Validate Url
        parsed_url = urlparse(original_url)
        if parsed_url.scheme == '':
            original_url = 'http://'+original_url

        #If Url is not valid, show the error message
        if not is_valid_url(original_url):
            return render_template('ShowResult.html', home_page='http://'+request.host)

        #But if the Url is fine, insert it in DB, and prepare a base 62 code based on unique ID
        record_id       = db.insert_url_and_get_id(original_url)
        encoder         = Base62Coder()
        short_url       = encoder.convert_to_base62(record_id)

        #Show the shortened Url to the user.
        return redirect (url_for('show_short_url', short_url= short_url))
    return render_template('form.html')

#
# Show short url
#
@app.route('/show_short_url/<short_url>', methods=['GET', 'POST'])
def show_short_url(short_url):
    return render_template('ShowResult.html', short_url='http://'+request.host+'/'+short_url)


#
# Redirect to original Url, if shortened URL has been entered by any user
#
@app.route('/<short_url>')
def redirect_to_original_url(short_url):
    encoder         = Base62Coder()
    #Compute the Unique Id by decoding base 62 shortened Url
    record_id       = encoder.back_to_decimal(short_url)

    #Fetch original Url and redirect to the Url
    original_url    = db.fetch_original_url(record_id)
    if original_url == 'INVALID':
        return render_template('ShowResult.html', home_page='http://'+request.host)
    return redirect(original_url)


#Validate Url based on a Django regular expression for URL validation
def is_valid_url(url):

    url_regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if url is not None and url_regex.match(url):
        return True
    else:
        return False