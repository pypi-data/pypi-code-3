# PySNMP SMI module. Autogenerated from smidump -f python RFC1381-MIB
# by libsmi2pysnmp-0.1.3 at Mon Apr  2 20:39:33 2012,
# Python version sys.version_info(major=2, minor=7, micro=2, releaselevel='final', serial=0)

# Imports

( Integer, ObjectIdentifier, OctetString, ) = mibBuilder.importSymbols("ASN1", "Integer", "ObjectIdentifier", "OctetString")
( NamedValues, ) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
( ConstraintsIntersection, ConstraintsUnion, SingleValueConstraint, ValueRangeConstraint, ValueSizeConstraint, ) = mibBuilder.importSymbols("ASN1-REFINEMENT", "ConstraintsIntersection", "ConstraintsUnion", "SingleValueConstraint", "ValueRangeConstraint", "ValueSizeConstraint")
( Bits, Counter32, Integer32, Integer32, MibIdentifier, MibScalar, MibTable, MibTableRow, MibTableColumn, TimeTicks, transmission, ) = mibBuilder.importSymbols("SNMPv2-SMI", "Bits", "Counter32", "Integer32", "Integer32", "MibIdentifier", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "TimeTicks", "transmission")

# Types

class IfIndexType(Integer32):
    subtypeSpec = Integer32.subtypeSpec+ValueRangeConstraint(1,2147483647)
    
class PositiveInteger(Integer32):
    subtypeSpec = Integer32.subtypeSpec+ValueRangeConstraint(0,2147483647)
    

# Objects

