# PySNMP SMI module. Autogenerated from smidump -f python MPLS-FTN-STD-MIB
# by libsmi2pysnmp-0.1.3 at Mon Apr  2 20:39:18 2012,
# Python version sys.version_info(major=2, minor=7, micro=2, releaselevel='final', serial=0)

# Imports

( Integer, ObjectIdentifier, OctetString, ) = mibBuilder.importSymbols("ASN1", "Integer", "ObjectIdentifier", "OctetString")
( NamedValues, ) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
( ConstraintsIntersection, ConstraintsUnion, SingleValueConstraint, ValueRangeConstraint, ValueSizeConstraint, ) = mibBuilder.importSymbols("ASN1-REFINEMENT", "ConstraintsIntersection", "ConstraintsUnion", "SingleValueConstraint", "ValueRangeConstraint", "ValueSizeConstraint")
( Dscp, ) = mibBuilder.importSymbols("DIFFSERV-DSCP-TC", "Dscp")
( InterfaceIndexOrZero, ifCounterDiscontinuityGroup, ifGeneralInformationGroup, ) = mibBuilder.importSymbols("IF-MIB", "InterfaceIndexOrZero", "ifCounterDiscontinuityGroup", "ifGeneralInformationGroup")
( InetAddress, InetAddressType, InetPortNumber, ) = mibBuilder.importSymbols("INET-ADDRESS-MIB", "InetAddress", "InetAddressType", "InetPortNumber")
( mplsStdMIB, ) = mibBuilder.importSymbols("MPLS-TC-STD-MIB", "mplsStdMIB")
( SnmpAdminString, ) = mibBuilder.importSymbols("SNMP-FRAMEWORK-MIB", "SnmpAdminString")
( ModuleCompliance, ObjectGroup, ) = mibBuilder.importSymbols("SNMPv2-CONF", "ModuleCompliance", "ObjectGroup")
( Bits, Counter64, Integer32, Integer32, ModuleIdentity, MibIdentifier, MibScalar, MibTable, MibTableRow, MibTableColumn, TimeTicks, Unsigned32, ) = mibBuilder.importSymbols("SNMPv2-SMI", "Bits", "Counter64", "Integer32", "Integer32", "ModuleIdentity", "MibIdentifier", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "TimeTicks", "Unsigned32")
( RowPointer, RowStatus, StorageType, TextualConvention, TimeStamp, ) = mibBuilder.importSymbols("SNMPv2-TC", "RowPointer", "RowStatus", "StorageType", "TextualConvention", "TimeStamp")

# Types

class MplsFTNEntryIndex(Unsigned32):
    subtypeSpec = Unsigned32.subtypeSpec+ValueRangeConstraint(1,4294967295)
    
class MplsFTNEntryIndexOrZero(Unsigned32):
    subtypeSpec = Unsigned32.subtypeSpec+ValueRangeConstraint(0,4294967295)
    

# Objects

mplsFTNStdMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 10, 166, 8)).setRevisions(("2004-06-03 00:00",))
if mibBuilder.loadTexts: mplsFTNStdMIB.setOrganization("Multiprotocol Label Switching (MPLS) Working Group")
if mibBuilder.loadTexts: mplsFTNStdMIB.setContactInfo("\nThomas D. Nadeau\nPostal: Cisco Systems, Inc.\n250 Apollo Drive\nChelmsford, MA 01824\nTel:    +1-978-244-3051\nEmail:  tnadeau@cisco.com\n\nCheenu Srinivasan\nPostal: Bloomberg L.P.\n499 Park Avenue\nNew York, NY 10022\nTel:    +1-212-893-3682\nEmail:  cheenu@bloomberg.net\n\nArun Viswanathan\nPostal: Force10 Networks, Inc.\n1440 McCarthy Blvd\nMilpitas, CA 95035\nTel:    +1-408-571-3516\nEmail:  arunv@force10networks.com\n\nIETF MPLS Working Group email: mpls@uu.net")
if mibBuilder.loadTexts: mplsFTNStdMIB.setDescription("Copyright (C) The Internet Society (2004). The\ninitial version of this MIB module was published\nin RFC 3814. For full legal notices see the RFC\nitself or see:\nhttp://www.ietf.org/copyrights/ianamib.html\n\nThis MIB module contains managed object definitions for\nspecifying FEC to NHLFE (FTN) mappings and corresponding\nperformance for MPLS.")
mplsFTNNotifications = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 166, 8, 0))
mplsFTNObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 166, 8, 1))
mplsFTNIndexNext = MibScalar((1, 3, 6, 1, 2, 1, 10, 166, 8, 1, 1), MplsFTNEntryIndexOrZero()).setMaxAccess("readonly")
if mibBuilder.loadTexts: mplsFTNIndexNext.setDescription("This object contains the next available valid value to\nbe used for mplsFTNIndex when creating entries in the\nmplsFTNTable.\n\nWhen creating a new conceptual row (configuration\nentry) in mplsFTNTable with an SNMP SET operation the\ncommand generator (Network Management Application) must\nfirst issue a management protocol retrieval operation\nto obtain the current value of this object.\n\nIf the command responder (agent) does not wish to allow\ncreation of more entries in mplsFTNTable, possibly\nbecause of resource exhaustion, this object MUST return\na value of 0.\n\nIf a non-zero value is returned the Network Management\n\n\n\nApplication must determine whether the value is indeed\nstill unused since two Network Management Applications\nmay attempt to create a row simultaneously and use the\nsame value.\n\nIf it is currently unused and the SET succeeds, the\nagent MUST change the value of this object to a\ncurrently unused non-zero value (according to an\nimplementation specific algorithm) or zero (if no\nfurther row creation will be permitted).\n\nIf the value is in use, however, the SET fails and the\nNetwork Management Application must then reread this\nobject to obtain a new usable value.")
mplsFTNTableLastChanged = MibScalar((1, 3, 6, 1, 2, 1, 10, 166, 8, 1, 2), TimeStamp()).setMaxAccess("readonly")
if mibBuilder.loadTexts: mplsFTNTableLastChanged.setDescription("Indicates the last time an entry was added, deleted or\nmodified in mplsFTNTable.  Management stations should\nconsult this object to determine if mplsFTNTable\nrequires their attention.  This object is particularly\nuseful for applications performing a retrieval on\nmplsFTNTable to ensure that the table is not modified\nduring the retrieval operation.")
mplsFTNTable = MibTable((1, 3, 6, 1, 2, 1, 10, 166, 8, 1, 3))
if mibBuilder.loadTexts: mplsFTNTable.setDescription("This table contains the currently defined FTN entries.\nThis table allows FEC to NHLFE mappings to be\nspecified.  Each entry in this table defines a rule to\nbe applied to incoming packets (on interfaces that the\nFTN entry is activated on using mplsFTNMapTable) and an\naction to be taken on matching packets\n(mplsFTNActionPointer).\n\nThis table supports 6-tuple matching rules based on one\nor more of source address range, destination address\nrange, source port range, destination port range, IPv4\n\n\n\nProtocol field or IPv6 next-header field and the\nDiffServ Code Point (DSCP) to be specified.\n\nThe action pointer points either to instance of\nmplsXCEntry in MPLS-LSR-STD-MIB when the NHLFE is a non-\nTE LSP, or to an instance of mplsTunnelEntry in the\nMPLS-TE-STD-MIB when the NHLFE is an originating TE\ntunnel.")
mplsFTNEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 166, 8, 1, 3, 1)).setIndexNames((0, "MPLS-FTN-STD-MIB", "mplsFTNIndex"))
if mibBuilder.loadTexts: mplsFTNEntry.setDescription("Each entry represents one FTN entry which defines a\nrule to compare incoming packets with and an action to\nbe taken on matching packets.")
mplsFTNIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 166, 8, 1, 3, 1, 1), MplsFTNEntryIndex()).setMaxAccess("noaccess")
if mibBuilder.loadTexts: mplsFTNIndex.setDescription("This is the unique index for a conceptual row in\nmplsFTNTable.\n\nTo create a new conceptual row in mplsFTNTable a\nNetwork Management Application SHOULD retrieve the\ncurrent value of mplsFTNIndexNext to determine the next\nvalid available value of mplsFTNIndex.")
mplsFTNRowStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 166, 8, 1, 3, 1, 2), RowStatus()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mplsFTNRowStatus.setDescription("Used for controlling the creation and deletion of this\nrow. All writeable objects in this row may be modified\nat any time. If a Network Management Application\nattempts to delete a conceptual row by setting this\nobject to 'destroy' and there are one or more entries\nin mplsFTNMapTable pointing to the row (i.e., when\nmplsFTNIndex of the conceptual row being deleted is\nequal to mplsFTNMapCurrIndex for one or more entries in\nmplsFTNMapTable), the agent MUST also destroy the\ncorresponding entries in mplsFTNMapTable.")
mplsFTNDescr = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 166, 8, 1, 3, 1, 3), SnmpAdminString()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mplsFTNDescr.setDescription("The description of this FTN entry. Since the index for\nthis table has no particular significance or meaning,\nthis object should contain some meaningful text that an\noperator could use to further distinguish entries in\nthis table.")
mplsFTNMask = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 166, 8, 1, 3, 1, 4), Bits().subtype(namedValues=NamedValues(("sourceAddr", 0), ("destAddr", 1), ("sourcePort", 2), ("destPort", 3), ("protocol", 4), ("dscp", 5), ))).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mplsFTNMask.setDescription("This bit map indicates which of the fields described\nnext, namely source address range, destination address\nrange, source port range, destination port range, IPv4\nProtocol field or IPv6 next-header field and\nDifferentiated Services Code Point (DSCP) is active for\nthis FTN entry. If a particular bit is set to zero then\nthe corresponding field in the packet MUST be ignored\nfor comparison purposes.")
mplsFTNAddrType = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 166, 8, 1, 3, 1, 5), InetAddressType()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mplsFTNAddrType.setDescription("This object determines the type of address contained in\nthe source and destination address objects\n(mplsFTNSourceAddrMin, mplsFTNSourceAddrMax,\nmplsFTNDestAddrMin and mplsFTNDestAddrMax) of a\nconceptual row.\n\nThis object MUST NOT be set to unknown(0) when\nmplsFTNMask has bit positions sourceAddr(0) or\ndestAddr(1) set to one.\n\nWhen both these bit positions of mplsFTNMask are set to\nzero the value of mplsFTNAddrType SHOULD be set to\nunknown(0) and the corresponding source and destination\n\n\n\naddress objects SHOULD be set to zero-length strings.")
mplsFTNSourceAddrMin = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 166, 8, 1, 3, 1, 6), InetAddress()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mplsFTNSourceAddrMin.setDescription("The lower end of the source address range. The type of\nthis object is determined by the corresponding\nmplsFTNAddrType object.")
mplsFTNSourceAddrMax = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 166, 8, 1, 3, 1, 7), InetAddress()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mplsFTNSourceAddrMax.setDescription("The upper end of the source address range. The type of\nthis object is determined by the corresponding\nmplsFTNAddrType object.")
mplsFTNDestAddrMin = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 166, 8, 1, 3, 1, 8), InetAddress()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mplsFTNDestAddrMin.setDescription("The lower end of the destination address range. The\ntype of this object is determined by the corresponding\nmplsFTNAddrType object.")
mplsFTNDestAddrMax = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 166, 8, 1, 3, 1, 9), InetAddress()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mplsFTNDestAddrMax.setDescription("The higher end of the destination address range. The\ntype of this object is determined by the corresponding\nmplsFTNAddrType object.")
mplsFTNSourcePortMin = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 166, 8, 1, 3, 1, 10), InetPortNumber().clone('0')).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mplsFTNSourcePortMin.setDescription("The lower end of the source port range.")
mplsFTNSourcePortMax = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 166, 8, 1, 3, 1, 11), InetPortNumber().clone('65535')).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mplsFTNSourcePortMax.setDescription("The higher end of the source port range ")
mplsFTNDestPortMin = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 166, 8, 1, 3, 1, 12), InetPortNumber().clone('0')).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mplsFTNDestPortMin.setDescription("The lower end of the destination port range.")
mplsFTNDestPortMax = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 166, 8, 1, 3, 1, 13), InetPortNumber().clone('65535')).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mplsFTNDestPortMax.setDescription("The higher end of the destination port range.")
mplsFTNProtocol = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 166, 8, 1, 3, 1, 14), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255)).clone(255)).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mplsFTNProtocol.setDescription("The IP protocol to match against the IPv4 protocol\nnumber or IPv6 Next-Header number in the packet. A\nvalue of 255 means match all.  Note that the protocol\nnumber of 255 is reserved by IANA, and Next-Header\nnumber of 0 is used in IPv6.")
mplsFTNDscp = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 166, 8, 1, 3, 1, 15), Dscp()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mplsFTNDscp.setDescription("The contents of the DSCP field.")
mplsFTNActionType = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 166, 8, 1, 3, 1, 16), Integer().subtype(subtypeSpec=SingleValueConstraint(2,1,)).subtype(namedValues=NamedValues(("redirectLsp", 1), ("redirectTunnel", 2), ))).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mplsFTNActionType.setDescription("The type of action to be taken on packets matching this\nFTN entry.")
mplsFTNActionPointer = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 166, 8, 1, 3, 1, 17), RowPointer()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mplsFTNActionPointer.setDescription("If mplsFTNActionType is redirectLsp(1), then this\nobject MUST contain zeroDotZero or point to a instance\nof mplsXCEntry indicating the LSP to redirect matching\npackets to.\n\nIf mplsFTNActionType is redirectTunnel(2), then this\nobject MUST contain zeroDotZero or point to a instance\nof mplsTunnelEntry indicating the MPLS TE tunnel to\nredirect matching packets to.\n\nIf this object points to a conceptual row instance in a\ntable consistent with mplsFTNActionType but this\ninstance does not currently exist then no action will\nbe taken on packets matching such an FTN entry till\nthis instance comes into existence.\n\nIf this object contains zeroDotZero then no action will\nbe taken on packets matching such an FTN entry till it\nis populated with a valid pointer consistent with the\nvalue of mplsFTNActionType as explained above.")
mplsFTNStorageType = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 166, 8, 1, 3, 1, 18), StorageType().clone('nonVolatile')).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mplsFTNStorageType.setDescription("The storage type for this FTN entry. Conceptual rows\nhaving the value 'permanent' need not allow write-\naccess to any columnar objects in the row.")
mplsFTNMapTableLastChanged = MibScalar((1, 3, 6, 1, 2, 1, 10, 166, 8, 1, 4), TimeStamp()).setMaxAccess("readonly")
if mibBuilder.loadTexts: mplsFTNMapTableLastChanged.setDescription("Indicates the last time an entry was added, deleted or\nmodified in mplsFTNMapTable. Management stations should\nconsult this object to determine if the table requires\ntheir attention.  This object is particularly useful\nfor applications performing a retrieval on\nmplsFTNMapTable to ensure that the table is not\nmodified during the retrieval operation.")
mplsFTNMapTable = MibTable((1, 3, 6, 1, 2, 1, 10, 166, 8, 1, 5))
if mibBuilder.loadTexts: mplsFTNMapTable.setDescription("This table contains objects which provide the\ncapability to apply or map FTN rules as defined by\nentries in mplsFTNTable to specific interfaces in the\nsystem.  FTN rules are compared with incoming packets\nin the order in which they are applied on an interface.\n\nThe indexing structure of mplsFTNMapTable is as\nfollows.\n\n- mplsFTNMapIndex indicates the interface to which the\n  rule is being applied.  A value of 0 represents the\n  application of the rule to all interfaces.\n\n\n\n\n- mplsFTNMapPrevIndex specifies the rule on the\n  interface prior to the one being applied.  A value of\n  0 specifies that the rule is being inserted at the\n  head of the list of rules currently applied to the\n  interface.\n\n- mplsFTNMapCurrIndex is the index in mplsFTNTable\n  corresponding to the rule being applied.\n\nThis indexing structure makes the entries in the table\nbehave like items in a linked-list.  The object\nmplsFTNMapPrevIndex in each conceptual row is a pointer\nto the previous entry that is applied to a particular\ninterface.  This allows a new entry to be 'inserted' at\nan arbitrary position in a list of entries currently\napplied to an interface.  This object is self-\nadjusting, i.e., its value is automatically adjusted by\nthe agent, if necessary, after an insertion or deletion\noperation.\n\nUsing this linked-list structure, one can retrieve FTN\nentries in the order of application on a per-interface\nbasis as follows:\n\n- To determine the first FTN entry on an interface\n  with index ifIndex perform a GETNEXT retrieval\n  operation on mplsFTNMapRowStatus.ifIndex.0.0; the\n  returned object, if one exists, is (say)\n  mplsFTNMapRowStatus.ifIndex.0.n (mplsFTNMapRowStatus\n  is the first accessible columnar object in the\n  conceptual row). Then the index of the first FTN\n  entry applied on this interface is n.\n\n- To determine the FTN entry applied to an interface\n  after the one indexed by n perform a GETNEXT\n  retrieval operation on\n  mplsFTNMapRowStatus.ifIndex.n.0.  If such an entry\n  exists the returned object would be of the form\n  mplsFTNMapRowStatus.ifIndex.n.m.  Then the index of\n  the next FTN entry applied on this interface is m.\n\n- If the FTN entry indexed by n is the last entry\n  applied to the interface with index ifIndex then the\n  object returned would either be:\n\n  1.mplsFTNMapRowStatus.ifIndexNext.0.k, where\n    ifIndexNext is the index of the next interface in\n\n\n\n    ifTable to which an FTN entry has been applied, in\n    which case k is the index of the first FTN entry\n    applied to the interface with index ifIndexNext;\n\n  or:\n\n  2.mplsFTNMapStorageType.firstIfIndex.0.p, if there\n    are no more entries in mplsFTNMapTable, where\n    firstIfIndex is the first entry in ifTable to\n    which an FTN entry has been mapped.\n\nUse the above steps to retrieve all the applied FTN\nentries on a per-interface basis in application order.\nNote that the number of retrieval operations is the\nsame as the number of applied FTN entries (i.e., the\nminimum number of GETNEXT operations needed using any\nindexing scheme).\n\nAgents MUST NOT allow the same FTN entry as specified\nby mplsFTNMapCurrIndex to be applied multiple times to\nthe same interface.\n\nAgents MUST NOT allow the creation of rows in this\ntable until the corresponding rows are created in the\nmplsFTNTable.\n\nIf a row in mplsFTNTable is destroyed, the agent MUST\ndestroy the corresponding entries (i.e., ones with a\nmatching value of mplsFTNCurrIndex) in this table as\nwell.")
mplsFTNMapEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 166, 8, 1, 5, 1)).setIndexNames((0, "MPLS-FTN-STD-MIB", "mplsFTNMapIndex"), (0, "MPLS-FTN-STD-MIB", "mplsFTNMapPrevIndex"), (0, "MPLS-FTN-STD-MIB", "mplsFTNMapCurrIndex"))
if mibBuilder.loadTexts: mplsFTNMapEntry.setDescription("Each conceptual row represents the application of an\nFTN rule at a specific position in the list of FTN\nrules applied on an interface. ")
mplsFTNMapIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 166, 8, 1, 5, 1, 1), InterfaceIndexOrZero()).setMaxAccess("noaccess")
if mibBuilder.loadTexts: mplsFTNMapIndex.setDescription("The interface index that this FTN entry is being\napplied to. A value of zero indicates an entry that is\napplied all interfaces.\n\nEntries mapped to an interface by specifying its (non-\nzero) interface index in mplsFTNMapIndex are applied\nahead of entries with mplsFTNMapIndex equal to zero.")
mplsFTNMapPrevIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 166, 8, 1, 5, 1, 2), MplsFTNEntryIndexOrZero()).setMaxAccess("noaccess")
if mibBuilder.loadTexts: mplsFTNMapPrevIndex.setDescription("The index of the previous FTN entry that was applied to\nthis interface. The special value zero indicates that\nthis should be the first FTN entry in the list.")
mplsFTNMapCurrIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 166, 8, 1, 5, 1, 3), MplsFTNEntryIndex()).setMaxAccess("noaccess")
if mibBuilder.loadTexts: mplsFTNMapCurrIndex.setDescription("Index of the current FTN entry that is being applied to\nthis interface.")
mplsFTNMapRowStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 166, 8, 1, 5, 1, 4), Integer().subtype(subtypeSpec=SingleValueConstraint(1,6,4,)).subtype(namedValues=NamedValues(("active", 1), ("createAndGo", 4), ("destroy", 6), ))).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mplsFTNMapRowStatus.setDescription("Used for controlling the creation and deletion of this\nrow.\n\nAll writable objects in this row may be modified at any\ntime.\n\nIf a conceptual row in mplsFTNMapTable points to a\nconceptual row in mplsFTNTable which is subsequently\ndeleted, the corresponding conceptual row in\nmplsFTNMapTable MUST also be deleted by the agent.")
mplsFTNMapStorageType = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 166, 8, 1, 5, 1, 5), StorageType().clone('nonVolatile')).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mplsFTNMapStorageType.setDescription("The storage type for this entry.  Conceptual rows\nhaving the value 'permanent' need not allow write-\naccess to any columnar objects in this row.")
mplsFTNPerfTable = MibTable((1, 3, 6, 1, 2, 1, 10, 166, 8, 1, 6))
if mibBuilder.loadTexts: mplsFTNPerfTable.setDescription("This table contains performance statistics on FTN\nentries on a per-interface basis.")
mplsFTNPerfEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 166, 8, 1, 6, 1)).setIndexNames((0, "MPLS-FTN-STD-MIB", "mplsFTNPerfIndex"), (0, "MPLS-FTN-STD-MIB", "mplsFTNPerfCurrIndex"))
if mibBuilder.loadTexts: mplsFTNPerfEntry.setDescription("Each entry contains performance information for the\nspecified interface and an FTN entry mapped to this\ninterface.")
mplsFTNPerfIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 166, 8, 1, 6, 1, 1), InterfaceIndexOrZero()).setMaxAccess("noaccess")
if mibBuilder.loadTexts: mplsFTNPerfIndex.setDescription("The interface index of an interface that an FTN entry\nhas been applied/mapped to.  Each instance of this\nobject corresponds to an instance of mplsFTNMapIndex.")
mplsFTNPerfCurrIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 166, 8, 1, 6, 1, 2), MplsFTNEntryIndex()).setMaxAccess("noaccess")
if mibBuilder.loadTexts: mplsFTNPerfCurrIndex.setDescription("Index of an FTN entry that has been applied/mapped to\nthe specified interface.  Each instance of this object\ncorresponds to an instance of mplsFTNMapCurrIndex.")
mplsFTNPerfMatchedPackets = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 166, 8, 1, 6, 1, 3), Counter64()).setMaxAccess("readonly")
if mibBuilder.loadTexts: mplsFTNPerfMatchedPackets.setDescription("Number of packets that matched the specified FTN entry\nif it is applied/mapped to the specified interface.\nDiscontinuities in the value of this counter can occur\nat re-initialization of the management system, and at\nother times as indicated by the value of\nmplsFTNDiscontinuityTime.")
mplsFTNPerfMatchedOctets = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 166, 8, 1, 6, 1, 4), Counter64()).setMaxAccess("readonly")
if mibBuilder.loadTexts: mplsFTNPerfMatchedOctets.setDescription("Number of octets that matched the specified FTN entry\nif it is applied/mapped to the specified interface.\n\n\n\nDiscontinuities in the value of this counter can occur\nat re-initialization of the management system, and at\nother times as indicated by the value of\nmplsFTNDiscontinuityTime.")
mplsFTNPerfDiscontinuityTime = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 166, 8, 1, 6, 1, 5), TimeStamp()).setMaxAccess("readonly")
if mibBuilder.loadTexts: mplsFTNPerfDiscontinuityTime.setDescription("The value of sysUpTime on the most recent occasion at\nwhich any one or more of this entry's counters suffered\na discontinuity.  If no such discontinuities have\noccurred since the last re-initialization of the local\nmanagement subsystem, then this object contains a zero\nvalue.")
mplsFTNConformance = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 166, 8, 2))
mplsFTNGroups = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 166, 8, 2, 1))
mplsFTNCompliances = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 166, 8, 2, 2))

