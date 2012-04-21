# PySNMP SMI module. Autogenerated from smidump -f python SIP-MIB
# by libsmi2pysnmp-0.1.3 at Mon Apr  2 20:39:37 2012,
# Python version sys.version_info(major=2, minor=7, micro=2, releaselevel='final', serial=0)

# Imports

( Integer, ObjectIdentifier, OctetString, ) = mibBuilder.importSymbols("ASN1", "Integer", "ObjectIdentifier", "OctetString")
( NamedValues, ) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
( ConstraintsIntersection, ConstraintsUnion, SingleValueConstraint, ValueRangeConstraint, ValueSizeConstraint, ) = mibBuilder.importSymbols("ASN1-REFINEMENT", "ConstraintsIntersection", "ConstraintsUnion", "SingleValueConstraint", "ValueRangeConstraint", "ValueSizeConstraint")
( ifIndex, ) = mibBuilder.importSymbols("IF-MIB", "ifIndex")
( ModuleCompliance, ObjectGroup, ) = mibBuilder.importSymbols("SNMPv2-CONF", "ModuleCompliance", "ObjectGroup")
( Bits, Counter32, Integer32, Integer32, IpAddress, ModuleIdentity, MibIdentifier, MibScalar, MibTable, MibTableRow, MibTableColumn, TimeTicks, mib_2, transmission, ) = mibBuilder.importSymbols("SNMPv2-SMI", "Bits", "Counter32", "Integer32", "Integer32", "IpAddress", "ModuleIdentity", "MibIdentifier", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "TimeTicks", "mib-2", "transmission")
( TextualConvention, TimeStamp, ) = mibBuilder.importSymbols("SNMPv2-TC", "TextualConvention", "TimeStamp")

# Types

class IfIndex(Integer32):
    pass

class SMDSAddress(TextualConvention, OctetString):
    displayHint = "1x:"
    subtypeSpec = OctetString.subtypeSpec+ValueSizeConstraint(8,8)
    fixedLength = 8
    

# Objects

