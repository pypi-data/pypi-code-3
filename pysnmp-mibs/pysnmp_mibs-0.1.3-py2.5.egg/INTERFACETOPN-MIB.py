# PySNMP SMI module. Autogenerated from smidump -f python INTERFACETOPN-MIB
# by libsmi2pysnmp-0.1.3 at Mon Apr  2 20:39:10 2012,
# Python version sys.version_info(major=2, minor=7, micro=2, releaselevel='final', serial=0)

# Imports

( Integer, ObjectIdentifier, OctetString, ) = mibBuilder.importSymbols("ASN1", "Integer", "ObjectIdentifier", "OctetString")
( NamedValues, ) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
( ConstraintsIntersection, ConstraintsUnion, SingleValueConstraint, ValueRangeConstraint, ValueSizeConstraint, ) = mibBuilder.importSymbols("ASN1-REFINEMENT", "ConstraintsIntersection", "ConstraintsUnion", "SingleValueConstraint", "ValueRangeConstraint", "ValueSizeConstraint")
( CounterBasedGauge64, ) = mibBuilder.importSymbols("HCNUM-TC", "CounterBasedGauge64")
( OwnerString, rmon, ) = mibBuilder.importSymbols("RMON-MIB", "OwnerString", "rmon")
( ModuleCompliance, ObjectGroup, ) = mibBuilder.importSymbols("SNMPv2-CONF", "ModuleCompliance", "ObjectGroup")
( Bits, Gauge32, Integer32, Integer32, ModuleIdentity, MibIdentifier, MibScalar, MibTable, MibTableRow, MibTableColumn, TimeTicks, ) = mibBuilder.importSymbols("SNMPv2-SMI", "Bits", "Gauge32", "Integer32", "Integer32", "ModuleIdentity", "MibIdentifier", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "TimeTicks")
( RowStatus, TimeStamp, TruthValue, ) = mibBuilder.importSymbols("SNMPv2-TC", "RowStatus", "TimeStamp", "TruthValue")

# Objects

interfaceTopNMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 16, 27)).setRevisions(("2001-03-27 00:00",))
if mibBuilder.loadTexts: interfaceTopNMIB.setOrganization("IETF RMON MIB Working Group")
if mibBuilder.loadTexts: interfaceTopNMIB.setContactInfo("\n\nDan Romascanu\nAvaya Inc.\nTel:  +972-3-645-8414\nEmail: dromasca@avaya.com")
if mibBuilder.loadTexts: interfaceTopNMIB.setDescription("The MIB module for sorting device interfaces for RMON and\nSMON monitoring in a multiple device implementation.")
interfaceTopNObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 16, 27, 1))
interfaceTopNCaps = MibScalar((1, 3, 6, 1, 2, 1, 16, 27, 1, 1), Bits().subtype(namedValues=NamedValues(("ifInOctets", 0), ("ifInUcastPkts", 1), ("ifOutErrors", 10), ("ifInMulticastPkts", 11), ("ifInBroadcastPkts", 12), ("ifOutMulticastPkts", 13), ("ifOutBroadcastPkts", 14), ("ifHCInOctets", 15), ("ifHCInUcastPkts", 16), ("ifHCInMulticastPkts", 17), ("ifHCInBroadcastPkts", 18), ("ifHCOutOctets", 19), ("ifInNUcastPkts", 2), ("ifHCOutUcastPkts", 20), ("ifHCOutMulticastPkts", 21), ("ifHCOutBroadcastPkts", 22), ("dot3StatsAlignmentErrors", 23), ("dot3StatsFCSErrors", 24), ("dot3StatsSingleCollisionFrames", 25), ("dot3StatsMultipleCollisionFrames", 26), ("dot3StatsSQETestErrors", 27), ("dot3StatsDeferredTransmissions", 28), ("dot3StatsLateCollisions", 29), ("ifInDiscards", 3), ("dot3StatsExcessiveCollisions", 30), ("dot3StatsInternalMacTxErrors", 31), ("dot3StatsCarrierSenseErrors", 32), ("dot3StatsFrameTooLongs", 33), ("dot3StatsInternalMacRxErrors", 34), ("dot3StatsSymbolErrors", 35), ("dot3InPauseFrames", 36), ("dot3OutPauseFrames", 37), ("dot5StatsLineErrors", 38), ("dot5StatsBurstErrors", 39), ("ifInErrors", 4), ("dot5StatsACErrors", 40), ("dot5StatsAbortTransErrors", 41), ("dot5StatsInternalErrors", 42), ("dot5StatsLostFrameErrors", 43), ("dot5StatsReceiveCongestions", 44), ("dot5StatsFrameCopiedErrors", 45), ("dot5StatsTokenErrors", 46), ("dot5StatsSoftErrors", 47), ("dot5StatsHardErrors", 48), ("dot5StatsSignalLoss", 49), ("ifInUnknownProtos", 5), ("dot5StatsTransmitBeacons", 50), ("dot5StatsRecoverys", 51), ("dot5StatsLobeWires", 52), ("dot5StatsRemoves", 53), ("dot5StatsSingles", 54), ("dot5StatsFreqErrors", 55), ("etherStatsDropEvents", 56), ("etherStatsOctets", 57), ("etherStatsPkts", 58), ("etherStatsBroadcastPkts", 59), ("ifOutOctets", 6), ("etherStatsMulticastPkts", 60), ("etherStatsCRCAlignErrors", 61), ("etherStatsUndersizePkts", 62), ("etherStatsOversizePkts", 63), ("etherStatsFragments", 64), ("etherStatsJabbers", 65), ("etherStatsCollisions", 66), ("etherStatsPkts64Octets", 67), ("etherStatsPkts65to127Octets", 68), ("etherStatsPkts128to255Octets", 69), ("ifOutUcastPkts", 7), ("etherStatsPkts256to511Octets", 70), ("etherStatsPkts512to1023Octets", 71), ("etherStatsPkts1024to1518Octets", 72), ("dot1dTpPortInFrames", 73), ("dot1dTpPortOutFrames", 74), ("dot1dTpPortInDiscards", 75), ("ifOutNUcastPkts", 8), ("ifOutDiscards", 9), ))).setMaxAccess("readonly")
if mibBuilder.loadTexts: interfaceTopNCaps.setDescription("The type(s) of sorting capabilities supported by the agent.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of ifInOctets, as defined in [RFC2863],\nthen the 'ifInOctets' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of ifInUcastPkts, as defined in [RFC2863],\nthen the 'ifInUcastPkts' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of ifInNUcastPkts, as defined in [RFC2863],\nthen the 'ifInNUcastPkts' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of ifInDiscards, as defined in [RFC2863],\nthen the 'ifInDiscards' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of ifInErrors, as defined in [RFC2863],\nthen the 'ifInErrors' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of ifInUnknownProtocols, as defined in [RFC2863],\nthen the 'ifInUnknownProtocols' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of ifOutOctets, as defined in [RFC2863],\nthen the 'ifOutOctets' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of ifOutUcastPackets, as defined in [RFC2863],\nthen the 'ifOutUcastPackets' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of ifOutNUcastPackets, as defined in [RFC2863],\nthen the 'ifOutNUcastPackets' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of ifOutDiscards, as defined in [RFC2863],\nthen the 'ifOutDiscards' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of ifOutErrors, as defined in [RFC2863],\nthen the 'ifOutErrors' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of ifInMulticastPkts, as defined in [RFC2863],\n\n\nthen the 'ifInMulticastPkts' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of ifInBroadcastPkts, as defined in [RFC2863],\nthen the 'ifInBroadcastPkts' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of ifOutMulticastPkts, as defined in [RFC2863],\nthen the 'ifOutMulticastPkts' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of ifOutBroadcastPkts, as defined in [RFC2863],\nthen the 'ifOutBroadcastPkts' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of ifHCInOctets, as defined in [RFC2863],\nthen the 'ifHCInOctets' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of ifHCInMulticastPkts, as defined in [RFC2863],\nthen the 'ifHCInMulticastPkts' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of ifHCInBroadcastPkts, as defined in [RFC2863],\nthen the 'ifHCInBroadcastPkts' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of ifHCOutOctets, as defined in [RFC2863],\nthen the 'ifHCOutOctets' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of ifHCOutUcastPkts, as defined in [RFC2863],\nthen the 'ifHCOutUcastPkts' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of ifHCOutMulticastPkts, as defined in [RFC2863],\nthen the 'ifHCOutMulticastPkts' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of ifHCOutBroadcastPkts, as defined in [RFC2863],\nthen the 'ifHCOutBroadcastPkts' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of dot3StatsAlignmentErrors, as defined in [RFC2665],\nthen the 'dot3StatsAlignmentErrors' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of dot3StatsFCSErrors, as defined in [RFC2665],\n\n\nthen the 'dot3StatsFCSErrors' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of dot3StatsSingleCollisionFrames, as defined in\n[RFC2665],then the 'dot3StatsSingleCollisionFrames' bit will\nbe set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of dot3StatsSQETestErrors, as defined in [RFC2665],\nthen the 'dot3StatsSQETestErrors' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of dot3StatsDeferredTransmissions, as defined in\n[RFC2665], then the 'dot3StatsDeferredTransmissions' bit\nwill be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of dot3StatsLateCollisions, as defined in [RFC2665],\nthen the 'dot3StatsLateCollisions' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of dot3StatsExcessiveCollisions, as defined in [RFC2665],\nthen the 'dot3StatsExcessiveCollisions' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of dot3StatsInternalMacTxErrors, as defined in\n[RFC2665],then the 'dot3StatsInternalMacTxErrors' bit\nwill be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of dot3StatsCarrierSenseErrors, as defined in [RFC2665],\nthen the 'dot3StatsCarrierSenseErrors' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of dot3StatsFrameTooLongs, as defined in [RFC2665],\nthen the 'dot3StatsFrameTooLongs' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of dot3StatsInternalMacRxErrors, as defined in\n[RFC2665], then the 'dot3StatsInternalMacRxErrors' bit\nwill be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of dot3StatsSymbolErrors, as defined in [RFC2665],\nthen the 'dot3StatsSymbolErrors' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of dot3InPauseFrames, as defined in [RFC2665],\n\n\nthen the 'dot3InPauseFrames' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of dot3OutPauseFrames, as defined in [RFC2665],\nthen the 'dot3OutPauseFrames' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of dot5StatsLineErrors, as defined in [RFC1748],\nthen the 'dot5StatsLineErrors' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of dot5StatsBurstErrors, as defined in [RFC1748],\nthen the 'dot5StatsBurstErrors' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of dot5StatsACErrors, as defined in [RFC1748],\nthen the 'dot5StatsACErrors' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of dot5StatsAbortTransErrors, as defined in [RFC1748],\nthen the 'dot5StatsAbortTransErrors' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of dot5StatsInternalErrors, as defined in [RFC1748],\nthen the 'dot5StatsInternalErrors' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of dot5StatsLostFrameErrors, as defined in [RFC1748],\nthen the 'dot5StatsLostFrameErrors' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of dot5StatsReceiveCongestionErrors, as defined in\n[RFC1748], then the 'dot5StatsReceiveCongestionErrors' bit will\nbe set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of dot5StatsFrameCopiedErrors, as defined in [RFC1748],\nthen the 'dot5StatsFrameCopiedErrors' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of dot5StatsTokenErrors, as defined in [RFC1748],\nthen the 'dot5StatsTokenErrors' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of dot5StatsSoftErrors, as defined in [RFC1748],\nthen the 'dot5StatsSoftErrors' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\n\n\nvalues of dot5StatsHardErrors, as defined in [RFC1748],\nthen the 'dot5StatsHardErrors' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of dot5StatsSignalLoss, as defined in [RFC1748],\nthen the 'dot5StatsSignalLoss' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of dot5StatsTransmitBeacons, as defined in [RFC1748],\nthen the 'dot5StatsTransmitBeacons' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of dot5StatsRecoverys, as defined in [RFC1748],\nthen the 'dot5StatsRecoverys' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of dot5StatsLobeWires, as defined in [RFC1748],\nthen the 'dot5StatsLobeWires' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of dot5StatsRemoves, as defined in [RFC1748],\nthen the 'dot5StatsRemoves' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of dot5StatsSingles, as defined in [RFC1748],\nthen the 'dot5StatsSingles' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of dot5StatsFreqErrors, as defined in [RFC1748],\nthen the 'dot5StatsFreqErrors' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of etherStatsDropEvents, as defined in [RFC2819],\nthen the 'etherStatsDropEvents' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of etherStatsOctets, as defined in [RFC2819],\nthen the 'etherStatsOctets' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of etherStatsPkts, as defined in [RFC2819],\nthen the 'etherStatsPkts' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of etherStatsBroadcastPkts, as defined in [RFC2819],\nthen the 'etherStatsBroadcastPkts' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\n\n\nvalues of etherStatsMulticastPkts, as defined in [RFC2819],\nthen the 'etherStatsMulticastPkts' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of etherStatsCRCAlignErrors, as defined in [RFC2819],\nthen the 'etherStatsCRCAlignErrors' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of etherStatsUndersizePkts, as defined in [RFC2819],\nthen the 'etherStatsUndersizePkts' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of etherStatsOversizePkts, as defined in [RFC2819],\nthen the 'etherStatsOversizePkts' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of etherStatsFragments, as defined in [RFC2819],\nthen the 'etherStatsFragments' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of etherStatsJabbers, as defined in [RFC2819],\nthen the 'etherStatsJabbers' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of etherStatsCollisions, as defined in [RFC2819],\nthen the 'etherStatsCollisions' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of etherStatsPkts64Octets, as defined in [RFC2819],\nthen the 'etherStatsPkts64Octets' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of etherStatsPkts65to127Octets, as defined in [RFC2819],\nthen the 'etherStatsPkts65to127Octets' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of etherStatsPkts128to255Octets, as defined in [RFC2819],\nthen the 'etherStatsPkts128to255Octets' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of etherStatsPkts256to511Octets, as defined in [RFC2819],\nthen the 'etherStatsPkts256to511Octets' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of etherStatsPkts512to1023Octets, as defined in [RFC2819],\nthen the 'etherStatsPkts512to1023Octets' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\n\n\nvalues of etherStatsPkts1024to1518Octets, as defined in\n[RFC2819], then the 'etherStatsPkts1024to1518Octets' bit will\nbe set.\n\n\nIf the agent can perform sorting of interfaces according to the\nvalues of dot1dTpPortInFrames, as defined in [RFC1493],\nthen the 'dot1dTpPortInFrames' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of dot1dTpPortOutFrames, as defined in [RFC1493],\nthen the 'dot1dTpPortOutFrames' bit will be set.\n\nIf the agent can perform sorting of interfaces according to the\nvalues of dot1dTpPortInDiscards, as defined in [RFC1493],\nthen the 'dot1dTpPortInDiscards' bit will be set.")
interfaceTopNControlTable = MibTable((1, 3, 6, 1, 2, 1, 16, 27, 1, 2))
if mibBuilder.loadTexts: interfaceTopNControlTable.setDescription("A table of control records for reports on the top `N'\ninterfaces for the value or rate of a selected object.\nThe number of entries depends on the configuration of the agent.\nThe maximum number of entries is implementation\ndependent.")
interfaceTopNControlEntry = MibTableRow((1, 3, 6, 1, 2, 1, 16, 27, 1, 2, 1)).setIndexNames((0, "INTERFACETOPN-MIB", "interfaceTopNControlIndex"))
if mibBuilder.loadTexts: interfaceTopNControlEntry.setDescription("A set of parameters that control the creation of a\nreport of the top N ports according to several metrics.")
interfaceTopNControlIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 27, 1, 2, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess("noaccess")
if mibBuilder.loadTexts: interfaceTopNControlIndex.setDescription("An index that uniquely identifies an entry in the\ninterfaceTopNControl table.  Each such entry defines\none top N report prepared for a probe.")
interfaceTopNObjectVariable = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 27, 1, 2, 1, 2), Integer().subtype(subtypeSpec=SingleValueConstraint(11,32,53,14,72,13,46,24,25,63,49,9,65,44,50,70,34,66,41,23,59,3,37,4,71,75,60,35,39,74,27,31,15,28,36,18,17,40,68,29,64,16,21,48,7,67,0,57,1,8,38,30,58,10,52,45,22,73,19,12,47,42,33,69,51,61,54,6,43,5,62,56,20,55,2,26,)).subtype(namedValues=NamedValues(("ifInOctets", 0), ("ifInUcastPkts", 1), ("ifOutErrors", 10), ("ifInMulticastPkts", 11), ("ifInBroadcastPkts", 12), ("ifOutMulticastPkts", 13), ("ifOutBroadcastPkts", 14), ("ifHCInOctets", 15), ("ifHCInUcastPkts", 16), ("ifHCInMulticastPkts", 17), ("ifHCInBroadcastPkts", 18), ("ifHCOutOctets", 19), ("ifInNUcastPkts", 2), ("ifHCOutUcastPkts", 20), ("ifHCOutMulticastPkts", 21), ("ifHCOutBroadcastPkts", 22), ("dot3StatsAlignmentErrors", 23), ("dot3StatsFCSErrors", 24), ("dot3StatsSingleCollisionFrames", 25), ("dot3StatsMultipleCollisionFrames", 26), ("dot3StatsSQETestErrors", 27), ("dot3StatsDeferredTransmissions", 28), ("dot3StatsLateCollisions", 29), ("ifInDiscards", 3), ("dot3StatsExcessiveCollisions", 30), ("dot3StatsInternalMacTxErrors", 31), ("dot3StatsCarrierSenseErrors", 32), ("dot3StatsFrameTooLongs", 33), ("dot3StatsInternalMacRxErrors", 34), ("dot3StatsSymbolErrors", 35), ("dot3InPauseFrames", 36), ("dot3OutPauseFrames", 37), ("dot5StatsLineErrors", 38), ("dot5StatsBurstErrors", 39), ("ifInErrors", 4), ("dot5StatsACErrors", 40), ("dot5StatsAbortTransErrors", 41), ("dot5StatsInternalErrors", 42), ("dot5StatsLostFrameErrors", 43), ("dot5StatsReceiveCongestions", 44), ("dot5StatsFrameCopiedErrors", 45), ("dot5StatsTokenErrors", 46), ("dot5StatsSoftErrors", 47), ("dot5StatsHardErrors", 48), ("dot5StatsSignalLoss", 49), ("ifInUnknownProtos", 5), ("dot5StatsTransmitBeacons", 50), ("dot5StatsRecoverys", 51), ("dot5StatsLobeWires", 52), ("dot5StatsRemoves", 53), ("dot5StatsSingles", 54), ("dot5StatsFreqErrors", 55), ("etherStatsDropEvents", 56), ("etherStatsOctets", 57), ("etherStatsPkts", 58), ("etherStatsBroadcastPkts", 59), ("ifOutOctets", 6), ("etherStatsMulticastPkts", 60), ("etherStatsCRCAlignErrors", 61), ("etherStatsUndersizePkts", 62), ("etherStatsOversizePkts", 63), ("etherStatsFragments", 64), ("etherStatsJabbers", 65), ("etherStatsCollisions", 66), ("etherStatsPkts64Octets", 67), ("etherStatsPkts65to127Octets", 68), ("etherStatsPkts128to255Octets", 69), ("ifOutUcastPkts", 7), ("etherStatsPkts256to511Octets", 70), ("etherStatsPkts512to1023Octets", 71), ("etherStatsPkts1024to1518Octets", 72), ("dot1dTpPortInFrames", 73), ("dot1dTpPortOutFrames", 74), ("dot1dTpPortInDiscards", 75), ("ifOutNUcastPkts", 8), ("ifOutDiscards", 9), ))).setMaxAccess("readcreate")
if mibBuilder.loadTexts: interfaceTopNObjectVariable.setDescription("The particular variable to be sampled.\n\nValues between 0 and 22, point to MIB objects defined in\nIF-MIB [RFC2863].\n\nValues between 23 and 37, point to MIB objects defined in\nEtherLike-MIB [RFC2665].\n\nValues between 38 and 55, point to MIB objects defined in\nTOKENRING-MIB [RFC1748].\n\nValues between 56 and 72, point to MIB objects defined in\nRMON-MIB [RFC2819].\n\nValues between 73 and 75, point to MIB objects defined in\nBRIDGE-MIB [RFC1493].\n\nBecause SNMP access control is articulated entirely in terms\nof the contents of MIB views, no access control mechanism\nexists that can restrict the value of this object to identify\nonly those objects that exist in a particular MIB view.\nBecause there is thus no acceptable means of restricting the\nread access that could be obtained through the TopN\nmechanism, the probe must only grant write access to this\nobject in those views that have read access to all objects on\nthe probe.\n\n\n\nDuring a set operation, if the supplied variable name is not\navailable in the selected MIB view, or does not conform the\nother conditions mentioned above, a badValue error must be\nreturned.\n\nThis object may not be modified if the associated\ninterfaceTopNControlStatus object is equal to active(1).")
interfaceTopNObjectSampleType = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 27, 1, 2, 1, 3), Integer().subtype(subtypeSpec=SingleValueConstraint(3,1,2,)).subtype(namedValues=NamedValues(("absoluteValue", 1), ("deltaValue", 2), ("bandwidthPercentage", 3), ))).setMaxAccess("readcreate")
if mibBuilder.loadTexts: interfaceTopNObjectSampleType.setDescription("The method of sampling the selected variable for storage in\nthe interfaceTopNTable.\n\nIf the value of this object is absoluteValue(1), the value of\nthe selected variable will be copied directly into the topNValue.\n\nIf the value of this object is deltaValue(2), the value of the\nselected variable at the last sample will be subtracted from\nthe current value, and the difference will be stored in topNValue.\n\nIf the value of this object is bandwidthPercentage(3), the agent\nrecords the total number of octets sent over an interval divided\nby the total number of octets that represent '100% bandwidth'\nfor that interface. This ratio is multiplied by 1000 to\nretain a 3 digit integer (0..1000) in units of\n'tenth of one percent'. This type of computation is accurate for\nthe octet counters. The usage of this option with respect to\npackets or error counters is not recommended.\n\nThis object may not be modified if the associated\ninterfaceTopNControlStatus object is equal to active(1).")
interfaceTopNNormalizationReq = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 27, 1, 2, 1, 4), TruthValue()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: interfaceTopNNormalizationReq.setDescription("This object indicates whether  normalization is required in the\n\n\ncomputation of the selected value.\n\nIf the value of this object is 'true', the value of\nthe selected variable will be multiplied by a factor equal to the\ninterfaceTopNNormalizationFactor divided by the value of\neffective speed of the interface\n\nIf the value of this object is 'false',\nthe value of the selected variable will be taken 'as is' in\nthe TopN computation.\n\nIf the value of the object interfaceTopNSampleType is\nbandwidthPercentage(3), the object\ninterfaceTopNNormalizationReq cannot take the value 'true'.\n\nThe value of this object MUST be false if the effective speed of\nthe interface sub-layer as determined from ifSpeed is zero. This\nconforms to the ifSpeed definition in [RFC2863]for a sub-layer\nthat has no concept of bandwidth.\n\nThis object may not be modified if the associated\ninterfaceTopNControlStatus object is equal to active(1).")
interfaceTopNNormalizationFactor = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 27, 1, 2, 1, 5), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647))).setMaxAccess("readcreate")
if mibBuilder.loadTexts: interfaceTopNNormalizationFactor.setDescription("The value used for normalization if\ninterfaceTopNNormalizationReq has the value 'true'.\n\nExample:\nThe following set of values is applied to a device with multiple\nEthernet interfaces running at 10 Mbps, 100 Mbps, and 1 Gbps.\ninterfaceTopNObjectVariable = 'ifInOctets'\ninterfaceTopNObjectSampleType = 'deltaValue'\ninterfaceTopNNormalizationReq = 'true'\ninterfaceTopNNormalizationFactor = 1000000000\nApplying this set of values will result in the sampled delta values\nto be multiplied by 100 for the 10 Mbps interfaces, and by 10 for\nthe 100 Mbps interfaces, while the sample values for the 1 Gbps\ninterface are left unchanged. The effective speed of the interface is\ntaken from the value of ifSpeed for each interface, if ifSpeed is\nless than 4,294,967,295, or from ifHighSpeed multiplied by\n1,000,000 otherwise.\n\nAt row creation the agent SHOULD set the value of this object to\n\n\nthe effective speed of the interface.")
interfaceTopNTimeRemaining = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 27, 1, 2, 1, 6), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647)).clone(0)).setMaxAccess("readcreate")
if mibBuilder.loadTexts: interfaceTopNTimeRemaining.setDescription("The number of seconds left in the report\ncurrently being collected.  When this object\nis modified by the management station, a new\ncollection is started, possibly aborting a\ncurrently running report.  The new value is\nused as the requested duration of this report,\nwhich is loaded into the associated\ninterfaceTopNDuration object.\n\nWhen this object is set to a non-zero value,\nany associated interfaceTopNEntries shall be\nmade inaccessible by the agent.  While the value\nof this object is non-zero, it decrements by one\nper second until it reaches zero.  During this\ntime, all associated interfaceTopNEntries shall\nremain inaccessible.  At the time that this object\ndecrements to zero, the report is made accessible\nin the interfaceTopNTable.  Thus, the interfaceTopN\ntable needs to be created only at the end of the\ncollection interval.\n\nIf the value of this object is set to zero\nwhile the associated report is running, the\nrunning report is aborted and no associated\ninterfaceTopNEntries are created.")
interfaceTopNDuration = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 27, 1, 2, 1, 7), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess("readonly")
if mibBuilder.loadTexts: interfaceTopNDuration.setDescription("The number of seconds that this report has\ncollected during the last sampling interval,\nor if this report is currently being collected,\nthe number of seconds that this report is being\ncollected during this sampling interval.\n\nWhen the associated interfaceTopNTimeRemaining\n\n\nobject is set, this object shall be set by the\nagent to the same value and shall not be modified\nuntil the next time the interfaceTopNTimeRemaining\nis set.\n\nThis value shall be zero if no reports have been\nrequested for this interfaceTopNControlEntry.")
interfaceTopNRequestedSize = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 27, 1, 2, 1, 8), Integer32().clone(10)).setMaxAccess("readcreate")
if mibBuilder.loadTexts: interfaceTopNRequestedSize.setDescription("The maximum number of interfaces requested\nfor the Top N Table.\n\nWhen this object is created or modified, the\nagent should set interfaceTopNGrantedSize as close\nto this object as is possible for the particular\nimplementation and available resources.")
interfaceTopNGrantedSize = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 27, 1, 2, 1, 9), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess("readonly")
if mibBuilder.loadTexts: interfaceTopNGrantedSize.setDescription("The maximum number of interfaces in the\ntop N table.\n\nWhen the associated interfaceTopNRequestedSize object is\ncreated or modified, the agent should set this object as\nclosely to the requested value as is possible for the\nparticular implementation and available resources.  The\nagent must not lower this value except as a result of a\nset to the associated interfaceTopNRequestedSize object.")
interfaceTopNStartTime = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 27, 1, 2, 1, 10), TimeStamp()).setMaxAccess("readonly")
if mibBuilder.loadTexts: interfaceTopNStartTime.setDescription("The value of sysUpTime when this top N report was\nlast started.  In other words, this is the time that\nthe associated interfaceTopNTimeRemaining object was\n\n\nmodified to start the requested report.\n\nIf the report has not yet been started, the value\nof this object is zero.")
interfaceTopNOwner = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 27, 1, 2, 1, 11), OwnerString()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: interfaceTopNOwner.setDescription("The entity that configured this entry and is\nusing the resources assigned to it.")
interfaceTopNLastCompletionTime = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 27, 1, 2, 1, 12), TimeStamp()).setMaxAccess("readonly")
if mibBuilder.loadTexts: interfaceTopNLastCompletionTime.setDescription("The value of sysUpTime when this top N report was\nlast completed. If no report was yet completed, the value\nof this object is zero.")
interfaceTopNRowStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 27, 1, 2, 1, 13), RowStatus()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: interfaceTopNRowStatus.setDescription("The status of this row.\n\nIf the value of this object is not equal to\nactive(1), all associated entries in the\ninterfaceTopNTable shall be deleted by the\nagent.")
interfaceTopNTable = MibTable((1, 3, 6, 1, 2, 1, 16, 27, 1, 3))
if mibBuilder.loadTexts: interfaceTopNTable.setDescription("A table of reports for the top `N' ports based on\n\n\nsetting of associated control table entries. The\nmaximum number of entries depends on the number\nof entries in table interfaceTopNControlTable and\nthe value of object interfaceTopNGrantedSize for\neach entry.\n\nFor each entry in the interfaceTopNControlTable,\ninterfaces with the highest value of\ninterfaceTopNValue shall be placed in this table\nin decreasing order of that rate until there is\nno more room or until there are no more ports.")
interfaceTopNEntry = MibTableRow((1, 3, 6, 1, 2, 1, 16, 27, 1, 3, 1)).setIndexNames((0, "INTERFACETOPN-MIB", "interfaceTopNControlIndex"), (0, "INTERFACETOPN-MIB", "interfaceTopNIndex"))
if mibBuilder.loadTexts: interfaceTopNEntry.setDescription("A set of statistics for an interface that is\npart of a top N report.")
interfaceTopNIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 27, 1, 3, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess("noaccess")
if mibBuilder.loadTexts: interfaceTopNIndex.setDescription("An index that uniquely identifies an entry in\nthe interfaceTopN table among those in the same\nreport.  This index is between 1 and N, where N\nis the number of entries in this report.  Increasing\nvalues of interfaceTopNIndex shall be assigned to\nentries with decreasing values of interfaceTopNValue\nor interfaceTopNValue64, whichever applies,\nuntil index N is assigned to the entry with the\n\n\nlowest value of interfaceTopNValue /\ninterfaceTopNValue64 or there are no\nmore interfaceTopNEntries.\n\nNo ports are included in a report where their\nvalue of interfaceTopNValue would be zero.")
interfaceTopNDataSourceIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 27, 1, 3, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647))).setMaxAccess("readonly")
if mibBuilder.loadTexts: interfaceTopNDataSourceIndex.setDescription("This object identifies the index corresponding\nto the dataSource for this entry.\n\nFor sorted values of variables belonging to the\nIF-MIB, EtherLike-MIB or TOKENRING-MIB, this value\nequals the ifIndex of the interface.\n\nFor sorted values of variables belonging to the\nRMON-MIB, this value equals the interface corresponding\nto the data source, pointed to by the value\nof etherStatsDataSource.\n\nFor sorted values of variables belonging to the\nBRIDGE-MIB, this value equals the interface corresponding\nto the bridge port, pointed to by the value\nof dot1dBasePortIfIndex.")
interfaceTopNValue = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 27, 1, 3, 1, 3), Gauge32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: interfaceTopNValue.setDescription("The value at the end of the sampling interval, or\nthe amount of change in the selected variable\nduring this sampling interval for the identified\ninterface.  The selected variable is that interfaces's\ninstance of the object selected by\ninterfaceTopNObjectVariable. This value may be normalized\nif interfaceTopNNormalization required equals 'true'.\nThis value of this object will be computed for all\ncases when interfaceTopNObjectVariable points to a\n32-bit counter or Gauge or when\ninterfaceTopNObjectSampleType equals bandwidthPercentage(3),\nand will be zero for all other cases.")
interfaceTopNValue64 = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 27, 1, 3, 1, 4), CounterBasedGauge64()).setMaxAccess("readonly")
if mibBuilder.loadTexts: interfaceTopNValue64.setDescription("The value at the end of the sampling interval, or\nthe amount of change in the selected variable\nduring this sampling interval for the identified\ninterface.  The selected variable is that interfaces's\ninstance of the object selected by\ninterfaceTopNObjectVariable. This value may be normalized\nif interfaceTopNNormalization required equals 'true'.\nThis value of this object will be computed for all\ncases when interfaceTopNObjectVariable points to\na 64-bit counter, and will be zero for all other cases.")
interfaceTopNNotifications = MibIdentifier((1, 3, 6, 1, 2, 1, 16, 27, 2))
interfaceTopNConformance = MibIdentifier((1, 3, 6, 1, 2, 1, 16, 27, 3))
interfaceTopNCompliances = MibIdentifier((1, 3, 6, 1, 2, 1, 16, 27, 3, 1))
interfaceTopNGroups = MibIdentifier((1, 3, 6, 1, 2, 1, 16, 27, 3, 2))