# Augmentions

# Groups

mplsFTNRuleGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 166, 8, 2, 1, 1)).setObjects(*(("MPLS-FTN-STD-MIB", "mplsFTNSourcePortMax"), ("MPLS-FTN-STD-MIB", "mplsFTNAddrType"), ("MPLS-FTN-STD-MIB", "mplsFTNIndexNext"), ("MPLS-FTN-STD-MIB", "mplsFTNDestPortMin"), ("MPLS-FTN-STD-MIB", "mplsFTNTableLastChanged"), ("MPLS-FTN-STD-MIB", "mplsFTNDestPortMax"), ("MPLS-FTN-STD-MIB", "mplsFTNDestAddrMin"), ("MPLS-FTN-STD-MIB", "mplsFTNStorageType"), ("MPLS-FTN-STD-MIB", "mplsFTNSourceAddrMin"), ("MPLS-FTN-STD-MIB", "mplsFTNDescr"), ("MPLS-FTN-STD-MIB", "mplsFTNProtocol"), ("MPLS-FTN-STD-MIB", "mplsFTNSourcePortMin"), ("MPLS-FTN-STD-MIB", "mplsFTNDestAddrMax"), ("MPLS-FTN-STD-MIB", "mplsFTNActionPointer"), ("MPLS-FTN-STD-MIB", "mplsFTNActionType"), ("MPLS-FTN-STD-MIB", "mplsFTNSourceAddrMax"), ("MPLS-FTN-STD-MIB", "mplsFTNDscp"), ("MPLS-FTN-STD-MIB", "mplsFTNRowStatus"), ("MPLS-FTN-STD-MIB", "mplsFTNMask"), ) )
if mibBuilder.loadTexts: mplsFTNRuleGroup.setDescription("Collection of objects that implement MPLS FTN rules.")
mplsFTNMapGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 166, 8, 2, 1, 2)).setObjects(*(("MPLS-FTN-STD-MIB", "mplsFTNMapTableLastChanged"), ("MPLS-FTN-STD-MIB", "mplsFTNMapStorageType"), ("MPLS-FTN-STD-MIB", "mplsFTNMapRowStatus"), ) )
if mibBuilder.loadTexts: mplsFTNMapGroup.setDescription("Collection of objects that implement activation of MPLS\nFTN entries on interfaces.")
mplsFTNPerfGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 166, 8, 2, 1, 3)).setObjects(*(("MPLS-FTN-STD-MIB", "mplsFTNPerfDiscontinuityTime"), ("MPLS-FTN-STD-MIB", "mplsFTNPerfMatchedOctets"), ("MPLS-FTN-STD-MIB", "mplsFTNPerfMatchedPackets"), ) )
if mibBuilder.loadTexts: mplsFTNPerfGroup.setDescription("Collection of objects providing MPLS FTN performance\ninformation.")

