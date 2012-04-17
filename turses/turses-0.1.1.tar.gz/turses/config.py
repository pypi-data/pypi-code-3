# -*- coding: utf-8 -*-

"""
turses.config
~~~~~~~~~~~~~

This module contains the configuration logic.


There is one mayor configuration file in turses:

    `config`
        contains user preferences: colors, bindings, etc.

An one default token file:

    `token`
        contains authentication token for the default user account

Each user account (that is no the default one) has its .token file.
Keep this secret.

    `<alias>.token`
        contains the oauth tokens

The standard location is under $HOME directory, in a folder called `.turses`.
Here is an example with two accounts apart from the default one, aliased
to `alice` and `bob`.

    ~
    |+.turses/
    | |-config
    | |-token
    | |-alice.token
    | `-bob.token
    |+...
    |-...
    `
"""

from ConfigParser import RawConfigParser
from os import getenv, path, mkdir, remove
from gettext import gettext as _

from .utils import encode, wrap_exceptions
from .api.base import authorization

# -- Defaults -----------------------------------------------------------------

KEY_BINDINGS = {
    # motion
    'up':
         ('k', _('scroll up')),
    'down':                   
         ('j', _('scroll down')),
    'left':                   
        ('h', _('activate the timeline on the left')),
    'right':                  
        ('l', _('activate the timeline on the right')),
    'scroll_to_top':          
        ('g', _('scroll to top')),
    'scroll_to_bottom':       
        ('G', _('scroll to bottom')),

    # buffers
    'activate_first_buffer':  
       ('a', _('activate first buffer')),
    'activate_last_buffer':   
        ('e', _('activate last buffer')),
    'shift_buffer_beggining': 
        ('ctrl a', _('shift active buffer to the beginning')),
    'shift_buffer_end':       
        ('ctrl e', _('shift active buffer to the end')),
    'shift_buffer_left':      
        ('<', _('shift active buffer one position to the left')),
    'shift_buffer_right':     
        ('>', _('shift active buffer one position to the right')),
    'expand_visible_left':    
        ('p', _('expand visible timelines one column to the left')),
    'expand_visible_right':   
        ('n', _('expand visible timelines one column to the right')),
    'shrink_visible_left':    
        ('P', _('shrink visible timelines one column from the left')),
    'shrink_visible_right':   
        ('N', _('shrink visible timelines one column from the left')),
    'delete_buffer':          
        ('d', _('delete buffer')),
    'clear':                  
        ('c', _('clear status bar')),
    'mark_all_as_read':       
        ('A', _('mark all tweets in the current timeline as read')),

    # tweets
    'tweet':                  
        ('t', _('compose a tweet')),
    'delete_tweet':           
        ('X', _('delete focused status')),
    'reply':                  
        ('r', _('reply to focused status')),
    'retweet':                
        ('R', _('retweet focused status')),
    'retweet_and_edit':       
        ('E', _('open a editor for manually retweeting the focused status')),
    'send_dm':                 
        ('D', _('compose a direct message')),
    'update':                 
        ('u', _('refresh the active timeline')),
    'update_all':                 
        ('S', _('refresh all the timelines')),

    'tweet_hashtag':          
        ('H', _('compose a tweet with the same hashtags as the focused status')),
    'fav':                    
        ('b', _('mark focused tweet as favorite')),
    'delete_fav':             
        ('ctrl b', _('remove tweet from favorites')),
    'follow_selected':        
        ('f', _('follow selected status\' author')),
    'unfollow_selected':      
        ('U', _('unfollow selected status\' author')),

    # timelines
    'home':                   
        ('.', _('open a home timeline')),
    'own_tweets':             
        ('_', _('open a timeline with your tweets')),
    'favorites':              
        ('B', _('open a timeline with your favorites')),
    'mentions':               
        ('m', _('open a mentions timeline')),
    'DMs':                    
        ('M', _('open a direct message timeline')),
    'search':                 
        ('/', _('search for term and show resulting timeline')),
    'search_user':            
        ('@', _('open a timeline with the tweets of the specified user')),
    'user_timeline':          
        ('+', _('open a timeline with the tweets of the focused status\' author')),
    'thread':                 
        ('T', _('open the thread of the focused status')),
    'hashtags':               
        ('L', _('open a search timeline with the hashtags of the focused status')),

    # meta
    'help':                   
        ('?', _('show program help')),
    'reload_config':                   
        ('C', _('reload configuration')),

    # turses
    'quit':                   
        ('q', _('exit program')),
    'openurl':              
        ('o', _('open URLs of the focused status in a browser')),
    'redraw':                 
        ('ctrl l', _('redraw the screen')),
}

