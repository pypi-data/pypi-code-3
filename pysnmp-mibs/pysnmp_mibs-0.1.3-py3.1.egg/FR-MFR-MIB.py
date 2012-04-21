# PySNMP SMI module. Autogenerated from smidump -f python FR-MFR-MIB
# by libsmi2pysnmp-0.1.3 at Mon Apr  2 20:39:00 2012,
# Python version sys.version_info(major=2, minor=7, micro=2, releaselevel='final', serial=0)

# Imports

( Integer, ObjectIdentifier, OctetString, ) = mibBuilder.importSymbols("ASN1", "Integer", "ObjectIdentifier", "OctetString")
( NamedValues, ) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
( ConstraintsIntersection, ConstraintsUnion, SingleValueConstraint, ValueRangeConstraint, ValueSizeConstraint, ) = mibBuilder.importSymbols("ASN1-REFINEMENT", "ConstraintsIntersection", "ConstraintsUnion", "SingleValueConstraint", "ValueRangeConstraint", "ValueSizeConstraint")
( InterfaceIndex, ifIndex, ) = mibBuilder.importSymbols("IF-MIB", "InterfaceIndex", "ifIndex")
( SnmpAdminString, ) = mibBuilder.importSymbols("SNMP-FRAMEWORK-MIB", "SnmpAdminString")
( ModuleCompliance, NotificationGroup, ObjectGroup, ) = mibBuilder.importSymbols("SNMPv2-CONF", "ModuleCompliance", "NotificationGroup", "ObjectGroup")
( Bits, Counter32, Integer32, Integer32, ModuleIdentity, MibIdentifier, NotificationType, MibScalar, MibTable, MibTableRow, MibTableColumn, TimeTicks, transmission, ) = mibBuilder.importSymbols("SNMPv2-SMI", "Bits", "Counter32", "Integer32", "Integer32", "ModuleIdentity", "MibIdentifier", "NotificationType", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "TimeTicks", "transmission")
( RowStatus, TextualConvention, TestAndIncr, ) = mibBuilder.importSymbols("SNMPv2-TC", "RowStatus", "TextualConvention", "TestAndIncr")

# Types

class MfrBundleLinkState(Integer):
    subtypeSpec = Integer.subtypeSpec+SingleValueConstraint(8,7,3,5,4,1,6,2,)
    namedValues = NamedValues(("mfrBundleLinkStateAddSent", 1), ("mfrBundleLinkStateAddRx", 2), ("mfrBundleLinkStateAddAckRx", 3), ("mfrBundleLinkStateUp", 4), ("mfrBundleLinkStateIdlePending", 5), ("mfrBundleLinkStateIdle", 6), ("mfrBundleLinkStateDown", 7), ("mfrBundleLinkStateDownIdle", 8), )
    

# Objects

