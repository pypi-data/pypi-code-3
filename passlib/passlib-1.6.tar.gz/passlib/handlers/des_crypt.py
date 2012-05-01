"""passlib.handlers.des_crypt - traditional unix (DES) crypt and variants"""
#=========================================================
#imports
#=========================================================
#core
import re
import logging; log = logging.getLogger(__name__)
from warnings import warn
#site
#libs
from passlib.utils import classproperty, h64, h64big, safe_crypt, test_crypt, to_unicode
from passlib.utils.compat import b, bytes, byte_elem_value, u, uascii_to_str, unicode
from passlib.utils.des import des_encrypt_int_block
import passlib.utils.handlers as uh
#pkg
#local
__all__ = [
    "des_crypt",
    "bsdi_crypt",
    "bigcrypt",
    "crypt16",
]

#=========================================================
# pure-python backend for des_crypt family
#=========================================================
_BNULL = b('\x00')

def _crypt_secret_to_key(secret):
    """convert secret to 64-bit DES key.

    this only uses the first 8 bytes of the secret,
    and discards the high 8th bit of each byte at that.
    a null parity bit is inserted after every 7th bit of the output.
    """
    # NOTE: this would set the parity bits correctly,
    # but des_encrypt_int_block() would just ignore them...
    ##return sum(expand_7bit(byte_elem_value(c) & 0x7f) << (56-i*8)
    ##           for i, c in enumerate(secret[:8]))
    return sum((byte_elem_value(c) & 0x7f) << (57-i*8)
               for i, c in enumerate(secret[:8]))

def _raw_des_crypt(secret, salt):
    "pure-python backed for des_crypt"
    assert len(salt) == 2

    # NOTE: some OSes will accept non-HASH64 characters in the salt,
    # but what value they assign these characters varies wildy,
    # so just rejecting them outright.
    # NOTE: the same goes for single-character salts...
    # some OSes duplicate the char, some insert a '.' char,
    # and openbsd does something which creates an invalid hash.
    try:
        salt_value = h64.decode_int12(salt)
    except ValueError: #pragma: no cover - always caught by class
        raise ValueError("invalid chars in salt")

    # gotta do something - no official policy since this predates unicode
    if isinstance(secret, unicode):
        secret = secret.encode("utf-8")
    assert isinstance(secret, bytes)

    # forbidding NULL char because underlying crypt() rejects them too.
    if _BNULL in secret:
        raise uh.exc.NullPasswordError(des_crypt)

    # convert first 8 bytes of secret string into an integer
    key_value = _crypt_secret_to_key(secret)

    # run data through des using input of 0
    result = des_encrypt_int_block(key_value, 0, salt_value, 25)

    # run h64 encode on result
    return h64big.encode_int64(result)

def _bsdi_secret_to_key(secret):
    "covert secret to DES key used by bsdi_crypt"
    key_value = _crypt_secret_to_key(secret)
    idx = 8
    end = len(secret)
    while idx < end:
        next = idx+8
        tmp_value = _crypt_secret_to_key(secret[idx:next])
        key_value = des_encrypt_int_block(key_value, key_value) ^ tmp_value
        idx = next
    return key_value

def _raw_bsdi_crypt(secret, rounds, salt):
    "pure-python backend for bsdi_crypt"

    # decode salt
    try:
        salt_value = h64.decode_int24(salt)
    except ValueError: #pragma: no cover - always caught by class
        raise ValueError("invalid salt")

    # gotta do something - no official policy since this predates unicode
    if isinstance(secret, unicode):
        secret = secret.encode("utf-8")
    assert isinstance(secret, bytes)

    # forbidding NULL char because underlying crypt() rejects them too.
    if _BNULL in secret:
        raise uh.exc.NullPasswordError(bsdi_crypt)

    # convert secret string into an integer
    key_value = _bsdi_secret_to_key(secret)

    # run data through des using input of 0
    result = des_encrypt_int_block(key_value, 0, salt_value, rounds)

    # run h64 encode on result
    return h64big.encode_int64(result)

