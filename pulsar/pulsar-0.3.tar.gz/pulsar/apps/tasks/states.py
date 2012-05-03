SUCCESS = "SUCCESS"
FAILURE = "FAILURE"
UNKNOWN = "UNKNOWN"
REVOKED = "REVOKED"
STARTED = "STARTED"
RECEIVED = "RECEIVED"
RETRY = "RETRY"
PENDING = "PENDING"
#: Lower index means higher precedence.
PRECEDENCE = (
              (SUCCESS,1),
              (FAILURE,2),
              (UNKNOWN,3),
              (REVOKED,4),
              (STARTED,5),
              (RECEIVED,6),
              (RETRY,7),
              (PENDING,8)
              )

PRECEDENCE_MAPPING = dict(PRECEDENCE)
UNKNOWN_STATE = PRECEDENCE_MAPPING[UNKNOWN]
READY_STATES = frozenset([SUCCESS, FAILURE, REVOKED])
NOT_STARTED_STATES = frozenset([PENDING, RECEIVED, RETRY])
UNREADY_STATES = frozenset([PENDING, RECEIVED, STARTED, RETRY])
EXCEPTION_STATES = frozenset([RETRY, FAILURE, REVOKED])
PROPAGATE_STATES = frozenset([FAILURE, REVOKED])
ALL_STATES = frozenset([PENDING, RECEIVED, STARTED,
                        SUCCESS, FAILURE, RETRY, REVOKED])