# Compliances

mplsFTNModuleFullCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 10, 166, 8, 2, 2, 1)).setObjects(*(("MPLS-FTN-STD-MIB", "mplsFTNMapGroup"), ("MPLS-FTN-STD-MIB", "mplsFTNPerfGroup"), ("MPLS-FTN-STD-MIB", "mplsFTNRuleGroup"), ("IF-MIB", "ifGeneralInformationGroup"), ("IF-MIB", "ifCounterDiscontinuityGroup"), ) )
if mibBuilder.loadTexts: mplsFTNModuleFullCompliance.setDescription("Compliance statement for agents that provide full\nsupport for MPLS-FTN-STD-MIB.")
mplsFTNModuleReadOnlyCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 10, 166, 8, 2, 2, 2)).setObjects(*(("MPLS-FTN-STD-MIB", "mplsFTNMapGroup"), ("MPLS-FTN-STD-MIB", "mplsFTNPerfGroup"), ("MPLS-FTN-STD-MIB", "mplsFTNRuleGroup"), ("IF-MIB", "ifGeneralInformationGroup"), ("IF-MIB", "ifCounterDiscontinuityGroup"), ) )
if mibBuilder.loadTexts: mplsFTNModuleReadOnlyCompliance.setDescription("Compliance requirement for implementations that only\n\n\n\nprovide read-only support for MPLS-FTN-STD-MIB. Such\ndevices can then be monitored but cannot be configured\nusing this MIB module.")

