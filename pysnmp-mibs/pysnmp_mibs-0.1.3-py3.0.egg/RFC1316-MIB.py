# PySNMP SMI module. Autogenerated from smidump -f python RFC1316-MIB
# by libsmi2pysnmp-0.1.3 at Mon Apr  2 20:39:32 2012,
# Python version sys.version_info(major=2, minor=7, micro=2, releaselevel='final', serial=0)

# Imports

( Integer, ObjectIdentifier, OctetString, ) = mibBuilder.importSymbols("ASN1", "Integer", "ObjectIdentifier", "OctetString")
( NamedValues, ) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
( ConstraintsIntersection, ConstraintsUnion, SingleValueConstraint, ValueRangeConstraint, ValueSizeConstraint, ) = mibBuilder.importSymbols("ASN1-REFINEMENT", "ConstraintsIntersection", "ConstraintsUnion", "SingleValueConstraint", "ValueRangeConstraint", "ValueSizeConstraint")
( Bits, Counter32, Gauge32, Integer32, Integer32, MibIdentifier, MibScalar, MibTable, MibTableRow, MibTableColumn, TimeTicks, TimeTicks, mib_2, ) = mibBuilder.importSymbols("SNMPv2-SMI", "Bits", "Counter32", "Gauge32", "Integer32", "Integer32", "MibIdentifier", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "TimeTicks", "TimeTicks", "mib-2")
( DisplayString, ) = mibBuilder.importSymbols("SNMPv2-TC", "DisplayString")

# Types

class AutonomousType(ObjectIdentifier):
    pass

class InstancePointer(ObjectIdentifier):
    pass


# Objects

