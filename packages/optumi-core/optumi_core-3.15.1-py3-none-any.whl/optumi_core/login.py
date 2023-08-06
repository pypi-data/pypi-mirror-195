##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
##

from .logging import optumi_format_and_log
from .sessions import get_session, get_mode, NotLoggedInException
from .exceptions import NotLoggedInException
from .utils import dev_version, get_portal_domain_and_port, get_portal_port

## Standard library imports

# Generic Operating System Services
import time, os
from pathlib import Path
from datetime import datetime
from dateutil import parser

# Python Runtime Services
import traceback

# Concurrent execution
from threading import Lock

# Internet Protocols and Support
from http.cookiejar import DefaultCookiePolicy, CookieJar
import requests
from requests.exceptions import HTTPError
from urllib.error import URLError
from urllib.parse import urlparse, parse_qs

# Internet Data Handling
import json, base64

# Networking and Interprocess Communication
import socket, ssl

# Structured Markup Processing Tools
import html

## Other imports
# from cryptography import x509
# from cryptography.hazmat.backends import default_backend
from pathlib import Path
import pickle

lock = Lock()
loginProgress = None


def get_cookie_file():
    COOKIE_FILE = os.path.expanduser("~") + "/.optumi/" + get_mode() + "_cookies.pickle"
    os.makedirs(Path(COOKIE_FILE).parent, exist_ok=True)
    return COOKIE_FILE


def get_token_file():
    TOKEN_FILE = os.path.expanduser("~") + "/.optumi/" + get_mode() + "_token"
    os.makedirs(Path(TOKEN_FILE).parent, exist_ok=True)
    return TOKEN_FILE

def get_login_progress():
    try:
        lock.acquire()
        return loginProgress
    except:
        pass
    finally:
        lock.release()

def set_login_progress(message):
    global loginProgress
    try:
        lock.acquire()
        loginProgress = message
    except:
        pass
    finally:
        lock.release()


def sign_agreement(timeOfSigning, hashOfSignedAgreement):
    URL = "/exp/jupyterlab/sign-agreement"
    try:
        return get_session().post(
            URL,
            data={
                "timeOfSigning": timeOfSigning,
                "hashOfSignedAgreement": hashOfSignedAgreement,
            },
            timeout=30,
        )
    except HTTPError as e:
        return e


def get_new_agreement():
    URL = "/exp/jupyterlab/get-new-agreement"
    try:
        return get_session().get(URL, timeout=30)
    except HTTPError as e:
        return e


def exchange_versions(version):
    try:
        # Load cookies from the disk
        COOKIE_FILE = get_cookie_file()
        if os.path.exists(COOKIE_FILE):
            with open(COOKIE_FILE, "rb") as f:
                get_session().cookies.update(pickle.load(f))
                if dev_version:
                    print("Reading", get_mode(), "cookies:")
                now = time.time()
                for cookie in get_session().cookies:
                    if cookie.expires != None and cookie.expires - now < 0:
                        if dev_version:
                            print(
                                "Clearing",
                                cookie.name,
                                cookie.value,
                                cookie.domain,
                                cookie.expires,
                            )
                        get_session().cookies.clear(cookie.domain)
                if dev_version:
                    for cookie in get_session().cookies:
                        print(cookie.name, cookie.value, cookie.domain, cookie.expires)
    except Exception as err:
        # pass
        print(err)

    URL = "/exp/jupyterlab/exchange-versions"
    try:
        return get_session().post(
            URL,
            data={
                "version": version,
            },
            timeout=30,
        )
    except HTTPError as e:
        return e