# Exports

# Module identity
mibBuilder.exportSymbols("MPLS-FTN-STD-MIB", PYSNMP_MODULE_ID=mplsFTNStdMIB)

# Types
mibBuilder.exportSymbols("MPLS-FTN-STD-MIB", MplsFTNEntryIndex=MplsFTNEntryIndex, MplsFTNEntryIndexOrZero=MplsFTNEntryIndexOrZero)

# Objects
mibBuilder.exportSymbols("MPLS-FTN-STD-MIB", mplsFTNStdMIB=mplsFTNStdMIB, mplsFTNNotifications=mplsFTNNotifications, mplsFTNObjects=mplsFTNObjects, mplsFTNIndexNext=mplsFTNIndexNext, mplsFTNTableLastChanged=mplsFTNTableLastChanged, mplsFTNTable=mplsFTNTable, mplsFTNEntry=mplsFTNEntry, mplsFTNIndex=mplsFTNIndex, mplsFTNRowStatus=mplsFTNRowStatus, mplsFTNDescr=mplsFTNDescr, mplsFTNMask=mplsFTNMask, mplsFTNAddrType=mplsFTNAddrType, mplsFTNSourceAddrMin=mplsFTNSourceAddrMin, mplsFTNSourceAddrMax=mplsFTNSourceAddrMax, mplsFTNDestAddrMin=mplsFTNDestAddrMin, mplsFTNDestAddrMax=mplsFTNDestAddrMax, mplsFTNSourcePortMin=mplsFTNSourcePortMin, mplsFTNSourcePortMax=mplsFTNSourcePortMax, mplsFTNDestPortMin=mplsFTNDestPortMin, mplsFTNDestPortMax=mplsFTNDestPortMax, mplsFTNProtocol=mplsFTNProtocol, mplsFTNDscp=mplsFTNDscp, mplsFTNActionType=mplsFTNActionType, mplsFTNActionPointer=mplsFTNActionPointer, mplsFTNStorageType=mplsFTNStorageType, mplsFTNMapTableLastChanged=mplsFTNMapTableLastChanged, mplsFTNMapTable=mplsFTNMapTable, mplsFTNMapEntry=mplsFTNMapEntry, mplsFTNMapIndex=mplsFTNMapIndex, mplsFTNMapPrevIndex=mplsFTNMapPrevIndex, mplsFTNMapCurrIndex=mplsFTNMapCurrIndex, mplsFTNMapRowStatus=mplsFTNMapRowStatus, mplsFTNMapStorageType=mplsFTNMapStorageType, mplsFTNPerfTable=mplsFTNPerfTable, mplsFTNPerfEntry=mplsFTNPerfEntry, mplsFTNPerfIndex=mplsFTNPerfIndex, mplsFTNPerfCurrIndex=mplsFTNPerfCurrIndex, mplsFTNPerfMatchedPackets=mplsFTNPerfMatchedPackets, mplsFTNPerfMatchedOctets=mplsFTNPerfMatchedOctets, mplsFTNPerfDiscontinuityTime=mplsFTNPerfDiscontinuityTime, mplsFTNConformance=mplsFTNConformance, mplsFTNGroups=mplsFTNGroups, mplsFTNCompliances=mplsFTNCompliances)

# Groups
mibBuilder.exportSymbols("MPLS-FTN-STD-MIB", mplsFTNRuleGroup=mplsFTNRuleGroup, mplsFTNMapGroup=mplsFTNMapGroup, mplsFTNPerfGroup=mplsFTNPerfGroup)

# Compliances
mibBuilder.exportSymbols("MPLS-FTN-STD-MIB", mplsFTNModuleFullCompliance=mplsFTNModuleFullCompliance, mplsFTNModuleReadOnlyCompliance=mplsFTNModuleReadOnlyCompliance)