mfrMib = ModuleIdentity((1, 3, 6, 1, 2, 1, 10, 47)).setRevisions(("2000-11-30 00:00",))
if mibBuilder.loadTexts: mfrMib.setOrganization("IETF Frame Relay Service MIB (frnetmib)\nWorking Group")
if mibBuilder.loadTexts: mfrMib.setContactInfo("WG Charter:\nhttp://www.ietf.org/html.charters/frnetmib-charter.html\nWG-email:      frnetmib@sunroof.eng.sun.com\nSubscribe:     frnetmib-request@sunroof.eng.sun.com\nEmail Archive: ftp://ftp.ietf.org/ietf-mail-archive/frnetmib\n\nChair:      Andy Malis\n        Vivace Networks\nEmail:      Andy.Malis@vivacenetworks.com\n\nWG editor:  Prayson Pate\n        Overture Networks\nEmail:      prayson.pate@overturenetworks.com\n\nCo-author:  Bob Lynch\n        Overture Networks\n\n\nEMail:      bob.lynch@overturenetworks.com\n\nCo-author:  Kenneth Rehbehn\n        Megisto Systems, Inc.\nEMail:      krehbehn@megisto.com")
if mibBuilder.loadTexts: mfrMib.setDescription("This is the MIB used to control and monitor the multilink\nframe relay (MFR) function described in FRF.16.")
mfrMibScalarObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 47, 1))
mfrBundleMaxNumBundles = MibScalar((1, 3, 6, 1, 2, 1, 10, 47, 1, 1), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: mfrBundleMaxNumBundles.setDescription("This object is used to inform the manager of the\nmaximum number of bundles supported by this device.")
mfrBundleNextIndex = MibScalar((1, 3, 6, 1, 2, 1, 10, 47, 1, 2), TestAndIncr()).setMaxAccess("readwrite")
if mibBuilder.loadTexts: mfrBundleNextIndex.setDescription("This object is used to assist the manager in\nselecting a value for mfrBundleIndex during row creation\nin the mfrBundleTable.  It can also be used to avoid race\nconditions with multiple managers trying to create\nrows in the table (see RFC 2494 [RFC2494] for one such\nalogrithm).")
mfrMibBundleObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 47, 2))
mfrBundleTable = MibTable((1, 3, 6, 1, 2, 1, 10, 47, 2, 3))
if mibBuilder.loadTexts: mfrBundleTable.setDescription("The bundle configuration and status table.  There\nis a one-to-one correspondence between a bundle\nand an interface represented in the ifTable.\n\nThe following objects of the ifTable have specific\nmeaning for an MFR bundle:\n   ifAdminStatus  - the bundle admin status\n   ifOperStatus   - the bundle operational status\n   ifSpeed        - the current bandwidth of the bundle\n   ifInUcastPkts  - the number of frames received\n                    on the bundle\n   ifOutUcastPkts - the number of frames transmitted\n                    on the bundle\n   ifInErrors     - frame (not fragment) errors\n   ifOutErrors    - frame (not fragment) errors\n   ")
mfrBundleEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 47, 2, 3, 1)).setIndexNames((0, "FR-MFR-MIB", "mfrBundleIndex"))
if mibBuilder.loadTexts: mfrBundleEntry.setDescription("An entry in the bundle table.")
mfrBundleIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 47, 2, 3, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647))).setMaxAccess("noaccess")
if mibBuilder.loadTexts: mfrBundleIndex.setDescription("The index into the table.  While this corresponds\nto an entry in the ifTable, the value of mfrBundleIndex\nneed not match that of the ifIndex in the ifTable.\nA manager can use mfrBundleNextIndex to select a unique\nmfrBundleIndex for creating a new row.")
mfrBundleIfIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 47, 2, 3, 1, 2), InterfaceIndex()).setMaxAccess("readonly")
if mibBuilder.loadTexts: mfrBundleIfIndex.setDescription("The value must match an entry in the interface\ntable whose ifType must be set to frf16MfrBundle(163).\n\nFor example: if the value of mfrBundleIfIndex is 10,\nthen a corresponding entry should be present in\n\n\nthe ifTable with an index of 10 and an ifType of 163.")
mfrBundleRowStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 47, 2, 3, 1, 3), RowStatus()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mfrBundleRowStatus.setDescription("The mfrBundleRowStatus object allows create, change,\nand delete operations on bundle entries.")
mfrBundleNearEndName = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 47, 2, 3, 1, 4), SnmpAdminString()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mfrBundleNearEndName.setDescription("The configured name of the bundle.")
mfrBundleFragmentation = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 47, 2, 3, 1, 5), Integer().subtype(subtypeSpec=SingleValueConstraint(1,2,)).subtype(namedValues=NamedValues(("enable", 1), ("disable", 2), )).clone(2)).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mfrBundleFragmentation.setDescription("Controls whether the bundle performs/accepts\nfragmentation and re-assembly.  The possible\nvalues are:\n\nenable(1) - Bundle links will fragment frames\n\ndisable(2) - Bundle links will not fragment\n            frames.")
mfrBundleMaxFragSize = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 47, 2, 3, 1, 6), Integer32().subtype(subtypeSpec=ValueRangeConstraint(-1, 8184)).clone(-1)).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mfrBundleMaxFragSize.setDescription("The maximum fragment size supported.  Note that this\n\n\nis only valid if mfrBundleFragmentation is set to enable(1).\n\nZero is not a valid fragment size.\n\nA bundle that does not support fragmentation must return\nthis object with a value of -1.")
mfrBundleTimerHello = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 47, 2, 3, 1, 7), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 180)).clone(10)).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mfrBundleTimerHello.setDescription("The configured MFR Hello Timer value.")
mfrBundleTimerAck = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 47, 2, 3, 1, 8), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 10)).clone(4)).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mfrBundleTimerAck.setDescription("The configured MFR T_ACK value.")
mfrBundleCountMaxRetry = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 47, 2, 3, 1, 9), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 5)).clone(2)).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mfrBundleCountMaxRetry.setDescription("The MFR N_MAX_RETRY value.")
mfrBundleActivationClass = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 47, 2, 3, 1, 10), Integer().subtype(subtypeSpec=SingleValueConstraint(4,3,1,2,)).subtype(namedValues=NamedValues(("mfrBundleActivationClassA", 1), ("mfrBundleActivationClassB", 2), ("mfrBundleActivationClassC", 3), ("mfrBundleActivationClassD", 4), )).clone(1)).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mfrBundleActivationClass.setDescription("Controls the conditions under which the bundle is activated.\nThe following settings are available:\n\n   mfrBundleActivationClassA(1) - at least one must link up\n   mfrBundleActivationClassB(2) - all links must be up\n   mfrBundleActivationClassC(3) - a certain number must be\n                                  up.  Refer to\n                                  mfrBundleThreshold for\n                                  the required number.\n   mfrBundleActivationClassD(4) - custom (implementation\n                                  specific).")
mfrBundleThreshold = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 47, 2, 3, 1, 11), Integer32().subtype(subtypeSpec=ValueRangeConstraint(-1, 2147483647)).clone(-1)).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mfrBundleThreshold.setDescription("Specifies the number of links that must be in operational\n'up' state before the bundle will transition to an\noperational up/active state.  If the number of\noperational 'up' links falls below this value,\nthen the bundle will transition to an inactive\nstate.\n\nNote - this is only valid when mfrBundleActivationClass\nis set to mfrBundleActivationClassC or, depending upon the\nimplementation, to mfrBundleActivationClassD.  A bundle that\nis not set to one of these must return this object with a\nvalue of -1.")
mfrBundleMaxDiffDelay = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 47, 2, 3, 1, 12), Integer32().subtype(subtypeSpec=ValueRangeConstraint(-1, 2147483647)).clone(-1)).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mfrBundleMaxDiffDelay.setDescription("The maximum delay difference between the bundle\nlinks.\n\n\nA value of -1 indicates that this object does not contain\na valid value")
mfrBundleSeqNumSize = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 47, 2, 3, 1, 13), Integer().subtype(subtypeSpec=SingleValueConstraint(2,1,)).subtype(namedValues=NamedValues(("seqNumSize12bit", 1), ("seqNumSize24bit", 2), )).clone(1)).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mfrBundleSeqNumSize.setDescription("Controls whether the standard FRF.12 12-bit\nsequence number is used or the optional 24-bit\nsequence number.")
mfrBundleMaxBundleLinks = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 47, 2, 3, 1, 14), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647))).setMaxAccess("readonly")
if mibBuilder.loadTexts: mfrBundleMaxBundleLinks.setDescription("The maximum number of bundle links supported for\nthis bundle.")
mfrBundleLinksConfigured = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 47, 2, 3, 1, 15), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647))).setMaxAccess("readonly")
if mibBuilder.loadTexts: mfrBundleLinksConfigured.setDescription("The number of links configured for the bundle.")
mfrBundleLinksActive = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 47, 2, 3, 1, 16), Integer32().subtype(subtypeSpec=ValueRangeConstraint(-1, 2147483647))).setMaxAccess("readonly")
if mibBuilder.loadTexts: mfrBundleLinksActive.setDescription("The number of links that are active.")
mfrBundleBandwidth = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 47, 2, 3, 1, 17), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: mfrBundleBandwidth.setDescription("The amount of available bandwidth on the bundle")
mfrBundleFarEndName = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 47, 2, 3, 1, 18), SnmpAdminString()).setMaxAccess("readonly")
if mibBuilder.loadTexts: mfrBundleFarEndName.setDescription("Name of the bundle received from the far end.")
mfrBundleResequencingErrors = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 47, 2, 3, 1, 19), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: mfrBundleResequencingErrors.setDescription("A count of the number of resequencing errors.  Each event\nmay correspond to multiple lost frames.  Example:\nSay sequence number 56, 59 and 60 is received for DLCI 100.\nIt is decided by some means that sequence 57 and 58 is lost.\nThis counter should then be incremented by ONE, even though\ntwo frames were lost.")
mfrBundleIfIndexMappingTable = MibTable((1, 3, 6, 1, 2, 1, 10, 47, 2, 4))
if mibBuilder.loadTexts: mfrBundleIfIndexMappingTable.setDescription("A table mapping the values of ifIndex to the\nmfrBundleIndex.  This is required in order to find\nthe mfrBundleIndex given an ifIndex.  The mapping of\nmfrBundleIndex to ifIndex is provided by the\nmfrBundleIfIndex entry in the mfrBundleTable.")
mfrBundleIfIndexMappingEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 47, 2, 4, 1)).setIndexNames((0, "IF-MIB", "ifIndex"))
if mibBuilder.loadTexts: mfrBundleIfIndexMappingEntry.setDescription("Each row describes one ifIndex to mfrBundleIndex mapping.")
mfrBundleIfIndexMappingIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 47, 2, 4, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647))).setMaxAccess("readonly")
if mibBuilder.loadTexts: mfrBundleIfIndexMappingIndex.setDescription("The mfrBundleIndex of the given ifIndex.")
mfrMibBundleLinkObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 47, 3))
mfrBundleLinkTable = MibTable((1, 3, 6, 1, 2, 1, 10, 47, 3, 1))
if mibBuilder.loadTexts: mfrBundleLinkTable.setDescription("The bundle link configuration and status table.  There\nis a one-to-one correspondence between a bundle link\nand a physical interface represented in the ifTable.  The\nifIndex of the physical interface is used to index the\nbundle link table, and to create rows.\n\nThe following objects of the ifTable have specific\nmeaning for an MFR bundle link:\n\n   ifAdminStatus  - the bundle link admin status\n   ifOperStatus   - the bundle link operational\n                    status\n\n\n   ifSpeed        - the bandwidth of the bundle\n                    link interface\n   ifInUcastPkts  - the number of frames received\n                    on the bundle link\n   ifOutUcastPkts - the number of frames transmitted\n                    on the bundle link\n   ifInErrors     - frame and fragment errors\n   ifOutErrors    - frame and fragment errors")
mfrBundleLinkEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 47, 3, 1, 1)).setIndexNames((0, "IF-MIB", "ifIndex"))
if mibBuilder.loadTexts: mfrBundleLinkEntry.setDescription("An entry in the bundle link table.")
mfrBundleLinkRowStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 47, 3, 1, 1, 1), RowStatus()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mfrBundleLinkRowStatus.setDescription("The mfrBundleLinkRowStatus object allows create, change,\nand delete operations on mfrBundleLink entries.\n\nThe create operation must fail if no physical interface\nis associated with the bundle link.")
mfrBundleLinkConfigBundleIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 47, 3, 1, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647))).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mfrBundleLinkConfigBundleIndex.setDescription("The mfrBundleLinkConfigBundleIndex object allows\nthe manager to control the bundle to which the bundle\nlink is assigned.  If no value were in this field, then\nthe bundle would remain in NOT_READY rowStatus and be\nunable to go to active.  With an appropriate mfrBundleIndex\nin this field, then we could put the mfrBundleLink row in\nNOT_IN_SERVICE or ACTIVE rowStatus.")
mfrBundleLinkNearEndName = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 47, 3, 1, 1, 3), SnmpAdminString()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mfrBundleLinkNearEndName.setDescription("The configured bundle link name that is sent to the far end.")
mfrBundleLinkState = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 47, 3, 1, 1, 4), MfrBundleLinkState()).setMaxAccess("readonly")
if mibBuilder.loadTexts: mfrBundleLinkState.setDescription("Current bundle link state as defined by the MFR protocol\ndescribed in Annex A of FRF.16.")
mfrBundleLinkFarEndName = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 47, 3, 1, 1, 5), SnmpAdminString()).setMaxAccess("readonly")
if mibBuilder.loadTexts: mfrBundleLinkFarEndName.setDescription("Name of bundle link received from far end.")
mfrBundleLinkFarEndBundleName = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 47, 3, 1, 1, 6), SnmpAdminString()).setMaxAccess("readonly")
if mibBuilder.loadTexts: mfrBundleLinkFarEndBundleName.setDescription("Name of far end bundle for this link received from far end.")
mfrBundleLinkDelay = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 47, 3, 1, 1, 7), Integer32().subtype(subtypeSpec=ValueRangeConstraint(-1, 2147483647))).setMaxAccess("readonly")
if mibBuilder.loadTexts: mfrBundleLinkDelay.setDescription("Current round-trip delay for this bundle link.  The\nvalue -1 is returned when an implementation does not\nsupport measurement of the bundle link delay.")
mfrBundleLinkFramesControlTx = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 47, 3, 1, 1, 8), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: mfrBundleLinkFramesControlTx.setDescription("Number of MFR control frames sent.")
mfrBundleLinkFramesControlRx = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 47, 3, 1, 1, 9), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: mfrBundleLinkFramesControlRx.setDescription("Number of valid MFR control frames received.")
mfrBundleLinkFramesControlInvalid = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 47, 3, 1, 1, 10), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: mfrBundleLinkFramesControlInvalid.setDescription("The number of invalid MFR control frames received.")
mfrBundleLinkTimerExpiredCount = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 47, 3, 1, 1, 11), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: mfrBundleLinkTimerExpiredCount.setDescription("Number of times the T_HELLO or T_ACK timers expired.")
mfrBundleLinkLoopbackSuspected = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 47, 3, 1, 1, 12), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: mfrBundleLinkLoopbackSuspected.setDescription("The number of times a loopback has been suspected\n(based upon the use of magic numbers).")
mfrBundleLinkUnexpectedSequence = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 47, 3, 1, 1, 13), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: mfrBundleLinkUnexpectedSequence.setDescription("The number of data MFR frames discarded because the sequence\nnumber of the frame for a DLCI was less than (delayed frame)\nor equal to (duplicate frame) the one expected for that DLCI.\n\nExample:\nSay frames with sequence numbers 56, 58, 59 is received for\nDLCI 100.  While waiting for sequence number 57 another frame\nwith sequence number 58 arrives.  Frame 58 is discarded and\nthe counter is incremented.")
mfrBundleLinkMismatch = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 47, 3, 1, 1, 14), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: mfrBundleLinkMismatch.setDescription("The number of times that the unit has been notified by the\nremote peer that the bundle name is inconsistent with other\nbundle links attached to the far-end bundle.")
mfrMibTraps = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 47, 4))
mfrMibTrapsPrefix = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 47, 4, 0))
mfrMibConformance = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 47, 5))
mfrMibGroups = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 47, 5, 1))
mfrMibCompliances = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 47, 5, 2))