def get_redirect():
    try:
        # Load cookies from the disk
        COOKIE_FILE = get_cookie_file()

        if os.path.exists(COOKIE_FILE):
            with open(COOKIE_FILE, "rb") as f:
                get_session().cookies.update(pickle.load(f))
                # if dev_version:
                #     print("reading", get_mode(), "cookies:")
                now = time.time()
                for cookie in get_session().cookies:
                    if cookie.expires != None and cookie.expires - now < 0:
                        # if dev_version:
                        #     print(
                        #         "Clearing",
                        #         cookie.name,
                        #         cookie.value,
                        #         cookie.domain,
                        #         cookie.expires,
                        #     )
                        get_session().cookies.clear(cookie.domain)
                # if dev_version:
                #     for cookie in get_session().cookies:
                #         print(cookie.name, cookie.value, cookie.domain, cookie.expires)
    except Exception as err:
        # pass
        print(err)

    URL = "/exp/jupyterlab/get-redirect"
    try:
        return get_session().get(URL, timeout=30)
    except HTTPError as e:
        return e


def check_login(login_domain, login_port):
    session = get_session()
    try:
        response = get_redirect()
        if response.url.endswith("/login"):
            session._domain_and_port = get_portal_domain_and_port()
            return False
        redirect = json.loads(response.text)
        if redirect == {}:
            # We have no assigned controller for a local station and therefore no redirect
            return True
        elif "dnsName" in redirect and "port" in redirect:
            session._domain_and_port = redirect["dnsName"] + ":" + str(redirect["port"])
            if redirect["dnsName"] == login_domain and redirect["port"] == login_port:
                return True
            else:
                return check_login(redirect["dnsName"], redirect["port"])
        session._domain_and_port = get_portal_domain_and_port()
        return False
    except (HTTPError, NotLoggedInException) as e:
        session._domain_and_port = get_portal_domain_and_port()
        return False


