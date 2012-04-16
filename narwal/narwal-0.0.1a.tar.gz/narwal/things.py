from .const import COMMENTS_PATH_PATTERN, MAX_REPRSTR
from .util import limstr, kind, relative_url
from .exceptions import NoMoreError


def identify_class(dict_):
    if 'kind' in dict_:
        k = kind(dict_['kind']).capitalize()
        return globals()[k]
    else:
        return Blob


class Blob(object):
    """A dumb container because ``obj.x`` is cooler then ``obj['x']``.
    
    :param reddit: a reddit session
    :type reddit: :class:`Reddit`
    """
    def __init__(self, reddit):
        self._reddit = reddit


class ListBlob(Blob):
    """A :class:`Blob` that almost looks and feels like a :class:`list`, but isn't.
    
    :param reddit: a reddit session
    :type reddit: :class:`Reddit`
    :param items: initial list to absorb
    """
    def __init__(self, reddit, items=[]):
        super(ListBlob, self).__init__(reddit)
        self._items = items
    
    def __iter__(self, *args, **kwargs):
        return self._items.__iter__(*args, **kwargs)
    
    def __getitem__(self, *args, **kwargs):
        return self._items.__getitem__(*args, **kwargs)
    
    def __setitem__(self, *args, **kwargs):
        return self._items.__setitem__(*args, **kwargs)
    
    def __delitem__(self, *args, **kwargs):
        return self._items.__delitem__(*args, **kwargs)
    
    def __len__(self, *args, **kwargs):
        return self._items.__len__(*args, **kwargs)
    
    def __reversed__(self, *args, **kwargs):
        return self._items.__reversed__(*args, **kwargs)
    
    def __contains__(self, *args, **kwargs):
        return self._items.__contains__(*args, **kwargs)
    
    #def __repr__(self, *args, **kwargs):
    #    return self._items.__repr__(*args, **kwargs)


class Thing(Blob):
    """A reddit `Thing`.  See https://github.com/reddit/reddit/wiki/thing for more details.  You will only be seeing instances of subclasses of this.
    
    `kind` is omitted because it will be implied by :class:`Thing`'s subclasses.
    `data` is omitted because data will be stored as attributes.
    """
    def __init__(self, *args, **kwargs):
        #: id, e.g. "c3v7f8u"
        self.id = None
        
        #: full name of the thing, e.g. "t1_c3v7f8u"
        self.name = None
        
        super(Thing, self).__init__(*args, **kwargs)
    
    def __repr__(self):
        return '<{0} [{1}]>'.format(self.__class__.__name__,
                                    limstr(self.__str__(), MAX_REPRSTR))
    
    def __str__(self):
        return self.__unicode__().encode('utf-8', 'replace')
    
    def __unicode__(self):
        return self.name 


class Created(Thing):
    """An implementation.  See https://github.com/reddit/reddit/wiki/thing for more details.
    """
    def __init__(self, *args, **kwargs):
        #: the localized time of creation in seconds
        self.created = None
        
        #: the UTC time this item was created in seconds
        self.created_utc = None
        
        super(Created, self).__init__(*args, **kwargs)


class Votable(Thing):
    """An implementation.  See https://github.com/reddit/reddit/wiki/thing for more details.
    """
    def __init__(self, *args, **kwargs):
        #: number of upvotes
        self.ups = None
        
        #: number of downvotes
        self.downs = None
        
        #: True if liked by the logged in user.
        self.likes = None
        
        super(Votable, self).__init__(*args, **kwargs)
    
    def vote(self, dir_):
        """POST a vote on the thing.
        
        :param dir\_: direction (up: 1, down: -1, no vote: 0)
        """
        return self._reddit.vote(self.name, dir_)
    
    def upvote(self):
        """Upvote the thing (POST)."""
        return self.vote(1)
    
    def downvote(self):
        """Downvote the thing (POST)."""
        return self.vote(-1)
    
    def unvote(self):
        """Unvote the thing (POST)."""
        return self.vote(0)


class Commentable(Thing):
    """Base class for :class:`Thing`s that are commentable (i.e. :class:`Link` and :class:`Comment`)
    """
    def comment(self, text):
        """POST a comment to this thing.
        
        :param text: comment's body text
        """
        return self._reddit.comment(self.name, text)


