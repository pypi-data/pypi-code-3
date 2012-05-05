# -*- coding: utf-8 -*-
"""
    # Shake.Auth

    Copyright © 2010–2011 by Lúcuma labs (http://lucumalabs.com).
    MIT License. (http://www.opensource.org/licenses/mit-license.php)

"""
from datetime import datetime
import hashlib
import time

from jinja2.exceptions import TemplateNotFound
from shake import url_for, from36, to36, redirect, Rule, StorageDict

try:
    import mailshake
except ImportError:
    pass

from .perms import REDIRECT_FIELD_NAME, is_valid
from .utils import (bcrypt, LazyUser, Token,
    auth_render, split_hash, hash_sha256, hash_sha512, hash_bcrypt)


class UserExistsError(ValueError):
    
    def __init__(self, login):
        self.login = login
    
    def __repr__(self):
        return "A user with the login '%s' already exists." % self.login


class UserDoesNotExistsError(ValueError):
    
    def __init__(self, login):
        self.login = login
    
    def __repr__(self):
        return "A user with the login '%s' dosen't exists." % self.login


class PasswordTooShortError(ValueError):
    
    def __init__(self, minlen):
        self.minlen = minlen
    
    def __repr__(self):
        return ("The password is too short. It must be at least "
            "%s chars long." % self.minlen)


CREDENTIAL_LOGIN = 'login'
CREDENTIAL_PASSWORD = 'password'
CREDENTIAL_TOKEN = 'token'