char = MibIdentifier((1, 3, 6, 1, 2, 1, 19))
charNumber = MibScalar((1, 3, 6, 1, 2, 1, 19, 1), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: charNumber.setDescription("The number of entries in charPortTable, regardless\nof their current state.")
charPortTable = MibTable((1, 3, 6, 1, 2, 1, 19, 2))
if mibBuilder.loadTexts: charPortTable.setDescription("A list of port entries.  The number of entries is\ngiven by the value of charNumber.")
charPortEntry = MibTableRow((1, 3, 6, 1, 2, 1, 19, 2, 1)).setIndexNames((0, "RFC1316-MIB", "charPortIndex"))
if mibBuilder.loadTexts: charPortEntry.setDescription("Status and parameter values for a character port.")
charPortIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 2, 1, 1), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: charPortIndex.setDescription("A unique value for each character port.  Its value\nranges between 1 and the value of charNumber.  By\nconvention and if possible, hardware port numbers\ncome first, with a simple, direct mapping.  The\nvalue for each port must remain constant at least\nfrom one re-initialization of the network management\nagent to the next.")
charPortName = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 2, 1, 2), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0, 32))).setMaxAccess("readwrite")
if mibBuilder.loadTexts: charPortName.setDescription("An administratively assigned name for the port,\ntypically with some local significance.")
charPortType = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 2, 1, 3), Integer().subtype(subtypeSpec=SingleValueConstraint(1,2,)).subtype(namedValues=NamedValues(("physical", 1), ("virtual", 2), ))).setMaxAccess("readonly")
if mibBuilder.loadTexts: charPortType.setDescription("The port's type, 'physical' if the port represents\nan external hardware connector, 'virtual' if it does\nnot.")
charPortHardware = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 2, 1, 4), AutonomousType()).setMaxAccess("readonly")
if mibBuilder.loadTexts: charPortHardware.setDescription("A reference to hardware MIB definitions specific to\na physical port's external connector.  For example,\nif the connector is RS-232, then the value of this\nobject refers to a MIB sub-tree defining objects\nspecific to RS-232.  If an agent is not configured\nto have such values, the agent returns the object\nidentifier:\n\n    nullHardware OBJECT IDENTIFIER ::= { 0 0 }")
charPortReset = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 2, 1, 5), Integer().subtype(subtypeSpec=SingleValueConstraint(1,2,)).subtype(namedValues=NamedValues(("ready", 1), ("execute", 2), ))).setMaxAccess("readwrite")
if mibBuilder.loadTexts: charPortReset.setDescription("A control to force the port into a clean, initial\nstate, both hardware and software, disconnecting all\nthe port's existing sessions.  In response to a\nget-request or get-next-request, the agent always\nreturns 'ready' as the value.  Setting the value to\n'execute' causes a reset.")
charPortAdminStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 2, 1, 6), Integer().subtype(subtypeSpec=SingleValueConstraint(2,3,1,4,)).subtype(namedValues=NamedValues(("enabled", 1), ("disabled", 2), ("off", 3), ("maintenance", 4), ))).setMaxAccess("readwrite")
if mibBuilder.loadTexts: charPortAdminStatus.setDescription("The port's desired state, independent of flow\ncontrol.  'enabled' indicates that the port is\nallowed to pass characters and form new sessions.\n'disabled' indicates that the port is allowed to\npass characters but not form new sessions.  'off'\nindicates that the port is not allowed to pass\ncharacters or have any sessions. 'maintenance'\nindicates a maintenance mode, exclusive of normal\noperation, such as running a test.")
charPortOperStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 2, 1, 7), Integer().subtype(subtypeSpec=SingleValueConstraint(4,1,2,3,5,)).subtype(namedValues=NamedValues(("up", 1), ("down", 2), ("maintenance", 3), ("absent", 4), ("active", 5), ))).setMaxAccess("readonly")
if mibBuilder.loadTexts: charPortOperStatus.setDescription("The port's actual, operational state, independent\nof flow control.  'up' indicates able to function\nnormally.  'down' indicates inability to function\nfor administrative or operational reasons.\n'maintenance' indicates a maintenance mode,\nexclusive of normal operation, such as running a\ntest.  'absent' indicates that port hardware is not\npresent.  'active' indicates up with a user present\n(e.g. logged in).")
charPortLastChange = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 2, 1, 8), TimeTicks()).setMaxAccess("readonly")
if mibBuilder.loadTexts: charPortLastChange.setDescription("The value of sysUpTime at the time the port entered\nits current operational state.  If the current state\nwas entered prior to the last reinitialization of\nthe local network management subsystem, then this\nobject contains a zero value.")
charPortInFlowType = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 2, 1, 9), Integer().subtype(subtypeSpec=SingleValueConstraint(1,2,3,5,4,)).subtype(namedValues=NamedValues(("none", 1), ("xonXoff", 2), ("hardware", 3), ("ctsRts", 4), ("dsrDtr", 5), ))).setMaxAccess("readwrite")
if mibBuilder.loadTexts: charPortInFlowType.setDescription("The port's type of input flow control.  'none'\nindicates no flow control at this level or below.\n'xonXoff' indicates software flow control by\nrecognizing XON and XOFF characters.  'hardware'\nindicates flow control delegated to the lower level,\nfor example a parallel port.\n\n'ctsRts' and 'dsrDtr' are specific to RS-232-like\nports.  Although not architecturally pure, they are\nincluded here for simplicity's sake.")
charPortOutFlowType = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 2, 1, 10), Integer().subtype(subtypeSpec=SingleValueConstraint(1,2,3,5,4,)).subtype(namedValues=NamedValues(("none", 1), ("xonXoff", 2), ("hardware", 3), ("ctsRts", 4), ("dsrDtr", 5), ))).setMaxAccess("readwrite")
if mibBuilder.loadTexts: charPortOutFlowType.setDescription("The port's type of output flow control.  'none'\nindicates no flow control at this level or below.\n'xonXoff' indicates software flow control by\nrecognizing XON and XOFF characters.  'hardware'\nindicates flow control delegated to the lower level,\nfor example a parallel port.\n\n'ctsRts' and 'dsrDtr' are specific to RS-232-like\nports.  Although not architecturally pure, they are\nincluded here for simplicy's sake.")
charPortInFlowState = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 2, 1, 11), Integer().subtype(subtypeSpec=SingleValueConstraint(4,2,1,3,)).subtype(namedValues=NamedValues(("none", 1), ("unknown", 2), ("stop", 3), ("go", 4), ))).setMaxAccess("readonly")
if mibBuilder.loadTexts: charPortInFlowState.setDescription("The current operational state of input flow control\non the port.  'none' indicates not applicable.\n'unknown' indicates this level does not know.\n'stop' indicates flow not allowed.  'go' indicates\nflow allowed.")
charPortOutFlowState = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 2, 1, 12), Integer().subtype(subtypeSpec=SingleValueConstraint(4,2,1,3,)).subtype(namedValues=NamedValues(("none", 1), ("unknown", 2), ("stop", 3), ("go", 4), ))).setMaxAccess("readonly")
if mibBuilder.loadTexts: charPortOutFlowState.setDescription("The current operational state of output flow\ncontrol on the port.  'none' indicates not\napplicable.  'unknown' indicates this level does not\nknow.  'stop' indicates flow not allowed.  'go'\nindicates flow allowed.")
charPortInCharacters = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 2, 1, 13), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: charPortInCharacters.setDescription("Total number of characters detected as input from\nthe port since system re-initialization and while\nthe port operational state was 'up', 'active', or\n'maintenance', including, for example, framing, flow\ncontrol (i.e. XON and XOFF), each occurrence of a\nBREAK condition, locally-processed input, and input\nsent to all sessions.")
charPortOutCharacters = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 2, 1, 14), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: charPortOutCharacters.setDescription("Total number of characters detected as output to\nthe port since system re-initialization and while\nthe port operational state was 'up', 'active', or\n'maintenance', including, for example, framing, flow\ncontrol (i.e. XON and XOFF), each occurrence of a\nBREAK condition, locally-created output, and output\nreceived from all sessions.")
charPortAdminOrigin = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 2, 1, 15), Integer().subtype(subtypeSpec=SingleValueConstraint(3,4,1,2,)).subtype(namedValues=NamedValues(("dynamic", 1), ("network", 2), ("local", 3), ("none", 4), ))).setMaxAccess("readwrite")
if mibBuilder.loadTexts: charPortAdminOrigin.setDescription("The administratively allowed origin for\nestablishing session on the port.  'dynamic' allows\n'network' or 'local' session establishment. 'none'\ndisallows session establishment.")
charPortSessionMaximum = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 2, 1, 16), Integer32()).setMaxAccess("readwrite")
if mibBuilder.loadTexts: charPortSessionMaximum.setDescription("The maximum number of concurrent sessions allowed\non the port.  A value of -1 indicates no maximum.\nSetting the maximum to less than the current number\nof sessions has unspecified results.")
charPortSessionNumber = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 2, 1, 17), Gauge32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: charPortSessionNumber.setDescription("The number of open sessions on the port that are in\nthe connecting, connected, or disconnecting state.")
charPortSessionIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 2, 1, 18), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: charPortSessionIndex.setDescription("The value of charSessIndex for the port's first or\nonly active session.  If the port has no active\nsession, the agent returns the value zero.")
charSessTable = MibTable((1, 3, 6, 1, 2, 1, 19, 3))
if mibBuilder.loadTexts: charSessTable.setDescription("A list of port session entries.")
charSessEntry = MibTableRow((1, 3, 6, 1, 2, 1, 19, 3, 1)).setIndexNames((0, "RFC1316-MIB", "charSessPortIndex"), (0, "RFC1316-MIB", "charSessIndex"))
if mibBuilder.loadTexts: charSessEntry.setDescription("Status and parameter values for a character port\nsession.")
charSessPortIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 3, 1, 1), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: charSessPortIndex.setDescription("The value of charPortIndex for the port to which\nthis session belongs.")
charSessIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 3, 1, 2), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: charSessIndex.setDescription("The session index in the context of the port, a\nnon-zero positive integer.  Session indexes within a\nport need not be sequential.  Session indexes may be\nreused for different ports.  For example, port 1 and\nport 3 may both have a session 2 at the same time.\nSession indexes may have any valid integer value,\nwith any meaning convenient to the agent\nimplementation.")
charSessKill = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 3, 1, 3), Integer().subtype(subtypeSpec=SingleValueConstraint(1,2,)).subtype(namedValues=NamedValues(("ready", 1), ("execute", 2), ))).setMaxAccess("readwrite")
if mibBuilder.loadTexts: charSessKill.setDescription("A control to terminate the session.  In response to\na get-request or get-next-request, the agent always\nreturns 'ready' as the value.  Setting the value to\n'execute' causes termination.")
charSessState = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 3, 1, 4), Integer().subtype(subtypeSpec=SingleValueConstraint(2,3,1,)).subtype(namedValues=NamedValues(("connecting", 1), ("connected", 2), ("disconnecting", 3), ))).setMaxAccess("readonly")
if mibBuilder.loadTexts: charSessState.setDescription("The current operational state of the session,\ndisregarding flow control.  'connected' indicates\nthat character data could flow on the network side\nof session.  'connecting' indicates moving from\nnonexistent toward 'connected'.  'disconnecting'\nindicates moving from 'connected' or 'connecting' to\nnonexistent.")
charSessProtocol = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 3, 1, 5), AutonomousType()).setMaxAccess("readonly")
if mibBuilder.loadTexts: charSessProtocol.setDescription("The network protocol over which the session is\nrunning.  Other OBJECT IDENTIFIER values may be\ndefined elsewhere, in association with specific\nprotocols.  However, this document assigns those of\nknown interest as of this writing.")
charSessOperOrigin = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 3, 1, 6), Integer().subtype(subtypeSpec=SingleValueConstraint(1,3,2,)).subtype(namedValues=NamedValues(("unknown", 1), ("network", 2), ("local", 3), ))).setMaxAccess("readonly")
if mibBuilder.loadTexts: charSessOperOrigin.setDescription("The session's source of establishment.")
charSessInCharacters = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 3, 1, 7), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: charSessInCharacters.setDescription("This session's subset of charPortInCharacters.")
charSessOutCharacters = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 3, 1, 8), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: charSessOutCharacters.setDescription("This session's subset of charPortOutCharacters.")
charSessConnectionId = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 3, 1, 9), InstancePointer()).setMaxAccess("readonly")
if mibBuilder.loadTexts: charSessConnectionId.setDescription("A reference to additional local MIB information.\nThis should be the highest available related MIB,\ncorresponding to charSessProtocol, such as Telnet.\nFor example, the value for a TCP connection (in the\nabsence of a Telnet MIB) is the object identifier of\ntcpConnState.  If an agent is not configured to have\nsuch values, the agent returns the object\nidentifier:\n\n    nullConnectionId OBJECT IDENTIFIER ::= { 0 0 }")
charSessStartTime = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 3, 1, 10), TimeTicks()).setMaxAccess("readonly")
if mibBuilder.loadTexts: charSessStartTime.setDescription("The value of sysUpTime in MIB-2 when the session\nentered connecting state.")
wellKnownProtocols = MibIdentifier((1, 3, 6, 1, 2, 1, 19, 4))
protocolOther = MibIdentifier((1, 3, 6, 1, 2, 1, 19, 4, 1))
protocolTelnet = MibIdentifier((1, 3, 6, 1, 2, 1, 19, 4, 2))
protocolRlogin = MibIdentifier((1, 3, 6, 1, 2, 1, 19, 4, 3))
protocolLat = MibIdentifier((1, 3, 6, 1, 2, 1, 19, 4, 4))
protocolX29 = MibIdentifier((1, 3, 6, 1, 2, 1, 19, 4, 5))
protocolVtp = MibIdentifier((1, 3, 6, 1, 2, 1, 19, 4, 6))