#=========================================================
# handlers
#=========================================================
class des_crypt(uh.HasManyBackends, uh.HasSalt, uh.GenericHandler):
    """This class implements the des-crypt password hash, and follows the :ref:`password-hash-api`.

    It supports a fixed-length salt.

    The :meth:`~passlib.ifc.PasswordHash.encrypt` and :meth:`~passlib.ifc.PasswordHash.genconfig` methods accept the following optional keywords:

    :type salt: str
    :param salt:
        Optional salt string.
        If not specified, one will be autogenerated (this is recommended).
        If specified, it must be 2 characters, drawn from the regexp range ``[./0-9A-Za-z]``.
    """
    #=========================================================
    # class attrs
    #=========================================================
    #--GenericHandler--
    name = "des_crypt"
    setting_kwds = ("salt",)
    checksum_chars = uh.HASH64_CHARS
    checksum_size = 11

    #--HasSalt--
    min_salt_size = max_salt_size = 2
    salt_chars = uh.HASH64_CHARS

    #=========================================================
    # formatting
    #=========================================================
    #FORMAT: 2 chars of H64-encoded salt + 11 chars of H64-encoded checksum

    _hash_regex = re.compile(u(r"""
        ^
        (?P<salt>[./a-z0-9]{2})
        (?P<chk>[./a-z0-9]{11})?
        $"""), re.X|re.I)

    @classmethod
    def from_string(cls, hash):
        hash = to_unicode(hash, "ascii", "hash")
        salt, chk = hash[:2], hash[2:]
        return cls(salt=salt, checksum=chk or None)

    def to_string(self):
        hash = u("%s%s") % (self.salt, self.checksum or u(''))
        return uascii_to_str(hash)

    #=========================================================
    # backend
    #=========================================================
    backends = ("os_crypt", "builtin")

    _has_backend_builtin = True

    @classproperty
    def _has_backend_os_crypt(cls):
        return test_crypt("test", 'abgOeLfPimXQo')

    def _calc_checksum_builtin(self, secret):
        return _raw_des_crypt(secret, self.salt.encode("ascii")).decode("ascii")

    def _calc_checksum_os_crypt(self, secret):
        # NOTE: safe_crypt encodes unicode secret -> utf8
        # no official policy since des-crypt predates unicode
        hash = safe_crypt(secret, self.salt)
        if hash:
            assert hash.startswith(self.salt) and len(hash) == 13
            return hash[2:]
        else:
            return self._calc_checksum_builtin(secret)

    #=========================================================
    # eoc
    #=========================================================