# Augmentions

# Groups

interfaceTopNGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 16, 27, 3, 2, 1)).setObjects(*(("INTERFACETOPN-MIB", "interfaceTopNDataSourceIndex"), ("INTERFACETOPN-MIB", "interfaceTopNNormalizationFactor"), ("INTERFACETOPN-MIB", "interfaceTopNTimeRemaining"), ("INTERFACETOPN-MIB", "interfaceTopNValue"), ("INTERFACETOPN-MIB", "interfaceTopNObjectVariable"), ("INTERFACETOPN-MIB", "interfaceTopNRowStatus"), ("INTERFACETOPN-MIB", "interfaceTopNLastCompletionTime"), ("INTERFACETOPN-MIB", "interfaceTopNRequestedSize"), ("INTERFACETOPN-MIB", "interfaceTopNCaps"), ("INTERFACETOPN-MIB", "interfaceTopNObjectSampleType"), ("INTERFACETOPN-MIB", "interfaceTopNValue64"), ("INTERFACETOPN-MIB", "interfaceTopNDuration"), ("INTERFACETOPN-MIB", "interfaceTopNOwner"), ("INTERFACETOPN-MIB", "interfaceTopNNormalizationReq"), ("INTERFACETOPN-MIB", "interfaceTopNGrantedSize"), ("INTERFACETOPN-MIB", "interfaceTopNStartTime"), ) )
if mibBuilder.loadTexts: interfaceTopNGroup.setDescription("A collection of objects providing interfaceTopN data for\na multiple interfaces device.")