class Auth(object):
    """
    # Parameters:

    User
    :   an User model.
        
    app
    :   a Shake instance. Can be added later by calling `auth.init_app`.

    settings
    :   named settings. The following settings are available.
    

    # Settings
    
    pepper
    :   required.
        A hardcoded (meaning "not stored in the database") system-wide
        secret 'salt'.
        
        By using this, an attacker would need to gain access to both
        the database and the filesystem (where your settings file is)
        in order to start trying an off-line attack.
        
        **You cannot change this value if there are already stored passwords
        or they all will become invalid**.
    
    hash_alg
    :   the name of the hashing algorithm, this can be one of the following:
        'bcrypt', 'sha512' or 'sha256'. If None, we use the best function
        available.
    
    hash_cost
    :   non-negative integer that control the cost of the hash algorithm.
        The number of operations is proportional to 2**cost.
    
    sign_in_redirect
    :   where to redirect the user, after signing in.
        This can be a callable.
    
    sign_out_redirect
    :   where to redirect the user, after signing out.
        This can be a callable.
        Ignored if `sign_out_view` is not None.

    password_minlen
    :   minimum number of chars the password must have.
        A `PasswordTooShortError` will be raised if it does not follow
        this limit.

    reset_expire
    :   number of hours after the reset-password one time use token become
        invalid.  This number can be a float to indicate a fraction of an
        hour (e.g.: 0.5 = 30 minutes).
    
    sign_in_view
    :   template used to render the sign in form.
    
    sign_out_view
    :   template rendered after the user sign out.
        
    change_password_view
    :   template udes to render the "Forgot your password?" form.
    
    reset_password_view
    :   template to render when resetting a password.
    
    email_reset_view
    :   template to use to send the reset-password email.

    render
    :   a render instance (used in all auth controllers)

    mailer
    :   a mailer instance (used in the reset password controller)
    
    ..:note::
    
    The passwords hashes are stored with the following
    format (without the spaces):
        
        sha_name $ cost $ salt $ salted_and_hashed_password
        - or -
        bcrypt $ cost $ salt salted_and_hashed_password

    """
    
    defaults = {
        'pepper': None,
        'hash_alg': None,
        'hash_cost': 12,

        'sign_in_redirect': '/',
        'sign_out_redirect': '/',
        'password_minlen': 5,
        'reset_expire': 3,  # hours

        'sign_in_view': 'auth_sign_in.html',
        'sign_out_view': None,
        'reset_password_view': 'auth_reset_password.html',
        'email_reset_view': 'auth_email_reset_password.html',
        'change_password_view': 'auth_change_password.html',

        'render': None,
        'mailer': None,
    }

    LazyUser = LazyUser
    
    def __init__(self, User, app=None, **settings):
        self.User = User
        self.db = User.db
        
        settings = StorageDict(settings)
        for k, default in self.defaults.items():
            settings.setdefault(k, default)
        
        assert settings.pepper is not None, "A `pepper` setting is required"
        
        hash_alg = settings.hash_alg
        
        if not hash_alg:
            if bcrypt:
                self.hash_func = hash_bcrypt
                settings.hash_alg = 'bcrypt'
            else:
                self.hash_func = hash_sha512
                settings.hash_alg = 'sha512'
        
        elif hash_alg == 'bcrypt':
            if not bcrypt:
                raise ImportError("Hash algorithm 'bcrypt' not available")
            self.hash_func = hash_bcrypt
        
        elif hash_alg == 'sha512':
            self.hash_func = hash_sha512
        
        elif hash_alg == 'sha256':
            self.hash_func = hash_sha256
        
        else:
            raise ValueError("The `hash_alg` parameter must be either " \
                "'bcrypt', 'sha512' or 'sha256'")
        
        hash_cost = settings.hash_cost
        assert isinstance(hash_cost, (int, long)) and hash_cost >= 0, \
            "`hash_cost` parameter must be a positive integer"
        
        if (hash_alg == 'bcrypt') and (hash_cost < 4):
            settings.hash_cost = 4
        
        assert settings.reset_expire >= 0, \
            "`reset_expire` parameter must be a positive number"
    
        self.settings = settings
        
        if app:
            self.init_app(app)
    
    
    def init_app(self, app):
        """This callback can be used to initialize an application for the
        use with this authentication setup.
        """
        self.app = app
        
        @app.before_request
        def set_user(request):
            self.get_user(request)
    

    def get_user(self, request):
        request.__class__.user = self.LazyUser(self.db, self.User)
    

    def authenticate(self, credentials, update=True):
        """Check if there's a matching pair of login/hashed_password in the
        database.
        
        Returns the user if the credentials are correct, or None.
        """
        login = credentials.get(CREDENTIAL_LOGIN)
        password = credentials.get(CREDENTIAL_PASSWORD)
        if login and password:
            return self._loginpass_authentication(login, password, update)
        
        token = credentials.get(CREDENTIAL_TOKEN)
        if token:
            return self._token_authentication(token)
    

    def _loginpass_authentication(self, login, password, update):
        # iOS by default makes you write the first letter as uppercase.
        # The username should be case insensitive anyway.
        login = login.lower()
        user = self.db.query(self.User) \
            .filter(self.User.login == login).first()
        if not user:
            return None
        if not self.check_password(password, user.password):
            return None
        
        if update:
            # If the authentication was successful, update the password hash
            # to the current algorithm and cost.
            hash_alg, hash_cost, salt = split_hash(user.password)
            must_update_hash = hash_alg != self.settings.hash_alg
            must_update_cost = hash_cost != self.settings.hash_cost
            if must_update_hash or must_update_cost:
                new_password = self.hash_password(password)
                user.password = new_password
        return user
    

    def _token_authentication(self, token):
        try:
            login, time36, mac = token.split('.')
        except ValueError:
            return None
        
        user = self.db.query(self.User) \
            .filter(self.User.login == login).first()
        if not user:
            return None
        
        # Check that the user/timestamp has not been tampered with
        retoken = self.get_reset_token(user, time36)
        if str(retoken) != token:
            return None
        
        timestamp = from36(time36)
        # Check if the token has not expired
        if (time.time() - timestamp) > (self.settings.reset_expire * 3600):
            return None
        
        return user
    

    def hash_password(self, password):
        return self.hash_func(password, cost=self.settings.hash_cost,
            pepper=self.settings.pepper)
    

    def check_password(self, password, stored_password):
        """Returns a boolean of whether the password is correct.
        
        Handles hashing behind the scenes.
        """
        if stored_password is None:
            return False
        
        try:
            hash_alg, hash_cost, salt = split_hash(stored_password)
        except ValueError:
            raise ValueError("The stored password isn't a valid hash")
        
        if hash_alg == 'bcrypt':
            assert 'bcrypt' in globals().keys(), ('\'bcrypt\' is not '
                'available but the stored password was hashed using it.\n '
                'Please install py-bcrypt '
                '<http://pypi.python.org/pypi/py-bcrypt/>')
            
            hashed = hash_bcrypt(password, hash_cost, stored_password,
                self.settings.pepper)
        
        elif hash_alg == 'sha512':
            hashed = hash_sha512(password, hash_cost, salt,
                self.settings.pepper)
        
        elif hash_alg == 'sha256':
            hashed = hash_sha256(password, hash_cost, salt,
                self.settings.pepper)
        
        else:
            raise ValueError("Hash algorithm '%s' not available" % hash_alg)
        return stored_password == hashed
    

    def set_password(self, user, passw):
        if len(passw) < self.settings.password_minlen:
            raise PasswordTooShortError(self.settings.password_minlen)
        user.password = self.hash_password(passw)
    

    def get_reset_token(self, user, time36=None):
        """Make a timestamped one-time-use token that can be used to
        identifying the user.
        
        By hashing on the internal state of the user that is sure to
        change (the password salt and the last_sign_in)
        we produce a token that will be invalid as soon as it or the
        old password is used.
        
        We hash also a secret key, so without access to the source code,
        fake tokens cannot be generated even if the database is compromised.
        """
        time36 = time36 or to36(int(time.time()))
        msg = ''.join([
            self.app.settings.SECRET_KEY,
            getattr(user, 'password', '')[10:50],
            unicode(getattr(user, 'last_sign_in', '')),
            unicode(getattr(user, 'id', 0)),
            unicode(time36),
        ])
        
        mac = hashlib.sha512(msg).hexdigest()[:50]
        
        token = '%s.%s.%s' % (user.login, time36, mac)
        return Token(token, self.settings.reset_expire)
    

    def sign_in(self, request, user):
        self.LazyUser.sign_in(request, user)
    

    def sign_out(self, request):
        self.LazyUser.sign_out(request)
    
    # This method is intended to be called from the command line.
    def create_user(self, login, passw, **data):
        """[-login] USER_NAME [-passw] PASSWORD
        Creates a new user."""
        # iOS by default makes you write the first letter as uppercase.
        # The username should be case insensitive anyway.
        login = login.lower()
        user_exists = self.db.query(self.User) \
            .filter(self.User.login == login).count()
        if user_exists:
            raise UserExistsError(login)
        if len(passw) < self.settings.password_minlen:
            raise PasswordTooShortError(self.settings.password_minlen)
        
        passw = self.hash_password(passw)
        user = self.User(login=login, password=passw, **data)
        self.db.add(user)
        self.db.commit()
        return user
    
    # This method is intended to be called from the command line.
    def change_password(self, login, passw):
        """[-login] USER_NAME [-passw] NEW_PASSWORD
        Changes the password of an existing user."""
        # iOS by default makes you write the first letter as uppercase.
        # The username should be case insensitive anyway.
        login = login.lower()
        user = self.db.query(self.User) \
            .filter(self.User.login == login).first()
        if not user:
            raise UserDoesNotExistsError(login)
        self.set_password(user, passw)
        self.db.commit()
        return user
    

    def render(self, view, **context):
        try:
            return self.settings.render(view, context)
        except TemplateNotFound:
            return auth_render(view, context)
    

    def render_to_string(self, view, **context):
        try:
            return self.settings.render.to_string(view, context)
        except TemplateNotFound:
            return auth_render.to_string(view, context)
    

    def sign_in_controller(self, request, **kwargs):
        """Signs a user in.
        """
        redirect_to = request.session.get(REDIRECT_FIELD_NAME)
        redirect_to = redirect_to or self.settings.sign_in_redirect
        if callable(redirect_to):
            redirect_to = redirect_to()
        
        # Redirect if there's already a signed user
        if request.user:
            request.session.pop(REDIRECT_FIELD_NAME, None)
            return redirect(redirect_to)
        
        credentials = request.form
        kwargs['auth'] = self
        kwargs['credentials'] = credentials
        kwargs['error'] = None
        
        if request.is_post:
            user = self.authenticate(credentials)
            if user:
                if hasattr(user, 'last_sign_in'):
                    user.last_sign_in = datetime.utcnow()
                    self.db.commit()
                self.sign_in(request, user)
                return redirect(redirect_to)
            kwargs['error'] = 'FAIL'
        
        view = self.settings.sign_in_view
        return self.render(view, **kwargs)
    

    def sign_out_controller(self, request, **kwargs):
        """Signs out a user.
        
        view
        :   Optional full name of a view to display after
            signing out the user.

        """
        redirect_to = request.session.get(REDIRECT_FIELD_NAME)
        redirect_to = redirect_to or self.settings.sign_out_redirect
        if callable(redirect_to):
            redirect_to = redirect_to()
        
        self.sign_out(request)
        
        view = self.settings.sign_out_view
        if view:
            kwargs['auth'] = self
            return self.render(view, **kwargs)
        return redirect(redirect_to)
    

    def change_password_controller(self, request, token=None, **kwargs):
        """A apge to generate a link to reset your password.
        
        token
        :   optional timestamped one-time-use token.
        
        """
        kwargs['auth'] = self
        kwargs['credentials'] = request.form
        kwargs['ok'] = False
        kwargs['error'] = None
        
        if not token and request.user:
            return redirect(url_for('auth.change_password'))
        
        # Phase 3
        if token:
            credentials = {CREDENTIAL_TOKEN: token}
            user = self.authenticate(credentials)
            if user:
                if request.user and (request.user != user):
                    self.sign_out(request)
                self.sign_in(request, user)
                return self.reset_password_controller(request, user_requested=False)
            
            kwargs['error'] = 'WRONG TOKEN'
        
        # Phase 2
        elif request.is_post:
            login = request.form.get('login')
            # iOS by default makes you write the first letter as uppercase.
            # The username should be case insensitive anyway.
            login = login.lower()
            user = self.db.query(self.User) \
                .filter(self.User.login == login).first()
            if not user:
                kwargs['error'] = 'NOT FOUND'
            else:
                # User founded. Send token by email
                token = self.get_reset_token(user)
                self.email_token(user, token)
                kwargs['ok'] = True
        
        view = self.settings.reset_password_view
        return self.render(view, **kwargs)
    

    def email_token(self, user, token):
        view = self.settings.email_reset_view
        self.render_to_string(view, {'user': user, 'token': token})
        msg = msg.encode('utf-8')
        
        mailer = self.settings.mailer
        email_msg = mailshake.EmailMessage(
            subject='Reset your password',
            text_content='',
            from_email=mailer.default_from,
            to=user.email
        )
        if view.endswith('.html'):
            email_msg.html_content = msg
        else:
            email_msg.text_content = msg

        mailer.send(email_msg)
    

    def reset_password_controller(self, request, user_requested=True, **kwargs):
        """A view to change your password.
        """
        if not is_valid(request):
            return redirect(url_for('auth.sign_in'))
        
        sign_in_redirect = self.settings.sign_in_redirect
        if callable(sign_in_redirect):
            sign_in_redirect = sign_in_redirect()
        
        kwargs['auth'] = self
        kwargs['user_requested'] = user_requested
        kwargs['sign_in_redirect'] = sign_in_redirect
        kwargs['ok'] = False
        kwargs['errors'] = []
        
        if request.is_post:
            data = request.form
            password = data.get('password', '')
            np1 = data.get('new_password_1', '')
            np2 = data.get('new_password_2', '')
            
            # Validate the new password
            if len(np1) < self.settings.password_minlen:
                kwargs['errors'].append('TOO SHORT')
            
            if (not np2) or (np1 != np2):
                kwargs['errors'].append('MISMATCH')
            
            # Validate the current password
            user = request.user
            if user_requested and not \
                    self.check_password(password, user.password):
                kwargs['errors'].append('FAIL')
            
            if not kwargs['errors']:
                user.password = self.hash_password(np1)
                self.db.commit()
                # Refresh the user hmac in the session
                self.sign_in(request, user)
                kwargs['ok'] = True
        
        view = self.settings.change_password_view
        return self.render(view, **kwargs)