class bsdi_crypt(uh.HasManyBackends, uh.HasRounds, uh.HasSalt, uh.GenericHandler):
    """This class implements the BSDi-Crypt password hash, and follows the :ref:`password-hash-api`.

    It supports a fixed-length salt, and a variable number of rounds.

    The :meth:`~passlib.ifc.PasswordHash.encrypt` and :meth:`~passlib.ifc.PasswordHash.genconfig` methods accept the following optional keywords:

    :type salt: str
    :param salt:
        Optional salt string.
        If not specified, one will be autogenerated (this is recommended).
        If specified, it must be 4 characters, drawn from the regexp range ``[./0-9A-Za-z]``.

    :type rounds: int
    :param rounds:
        Optional number of rounds to use.
        Defaults to 5001, must be between 1 and 16777215, inclusive.

    .. versionchanged:: 1.6
        :meth:`encrypt` will now issue a warning if an even number of rounds is used
        (see :ref:`bsdi-crypt-security-issues` regarding weak DES keys).
    """
    #=========================================================
    # class attrs
    #=========================================================
    #--GenericHandler--
    name = "bsdi_crypt"
    setting_kwds = ("salt", "rounds")
    checksum_size = 11
    checksum_chars = uh.HASH64_CHARS

    #--HasSalt--
    min_salt_size = max_salt_size = 4
    salt_chars = uh.HASH64_CHARS

    #--HasRounds--
    default_rounds = 5001
    min_rounds = 1
    max_rounds = 16777215 # (1<<24)-1
    rounds_cost = "linear"

    # NOTE: OpenBSD login.conf reports 7250 as minimum allowed rounds,
    # but that seems to be an OS policy, not a algorithm limitation.

    #=========================================================
    # parsing
    #=========================================================
    _hash_regex = re.compile(u(r"""
        ^
        _
        (?P<rounds>[./a-z0-9]{4})
        (?P<salt>[./a-z0-9]{4})
        (?P<chk>[./a-z0-9]{11})?
        $"""), re.X|re.I)

    @classmethod
    def from_string(cls, hash):
        hash = to_unicode(hash, "ascii", "hash")
        m = cls._hash_regex.match(hash)
        if not m:
            raise uh.exc.InvalidHashError(cls)
        rounds, salt, chk = m.group("rounds", "salt", "chk")
        return cls(
            rounds=h64.decode_int24(rounds.encode("ascii")),
            salt=salt,
            checksum=chk,
        )

    def to_string(self):
        hash = u("_%s%s%s") % (h64.encode_int24(self.rounds).decode("ascii"),
                             self.salt, self.checksum or u(''))
        return uascii_to_str(hash)

    #=========================================================
    # validation
    #=========================================================

    # flag so CryptContext won't generate even rounds.
    _avoid_even_rounds = True

    def _norm_rounds(self, rounds):
        rounds = super(bsdi_crypt, self)._norm_rounds(rounds)
        # issue warning if app provided an even rounds value
        if self.use_defaults and not rounds & 1:
            warn("bsdi_crypt rounds should be odd, "
                 "as even rounds may reveal weak DES keys",
                 uh.exc.PasslibSecurityWarning)
        return rounds

    @classmethod
    def _bind_needs_update(cls, **settings):
        return cls._needs_update

    @classmethod
    def _needs_update(cls, hash, secret):
        # mark bsdi_crypt hashes as deprecated if they have even rounds.
        assert cls.identify(hash)
        if isinstance(hash, unicode):
            hash = hash.encode("ascii")
        rounds = h64.decode_int24(hash[1:5])
        return not rounds & 1

    #=========================================================
    # backends
    #=========================================================
    backends = ("os_crypt", "builtin")

    _has_backend_builtin = True

    @classproperty
    def _has_backend_os_crypt(cls):
        return test_crypt("test", '_/...lLDAxARksGCHin.')

    def _calc_checksum_builtin(self, secret):
        return _raw_bsdi_crypt(secret, self.rounds, self.salt.encode("ascii")).decode("ascii")

    def _calc_checksum_os_crypt(self, secret):
        config = self.to_string()
        hash = safe_crypt(secret, config)
        if hash:
            assert hash.startswith(config[:9]) and len(hash) == 20
            return hash[-11:]
        else:
            return self._calc_checksum_builtin(secret)

    #=========================================================
    # eoc
    #=========================================================