# Compliances

interfaceTopNCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 16, 27, 3, 1, 1)).setObjects(*(("INTERFACETOPN-MIB", "interfaceTopNGroup"), ) )
if mibBuilder.loadTexts: interfaceTopNCompliance.setDescription("Describes the requirements for conformance to the\nInterfaceTopN MIB.")

# Exports

# Module identity
mibBuilder.exportSymbols("INTERFACETOPN-MIB", PYSNMP_MODULE_ID=interfaceTopNMIB)

# Objects
mibBuilder.exportSymbols("INTERFACETOPN-MIB", interfaceTopNMIB=interfaceTopNMIB, interfaceTopNObjects=interfaceTopNObjects, interfaceTopNCaps=interfaceTopNCaps, interfaceTopNControlTable=interfaceTopNControlTable, interfaceTopNControlEntry=interfaceTopNControlEntry, interfaceTopNControlIndex=interfaceTopNControlIndex, interfaceTopNObjectVariable=interfaceTopNObjectVariable, interfaceTopNObjectSampleType=interfaceTopNObjectSampleType, interfaceTopNNormalizationReq=interfaceTopNNormalizationReq, interfaceTopNNormalizationFactor=interfaceTopNNormalizationFactor, interfaceTopNTimeRemaining=interfaceTopNTimeRemaining, interfaceTopNDuration=interfaceTopNDuration, interfaceTopNRequestedSize=interfaceTopNRequestedSize, interfaceTopNGrantedSize=interfaceTopNGrantedSize, interfaceTopNStartTime=interfaceTopNStartTime, interfaceTopNOwner=interfaceTopNOwner, interfaceTopNLastCompletionTime=interfaceTopNLastCompletionTime, interfaceTopNRowStatus=interfaceTopNRowStatus, interfaceTopNTable=interfaceTopNTable, interfaceTopNEntry=interfaceTopNEntry, interfaceTopNIndex=interfaceTopNIndex, interfaceTopNDataSourceIndex=interfaceTopNDataSourceIndex, interfaceTopNValue=interfaceTopNValue, interfaceTopNValue64=interfaceTopNValue64, interfaceTopNNotifications=interfaceTopNNotifications, interfaceTopNConformance=interfaceTopNConformance, interfaceTopNCompliances=interfaceTopNCompliances, interfaceTopNGroups=interfaceTopNGroups)

# Groups
mibBuilder.exportSymbols("INTERFACETOPN-MIB", interfaceTopNGroup=interfaceTopNGroup)

# Compliances
mibBuilder.exportSymbols("INTERFACETOPN-MIB", interfaceTopNCompliance=interfaceTopNCompliance)
