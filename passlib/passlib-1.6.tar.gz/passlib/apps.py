"""passlib.apps"""
#=========================================================
#imports
#=========================================================
#core
import logging; log = logging.getLogger(__name__)
from itertools import chain
#site
#libs
from passlib import hash
from passlib.context import LazyCryptContext
from passlib.utils import sys_bits
#pkg
#local
__all__ = [
    'custom_app_context',
    'django_context',
    'ldap_context', 'ldap_nocrypt_context',
    'mysql_context', 'mysql4_context', 'mysql3_context',
    'phpass_context',
    'phpbb3_context',
    'postgres_context',
]

#=========================================================
# master containing all identifiable hashes
#=========================================================
def _load_master_config():
    from passlib.registry import list_crypt_handlers

    # get master list
    schemes = list_crypt_handlers()

    # exclude the ones we know have ambiguous or greedy identify() methods.
    excluded = [
        # frequently confused for eachother
        'bigcrypt',
        'crypt16',

        # no good identifiers
        'cisco_pix',
        'cisco_type7',
        'htdigest',
        'mysql323',
        'oracle10',

        # all have same size
        'lmhash',
        'msdcc',
        'msdcc2',
        'nthash',

        # plaintext handlers
        'plaintext',
        'ldap_plaintext',

        # disabled handlers
        'django_disabled',
        'unix_disabled',
        'unix_fallback',
    ]
    for name in excluded:
        schemes.remove(name)

    # return config
    return dict(schemes=schemes, default="sha256_crypt")
master_context = LazyCryptContext(onload=_load_master_config)

#=========================================================
#for quickly bootstrapping new custom applications
#=========================================================
custom_app_context = LazyCryptContext(
    #choose some reasonbly strong schemes
    schemes=["sha512_crypt", "sha256_crypt"],

    #set some useful global options
    default="sha256_crypt" if sys_bits < 64 else "sha512_crypt",
    all__vary_rounds = 0.1,

    #set a good starting point for rounds selection
    sha512_crypt__min_rounds = 60000,
    sha256_crypt__min_rounds = 80000,

    #if the admin user category is selected, make a much stronger hash,
    admin__sha512_crypt__min_rounds = 120000,
    admin__sha256_crypt__min_rounds = 160000,
    )

#=========================================================
#django
#=========================================================
_django10_schemes = [
        "django_salted_sha1", "django_salted_md5", "django_des_crypt",
        "hex_md5", "django_disabled",
]

django10_context = LazyCryptContext(
    schemes=_django10_schemes,
    default="django_salted_sha1",
    deprecated=["hex_md5"],
)

django14_context = LazyCryptContext(
    schemes=["django_pbkdf2_sha256", "django_pbkdf2_sha1", "django_bcrypt"] \
            + _django10_schemes,
    deprecated=_django10_schemes,
)

# this will always point to latest version
django_context = django14_context

#=========================================================
#ldap
#=========================================================
std_ldap_schemes = ["ldap_salted_sha1", "ldap_salted_md5",
                      "ldap_sha1", "ldap_md5",
                      "ldap_plaintext" ]

#create context with all std ldap schemes EXCEPT crypt
ldap_nocrypt_context = LazyCryptContext(std_ldap_schemes)

#create context with all possible std ldap + ldap crypt schemes
def _iter_ldap_crypt_schemes():
    from passlib.utils import unix_crypt_schemes
    return ('ldap_' + name for name in unix_crypt_schemes)

def _iter_ldap_schemes():
    "helper which iterates over supported std ldap schemes"
    return chain(std_ldap_schemes, _iter_ldap_crypt_schemes())
ldap_context = LazyCryptContext(_iter_ldap_schemes())

###create context with all std ldap schemes + crypt schemes for localhost
##def _iter_host_ldap_schemes():
##    "helper which iterates over supported std ldap schemes"
##    from passlib.handlers.ldap_digests import get_host_ldap_crypt_schemes
##    return chain(std_ldap_schemes, get_host_ldap_crypt_schemes())
##ldap_host_context = LazyCryptContext(_iter_host_ldap_schemes())

#=========================================================
#mysql
#=========================================================
mysql3_context = LazyCryptContext(["mysql323"])
mysql4_context = LazyCryptContext(["mysql41", "mysql323"], deprecated="mysql323")
mysql_context = mysql4_context #tracks latest mysql version supported

#=========================================================
#postgres
#=========================================================
postgres_context = LazyCryptContext(["postgres_md5"])

#=========================================================
#phpass & variants
#=========================================================
def _create_phpass_policy(**kwds):
    "helper to choose default alg based on bcrypt availability"
    kwds['default'] = 'bcrypt' if hash.bcrypt.has_backend() else 'phpass'
    return kwds

phpass_context = LazyCryptContext(
    schemes=["bcrypt", "phpass", "bsdi_crypt"],
    onload=_create_phpass_policy,
    )

phpbb3_context = LazyCryptContext(["phpass"], phpass__ident="H")

#TODO: support the drupal phpass variants (see phpass homepage)

#=========================================================
#roundup
#=========================================================

_std_roundup_schemes = [ "ldap_hex_sha1", "ldap_hex_md5", "ldap_des_crypt", "roundup_plaintext" ]
roundup10_context = LazyCryptContext(_std_roundup_schemes)

#NOTE: 'roundup15' really applies to roundup 1.4.17+
roundup_context = roundup15_context = LazyCryptContext(
    schemes=_std_roundup_schemes + [ "ldap_pbkdf2_sha1" ],
    deprecated=_std_roundup_schemes,
    default = "ldap_pbkdf2_sha1",
    ldap_pbkdf2_sha1__default_rounds = 10000,
    )

#=========================================================
# eof
#=========================================================