class Listing(ListBlob):
    """A reddit :class:`Listing`.  See https://github.com/reddit/reddit/wiki/thing for more details.
    
    `data` is omitted because data will be stored as attributes.
    """
    def __init__(self, *args, **kwargs):
        self._limit = None
        
        #: fullname of the listing that follows before this page
        self.before = None
        
        #: fullname of the listing that follows after this page
        self.after = None
        
        #: modhash supplied again.  pretty useless, since you can always use the old one
        self.modhash = None
        
        super(Listing, self).__init__(*args, **kwargs)
    
    @property
    def children(self):
        """Property that aliases `self.children` to `self._items`.  This is done so that :class:`ListBlob` special methods work automagically."""
        return self._items
    
    @children.setter
    def children(self, value):
        self._items = value
    
    @children.deleter
    def children(self):
        del self._items
    
    @property
    def _has_literally_more(self):
        return len(self) > 0 and isinstance(self[-1], More)
    
    @property
    def has_more(self):
        """Returns True if there are more things that can be retrieved."""
        return bool(self.after or self._has_literally_more())
    
    def more(self, limit=None):
        """A convenience function.  Calls `self.next_listing`."""
        return self.next_listing(limit=limit)
        
    def next_listing(self, limit=None):
        """GETs next :class:`Listing` directed to by this :class:`Listing`.  Returns :class:`Listing` object.
        
        :param limit: max number of entries to get
        """
        if self.after:
            return self._reddit._limit_get(self._path, params={'after': self.after}, limit=limit or self._limit)
        elif self._has_literally_more():
            start, link_id, link_title = COMMENTS_PATH_PATTERN.match(self._path)
            more_id = self[-1].id
            return self._reddit._limit_get(start, link_id, link_title, more_id, limit=limit or self._limit)
        else:
            raise NoMoreError('no more items')
    
    def prev_listing(self, limit=None):
        """GETs previous :class:`Listing` directed to by this :class:`Listing`.  Returns :class:`Listing` object.
        
        :param limit: max number of entries to get
        """
        if self.before:
            return self._reddit._limit_get(self._path, eparams={'before': self.before}, limit=limit or self._limit)
        else:
            raise NoMoreError('no previous items')


class Userlist(ListBlob):
    pass


class Comment(Votable, Created, Commentable):
    """A reddit :class:`Comment`. See https://github.com/reddit/reddit/wiki/thing for more details.
    
    
    """  
    def __init__(self, *args, **kwargs):
        self.author = None
        self.author_flair_css_class = None
        self.author_flair_text = None
        self.body = None
        self.body_html = None
        self.link_id = None
        self.parent_id = None
        self.subreddit = None
        self.subreddit_id = None
        super(Comment, self).__init__(*args, **kwargs)
    
    def __unicode__(self):
        score = None
        if self.ups is not None and self.downs is not None:
            score = self.ups - self.downs
        return u'({}) {}: {}'.format(score,
                                     self.author,
                                     self.body.replace('\n', ' '))
    
    def _permalink(self, relative=False):
        args = ('comments', self.link_id[3:], '_', self.id)
        if self.subreddit:
            args = ('r', self.subreddit) + args
        r = '/'.join(args)
        if relative:
            return '/{}'.format(r) 
        else:
            return relative_url(r)
    
    def reply(self, text):
        return self.comment(text)
    
    @property
    def permalink(self):
        return self._permalink()
    
    def comments(self, limit=None):
        return self._reddit._limit_get(self._permalink(relative=True), limit=limit)[1]
    
    def delete(self):
        return self._reddit.delete(self.name)
    
    def remove(self):
        return self._reddit.remove(self.name)


class Link(Votable, Created, Commentable):
    def __init__(self, *args, **kwargs):
        self.author = None
        self.author_flair_css_class = None
        self.author_flair_text = None
        self.clicked = None
        self.domain = None
        self.hidden = None
        self.is_self = None
        self.media = None
        self.media_embed = None
        self.num_comments = None
        self.over_18 = None
        self.permalink = None
        self.saved = None
        self.score = None
        self.selftext = None
        self.selftext_html = None
        self.subreddit = None
        self.subreddit_id = None
        self.thumbnail = None
        self.title = None
        self.url = None
        super(Link, self).__init__(*args, **kwargs)
    
    def __unicode__(self):
        return u'({}) {}'.format(self.score, self.title)
    
    def comments(self, limit=None):
        return self._reddit._limit_get(self.permalink, limit=limit)[1]
    
    def save(self):
        return self._reddit.save(self.name)
    
    def unsave(self):
        return self._reddit.unsave(self.name)
    
    def hide(self):
        return self._reddit.hide(self.name)
    
    def unhide(self):
        return self._reddit.unhide(self.name)
    
    def marknsfw(self):
        return self._reddit.marknsfw(self.name)
    
    def unmarknsfw(self):
        return self._reddit.unmarknsfw(self.name)
    
    def approve(self):
        return self._reddit.approve(self.name)
    
    def remove(self):
        return self._reddit.remove(self.name)
    
    def delete(self):
        return self._reddit.delete(self.name)