lapb = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 16))
lapbAdmnTable = MibTable((1, 3, 6, 1, 2, 1, 10, 16, 1))
if mibBuilder.loadTexts: lapbAdmnTable.setDescription("This table contains objects that can be\nchanged to manage a LAPB interface.\nChanging one of these parameters may take\neffect in the operating LAPB immediately or\nmay wait until the interface is restarted\ndepending on the details of the\nimplementation.\n\nMost of the objects in this read-write table\nhave corresponding read-only objects in the\nlapbOperTable that return the current\noperating value.\n\nThe operating values may be different from\nthese configured values if changed by XID\nnegotiation or if a configured parameter was\nchanged after the interface was started.")
lapbAdmnEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 16, 1, 1)).setIndexNames((0, "RFC1381-MIB", "lapbAdmnIndex"))
if mibBuilder.loadTexts: lapbAdmnEntry.setDescription("Configured parameter values for a specific\nLAPB.")
lapbAdmnIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 1, 1, 1), IfIndexType()).setMaxAccess("readonly")
if mibBuilder.loadTexts: lapbAdmnIndex.setDescription("The ifIndex value for the LAPB interface.")
lapbAdmnStationType = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 1, 1, 2), Integer().subtype(subtypeSpec=SingleValueConstraint(3,2,1,)).subtype(namedValues=NamedValues(("dte", 1), ("dce", 2), ("dxe", 3), )).clone(1)).setMaxAccess("readwrite")
if mibBuilder.loadTexts: lapbAdmnStationType.setDescription("Identifies the desired station type of this\ninterface.")
lapbAdmnControlField = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 1, 1, 3), Integer().subtype(subtypeSpec=SingleValueConstraint(1,2,)).subtype(namedValues=NamedValues(("modulo8", 1), ("modulo128", 2), )).clone(1)).setMaxAccess("readwrite")
if mibBuilder.loadTexts: lapbAdmnControlField.setDescription("The desired size of the sequence numbers\nused to number frames.")
lapbAdmnTransmitN1FrameSize = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 1, 1, 4), PositiveInteger().clone('36000')).setMaxAccess("readwrite")
if mibBuilder.loadTexts: lapbAdmnTransmitN1FrameSize.setDescription("The default maximum N1 frame size desired\nin number of bits for a frame transmitted by\nthis DTE.  This excludes flags and 0 bits\ninserted for transparency.")
lapbAdmnReceiveN1FrameSize = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 1, 1, 5), PositiveInteger().clone('36000')).setMaxAccess("readwrite")
if mibBuilder.loadTexts: lapbAdmnReceiveN1FrameSize.setDescription("The default maximum N1 frame size desired\nin number of bits for a frame the DCE/remote\nDTE transmits to this DTE.  This excludes\nflags and 0 bits inserted for transparency.")
lapbAdmnTransmitKWindowSize = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 1, 1, 6), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 127)).clone(7)).setMaxAccess("readwrite")
if mibBuilder.loadTexts: lapbAdmnTransmitKWindowSize.setDescription("The default transmit window size for this\nInterface.  This is the maximum number of\nunacknowledged sequenced PDUs that may be\noutstanding from this DTE at any one time.")
lapbAdmnReceiveKWindowSize = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 1, 1, 7), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 127)).clone(7)).setMaxAccess("readwrite")
if mibBuilder.loadTexts: lapbAdmnReceiveKWindowSize.setDescription("The default receive window size for this\nInterface.  This is the maximum number of\nunacknowledged sequenced PDUs that may be\noutstanding from the DCE/remote DTE at any\none time.")
lapbAdmnN2RxmitCount = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 1, 1, 8), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535)).clone(20)).setMaxAccess("readwrite")
if mibBuilder.loadTexts: lapbAdmnN2RxmitCount.setDescription("The default N2 retry counter for this\ninterface.  This specifies the number of\ntimes a PDU will be resent after the T1\ntimer expires without an acknowledgement for\nthe PDU.")
lapbAdmnT1AckTimer = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 1, 1, 9), PositiveInteger().clone('3000')).setMaxAccess("readwrite")
if mibBuilder.loadTexts: lapbAdmnT1AckTimer.setDescription("The default T1 timer for this interface.\nThis specifies the maximum time in\nMilliseconds to wait for acknowledgment of a\nPDU.")
lapbAdmnT2AckDelayTimer = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 1, 1, 10), PositiveInteger().clone('0')).setMaxAccess("readwrite")
if mibBuilder.loadTexts: lapbAdmnT2AckDelayTimer.setDescription("The default T2 timer for this interface.\nThis specifies the maximum time in\nMilliseconds to wait before sending an\nacknowledgment for a sequenced PDU.  A value\nof zero means there will be no delay in\nacknowledgement generation.")
lapbAdmnT3DisconnectTimer = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 1, 1, 11), PositiveInteger().clone('60000')).setMaxAccess("readwrite")
if mibBuilder.loadTexts: lapbAdmnT3DisconnectTimer.setDescription("The T3 timer for this interface.  This\nspecifies the time in Milliseconds to wait\nbefore considering the link disconnected.  A\nvalue of zero indicates the link will be\nconsidered disconnected upon completion of\nthe frame exchange to disconnect the link.")
lapbAdmnT4IdleTimer = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 1, 1, 12), PositiveInteger().clone('2147483647')).setMaxAccess("readwrite")
if mibBuilder.loadTexts: lapbAdmnT4IdleTimer.setDescription("The T4 timer for this interface.  This\nspecifies the maximum time in Milliseconds\nto allow without frames being exchanged on\nthe data link.  A value of 2147483647\nindicates no idle timer is being kept.")
lapbAdmnActionInitiate = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 1, 1, 13), Integer().subtype(subtypeSpec=SingleValueConstraint(4,3,5,1,2,)).subtype(namedValues=NamedValues(("sendSABM", 1), ("sendDISC", 2), ("sendDM", 3), ("none", 4), ("other", 5), )).clone(1)).setMaxAccess("readwrite")
if mibBuilder.loadTexts: lapbAdmnActionInitiate.setDescription("This identifies the action LAPB will take\nto initiate link set-up.")
lapbAdmnActionRecvDM = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 1, 1, 14), Integer().subtype(subtypeSpec=SingleValueConstraint(2,3,1,)).subtype(namedValues=NamedValues(("sendSABM", 1), ("sendDISC", 2), ("other", 3), )).clone(1)).setMaxAccess("readwrite")
if mibBuilder.loadTexts: lapbAdmnActionRecvDM.setDescription("This identifies the action LAPB will take\nwhen it receives a DM response.")
lapbOperTable = MibTable((1, 3, 6, 1, 2, 1, 10, 16, 2))
if mibBuilder.loadTexts: lapbOperTable.setDescription("This table contains configuration\ninformation about interface parameters\ncurrently set in the interface.  Many of\nthese objects have corresponding objects in\nthe lapbAdmnTable.")
lapbOperEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 16, 2, 1)).setIndexNames((0, "RFC1381-MIB", "lapbOperIndex"))
if mibBuilder.loadTexts: lapbOperEntry.setDescription("Currently set parameter values for a\nspecific LAPB.")
lapbOperIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 2, 1, 1), IfIndexType()).setMaxAccess("readonly")
if mibBuilder.loadTexts: lapbOperIndex.setDescription("The ifIndex value for the LAPB interface.")
lapbOperStationType = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 2, 1, 2), Integer().subtype(subtypeSpec=SingleValueConstraint(3,2,1,)).subtype(namedValues=NamedValues(("dte", 1), ("dce", 2), ("dxe", 3), ))).setMaxAccess("readonly")
if mibBuilder.loadTexts: lapbOperStationType.setDescription("Identifies the current operating station\ntype of this interface.  A value of dxe (3)\nindicates XID negotiation has not yet taken\nplace.")
lapbOperControlField = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 2, 1, 3), Integer().subtype(subtypeSpec=SingleValueConstraint(1,2,)).subtype(namedValues=NamedValues(("modulo8", 1), ("modulo128", 2), ))).setMaxAccess("readonly")
if mibBuilder.loadTexts: lapbOperControlField.setDescription("The current operating size of the sequence\nnumbers used to number frames.")
lapbOperTransmitN1FrameSize = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 2, 1, 4), PositiveInteger()).setMaxAccess("readonly")
if mibBuilder.loadTexts: lapbOperTransmitN1FrameSize.setDescription("The current operating N1 frame size used\nfor the maximum number of bits in a frame\nthis DTE can transmit.  This excludes flags\nand 0 bits inserted for transparency.")
lapbOperReceiveN1FrameSize = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 2, 1, 5), PositiveInteger()).setMaxAccess("readonly")
if mibBuilder.loadTexts: lapbOperReceiveN1FrameSize.setDescription("The current operating N1 frame size used\nfor the maximum number of bits in a frame\nthe DCE/remote DTE can transmit.  This\nexcludes flags and 0 bits inserted for\ntransparency.")
lapbOperTransmitKWindowSize = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 2, 1, 6), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 127))).setMaxAccess("readonly")
if mibBuilder.loadTexts: lapbOperTransmitKWindowSize.setDescription("The current PDU window size this Interface\nuses to transmit.  This is the maximum\nnumber of unacknowledged sequenced PDUs that\nmay be outstanding from this DTE at any one\ntime.")
lapbOperReceiveKWindowSize = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 2, 1, 7), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 127))).setMaxAccess("readonly")
if mibBuilder.loadTexts: lapbOperReceiveKWindowSize.setDescription("The current receive PDU window size for\nthis Interface.  This is the maximum number\nof unacknowledged sequenced PDUs that may be\noutstanding from the DCE/remote DTE at any\none time.")
lapbOperN2RxmitCount = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 2, 1, 8), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess("readonly")
if mibBuilder.loadTexts: lapbOperN2RxmitCount.setDescription("The current N2 retry counter used for this\ninterface.  This specifies the number of\ntimes a PDU will be resent after the T1\ntimer expires without an acknowledgement for\nthe PDU.")
lapbOperT1AckTimer = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 2, 1, 9), PositiveInteger()).setMaxAccess("readonly")
if mibBuilder.loadTexts: lapbOperT1AckTimer.setDescription("The current T1 timer for this interface.\nThis specifies the maximum time in\nMilliseconds to wait for acknowledgment of a\nPDU.")
lapbOperT2AckDelayTimer = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 2, 1, 10), PositiveInteger()).setMaxAccess("readonly")
if mibBuilder.loadTexts: lapbOperT2AckDelayTimer.setDescription("The current T2 timer for this interface.\nThis specifies the maximum time in\nMilliseconds to wait before sending an\nacknowledgment for a sequenced PDU.  A value\nof zero means there will be no delay in\nacknowledgement generation.")
lapbOperT3DisconnectTimer = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 2, 1, 11), PositiveInteger()).setMaxAccess("readonly")
if mibBuilder.loadTexts: lapbOperT3DisconnectTimer.setDescription("The current T3 timer for this interface.\nThis specifies the time in Milliseconds to\nwait before considering the link\ndisconnected.  A value of zero indicates the\nlink will be considered disconnected upon\ncompletion of the frame exchange to\ndisconnect the link.")
lapbOperT4IdleTimer = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 2, 1, 12), PositiveInteger()).setMaxAccess("readwrite")
if mibBuilder.loadTexts: lapbOperT4IdleTimer.setDescription("The current T4 timer for this interface.\nThis specifies the maximum time in\nMilliseconds to allow without frames being\nexchanged on the data link.  A value of\n2147483647 indicates no idle timer is being\nkept.")
lapbOperPortId = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 2, 1, 13), ObjectIdentifier()).setMaxAccess("readonly")
if mibBuilder.loadTexts: lapbOperPortId.setDescription("This object identifies an instance of the\nindex object in the first group of objects\nin the MIB specific to the physical device\nor interface used to send and receive\nframes.  If an agent does not support any\nsuch objects, it should return nullSpec\nOBJECT IDENTIFIER {0 0}.")
lapbOperProtocolVersionId = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 2, 1, 14), ObjectIdentifier()).setMaxAccess("readonly")
if mibBuilder.loadTexts: lapbOperProtocolVersionId.setDescription("This object identifies the version of the\nlapb protocol implemented by this\ninterface.")
lapbFlowTable = MibTable((1, 3, 6, 1, 2, 1, 10, 16, 3))
if mibBuilder.loadTexts: lapbFlowTable.setDescription("This table defines the objects recorded by\nLAPB to provide information about the\ntraffic flow through the interface.")
lapbFlowEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 16, 3, 1)).setIndexNames((0, "RFC1381-MIB", "lapbFlowIfIndex"))
if mibBuilder.loadTexts: lapbFlowEntry.setDescription("The information regarding the effects of\nflow controls in LAPB.")
lapbFlowIfIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 3, 1, 1), IfIndexType()).setMaxAccess("readonly")
if mibBuilder.loadTexts: lapbFlowIfIndex.setDescription("The ifIndex value for the LAPB Interface.")
lapbFlowStateChanges = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 3, 1, 2), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: lapbFlowStateChanges.setDescription("The number of LAPB State Changes, including\nresets.")
lapbFlowChangeReason = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 3, 1, 3), Integer().subtype(subtypeSpec=SingleValueConstraint(7,8,1,2,4,12,5,9,13,11,10,6,3,)).subtype(namedValues=NamedValues(("notStarted", 1), ("frmrReceived", 10), ("frmrSent", 11), ("n2Timeout", 12), ("other", 13), ("abmEntered", 2), ("abmeEntered", 3), ("abmReset", 4), ("abmeReset", 5), ("dmReceived", 6), ("dmSent", 7), ("discReceived", 8), ("discSent", 9), ))).setMaxAccess("readonly")
if mibBuilder.loadTexts: lapbFlowChangeReason.setDescription("The reason for the most recent incrementing\nof lapbFlowStateChanges.  A DM or DISC frame\ngenerated to initiate link set-up does not\nalter this object.  When the MIB-II object\nifOperStatus does not have a value of\ntesting, there exists a correlation between\nthis object and ifOperStatus.  IfOperStatus\nwill have a value of up when this object\ncontains:  abmEntered, abmeEntered,\nabmReset, or abmeReset.  IfOperStatus will\nhave a value of down when this object has a\nvalue of notStarted, or dmReceived through\nn2Timeout.  There is no correlation when\nthis object has the value other.")
lapbFlowCurrentMode = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 3, 1, 4), Integer().subtype(subtypeSpec=SingleValueConstraint(3,6,1,8,13,12,10,11,5,2,16,15,9,14,4,17,7,)).subtype(namedValues=NamedValues(("disconnected", 1), ("bothStationsBusy", 10), ("waitingAckStationBusy", 11), ("waitingAckRemoteBusy", 12), ("waitingAckBothBusy", 13), ("rejFrameSentRemoteBusy", 14), ("xidFrameSent", 15), ("error", 16), ("other", 17), ("linkSetup", 2), ("frameReject", 3), ("disconnectRequest", 4), ("informationTransfer", 5), ("rejFrameSent", 6), ("waitingAcknowledgement", 7), ("stationBusy", 8), ("remoteStationBusy", 9), ))).setMaxAccess("readonly")
if mibBuilder.loadTexts: lapbFlowCurrentMode.setDescription("The current condition of the conversation.")
lapbFlowBusyDefers = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 3, 1, 5), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: lapbFlowBusyDefers.setDescription("The number of times this device was unable\nto transmit a frame due to a perceived\nremote busy condition.  Busy conditions can\nresult from the receipt of an RNR from the\nremote device, the lack of valid sequence\nnumber space (window saturation), or other\nconditions.")
lapbFlowRejOutPkts = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 3, 1, 6), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: lapbFlowRejOutPkts.setDescription("The number of REJ or SREJ frames sent by\nthis station.")
lapbFlowRejInPkts = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 3, 1, 7), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: lapbFlowRejInPkts.setDescription("The number of REJ or SREJ frames received\nby this station.")
lapbFlowT1Timeouts = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 3, 1, 8), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: lapbFlowT1Timeouts.setDescription("The number of times a re-transmission was\neffected by the T1 Timer expiring.")
lapbFlowFrmrSent = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 3, 1, 9), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 7))).setMaxAccess("readonly")
if mibBuilder.loadTexts: lapbFlowFrmrSent.setDescription("The Information Field of the FRMR most\nrecently sent.  If no FRMR has been sent\n(the normal case) or the information isn't\navailable, this will be an OCTET STRING of\nzero length.")
lapbFlowFrmrReceived = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 3, 1, 10), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 7))).setMaxAccess("readonly")
if mibBuilder.loadTexts: lapbFlowFrmrReceived.setDescription("The Information Field of the FRMR most\nrecently received.  If no FRMR has been\nreceived (the normal case) or the\ninformation isn't available, this will be an\nOCTET STRING of zero length.")
lapbFlowXidReceived = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 3, 1, 11), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 8206))).setMaxAccess("readonly")
if mibBuilder.loadTexts: lapbFlowXidReceived.setDescription("The Information Field of the XID frame most\nrecently received.  If no XID frame has been\nreceived, this will be an OCTET STRING of\nzero length.")
lapbXidTable = MibTable((1, 3, 6, 1, 2, 1, 10, 16, 4))
if mibBuilder.loadTexts: lapbXidTable.setDescription("This table defines values to use for XID\nnegotiation that are not found in the\nlapbAdmnTable.  This table is optional for\nimplementations that don't support XID and\nmandatory for implementations that do\ninitiate XID negotiation.")
lapbXidEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 16, 4, 1)).setIndexNames((0, "RFC1381-MIB", "lapbXidIndex"))
if mibBuilder.loadTexts: lapbXidEntry.setDescription("XId negotiation parameter values for a\nspecific LAPB.")
lapbXidIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 4, 1, 1), IfIndexType()).setMaxAccess("readonly")
if mibBuilder.loadTexts: lapbXidIndex.setDescription("The ifIndex value for the LAPB interface.")
lapbXidAdRIdentifier = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 4, 1, 2), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 255)).clone('')).setMaxAccess("readwrite")
if mibBuilder.loadTexts: lapbXidAdRIdentifier.setDescription("The value of the Address Resolution\nIdentifier.  A zero length string indicates\nno Identifier value has been assigned.")
lapbXidAdRAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 4, 1, 3), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 255)).clone('')).setMaxAccess("readwrite")
if mibBuilder.loadTexts: lapbXidAdRAddress.setDescription("The value of the Address Resolution\nAddress.  A zero length string indicates no\nAddress value has been assigned.")
lapbXidParameterUniqueIdentifier = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 4, 1, 4), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 255)).clone('')).setMaxAccess("readwrite")
if mibBuilder.loadTexts: lapbXidParameterUniqueIdentifier.setDescription("The value of the parameter unique\nIdentifier.  A zero length string indicates\nno Unique identifier value has been\nassigned.")
lapbXidGroupAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 4, 1, 5), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 255)).clone('')).setMaxAccess("readwrite")
if mibBuilder.loadTexts: lapbXidGroupAddress.setDescription("The value of the parameter Group address.\nA zero length string indicates no Group\naddress value has been assigned.")
lapbXidPortNumber = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 4, 1, 6), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 255)).clone('')).setMaxAccess("readwrite")
if mibBuilder.loadTexts: lapbXidPortNumber.setDescription("The port number assigned for this link.  A\nzero length string indicates no local port\nnumber identifier has been assigned.")
lapbXidUserDataSubfield = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 16, 4, 1, 7), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 8206)).clone('')).setMaxAccess("readwrite")
if mibBuilder.loadTexts: lapbXidUserDataSubfield.setDescription("A user data subfield, if any, to be\ntransmitted in an XID frame.  A zero length\nframe indicates no user data subfield has\nbeen assigned.  The octet string should\ninclude both the User data identifier and\nUser data field as shown in Figures 1 and\n4.")
lapbProtocolVersion = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 16, 5))
lapbProtocolIso7776v1986 = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 16, 5, 1))
lapbProtocolCcittV1980 = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 16, 5, 2))
lapbProtocolCcittV1984 = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 16, 5, 3))