class bigcrypt(uh.HasSalt, uh.GenericHandler):
    """This class implements the BigCrypt password hash, and follows the :ref:`password-hash-api`.

    It supports a fixed-length salt.

    The :meth:`~passlib.ifc.PasswordHash.encrypt` and :meth:`~passlib.ifc.PasswordHash.genconfig` methods accept the following optional keywords:

    :type salt: str
    :param salt:
        Optional salt string.
        If not specified, one will be autogenerated (this is recommended).
        If specified, it must be 22 characters, drawn from the regexp range ``[./0-9A-Za-z]``.
    """
    #=========================================================
    # class attrs
    #=========================================================
    #--GenericHandler--
    name = "bigcrypt"
    setting_kwds = ("salt",)
    checksum_chars = uh.HASH64_CHARS
    #NOTE: checksum chars must be multiple of 11

    #--HasSalt--
    min_salt_size = max_salt_size = 2
    salt_chars = uh.HASH64_CHARS

    #=========================================================
    # internal helpers
    #=========================================================
    _hash_regex = re.compile(u(r"""
        ^
        (?P<salt>[./a-z0-9]{2})
        (?P<chk>([./a-z0-9]{11})+)?
        $"""), re.X|re.I)

    @classmethod
    def from_string(cls, hash):
        hash = to_unicode(hash, "ascii", "hash")
        m = cls._hash_regex.match(hash)
        if not m:
            raise uh.exc.InvalidHashError(cls)
        salt, chk = m.group("salt", "chk")
        return cls(salt=salt, checksum=chk)

    def to_string(self):
        hash = u("%s%s") % (self.salt, self.checksum or u(''))
        return uascii_to_str(hash)

    def _norm_checksum(self, value):
        value = super(bigcrypt, self)._norm_checksum(value)
        if value and len(value) % 11:
            raise uh.exc.InvalidHashError(self)
        return value

    #=========================================================
    # backend
    #=========================================================
    def _calc_checksum(self, secret):
        if isinstance(secret, unicode):
            secret = secret.encode("utf-8")
        chk = _raw_des_crypt(secret, self.salt.encode("ascii"))
        idx = 8
        end = len(secret)
        while idx < end:
            next = idx + 8
            chk += _raw_des_crypt(secret[idx:next], chk[-11:-9])
            idx = next
        return chk.decode("ascii")

    #=========================================================
    # eoc
    #=========================================================

class crypt16(uh.HasSalt, uh.GenericHandler):
    """This class implements the crypt16 password hash, and follows the :ref:`password-hash-api`.

    It supports a fixed-length salt.

    The :meth:`~passlib.ifc.PasswordHash.encrypt` and :meth:`~passlib.ifc.PasswordHash.genconfig` methods accept the following optional keywords:

    :type salt: str
    :param salt:
        Optional salt string.
        If not specified, one will be autogenerated (this is recommended).
        If specified, it must be 2 characters, drawn from the regexp range ``[./0-9A-Za-z]``.
    """
    #=========================================================
    # class attrs
    #=========================================================
    #--GenericHandler--
    name = "crypt16"
    setting_kwds = ("salt",)
    checksum_size = 22
    checksum_chars = uh.HASH64_CHARS

    #--HasSalt--
    min_salt_size = max_salt_size = 2
    salt_chars = uh.HASH64_CHARS

    #=========================================================
    # internal helpers
    #=========================================================
    _hash_regex = re.compile(u(r"""
        ^
        (?P<salt>[./a-z0-9]{2})
        (?P<chk>[./a-z0-9]{22})?
        $"""), re.X|re.I)

    @classmethod
    def from_string(cls, hash):
        hash = to_unicode(hash, "ascii", "hash")
        m = cls._hash_regex.match(hash)
        if not m:
            raise uh.exc.InvalidHashError(cls)
        salt, chk = m.group("salt", "chk")
        return cls(salt=salt, checksum=chk)

    def to_string(self):
        hash = u("%s%s") % (self.salt, self.checksum or u(''))
        return uascii_to_str(hash)

    #=========================================================
    # backend
    #=========================================================
    def _calc_checksum(self, secret):
        if isinstance(secret, unicode):
            secret = secret.encode("utf-8")

        #parse salt value
        try:
            salt_value = h64.decode_int12(self.salt.encode("ascii"))
        except ValueError: #pragma: no cover - caught by class
            raise ValueError("invalid chars in salt")

        #convert first 8 byts of secret string into an integer,
        key1 = _crypt_secret_to_key(secret)

        #run data through des using input of 0
        result1 = des_encrypt_int_block(key1, 0, salt_value, 20)

        #convert next 8 bytes of secret string into integer (key=0 if secret < 8 chars)
        key2 = _crypt_secret_to_key(secret[8:16])

        #run data through des using input of 0
        result2 = des_encrypt_int_block(key2, 0, salt_value, 5)

        #done
        chk = h64big.encode_int64(result1) + h64big.encode_int64(result2)
        return chk.decode("ascii")

    #=========================================================
    # eoc
    #=========================================================

#=========================================================
# eof
#=========================================================