MOTION_KEY_BINDINGS = [
    'up',
    'down',                   
    'left',                   
    'right',                  
    'scroll_to_top',          
    'scroll_to_bottom',       
]

BUFFERS_KEY_BINDINGS = [
    'activate_first_buffer',  
    'activate_last_buffer',   
    'shift_buffer_beggining', 
    'shift_buffer_end',       
    'shift_buffer_left',      
    'shift_buffer_right',     
    'expand_visible_left',    
    'expand_visible_right',   
    'shrink_visible_left',    
    'shrink_visible_right',   
    'delete_buffer',          
    'clear',                  
    'mark_all_as_read',       
]

TWEETS_KEY_BINDINGS = [
    'tweet',                  
    'delete_tweet',           
    'reply',                  
    'retweet',                
    'retweet_and_edit',       
    'send_dm',                 
    'update',                 
    'update_all',
    'tweet_hashtag',          
    'fav',                    
    'delete_fav',             
    'follow_selected',        
    'unfollow_selected',      
]

TIMELINES_KEY_BINDINGS = [
    'home',                   
    'own_tweets',             
    'favorites',              
    'mentions',               
    'DMs',                    
    'search',                 
    'search_user',            
    'user_timeline',          
    'thread',                 
    'hashtags',               
]

META_KEY_BINDINGS = [
    'help',                   
    'reload_config',
]

TURSES_KEY_BINDINGS = [
    'quit',                   
    'openurl',              
    'redraw',                 
]

# TODO: not hard coded
# valid colors for `urwid`s palette
VALID_COLORS = [
    'default',
    'black',
    'dark red',
    'dark green',
    'brown',
    'dark blue',
    'dark magenta',
    'dark cyan',
    'light gray',
    'dark gray',
    'light red',
    'light green',
    'yellow',
    'light blue',
    'light magenta',
    'light cyan',
    'white',
]

def validate_color(colorstring):
    return colorstring if colorstring in VALID_COLORS else ''

PALETTE = [
    #Tabs
    ['active_tab',  'white', 'dark blue'],
    ['visible_tab', 'yellow', 'dark blue'],
    ['inactive_tab', 'dark blue', ''],

    # Statuses
    ['header', 'light blue', ''],
    ['body', 'white', ''],
    ['focus', 'light red', ''],
    ['line', 'black', ''],
    ['unread', 'dark red', ''],
    ['read', 'dark blue', ''],
    ['favorited', 'yellow', ''],

    # Text
    ['highlight', 'dark red', ''],
    ['highlight_nick', 'light red', ''],
    ['attag', 'brown', ''],
    ['hashtag', 'dark green', ''],

    # Messages
    ['error', 'white', 'dark red'],
    ['info', 'white', 'dark blue'],

    # Editor
    ['editor', 'white', 'dark blue'],
]

STYLES = {
    # TODO: make time string configurable 
    'header_template':      ' {username}{retweeted}{retweeter} - {time}{reply} {retweet_count} ',
    'dm_template':          ' {sender_screen_name} => {recipient_screen_name} - {time} ',
}

# Debug
LOGGING_LEVEL = 3

# Environment
HOME = getenv('HOME')
BROWSER = getenv('BROWSER')

# -- Configuration ------------------------------------------------------------

# Default config path
CONFIG_DIR = '.turses'
CONFIG_PATH = path.join(HOME, CONFIG_DIR)
DEFAULT_CONFIG_FILE = path.join(CONFIG_PATH, 'config')
DEFAULT_TOKEN_FILE = path.join(CONFIG_PATH, 'token')

LEGACY_CONFIG_DIR = '.config/turses'
LEGACY_CONFIG_PATH = path.join(HOME, LEGACY_CONFIG_DIR)
LEGACY_CONFIG_FILE = path.join(LEGACY_CONFIG_PATH, 'turses.cfg')
LEGACY_TOKEN_FILE = path.join(LEGACY_CONFIG_PATH, 'turses.tok')

# Names of the sections in the configuration
SECTION_KEY_BINDINGS = 'bindings'
SECTION_PALETTE = 'colors'
SECTION_STYLES = 'styles'
SECTION_DEBUG = 'debug'
SECTION_TOKEN = 'token'