def login_rest_server(
    login_domain,
    login_port,
    token=None,
    login_type="oauth",
    save_token=False,
):
    try:
        start_time = None
        last_domain_and_port = None
        session = get_session()
        while True:
            if start_time == None:
                start_time = time.time()
            elif time.time() - start_time > 600:  # 10 minute timeout
                session._domain_and_port = get_portal_domain_and_port()
                return -1, "Timed out"
            # If we want to move back to using a devserver certificate we need to check for devserver.optumi.com explicitly
            # Since we are bypassing the hostname check for the SSL context, we manually check it here
            # cert = ssl.get_server_certificate((DOMAIN, 8443))
            # cert = x509.load_pem_x509_certificate(cert.encode(), default_backend())
            # name = cert.subject.get_attributes_for_oid(x509.oid.NameOID.COMMON_NAME)[0].value
            # if name != 'devserver.optumi.com':
            #     raise ssl.SSLCertVerificationError("SSL domain check failed (" + name + " is not devserver.optumi.com)")

            session._domain_and_port = login_domain + ":" + str(login_port)

            URL = "/login"
            errorURL = URL + "?error"

            # We only want to print to the log when we try to contact somewhere new
            if session._domain_and_port != last_domain_and_port:
                if dev_version:
                    print(optumi_format_and_log(None, "Contacting " + URL))
                else:
                    optumi_format_and_log(None, "Contacting " + URL)

            # since it can take a long time to log in to actually log in to the station, set a longer timeout for that request
            timeout = (
                30
                if session._domain_and_port == get_portal_domain_and_port()
                or session._domain_and_port
                == "portal.optumi.net:" + str(get_portal_port())
                else 120
            )

            if login_type == "token" and token is None:
                # Try to load the token from the disk
                TOKEN_FILE = get_token_file()

                if os.path.exists(TOKEN_FILE):
                    with open(TOKEN_FILE, "r") as f:
                        token = f.read()
                else:
                    session._domain_and_port = get_portal_domain_and_port()
                    return -1, "No login token"

            try:
                response = session.post(
                    URL,
                    data={"login_type": login_type, "username": "", "password": token},
                    timeout=timeout,
                )
            except URLError as err:
                if isinstance(err.reason, socket.timeout):
                    return -1, "Timed out"
                if isinstance(err.reason, socket.gaierror):
                    if (
                        session._domain_and_port == get_portal_domain_and_port()
                        or session._domain_and_port
                        == "portal.optumi.net:" + str(get_portal_port())
                    ):
                        # If we failed trying to access portalAB.optumi.net or portal.optumi.net, redirect to the top level portal.optumi.net
                        login_domain = "portal.optumi.net"
                        login_port = PORTAL_PORT
                        last_domain_and_port = session._domain_and_port
                        continue
                    else:
                        # If we were trying to access a station, redirect to portalAB.optumi.net
                        login_domain = PORTAL
                        login_port = PORTAL_PORT
                        last_domain_and_port = session._domain_and_port
                        continue
                if isinstance(err.reason, ConnectionRefusedError):
                    time.sleep(2)
                    login_domain = login_domain
                    login_port = login_port
                    last_domain_and_port = session._domain_and_port
                    continue
                raise err

            parsed = urlparse(response.url)

            redirect = None
            try:
                redirect = json.loads(response.text)
            except:
                pass

            if redirect != None:
                if redirect["dnsName"] == "unknown":
                    set_login_progress("Allocating...")
                    time.sleep(2)
                    login_domain = login_domain
                    login_port = login_port
                    last_domain_and_port = session._domain_and_port
                    continue
                elif (
                    redirect["dnsName"] == "no more stations"
                    or redirect["dnsName"] == "no more trial stations"
                ):
                    session._domain_and_port = get_portal_domain_and_port()
                    return -1, redirect["dnsName"]
                else:
                    set_login_progress("Restoring context...")
                    login_domain = redirect["dnsName"]
                    login_port = redirect["port"]
                    last_domain_and_port = session._domain_and_port
                    continue

            if parsed.path == "/login" and parsed.query == "error":
                # Parse the error message to pass on to the user
                raw_html = response.text
                try:
                    message = raw_html.split(
                        '<div class="alert alert-danger" role="alert">'
                    )[1].split("</div>")[0]
                except:
                    message = "Invalid username/password"

                session._domain_and_port = get_portal_domain_and_port()
                return -1, message

            ## This is currently necessary in order for the controller to recognize that the user has signed the agreement
            get_new_agreement()

            # Save cookies to the disk
            try:
                # Load cookies from the disk
                COOKIE_FILE = get_cookie_file()

                with open(COOKIE_FILE, "wb") as f:
                    # if dev_version:
                    #     print("Writing", get_mode(), "cookies:")
                    #     for cookie in get_session().cookies:
                    #         print(
                    #             cookie.name, cookie.value, cookie.domain, cookie.expires
                    #         )
                    pickle.dump(get_session().cookies, f)
                    os.chmod(COOKIE_FILE, 0o600)
            except Exception as err:
                # pass
                print(err)

            if save_token:
                TOKEN_FILE = get_token_file()

                print("Saving connection token to", TOKEN_FILE)

                # Get a token and save it on the disk so the user will stay logged in
                if login_type != "token":
                    from .core import get_connection_token  # Avoid circular import

                    response = json.loads(get_connection_token(False).text)
                    expiration = None if response["expiration"] is None else parser.parse(response["expiration"])
                    if expiration is None or expiration < parser.parse(datetime.now().isoformat() + "Z"):
                        response = json.loads(get_connection_token(True).text)
                    token = response["token"]
                with open(TOKEN_FILE, "w+") as f:
                    f.write(token)

                os.chmod(TOKEN_FILE, 0o600)

            # On success return the status value 1 and the domain that we logged in to
            return 1, session._domain_and_port
    except Exception as err:
        print(optumi_format_and_log(None, str(err)))
        traceback.print_exc()
        session._domain_and_port = get_portal_domain_and_port()
        return -2, ""


def logout(remove_token=True):
    URL = "/logout"
    try:
        if remove_token:
            TOKEN_FILE = get_token_file()
            try:
                os.remove(TOKEN_FILE)
                print("Removed connection token")
            except OSError:
                pass
        return get_session().get(URL, timeout=120)
    except HTTPError as e:
        return e