# Augmentions

# Notifications

mfrMibTrapBundleLinkMismatch = NotificationType((1, 3, 6, 1, 2, 1, 10, 47, 4, 0, 1)).setObjects(*(("FR-MFR-MIB", "mfrBundleFarEndName"), ("FR-MFR-MIB", "mfrBundleLinkNearEndName"), ("FR-MFR-MIB", "mfrBundleLinkFarEndBundleName"), ("FR-MFR-MIB", "mfrBundleLinkFarEndName"), ("FR-MFR-MIB", "mfrBundleNearEndName"), ) )
if mibBuilder.loadTexts: mfrMibTrapBundleLinkMismatch.setDescription("This trap indicates that a bundle link mismatch has\nbeen detected.  The following objects are reported:\n\nmfrBundleNearEndName:    configured name of near end bundle\n\nmfrBundleFarEndName:     previously reported name of\n                      far end bundle\n\nmfrBundleLinkNearEndName: configured name of near end bundle\n\nmfrBundleLinkFarEndName: reported name of far end bundle\n\nmfrBundleLinkFarEndBundleName: currently reported name of\n                      far end bundle\n\nNote: that the configured items may have been configured\n      automatically.\n\nNote: The mfrBundleLinkMismatch counter is incremented when\n      the trap is sent.")