def print_deprecation_notice():
    print "NOTE:"
    print
    print "The configuration file in %s has been deprecated." % LEGACY_CONFIG_FILE
    print "A new configuration directory is being generated in %s." % CONFIG_PATH
    print


class Configuration(object):
    """
    Generate and parse configuration files.

    Has backwards compatibility with the Tyrs legacy configuration.
    """

    def __init__(self, cli_args=None):
        """
        Create a `Configuration` taking into account the arguments
        from the command line interface (if any).
        """
        self.load_defaults()

        self.browser = BROWSER

        # create the config directory if it does not exist
        if not path.isdir(CONFIG_PATH):
            try:
                mkdir(CONFIG_PATH)
            except:
                print encode(_('Error creating config directory in %s' % CONFIG_DIR))
                exit(3)

        # generate config file and exit
        if cli_args and cli_args.generate_config:
            self.generate_config_file(config_file=cli_args.generate_config,)
            exit(0)

        if cli_args and cli_args.config:
            config_file = cli_args.config
        else:
            config_file = DEFAULT_CONFIG_FILE
        self.config_file = config_file

        if cli_args and cli_args.account:
            token_file = path.join(CONFIG_PATH, '%s.token' % cli_args.account)
        else:
            # loads the default `token' if no account was specified 
            token_file = DEFAULT_TOKEN_FILE
        self.token_file = token_file

    def load(self):
        """Loads configuration from files."""
        self._init_config()
        self._init_token()

    def load_defaults(self):
        """Load default values into configuration."""
        self.key_bindings = KEY_BINDINGS
        self.palette = PALETTE
        self.styles = STYLES
        self.logging_level = LOGGING_LEVEL

    def _init_config(self):
        if path.isfile(LEGACY_CONFIG_FILE):
            self._parse_legacy_config_file()
            print_deprecation_notice()
            remove(LEGACY_CONFIG_FILE)
            self.generate_config_file(self.config_file)
        elif path.isfile(self.config_file):
            self.parse_config_file(self.config_file)
        else:
            self.generate_config_file(self.config_file)

    def _init_token(self):
        if path.isfile(LEGACY_TOKEN_FILE):
            self.parse_token_file(LEGACY_TOKEN_FILE)
            remove(LEGACY_TOKEN_FILE)
            if hasattr(self, 'oauth_token') and \
               hasattr(self, 'oauth_token_secret'):
                   self.generate_token_file(self.token_file,
                                            self.oauth_token,
                                            self.oauth_token_secret)
        elif not path.isfile(self.token_file):
            self.authorize_new_account()
        else:
            self.parse_token_file(self.token_file)

    def _parse_legacy_config_file(self):
        """
        Parse a legacy configuration file.
        """
        conf = RawConfigParser()
        conf.read(LEGACY_CONFIG_FILE)

        styles = self.styles.copy()

        if conf.has_option('params', 'dm_template'):
            styles['dm_template'] = conf.get('params', 'dm_template')

        if conf.has_option('params', 'header_template'):
            styles['header_template'] = conf.get('params', 'header_template')

        self.styles.update(styles)

        if conf.has_option('params', 'logging_level'):
            self.logging_level  = conf.getint('params', 'logging_level')

        for binding in self.key_bindings:
            if conf.has_option('keys', binding):
                custom_key = conf.get('keys', binding) 
                self._set_key_binding(binding, custom_key)

        palette_labels = [color[0] for color in PALETTE]
        for label in palette_labels:
            if conf.has_option('colors', label):
                custom_fg  = conf.get('colors', label) 
                self._set_color(label, custom_fg)

    def _parse_legacy_token_file(self):
        conf = RawConfigParser()
        conf.read(LEGACY_TOKEN_FILE)

        if conf.has_option(SECTION_TOKEN, 'oauth_token'):
            self.oauth_token = conf.get(SECTION_TOKEN, 'oauth_token')

        if conf.has_option(SECTION_TOKEN, 'oauth_token'):
            self.oauth_token_secret = conf.get(SECTION_TOKEN, 'oauth_token_secret')

    def _set_color(self, color_label, custom_fg=None, custom_bg=None):
        for color in self.palette:
            label, fg, bg = color[0], color[1], color[2]
            if label == color_label:
                color[1] = custom_fg if validate_color(custom_fg) is not None else fg
                color[2] = custom_bg if validate_color(custom_bg) is not None else bg

    def _set_key_binding(self, binding, new_key):
        if not self.key_bindings.has_key(binding):
            return

        key, description = self.key_bindings[binding]
        new_key_binding = new_key, description
        self.key_bindings[binding] = new_key_binding

    def generate_config_file(self, config_file):
        self._generate_config_file(config_file=config_file,
                                   on_error=self._config_generation_error,
                                   on_success=self._config_generation_success)

    @wrap_exceptions
    def _generate_config_file(self, config_file):
        conf = RawConfigParser()

        self.config_file = config_file

        # Key bindings
        conf.add_section(SECTION_KEY_BINDINGS)
        binding_lists = [MOTION_KEY_BINDINGS,
                         BUFFERS_KEY_BINDINGS,
                         TWEETS_KEY_BINDINGS,
                         TIMELINES_KEY_BINDINGS,
                         META_KEY_BINDINGS,
                         TURSES_KEY_BINDINGS,]
        for binding_list in binding_lists:
            for binding in binding_list:
                key = self.key_bindings[binding][0]
                conf.set(SECTION_KEY_BINDINGS, binding, key)
        

        # Color
        conf.add_section(SECTION_PALETTE)
        for label in self.palette:
            label_name, fg, bg = label[0], label[1], label[2]
            conf.set(SECTION_PALETTE, label_name, fg)
            conf.set(SECTION_PALETTE, label_name + '_bg', bg)

        # Styles
        conf.add_section(SECTION_STYLES)
        for style in self.styles:
            conf.set(SECTION_STYLES, style, self.styles[style])

        # Debug
        conf.add_section(SECTION_DEBUG)
        conf.set(SECTION_DEBUG, 'logging_level', LOGGING_LEVEL)

        with open(config_file, 'wb') as config:
            conf.write(config)

    def _config_generation_error(self):
        print encode(_('Unable to generate configuration file in %s')) % self.config_file
        exit(2)

    def _config_generation_success(self):
        print encode(_('Generated configuration file in %s')) % self.config_file

    def generate_token_file(self, 
                            token_file,
                            oauth_token,
                            oauth_token_secret):
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret

        conf = RawConfigParser()
        conf.add_section(SECTION_TOKEN)
        conf.set(SECTION_TOKEN, 'oauth_token', oauth_token)
        conf.set(SECTION_TOKEN, 'oauth_token_secret', oauth_token_secret)

        with open(token_file, 'wb') as tokens:
            conf.write(tokens)

        print encode(_('your account has been saved'))

    def parse_config_file(self, config_file):
        self._conf = RawConfigParser()
        self._conf.read(config_file)

        self._parse_key_bindings()
        self._parse_palette()
        self._parse_styles()
        self._parse_debug()

    def _parse_key_bindings(self):
        for binding in self.key_bindings:
            if self._conf.has_option(SECTION_KEY_BINDINGS, binding):
                custom_key = self._conf.get(SECTION_KEY_BINDINGS, binding) 
                self._set_key_binding(binding, custom_key)

    def _parse_palette(self):
        # Color
        for label in self.palette:
            label_name, fg, bg = label[0], label[1], label[2]
            if self._conf.has_option(SECTION_PALETTE, label_name):
                fg = self._conf.get(SECTION_PALETTE, label_name)
            if self._conf.has_option(SECTION_PALETTE, label_name + '_bg'):
                bg = self._conf.get(SECTION_PALETTE, label_name + '_bg')
            self._set_color(label_name, fg, bg)

    def _parse_styles(self):
        for style in self.styles:
            if self._conf.has_option(SECTION_STYLES, style):
                self.styles[style] = self._conf.get(SECTION_STYLES, style)

    def _parse_debug(self):
        if self._conf.has_option(SECTION_DEBUG, 'logging_level'):
            self.logging_level = self._conf.get(SECTION_DEBUG, 'logging_level')

    def parse_token_file(self, token_file):
        self._conf = RawConfigParser()
        self._conf.read(token_file)

        if self._conf.has_option(SECTION_TOKEN, 'oauth_token'):
            self.oauth_token = self._conf.get(SECTION_TOKEN, 'oauth_token')
        if self._conf.has_option(SECTION_TOKEN, 'oauth_token_secret'):
            self.oauth_token_secret = self._conf.get(SECTION_TOKEN, 'oauth_token_secret')

    def authorize_new_account(self):
        access_token = authorization()
        if access_token:
            self.oauth_token = access_token['oauth_token']
            self.generate_token_file(self.token_file,
                                   access_token['oauth_token'],
                                   access_token['oauth_token_secret'])
        else:
            # TODO: exit codes
            exit(2)

    def reload(self):
        self.parse_config_file(self.config_file)