# Augmentions

# Exports

# Types
mibBuilder.exportSymbols("RFC1381-MIB", IfIndexType=IfIndexType, PositiveInteger=PositiveInteger)

# Objects
mibBuilder.exportSymbols("RFC1381-MIB", lapb=lapb, lapbAdmnTable=lapbAdmnTable, lapbAdmnEntry=lapbAdmnEntry, lapbAdmnIndex=lapbAdmnIndex, lapbAdmnStationType=lapbAdmnStationType, lapbAdmnControlField=lapbAdmnControlField, lapbAdmnTransmitN1FrameSize=lapbAdmnTransmitN1FrameSize, lapbAdmnReceiveN1FrameSize=lapbAdmnReceiveN1FrameSize, lapbAdmnTransmitKWindowSize=lapbAdmnTransmitKWindowSize, lapbAdmnReceiveKWindowSize=lapbAdmnReceiveKWindowSize, lapbAdmnN2RxmitCount=lapbAdmnN2RxmitCount, lapbAdmnT1AckTimer=lapbAdmnT1AckTimer, lapbAdmnT2AckDelayTimer=lapbAdmnT2AckDelayTimer, lapbAdmnT3DisconnectTimer=lapbAdmnT3DisconnectTimer, lapbAdmnT4IdleTimer=lapbAdmnT4IdleTimer, lapbAdmnActionInitiate=lapbAdmnActionInitiate, lapbAdmnActionRecvDM=lapbAdmnActionRecvDM, lapbOperTable=lapbOperTable, lapbOperEntry=lapbOperEntry, lapbOperIndex=lapbOperIndex, lapbOperStationType=lapbOperStationType, lapbOperControlField=lapbOperControlField, lapbOperTransmitN1FrameSize=lapbOperTransmitN1FrameSize, lapbOperReceiveN1FrameSize=lapbOperReceiveN1FrameSize, lapbOperTransmitKWindowSize=lapbOperTransmitKWindowSize, lapbOperReceiveKWindowSize=lapbOperReceiveKWindowSize, lapbOperN2RxmitCount=lapbOperN2RxmitCount, lapbOperT1AckTimer=lapbOperT1AckTimer, lapbOperT2AckDelayTimer=lapbOperT2AckDelayTimer, lapbOperT3DisconnectTimer=lapbOperT3DisconnectTimer, lapbOperT4IdleTimer=lapbOperT4IdleTimer, lapbOperPortId=lapbOperPortId, lapbOperProtocolVersionId=lapbOperProtocolVersionId, lapbFlowTable=lapbFlowTable, lapbFlowEntry=lapbFlowEntry, lapbFlowIfIndex=lapbFlowIfIndex, lapbFlowStateChanges=lapbFlowStateChanges, lapbFlowChangeReason=lapbFlowChangeReason, lapbFlowCurrentMode=lapbFlowCurrentMode, lapbFlowBusyDefers=lapbFlowBusyDefers, lapbFlowRejOutPkts=lapbFlowRejOutPkts, lapbFlowRejInPkts=lapbFlowRejInPkts, lapbFlowT1Timeouts=lapbFlowT1Timeouts, lapbFlowFrmrSent=lapbFlowFrmrSent, lapbFlowFrmrReceived=lapbFlowFrmrReceived, lapbFlowXidReceived=lapbFlowXidReceived, lapbXidTable=lapbXidTable, lapbXidEntry=lapbXidEntry, lapbXidIndex=lapbXidIndex, lapbXidAdRIdentifier=lapbXidAdRIdentifier, lapbXidAdRAddress=lapbXidAdRAddress, lapbXidParameterUniqueIdentifier=lapbXidParameterUniqueIdentifier, lapbXidGroupAddress=lapbXidGroupAddress, lapbXidPortNumber=lapbXidPortNumber, lapbXidUserDataSubfield=lapbXidUserDataSubfield, lapbProtocolVersion=lapbProtocolVersion, lapbProtocolIso7776v1986=lapbProtocolIso7776v1986, lapbProtocolCcittV1980=lapbProtocolCcittV1980, lapbProtocolCcittV1984=lapbProtocolCcittV1984)