# Augmentions

# Exports

# Types
mibBuilder.exportSymbols("RFC1316-MIB", AutonomousType=AutonomousType, InstancePointer=InstancePointer)

# Objects
mibBuilder.exportSymbols("RFC1316-MIB", char=char, charNumber=charNumber, charPortTable=charPortTable, charPortEntry=charPortEntry, charPortIndex=charPortIndex, charPortName=charPortName, charPortType=charPortType, charPortHardware=charPortHardware, charPortReset=charPortReset, charPortAdminStatus=charPortAdminStatus, charPortOperStatus=charPortOperStatus, charPortLastChange=charPortLastChange, charPortInFlowType=charPortInFlowType, charPortOutFlowType=charPortOutFlowType, charPortInFlowState=charPortInFlowState, charPortOutFlowState=charPortOutFlowState, charPortInCharacters=charPortInCharacters, charPortOutCharacters=charPortOutCharacters, charPortAdminOrigin=charPortAdminOrigin, charPortSessionMaximum=charPortSessionMaximum, charPortSessionNumber=charPortSessionNumber, charPortSessionIndex=charPortSessionIndex, charSessTable=charSessTable, charSessEntry=charSessEntry, charSessPortIndex=charSessPortIndex, charSessIndex=charSessIndex, charSessKill=charSessKill, charSessState=charSessState, charSessProtocol=charSessProtocol, charSessOperOrigin=charSessOperOrigin, charSessInCharacters=charSessInCharacters, charSessOutCharacters=charSessOutCharacters, charSessConnectionId=charSessConnectionId, charSessStartTime=charSessStartTime, wellKnownProtocols=wellKnownProtocols, protocolOther=protocolOther, protocolTelnet=protocolTelnet, protocolRlogin=protocolRlogin, protocolLat=protocolLat, protocolX29=protocolX29, protocolVtp=protocolVtp)