# Groups

mfrMibBundleGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 47, 5, 1, 1)).setObjects(*(("FR-MFR-MIB", "mfrBundleBandwidth"), ("FR-MFR-MIB", "mfrBundleIfIndexMappingIndex"), ("FR-MFR-MIB", "mfrBundleThreshold"), ("FR-MFR-MIB", "mfrBundleFarEndName"), ("FR-MFR-MIB", "mfrBundleSeqNumSize"), ("FR-MFR-MIB", "mfrBundleRowStatus"), ("FR-MFR-MIB", "mfrBundleCountMaxRetry"), ("FR-MFR-MIB", "mfrBundleResequencingErrors"), ("FR-MFR-MIB", "mfrBundleLinksActive"), ("FR-MFR-MIB", "mfrBundleNearEndName"), ("FR-MFR-MIB", "mfrBundleMaxDiffDelay"), ("FR-MFR-MIB", "mfrBundleTimerAck"), ("FR-MFR-MIB", "mfrBundleTimerHello"), ("FR-MFR-MIB", "mfrBundleMaxNumBundles"), ("FR-MFR-MIB", "mfrBundleMaxFragSize"), ("FR-MFR-MIB", "mfrBundleActivationClass"), ("FR-MFR-MIB", "mfrBundleNextIndex"), ("FR-MFR-MIB", "mfrBundleLinksConfigured"), ("FR-MFR-MIB", "mfrBundleMaxBundleLinks"), ("FR-MFR-MIB", "mfrBundleIfIndex"), ("FR-MFR-MIB", "mfrBundleFragmentation"), ) )
if mibBuilder.loadTexts: mfrMibBundleGroup.setDescription("Group of objects describing bundles.")
mfrMibBundleLinkGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 47, 5, 1, 2)).setObjects(*(("FR-MFR-MIB", "mfrBundleLinkUnexpectedSequence"), ("FR-MFR-MIB", "mfrBundleLinkFarEndName"), ("FR-MFR-MIB", "mfrBundleLinkTimerExpiredCount"), ("FR-MFR-MIB", "mfrBundleLinkLoopbackSuspected"), ("FR-MFR-MIB", "mfrBundleLinkRowStatus"), ("FR-MFR-MIB", "mfrBundleLinkFramesControlInvalid"), ("FR-MFR-MIB", "mfrBundleLinkNearEndName"), ("FR-MFR-MIB", "mfrBundleLinkFarEndBundleName"), ("FR-MFR-MIB", "mfrBundleLinkDelay"), ("FR-MFR-MIB", "mfrBundleLinkFramesControlTx"), ("FR-MFR-MIB", "mfrBundleLinkMismatch"), ("FR-MFR-MIB", "mfrBundleLinkConfigBundleIndex"), ("FR-MFR-MIB", "mfrBundleLinkFramesControlRx"), ("FR-MFR-MIB", "mfrBundleLinkState"), ) )
if mibBuilder.loadTexts: mfrMibBundleLinkGroup.setDescription("Group of objects describing bundle links.")
mfrMibTrapGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 47, 5, 1, 3)).setObjects(*(("FR-MFR-MIB", "mfrMibTrapBundleLinkMismatch"), ) )
if mibBuilder.loadTexts: mfrMibTrapGroup.setDescription("Group of objects describing notifications (traps).")