class Subreddit(Thing):
    def __init__(self, *args, **kwargs):
        self.description = None
        self.display_name = None
        self.over18 = None
        self.subscribers = None
        self.title = None
        self.url = None
        super(Subreddit, self).__init__(*args, **kwargs)
    
    def __unicode__(self):
        return u'r/{}'.format(self.display_name)
    
    def hot(self, limit=None):
        return self._reddit.hot(self.display_name, limit=limit)
    
    def new(self, limit=None):
        return self._reddit.new(self.display_name, limit=limit)
    
    def top(self, limit=None):
        return self._reddit.top(self.display_name, limit=limit)
    
    def controversial(self, limit=None):
        return self._reddit.controversial(self.display_name, limit=limit)
    
    def comments(self, limit=None):
        return self._reddit.comments(self.display_name, limit=limit)
    
    def subscribe(self):
        return self._reddit.subscribe(self.name)
    
    def unsubscribe(self):
        return self._reddit.unsubscribe(self.name)
    
    def submit_link(self, title, url):
        return self._reddit.submit_link(self.display_name, title, url)
    
    def submit_text(self, title, text):
        return self._reddit.submit_text(self.display_name, title, text)
    
    def moderators(self):
        return self._reddit.moderators(self.display_name)
    
    def contributors(self):
        return self._reddit.contributors(self.display_name)


class Message(Created):
    def __init__(self, *args, **kwargs):
        self.author = None
        self.body = None
        self.body_html = None
        self.context = None
        self.dest = None  # destination
        self.first_message = None
        self.name = None
        self.new = None
        self.parent_id = None
        self.replies = None
        self.subject = None
        self.subreddit = None
        self.was_comment = None
        super(Message, self).__init__(*args, **kwargs)
    
    def __unicode__(self):
        return u'{}: {}'.format(self.author,
                                self.body.replace('\n', ' ')) 
    
    def read(self):
        return self._reddit.read_message(self.name)
    
    def unread(self):
        return self._reddit.unread_message(self.name)
    
    def hide(self):
        return self._reddit.hide_message(self.name)
    
    def unhide(self):
        return self._reddit.unhide_message(self.name)
    
    def reply(self, text):
        data = {
            'thing_id': self.name,
            'id': '#commentreply_{}'.format(self.name),
            'text': text,
        }
        return self._reddit.post('api', 'comment', data=data)
    
    def report(self):
        return self._reddit.report(self.name)


class Account(Thing):
    def __init__(self, *args, **kwargs):
        self.comment_karma = None
        self.created = None
        self.created_utc = None
        self.has_mail = None
        self.has_mod_mail = None
        self.id = None
        self.is_gold = None
        self.is_mod = None
        self.link_karma = None
        self.modhash = None
        self.name = None
        super(Account, self).__init__(*args, **kwargs)
    
    def __unicode__(self):
        return unicode(self.name)
    
    def overview(self):
        return self._reddit.get('user', self.name, 'overview')
    
    def comments(self, limit=None):
        return self._reddit._limit_get('user', self.name, 'comments', limit=limit)
    
    def submitted(self, limit=None):
        return self._reddit._limit_get('user', self.name, 'submitted', limit=limit)
    
    def liked(self, limit=None):
        return self._reddit._limit_get('user', self.name, 'liked', limit=limit)
    
    def disliked(self, limit=None):
        return self._reddit._limit_get('user', self.name, 'disliked', limit=limit)
    
    def hidden(self, limit=None):
        return self._reddit._limit_get('user', self.name, 'hidden', limit=limit)
    
    def about(self):
        return self._reddit.get('user', self.name, 'about')


class More(Thing):
    def __init__(self, *args, **kwargs):
        self.children = None
        super(More, self).__init__(*args, **kwargs)