sip = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 31))
sipL3Table = MibTable((1, 3, 6, 1, 2, 1, 10, 31, 1))
if mibBuilder.loadTexts: sipL3Table.setDescription("This table contains SIP L3 parameters and\nstate variables, one entry per SIPL3 interface.")
sipL3Entry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 31, 1, 1)).setIndexNames((0, "SIP-MIB", "sipL3Index"))
if mibBuilder.loadTexts: sipL3Entry.setDescription("This list contains SIP L3 parameters and\nstate variables.")
sipL3Index = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 31, 1, 1, 1), IfIndex()).setMaxAccess("readonly")
if mibBuilder.loadTexts: sipL3Index.setDescription("The value of this object identifies the SIP\nL3 interface for which this entry contains\nmanagement information. ")
sipL3ReceivedIndividualDAs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 31, 1, 1, 2), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: sipL3ReceivedIndividualDAs.setDescription("The total number of individually addressed SIP\nLevel 3 PDUs received from the remote system\nacross the SNI.  The total includes only\nunerrored L3PDUs.")
sipL3ReceivedGAs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 31, 1, 1, 3), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: sipL3ReceivedGAs.setDescription("The total number of group addressed SIP Level 3\nPDUs received from the remote system across the\nSNI.  The total includes only unerrored L3PDUs.")
sipL3UnrecognizedIndividualDAs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 31, 1, 1, 4), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: sipL3UnrecognizedIndividualDAs.setDescription("The number of SIP Level 3 PDUs received from the\nremote system with invalid or unknown individual\ndestination addresses (Destination Address\nScreening violations are not included).  See SMDS\nSubscription MIB module.")
sipL3UnrecognizedGAs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 31, 1, 1, 5), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: sipL3UnrecognizedGAs.setDescription("The number of SIP Level 3 PDUs received from the\nremote system with invalid or unknown group\naddresses.  (Destination Address Screening\nviolations are not included).  See SMDS\nSubscription MIB module.")
sipL3SentIndividualDAs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 31, 1, 1, 6), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: sipL3SentIndividualDAs.setDescription("The number of individually addressed SIP Level 3\nPDUs that have been sent by this system across the\nSNI.")
sipL3SentGAs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 31, 1, 1, 7), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: sipL3SentGAs.setDescription("The number of group addressed SIP L3PDUs that\nhave been sent by this system across the SNI.")
sipL3Errors = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 31, 1, 1, 8), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: sipL3Errors.setDescription("The total number of SIP Level 3 PDUs received\nfrom the remote system that were discovered to\nhave errors (including protocol processing and bit\nerrors but excluding addressing-related errors)\nand were discarded.  Includes both group addressed\nL3PDUs and L3PDUs containing an individual\ndestination address.")
sipL3InvalidSMDSAddressTypes = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 31, 1, 1, 9), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: sipL3InvalidSMDSAddressTypes.setDescription("The number of SIP Level 3 PDUs received from the\nremote system that had the Source or Destination\nAddress_Type subfields, (the four most significant\nbits of the 64 bit address field), not equal to\nthe value 1100 or 1110.  Also, an error is\nconsidered to have occurred if the Address_Type\nfield for a Source Address, the four most\nsignificant bits of the 64 bits, is equal to 1110\n(a group address).")
sipL3VersionSupport = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 31, 1, 1, 10), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: sipL3VersionSupport.setDescription("A value which indicates the version(s) of SIP\nthat this interface supports.  The value is a sum.\nThis sum initially takes the value zero.  For each\nversion, V, that this interface supports, 2 raised\nto (V - 1) is added to the sum. For example, a\nport supporting versions 1 and 2 would have a\nvalue of (2^(1-1)+2^(2-1))=3.  The\nsipL3VersionSupport is effectively a bit mask with\nVersion 1 equal to the least significant bit\n(LSB).")
sipL2Table = MibTable((1, 3, 6, 1, 2, 1, 10, 31, 2))
if mibBuilder.loadTexts: sipL2Table.setDescription("This table contains SIP L2PDU parameters and\nstate variables, one entry per SIP L2 interface.")
sipL2Entry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 31, 2, 1)).setIndexNames((0, "SIP-MIB", "sipL2Index"))
if mibBuilder.loadTexts: sipL2Entry.setDescription("This list contains SIP L2 parameters and state\nvariables.")
sipL2Index = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 31, 2, 1, 1), IfIndex()).setMaxAccess("readonly")
if mibBuilder.loadTexts: sipL2Index.setDescription("The value of this object identifies the SIP\ninterface for which this entry contains management\ninformation.")
sipL2ReceivedCounts = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 31, 2, 1, 2), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: sipL2ReceivedCounts.setDescription("The number of SIP Level 2 PDUs received from the\nremote system across the SNI. The total includes\nonly unerrored L2PDUs.")
sipL2SentCounts = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 31, 2, 1, 3), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: sipL2SentCounts.setDescription("The number of SIP Level 2 PDUs that have been\nsent by this system across the SNI.")
sipL2HcsOrCRCErrors = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 31, 2, 1, 4), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: sipL2HcsOrCRCErrors.setDescription("The number of received SIP Level 2 PDUs that were\ndiscovered to have either a Header Check Sequence\nerror or a Payload CRC violation.")
sipL2PayloadLengthErrors = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 31, 2, 1, 5), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: sipL2PayloadLengthErrors.setDescription("The number of received SIP Level 2 PDUs that had\nPayload Length errors that fall in the following\nspecifications:\n- SSM L2_PDU payload length field value less\n- than 28 octets or greater than 44 octets,\n\n- BOM or COM L2_PDU payload length field not\n- equal to 44 octets,\n- EOM L2_PDU payload length field value less\n- than 4 octets or greater than 44 octets.")
sipL2SequenceNumberErrors = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 31, 2, 1, 6), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: sipL2SequenceNumberErrors.setDescription("The number of received SIP Level 2 PDUs that had\na sequence number within the L2PDU not equal to\nthe expected sequence number of the SMDS SS\nreceive process.")
sipL2MidCurrentlyActiveErrors = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 31, 2, 1, 7), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: sipL2MidCurrentlyActiveErrors.setDescription("The number of received SIP Level 2 PDUs that are\nBOMs for which an active receive process is\nalready started.")
sipL2BomOrSSMsMIDErrors = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 31, 2, 1, 8), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: sipL2BomOrSSMsMIDErrors.setDescription("The number of received SIP Level 2 PDUs that are\nSSMs with a MID not equal to zero or are BOMs with\nMIDs equal to zero.")
sipL2EomsMIDErrors = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 31, 2, 1, 9), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: sipL2EomsMIDErrors.setDescription("The number of received SIP Level 2 PDUs that are\nEOMs for which there is no active receive process\nfor the MID (i.e., the receipt of an EOM which\ndoes not correspond to a BOM) OR the EOM has a MID\nequal to zero.")
sipPLCP = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 31, 3))
sipDS1PLCPTable = MibTable((1, 3, 6, 1, 2, 1, 10, 31, 3, 1))
if mibBuilder.loadTexts: sipDS1PLCPTable.setDescription("This table contains SIP DS1 PLCP parameters and\nstate variables, one entry per SIP port.")
sipDS1PLCPEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 31, 3, 1, 1)).setIndexNames((0, "SIP-MIB", "sipDS1PLCPIndex"))
if mibBuilder.loadTexts: sipDS1PLCPEntry.setDescription("This list contains SIP DS1 PLCP parameters and\nstate variables.")
sipDS1PLCPIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 31, 3, 1, 1, 1), IfIndex()).setMaxAccess("readonly")
if mibBuilder.loadTexts: sipDS1PLCPIndex.setDescription("The value of this object identifies the\ninterface for which this entry contains management\ninformation. ")
sipDS1PLCPSEFSs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 31, 3, 1, 1, 2), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: sipDS1PLCPSEFSs.setDescription("A DS1 Severely Errored Framing Second (SEFS) is a\ncount of one-second intervals containing one or\nmore SEF events.  A Severely Errored Framing (SEF)\nevent is declared when an error in the A1 octet\nand an error in the A2 octet of a framing octet\npair (i.e., errors in both framing octets), or two\nconsecutive invalid and/or nonsequential Path\nOverhead Identifier octets are detected.")
sipDS1PLCPAlarmState = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 31, 3, 1, 1, 3), Integer().subtype(subtypeSpec=SingleValueConstraint(3,1,2,)).subtype(namedValues=NamedValues(("noAlarm", 1), ("receivedFarEndAlarm", 2), ("incomingLOF", 3), ))).setMaxAccess("readonly")
if mibBuilder.loadTexts: sipDS1PLCPAlarmState.setDescription("This variable indicates if there is an alarm\npresent for the DS1 PLCP.  The value\nreceivedFarEndAlarm means that the DS1 PLCP has\nreceived an incoming Yellow Signal, the value\nincomingLOF means that the DS1 PLCP has declared a\nloss of frame (LOF) failure condition, and the\nvalue noAlarm means that there are no alarms\npresent.  See TR-TSV-000773 for a description of\nalarm states.")
sipDS1PLCPUASs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 31, 3, 1, 1, 4), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: sipDS1PLCPUASs.setDescription("The counter associated with the number of\nUnavailable Seconds, as defined by TR-TSV-000773,\nencountered by the PLCP.")
sipDS3PLCPTable = MibTable((1, 3, 6, 1, 2, 1, 10, 31, 3, 2))
if mibBuilder.loadTexts: sipDS3PLCPTable.setDescription("This table contains SIP DS3 PLCP parameters and\nstate variables, one entry per SIP port.")
sipDS3PLCPEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 31, 3, 2, 1)).setIndexNames((0, "SIP-MIB", "sipDS3PLCPIndex"))
if mibBuilder.loadTexts: sipDS3PLCPEntry.setDescription("This list contains SIP DS3 PLCP parameters and\nstate variables.")
sipDS3PLCPIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 31, 3, 2, 1, 1), IfIndex()).setMaxAccess("readonly")
if mibBuilder.loadTexts: sipDS3PLCPIndex.setDescription("The value of this object identifies the\ninterface for which this entry contains management\ninformation.  ")
sipDS3PLCPSEFSs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 31, 3, 2, 1, 2), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: sipDS3PLCPSEFSs.setDescription("A DS3 Severely Errored Framing Second (SEFS) is a\ncount of one-second intervals containing one or\nmore SEF events.  A Severely Errored Framing (SEF)\nevent is declared when an error in the A1 octet\nand an error in the A2 octet of a framing octet\npair (i.e., errors in both framing octets), or two\nconsecutive invalid and/or nonsequential Path\nOverhead Identifier octets are detected.")
sipDS3PLCPAlarmState = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 31, 3, 2, 1, 3), Integer().subtype(subtypeSpec=SingleValueConstraint(3,1,2,)).subtype(namedValues=NamedValues(("noAlarm", 1), ("receivedFarEndAlarm", 2), ("incomingLOF", 3), ))).setMaxAccess("readonly")
if mibBuilder.loadTexts: sipDS3PLCPAlarmState.setDescription("This variable indicates if there is an alarm\npresent for the DS3 PLCP.  The value\nreceivedFarEndAlarm means that the DS3 PLCP has\nreceived an incoming Yellow Signal, the value\nincomingLOF means that the DS3 PLCP has declared a\nloss of frame (LOF) failure condition, and the\nvalue noAlarm means that there are no alarms\npresent.  See TR-TSV-000773 for a description of\nalarm states.")
sipDS3PLCPUASs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 31, 3, 2, 1, 4), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: sipDS3PLCPUASs.setDescription("The counter associated with the number of\nUnavailable Seconds, as defined by TR-TSV-000773,\nencountered by the PLCP.")
smdsApplications = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 31, 4))
ipOverSMDS = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 31, 4, 1))
ipOverSMDSTable = MibTable((1, 3, 6, 1, 2, 1, 10, 31, 4, 1, 1))
if mibBuilder.loadTexts: ipOverSMDSTable.setDescription("The table of addressing information relevant to\nthis entity's IP addresses.")
ipOverSMDSEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 31, 4, 1, 1, 1)).setIndexNames((0, "SIP-MIB", "ipOverSMDSIndex"), (0, "SIP-MIB", "ipOverSMDSAddress"))
if mibBuilder.loadTexts: ipOverSMDSEntry.setDescription("The addressing information for one of this\nentity's IP addresses.")
ipOverSMDSIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 31, 4, 1, 1, 1, 1), IfIndex()).setMaxAccess("readonly")
if mibBuilder.loadTexts: ipOverSMDSIndex.setDescription("The value of this object identifies the\ninterface for which this entry contains management\ninformation. ")
ipOverSMDSAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 31, 4, 1, 1, 1, 2), IpAddress()).setMaxAccess("readonly")
if mibBuilder.loadTexts: ipOverSMDSAddress.setDescription("The IP address to which this entry's addressing\ninformation pertains.")
ipOverSMDSHA = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 31, 4, 1, 1, 1, 3), SMDSAddress()).setMaxAccess("readonly")
if mibBuilder.loadTexts: ipOverSMDSHA.setDescription("The SMDS Individual address of the IP station.")
ipOverSMDSLISGA = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 31, 4, 1, 1, 1, 4), SMDSAddress()).setMaxAccess("readonly")
if mibBuilder.loadTexts: ipOverSMDSLISGA.setDescription("The SMDS Group Address that has been configured\nto identify the SMDS Subscriber-Network Interfaces\n(SNIs) of all members of the Logical IP Subnetwork\n(LIS) connected to the network supporting SMDS.")
ipOverSMDSARPReq = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 31, 4, 1, 1, 1, 5), SMDSAddress()).setMaxAccess("readonly")
if mibBuilder.loadTexts: ipOverSMDSARPReq.setDescription("The SMDS address (individual or group) to which\nARP Requests are to be sent.")
smdsCarrierSelection = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 31, 5))
sipErrorLog = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 31, 6))
sipL3PDUErrorTable = MibTable((1, 3, 6, 1, 2, 1, 10, 31, 6, 1))
if mibBuilder.loadTexts: sipL3PDUErrorTable.setDescription("A table that contains the latest occurrence of\nthe following syntactical SIP L3PDU errors:\n\n- Destination Address Field Format Error,\n\nThe following pertains to the 60 least significant\nbits of the 64 bit address field.  The 60 bits\ncontained in the address subfield can be used to\nrepresent addresses up to 15 decimal digits.  Each\ndecimal digit shall be encoded into four bits\nusing Binary Coded Decimal (BCD), with the most\nsignificant digit occurring left-most.  If not all\n15 digits are required, then the remainder of this\nfield shall be padded on the right with bits set\nto one.  An error is considered to have occurred:\na).  if the first four bits of the address\nsubfield are not BCD, OR b).  if the first four\nbits of the address subfield are populated with\nthe country code value 0001, AND the 40 bits which\nfollow are not Binary Coded Decimal (BCD) encoded\nvalues of the 10 digit addresses, OR the remaining\n16 least significant bits are not populated with\n1's, OR c).  if the address subfield is not\ncorrect according to another numbering plan which\nis dependent upon the carrier assigning the\nnumbers and offering SMDS.\n\n- Source Address Field Format Error,\n\nThe description of this parameter is the same as\nthe description of the Destination Address Field\nFormat Error.\n- Invalid BAsize Field Value,\n\nAn error is considered to have occurred when the\nBAsize field of an SIP L3PDU contains a value less\nthat 32, greater than 9220 octets without the\nCRC32 field present, greater than 9224 octets with\nthe CRC32 field present, or not equal to a\nmultiple of 4 octets,\n\n- Invalid Header Extension Length Field Value,\n\nAn error is considered to have occurred when the\nHeader Extension Length field value is not equal\n3.\n\n- Invalid Header Extension - Element Length,\n\nAn error is considered to have occurred when the\nHeader Extension - Element Length is greater than\n12.\n\n- Invalid Header Extension - Version Element\nPosition, Length, or Value,\n\nAn error is considered to have occurred when a\nVersion element with Length=3, Type=0, and Value=1\ndoes not appear first within the Header Extension,\nor an element Type=0 appears somewhere other than\nwithin the first three octets in the Header\nExtension.\n\n- Invalid Header Extension - Carrier Selection\nElement Position, Length, Value or Format,\n\nAn error is considered to have occurred when a\nCarrier Selection element does not appear second\nwithin the Header Extension, if the Element Type\ndoes not equal 1, the Element Length does not\nequal 4, 6, or 8, the Element Value field is not\nfour BCD encoded decimal digits used in specifying\nthe Carrier Identification Code (CIC), or the\nidentified CIC code is invalid.\n\n- Header Extension PAD Error\n\nAn error is considered to have occurred when the\nHeader Extension PAD is 9 octets in length, or if\nthe Header Extension PAD is greater than zero\noctets in length and the Header Extension PAD does\nnot follow all Header Extension elements or does\nnot begin with at least one octet of all zeros.\n\n- BEtag Mismatch Error,\n\nAn error is considered to have occurred when the\nBeginning-End Tags in the SIP L3PDU header and\ntrailer are not equal.\n\n- BAsize Field not equal to Length Field Error,\n\nAn error is considered to have occurred when the\nvalue of the BAsize Field does not equal the value\nof the Length Field.\n\n- Incorrect Length Error, and\n\nAn error is considered to have occurred when the\nthe Length field value is not equal to the portion\nof the SIP L3PDU which extends from the\nDestination Address field up to and including the\nCRC32 field (if present) or up to and including\nthe PAD field (if the CRC32 field is not present).\nAs an optional check, an error is considered to\nhave occurred when the length of a partially\nreceived SIP L3PDU exceeds the BAsize value.\n\n- MRI Timeout Error.\n\nAn error is considered to have occurred when the\nelapsed time between receipt of BOM and\ncorresponding EOM exceeds the value of the MRI\n(Message Receive Interval) for a particular\ntransport signal format.\n\nAn entry is indexed by interface number and error\ntype, and contains Source Address, Destination\nAddress and a timestamp. All these errors are\ncounted in the sipL3Errors counter.  When\nsipL3PDUErrorTimeStamp is equal to zero, the\nSipL3PDUErrorEntry does not contain any valid\ninformation.")
sipL3PDUErrorEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 31, 6, 1, 1)).setIndexNames((0, "SIP-MIB", "sipL3PDUErrorIndex"), (0, "SIP-MIB", "sipL3PDUErrorType"))
if mibBuilder.loadTexts: sipL3PDUErrorEntry.setDescription("An entry in the service disagreement table.")
sipL3PDUErrorIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 31, 6, 1, 1, 1), IfIndex()).setMaxAccess("readonly")
if mibBuilder.loadTexts: sipL3PDUErrorIndex.setDescription("The value of this object identifies the\ninterface for which this entry contains management\ninformation.")
sipL3PDUErrorType = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 31, 6, 1, 1, 2), Integer().subtype(subtypeSpec=SingleValueConstraint(8,12,5,7,10,9,2,3,4,1,6,11,)).subtype(namedValues=NamedValues(("erroredDAFieldFormat", 1), ("baSizeFieldNotEqualToLengthField", 10), ("incorrectLength", 11), ("mriTimeout", 12), ("erroredSAFieldFormat", 2), ("invalidBAsizeFieldValue", 3), ("invalidHdrExtLength", 4), ("invalidHdrExtElementLength", 5), ("invalidHdrExtVersionElementPositionLenthOrValue", 6), ("invalidHdrExtCarSelectElementPositionLenghtValueOrFormat", 7), ("hePADError", 8), ("beTagMismatch", 9), ))).setMaxAccess("readonly")
if mibBuilder.loadTexts: sipL3PDUErrorType.setDescription("The type of error.")
sipL3PDUErrorSA = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 31, 6, 1, 1, 3), SMDSAddress()).setMaxAccess("readonly")
if mibBuilder.loadTexts: sipL3PDUErrorSA.setDescription("A rejected SMDS source address.")
sipL3PDUErrorDA = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 31, 6, 1, 1, 4), SMDSAddress()).setMaxAccess("readonly")
if mibBuilder.loadTexts: sipL3PDUErrorDA.setDescription("A rejected SMDS destination address.")
sipL3PDUErrorTimeStamp = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 31, 6, 1, 1, 5), TimeStamp()).setMaxAccess("readonly")
if mibBuilder.loadTexts: sipL3PDUErrorTimeStamp.setDescription("The timestamp for the service disagreement.  The\ntimestamp contains the value of sysUpTime at the\nlatest occurrence of this type of service\ndisagreement.  See textual description under\nsipL3PDUErrorTable for boundary conditions.")
sipMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 36)).setRevisions(("1994-03-31 18:18",))
if mibBuilder.loadTexts: sipMIB.setOrganization("IETF Interfaces Working Group")
if mibBuilder.loadTexts: sipMIB.setContactInfo("        Tracy Brown\nPostal: Bell Communications Research\n        331 Newman Springs Road\n        P.O. Box 7020\n        Red Bank, NJ  07701-7020\n        US\n\n   Tel: +1 908  758-2107\n   Fax: +1 908  758-4177\nE-mail: tacox@mail.bellcore.com\n\n        Kaj Tesink\nPostal: Bell Communications Research\n        331 Newman Springs Road\n        P.O. Box 7020\n        Red Bank, NJ  07701-7020\n        US\n\n   Tel: +1 908 758 5254\n   Fax: +1 908 758 4177\nE-mail: kaj@cc.bellcore.com.")
if mibBuilder.loadTexts: sipMIB.setDescription("The MIB module to describe\nSMDS interfaces objects.")
sipMIBObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 36, 1))
sipDxiTable = MibTable((1, 3, 6, 1, 2, 1, 36, 1, 1))
if mibBuilder.loadTexts: sipDxiTable.setDescription("The DXI table.")
sipDxiEntry = MibTableRow((1, 3, 6, 1, 2, 1, 36, 1, 1, 1)).setIndexNames((0, "IF-MIB", "ifIndex"))
if mibBuilder.loadTexts: sipDxiEntry.setDescription("An entry in the DXI table.")
sipDxiCrc = MibTableColumn((1, 3, 6, 1, 2, 1, 36, 1, 1, 1, 1), Integer().subtype(subtypeSpec=SingleValueConstraint(2,1,)).subtype(namedValues=NamedValues(("crc16", 1), ("crc32", 2), ))).setMaxAccess("readonly")
if mibBuilder.loadTexts: sipDxiCrc.setDescription("The value of this object indicates the type\nof Frame Checksum used by DXI.  Current\nchoices include CCITT CRC16 or CRC32.")
sipDxiOutDiscards = MibTableColumn((1, 3, 6, 1, 2, 1, 36, 1, 1, 1, 2), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: sipDxiOutDiscards.setDescription("The number of outbound frames discarded\nbecause of congestion.")
sipDxiInErrors = MibTableColumn((1, 3, 6, 1, 2, 1, 36, 1, 1, 1, 3), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: sipDxiInErrors.setDescription("The number of inbound frames discarded\nbecause of errors such as frame checksum\n(CRC) violations,\nnon-integral number of octets, address\nand control field violations, and frame\nsize errors.")
sipDxiInAborts = MibTableColumn((1, 3, 6, 1, 2, 1, 36, 1, 1, 1, 4), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: sipDxiInAborts.setDescription("The number of inbound frames discarded\nbecause of an abort bit sequence (1111111)\nreceived before closing flag.")
sipDxiInTestFrames = MibTableColumn((1, 3, 6, 1, 2, 1, 36, 1, 1, 1, 5), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: sipDxiInTestFrames.setDescription("The number of unerrored,\ninbound Test frames received\n(generally as part of Heart\nBeat Poll procedure).")
sipDxiOutTestFrames = MibTableColumn((1, 3, 6, 1, 2, 1, 36, 1, 1, 1, 6), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: sipDxiOutTestFrames.setDescription("The number of unerrored,\noutbound Test frames sent\n(generally as part of Heart\nBeat Poll procedure).")
sipDxiHbpNoAcks = MibTableColumn((1, 3, 6, 1, 2, 1, 36, 1, 1, 1, 7), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: sipDxiHbpNoAcks.setDescription("The number of Heart Beat\nPoll (HBP) No Ack timeouts.")
smdsConformance = MibIdentifier((1, 3, 6, 1, 2, 1, 36, 2))
smdsGroups = MibIdentifier((1, 3, 6, 1, 2, 1, 36, 2, 1))
smdsCompliances = MibIdentifier((1, 3, 6, 1, 2, 1, 36, 2, 2))

# Augmentions

# Groups

sipLevel3Stuff = ObjectGroup((1, 3, 6, 1, 2, 1, 36, 2, 1, 1)).setObjects(*(("SIP-MIB", "sipL3PDUErrorDA"), ("SIP-MIB", "sipL3PDUErrorSA"), ("SIP-MIB", "sipL3PDUErrorIndex"), ("SIP-MIB", "sipL3PDUErrorTimeStamp"), ("SIP-MIB", "sipL3Index"), ("SIP-MIB", "sipL3PDUErrorType"), ("SIP-MIB", "sipL3VersionSupport"), ) )
if mibBuilder.loadTexts: sipLevel3Stuff.setDescription("A collection of objects providing information\napplicable to all SMDS interfaces.")
sipLevel2Stuff = ObjectGroup((1, 3, 6, 1, 2, 1, 36, 2, 1, 2)).setObjects(*(("SIP-MIB", "sipL2Index"), ("SIP-MIB", "sipL2EomsMIDErrors"), ("SIP-MIB", "sipL2MidCurrentlyActiveErrors"), ("SIP-MIB", "sipL2BomOrSSMsMIDErrors"), ("SIP-MIB", "sipL2SequenceNumberErrors"), ("SIP-MIB", "sipL2PayloadLengthErrors"), ("SIP-MIB", "sipL2HcsOrCRCErrors"), ) )
if mibBuilder.loadTexts: sipLevel2Stuff.setDescription("A collection of objects providing information\nspecific to interfaces using the SIP Level 2.")
sipDS1PLCPStuff = ObjectGroup((1, 3, 6, 1, 2, 1, 36, 2, 1, 3)).setObjects(*(("SIP-MIB", "sipDS1PLCPSEFSs"), ("SIP-MIB", "sipDS1PLCPAlarmState"), ("SIP-MIB", "sipDS1PLCPIndex"), ("SIP-MIB", "sipDS1PLCPUASs"), ) )
if mibBuilder.loadTexts: sipDS1PLCPStuff.setDescription("A collection of objects providing information\nspecific to interfaces using the DS1 PLCP.")
sipDS3PLCPStuff = ObjectGroup((1, 3, 6, 1, 2, 1, 36, 2, 1, 4)).setObjects(*(("SIP-MIB", "sipDS3PLCPAlarmState"), ("SIP-MIB", "sipDS3PLCPSEFSs"), ("SIP-MIB", "sipDS3PLCPUASs"), ("SIP-MIB", "sipDS3PLCPIndex"), ) )
if mibBuilder.loadTexts: sipDS3PLCPStuff.setDescription("A collection of objects providing information\nspecific to interfaces using the DS3 PLCP.")
sipIPApplicationsStuff = ObjectGroup((1, 3, 6, 1, 2, 1, 36, 2, 1, 5)).setObjects(*(("SIP-MIB", "ipOverSMDSIndex"), ("SIP-MIB", "ipOverSMDSLISGA"), ("SIP-MIB", "ipOverSMDSAddress"), ("SIP-MIB", "ipOverSMDSARPReq"), ("SIP-MIB", "ipOverSMDSHA"), ) )
if mibBuilder.loadTexts: sipIPApplicationsStuff.setDescription("A collection of objects providing information\nfor running IP over SMDS.")
sipDxiStuff = ObjectGroup((1, 3, 6, 1, 2, 1, 36, 2, 1, 6)).setObjects(*(("SIP-MIB", "sipDxiInAborts"), ("SIP-MIB", "sipDxiHbpNoAcks"), ("SIP-MIB", "sipDxiOutDiscards"), ("SIP-MIB", "sipDxiCrc"), ("SIP-MIB", "sipDxiOutTestFrames"), ("SIP-MIB", "sipDxiInTestFrames"), ("SIP-MIB", "sipDxiInErrors"), ) )
if mibBuilder.loadTexts: sipDxiStuff.setDescription("A collection of objects providing information\nspecific to interfaces using the DXI protocol.")

# Compliances

smdsCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 36, 2, 2, 1)).setObjects(*(("SIP-MIB", "sipIPApplicationsStuff"), ("SIP-MIB", "sipDS3PLCPStuff"), ("SIP-MIB", "sipDS1PLCPStuff"), ("SIP-MIB", "sipLevel3Stuff"), ("SIP-MIB", "sipDxiStuff"), ("SIP-MIB", "sipLevel2Stuff"), ) )
if mibBuilder.loadTexts: smdsCompliance.setDescription("The compliance statement for SMDS interfaces.")

# Exports

# Module identity
mibBuilder.exportSymbols("SIP-MIB", PYSNMP_MODULE_ID=sipMIB)

# Types
mibBuilder.exportSymbols("SIP-MIB", IfIndex=IfIndex, SMDSAddress=SMDSAddress)

# Objects
mibBuilder.exportSymbols("SIP-MIB", sip=sip, sipL3Table=sipL3Table, sipL3Entry=sipL3Entry, sipL3Index=sipL3Index, sipL3ReceivedIndividualDAs=sipL3ReceivedIndividualDAs, sipL3ReceivedGAs=sipL3ReceivedGAs, sipL3UnrecognizedIndividualDAs=sipL3UnrecognizedIndividualDAs, sipL3UnrecognizedGAs=sipL3UnrecognizedGAs, sipL3SentIndividualDAs=sipL3SentIndividualDAs, sipL3SentGAs=sipL3SentGAs, sipL3Errors=sipL3Errors, sipL3InvalidSMDSAddressTypes=sipL3InvalidSMDSAddressTypes, sipL3VersionSupport=sipL3VersionSupport, sipL2Table=sipL2Table, sipL2Entry=sipL2Entry, sipL2Index=sipL2Index, sipL2ReceivedCounts=sipL2ReceivedCounts, sipL2SentCounts=sipL2SentCounts, sipL2HcsOrCRCErrors=sipL2HcsOrCRCErrors, sipL2PayloadLengthErrors=sipL2PayloadLengthErrors, sipL2SequenceNumberErrors=sipL2SequenceNumberErrors, sipL2MidCurrentlyActiveErrors=sipL2MidCurrentlyActiveErrors, sipL2BomOrSSMsMIDErrors=sipL2BomOrSSMsMIDErrors, sipL2EomsMIDErrors=sipL2EomsMIDErrors, sipPLCP=sipPLCP, sipDS1PLCPTable=sipDS1PLCPTable, sipDS1PLCPEntry=sipDS1PLCPEntry, sipDS1PLCPIndex=sipDS1PLCPIndex, sipDS1PLCPSEFSs=sipDS1PLCPSEFSs, sipDS1PLCPAlarmState=sipDS1PLCPAlarmState, sipDS1PLCPUASs=sipDS1PLCPUASs, sipDS3PLCPTable=sipDS3PLCPTable, sipDS3PLCPEntry=sipDS3PLCPEntry, sipDS3PLCPIndex=sipDS3PLCPIndex, sipDS3PLCPSEFSs=sipDS3PLCPSEFSs, sipDS3PLCPAlarmState=sipDS3PLCPAlarmState, sipDS3PLCPUASs=sipDS3PLCPUASs, smdsApplications=smdsApplications, ipOverSMDS=ipOverSMDS, ipOverSMDSTable=ipOverSMDSTable, ipOverSMDSEntry=ipOverSMDSEntry, ipOverSMDSIndex=ipOverSMDSIndex, ipOverSMDSAddress=ipOverSMDSAddress, ipOverSMDSHA=ipOverSMDSHA, ipOverSMDSLISGA=ipOverSMDSLISGA, ipOverSMDSARPReq=ipOverSMDSARPReq, smdsCarrierSelection=smdsCarrierSelection, sipErrorLog=sipErrorLog, sipL3PDUErrorTable=sipL3PDUErrorTable, sipL3PDUErrorEntry=sipL3PDUErrorEntry, sipL3PDUErrorIndex=sipL3PDUErrorIndex, sipL3PDUErrorType=sipL3PDUErrorType, sipL3PDUErrorSA=sipL3PDUErrorSA, sipL3PDUErrorDA=sipL3PDUErrorDA, sipL3PDUErrorTimeStamp=sipL3PDUErrorTimeStamp, sipMIB=sipMIB, sipMIBObjects=sipMIBObjects, sipDxiTable=sipDxiTable, sipDxiEntry=sipDxiEntry, sipDxiCrc=sipDxiCrc, sipDxiOutDiscards=sipDxiOutDiscards, sipDxiInErrors=sipDxiInErrors, sipDxiInAborts=sipDxiInAborts, sipDxiInTestFrames=sipDxiInTestFrames, sipDxiOutTestFrames=sipDxiOutTestFrames, sipDxiHbpNoAcks=sipDxiHbpNoAcks, smdsConformance=smdsConformance, smdsGroups=smdsGroups, smdsCompliances=smdsCompliances)

# Groups
mibBuilder.exportSymbols("SIP-MIB", sipLevel3Stuff=sipLevel3Stuff, sipLevel2Stuff=sipLevel2Stuff, sipDS1PLCPStuff=sipDS1PLCPStuff, sipDS3PLCPStuff=sipDS3PLCPStuff, sipIPApplicationsStuff=sipIPApplicationsStuff, sipDxiStuff=sipDxiStuff)

# Compliances
mibBuilder.exportSymbols("SIP-MIB", smdsCompliance=smdsCompliance)