# Compliances

mfrMibCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 10, 47, 5, 2, 1)).setObjects(*(("FR-MFR-MIB", "mfrMibBundleGroup"), ("FR-MFR-MIB", "mfrMibTrapGroup"), ("FR-MFR-MIB", "mfrMibBundleLinkGroup"), ) )
if mibBuilder.loadTexts: mfrMibCompliance.setDescription("The compliance statement for equipment that implements\nthe FRF16 MIB.  All of the current groups are mandatory,\nbut a number of objects may be read-only if the\nimplementation does not allow configuration.")

# Exports

# Module identity
mibBuilder.exportSymbols("FR-MFR-MIB", PYSNMP_MODULE_ID=mfrMib)

# Types
mibBuilder.exportSymbols("FR-MFR-MIB", MfrBundleLinkState=MfrBundleLinkState)

# Objects
mibBuilder.exportSymbols("FR-MFR-MIB", mfrMib=mfrMib, mfrMibScalarObjects=mfrMibScalarObjects, mfrBundleMaxNumBundles=mfrBundleMaxNumBundles, mfrBundleNextIndex=mfrBundleNextIndex, mfrMibBundleObjects=mfrMibBundleObjects, mfrBundleTable=mfrBundleTable, mfrBundleEntry=mfrBundleEntry, mfrBundleIndex=mfrBundleIndex, mfrBundleIfIndex=mfrBundleIfIndex, mfrBundleRowStatus=mfrBundleRowStatus, mfrBundleNearEndName=mfrBundleNearEndName, mfrBundleFragmentation=mfrBundleFragmentation, mfrBundleMaxFragSize=mfrBundleMaxFragSize, mfrBundleTimerHello=mfrBundleTimerHello, mfrBundleTimerAck=mfrBundleTimerAck, mfrBundleCountMaxRetry=mfrBundleCountMaxRetry, mfrBundleActivationClass=mfrBundleActivationClass, mfrBundleThreshold=mfrBundleThreshold, mfrBundleMaxDiffDelay=mfrBundleMaxDiffDelay, mfrBundleSeqNumSize=mfrBundleSeqNumSize, mfrBundleMaxBundleLinks=mfrBundleMaxBundleLinks, mfrBundleLinksConfigured=mfrBundleLinksConfigured, mfrBundleLinksActive=mfrBundleLinksActive, mfrBundleBandwidth=mfrBundleBandwidth, mfrBundleFarEndName=mfrBundleFarEndName, mfrBundleResequencingErrors=mfrBundleResequencingErrors, mfrBundleIfIndexMappingTable=mfrBundleIfIndexMappingTable, mfrBundleIfIndexMappingEntry=mfrBundleIfIndexMappingEntry, mfrBundleIfIndexMappingIndex=mfrBundleIfIndexMappingIndex, mfrMibBundleLinkObjects=mfrMibBundleLinkObjects, mfrBundleLinkTable=mfrBundleLinkTable, mfrBundleLinkEntry=mfrBundleLinkEntry, mfrBundleLinkRowStatus=mfrBundleLinkRowStatus, mfrBundleLinkConfigBundleIndex=mfrBundleLinkConfigBundleIndex, mfrBundleLinkNearEndName=mfrBundleLinkNearEndName, mfrBundleLinkState=mfrBundleLinkState, mfrBundleLinkFarEndName=mfrBundleLinkFarEndName, mfrBundleLinkFarEndBundleName=mfrBundleLinkFarEndBundleName, mfrBundleLinkDelay=mfrBundleLinkDelay, mfrBundleLinkFramesControlTx=mfrBundleLinkFramesControlTx, mfrBundleLinkFramesControlRx=mfrBundleLinkFramesControlRx, mfrBundleLinkFramesControlInvalid=mfrBundleLinkFramesControlInvalid, mfrBundleLinkTimerExpiredCount=mfrBundleLinkTimerExpiredCount, mfrBundleLinkLoopbackSuspected=mfrBundleLinkLoopbackSuspected, mfrBundleLinkUnexpectedSequence=mfrBundleLinkUnexpectedSequence, mfrBundleLinkMismatch=mfrBundleLinkMismatch, mfrMibTraps=mfrMibTraps, mfrMibTrapsPrefix=mfrMibTrapsPrefix, mfrMibConformance=mfrMibConformance, mfrMibGroups=mfrMibGroups, mfrMibCompliances=mfrMibCompliances)

# Notifications
mibBuilder.exportSymbols("FR-MFR-MIB", mfrMibTrapBundleLinkMismatch=mfrMibTrapBundleLinkMismatch)

# Groups
mibBuilder.exportSymbols("FR-MFR-MIB", mfrMibBundleGroup=mfrMibBundleGroup, mfrMibBundleLinkGroup=mfrMibBundleLinkGroup, mfrMibTrapGroup=mfrMibTrapGroup)

# Compliances
mibBuilder.exportSymbols("FR-MFR-MIB", mfrMibCompliance=mfrMibCompliance)
