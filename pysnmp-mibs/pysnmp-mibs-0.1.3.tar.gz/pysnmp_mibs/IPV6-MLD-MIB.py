# PySNMP SMI module. Autogenerated from smidump -f python IPV6-MLD-MIB
# by libsmi2pysnmp-0.1.3 at Mon Apr  2 20:39:13 2012,
# Python version sys.version_info(major=2, minor=7, micro=2, releaselevel='final', serial=0)

# Imports

( Integer, ObjectIdentifier, OctetString, ) = mibBuilder.importSymbols("ASN1", "Integer", "ObjectIdentifier", "OctetString")
( NamedValues, ) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
( ConstraintsIntersection, ConstraintsUnion, SingleValueConstraint, ValueRangeConstraint, ValueSizeConstraint, ) = mibBuilder.importSymbols("ASN1-REFINEMENT", "ConstraintsIntersection", "ConstraintsUnion", "SingleValueConstraint", "ValueRangeConstraint", "ValueSizeConstraint")
( InterfaceIndex, InterfaceIndexOrZero, ) = mibBuilder.importSymbols("IF-MIB", "InterfaceIndex", "InterfaceIndexOrZero")
( InetAddressIPv6, ) = mibBuilder.importSymbols("INET-ADDRESS-MIB", "InetAddressIPv6")
( ModuleCompliance, ObjectGroup, ) = mibBuilder.importSymbols("SNMPv2-CONF", "ModuleCompliance", "ObjectGroup")
( Bits, Counter32, Gauge32, Integer32, ModuleIdentity, MibIdentifier, MibScalar, MibTable, MibTableRow, MibTableColumn, TimeTicks, TimeTicks, Unsigned32, mib_2, ) = mibBuilder.importSymbols("SNMPv2-SMI", "Bits", "Counter32", "Gauge32", "Integer32", "ModuleIdentity", "MibIdentifier", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "TimeTicks", "TimeTicks", "Unsigned32", "mib-2")
( RowStatus, TruthValue, ) = mibBuilder.importSymbols("SNMPv2-TC", "RowStatus", "TruthValue")

# Objects

mldMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 91)).setRevisions(("2001-01-25 00:00",))
if mibBuilder.loadTexts: mldMIB.setOrganization("IETF IPNGWG Working Group.")
if mibBuilder.loadTexts: mldMIB.setContactInfo(" Brian Haberman\nNortel Networks\n4309 Emperor Blvd.\nDurham, NC  27703\nUSA\n\nPhone: +1 919 992 4439\ne-mail: haberman@nortelnetworks.com")
if mibBuilder.loadTexts: mldMIB.setDescription("The MIB module for MLD Management.")
mldMIBObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 91, 1))
mldInterfaceTable = MibTable((1, 3, 6, 1, 2, 1, 91, 1, 1))
if mibBuilder.loadTexts: mldInterfaceTable.setDescription("The (conceptual) table listing the interfaces on which\nMLD is enabled.")
mldInterfaceEntry = MibTableRow((1, 3, 6, 1, 2, 1, 91, 1, 1, 1)).setIndexNames((0, "IPV6-MLD-MIB", "mldInterfaceIfIndex"))
if mibBuilder.loadTexts: mldInterfaceEntry.setDescription("An entry (conceptual row) representing an interface on\nwhich MLD is enabled.")
mldInterfaceIfIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 91, 1, 1, 1, 1), InterfaceIndex()).setMaxAccess("noaccess")
if mibBuilder.loadTexts: mldInterfaceIfIndex.setDescription("The internetwork-layer interface value of the interface\nfor which MLD is enabled.")
mldInterfaceQueryInterval = MibTableColumn((1, 3, 6, 1, 2, 1, 91, 1, 1, 1, 2), Unsigned32().clone(125)).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mldInterfaceQueryInterval.setDescription("The frequency at which MLD Host-Query packets are\ntransmitted on this interface.")
mldInterfaceStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 91, 1, 1, 1, 3), RowStatus()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mldInterfaceStatus.setDescription("The activation of a row enables MLD on the interface.\nThe destruction of a row disables MLD on the interface.")
mldInterfaceVersion = MibTableColumn((1, 3, 6, 1, 2, 1, 91, 1, 1, 1, 4), Unsigned32().clone(1)).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mldInterfaceVersion.setDescription("The version of MLD which is running on this interface.\nThis object is a place holder to allow for new versions\nof MLD to be introduced.  Version 1 of MLD is defined\nin RFC 2710.")
mldInterfaceQuerier = MibTableColumn((1, 3, 6, 1, 2, 1, 91, 1, 1, 1, 5), InetAddressIPv6().subtype(subtypeSpec=ValueSizeConstraint(16, 16)).setFixedLength(16)).setMaxAccess("readonly")
if mibBuilder.loadTexts: mldInterfaceQuerier.setDescription("The address of the MLD Querier on the IPv6 subnet to\nwhich this interface is attached.")
mldInterfaceQueryMaxResponseDelay = MibTableColumn((1, 3, 6, 1, 2, 1, 91, 1, 1, 1, 6), Unsigned32().clone(10)).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mldInterfaceQueryMaxResponseDelay.setDescription("The maximum query response time advertised in MLD\nqueries on this interface.")
mldInterfaceJoins = MibTableColumn((1, 3, 6, 1, 2, 1, 91, 1, 1, 1, 7), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: mldInterfaceJoins.setDescription("The number of times a group membership has been added on\nthis interface; that is, the number of times an entry for\nthis interface has been added to the Cache Table.  This\nobject gives an indication of the amount of MLD activity\nover time.")
mldInterfaceGroups = MibTableColumn((1, 3, 6, 1, 2, 1, 91, 1, 1, 1, 8), Gauge32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: mldInterfaceGroups.setDescription("The current number of entries for this interface in the\nCache Table.")
mldInterfaceRobustness = MibTableColumn((1, 3, 6, 1, 2, 1, 91, 1, 1, 1, 9), Unsigned32().clone(2)).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mldInterfaceRobustness.setDescription("The Robustness Variable allows tuning for the expected\npacket loss on a subnet.  If a subnet is expected to be\nlossy, the Robustness Variable may be increased.  MLD is\nrobust to (Robustness Variable-1) packet losses.  The\ndiscussion of the Robustness Variable is in Section 7.1\nof RFC 2710.")
mldInterfaceLastListenQueryIntvl = MibTableColumn((1, 3, 6, 1, 2, 1, 91, 1, 1, 1, 10), Unsigned32().clone(1)).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mldInterfaceLastListenQueryIntvl.setDescription("The Last Member Query Interval is the Max Response\nDelay inserted into Group-Specific Queries sent in\nresponse to Leave Group messages, and is also the amount\nof time between Group-Specific Query messages.  This\nvalue may be tuned to modify the leave latency of the\nnetwork.  A reduced value results in reduced time to\ndetect the loss of the last member of a group.")
mldInterfaceProxyIfIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 91, 1, 1, 1, 11), InterfaceIndexOrZero().clone('0')).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mldInterfaceProxyIfIndex.setDescription("Some devices implement a form of MLD proxying whereby\nmemberships learned on the interface represented by this\nrow, cause MLD Multicast Listener Reports to be sent on\nthe internetwork-layer interface identified by this\nobject.  Such a device would implement mldRouterMIBGroup\nonly on its router interfaces (those interfaces with\nnon-zero mldInterfaceProxyIfIndex).  Typically, the\nvalue of this object is 0, indicating that no proxying\nis being done.")
mldInterfaceQuerierUpTime = MibTableColumn((1, 3, 6, 1, 2, 1, 91, 1, 1, 1, 12), TimeTicks()).setMaxAccess("readonly")
if mibBuilder.loadTexts: mldInterfaceQuerierUpTime.setDescription("The time since mldInterfaceQuerier was last changed.")
mldInterfaceQuerierExpiryTime = MibTableColumn((1, 3, 6, 1, 2, 1, 91, 1, 1, 1, 13), TimeTicks()).setMaxAccess("readonly")
if mibBuilder.loadTexts: mldInterfaceQuerierExpiryTime.setDescription("The time remaining before the Other Querier Present\nTimer expires.  If the local system is the querier,\nthe value of this object is zero.")
mldCacheTable = MibTable((1, 3, 6, 1, 2, 1, 91, 1, 2))
if mibBuilder.loadTexts: mldCacheTable.setDescription("The (conceptual) table listing the IPv6 multicast\n\n\ngroups for which there are members on a particular\ninterface.")
mldCacheEntry = MibTableRow((1, 3, 6, 1, 2, 1, 91, 1, 2, 1)).setIndexNames((0, "IPV6-MLD-MIB", "mldCacheAddress"), (0, "IPV6-MLD-MIB", "mldCacheIfIndex"))
if mibBuilder.loadTexts: mldCacheEntry.setDescription("An entry (conceptual row) in the mldCacheTable.")
mldCacheAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 91, 1, 2, 1, 1), InetAddressIPv6().subtype(subtypeSpec=ValueSizeConstraint(16, 16)).setFixedLength(16)).setMaxAccess("noaccess")
if mibBuilder.loadTexts: mldCacheAddress.setDescription("The IPv6 multicast group address for which this entry\ncontains information.")
mldCacheIfIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 91, 1, 2, 1, 2), InterfaceIndex()).setMaxAccess("noaccess")
if mibBuilder.loadTexts: mldCacheIfIndex.setDescription("The internetwork-layer interface for which this entry\ncontains information for an IPv6 multicast group\naddress.")
mldCacheSelf = MibTableColumn((1, 3, 6, 1, 2, 1, 91, 1, 2, 1, 3), TruthValue().clone('true')).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mldCacheSelf.setDescription("An indication of whether the local system is a member of\n\n\nthis group address on this interface.")
mldCacheLastReporter = MibTableColumn((1, 3, 6, 1, 2, 1, 91, 1, 2, 1, 4), InetAddressIPv6().subtype(subtypeSpec=ValueSizeConstraint(16, 16)).setFixedLength(16)).setMaxAccess("readonly")
if mibBuilder.loadTexts: mldCacheLastReporter.setDescription("The IPv6 address of the source of the last membership\nreport received for this IPv6 Multicast group address on\nthis interface.  If no membership report has been\nreceived, this object has the value 0::0.")
mldCacheUpTime = MibTableColumn((1, 3, 6, 1, 2, 1, 91, 1, 2, 1, 5), TimeTicks()).setMaxAccess("readonly")
if mibBuilder.loadTexts: mldCacheUpTime.setDescription("The time elapsed since this entry was created.")
mldCacheExpiryTime = MibTableColumn((1, 3, 6, 1, 2, 1, 91, 1, 2, 1, 6), TimeTicks()).setMaxAccess("readonly")
if mibBuilder.loadTexts: mldCacheExpiryTime.setDescription("The minimum amount of time remaining before this entry\nwill be aged out.  A value of 0 indicates that the entry\nis only present because mldCacheSelf is true and that if\nthe router left the group, this entry would be aged out\nimmediately.  Note that some implementations may process\nMembership Reports from the local system in the same way\nas reports from other hosts, so a value of 0 is not\nrequired.")
mldCacheStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 91, 1, 2, 1, 7), RowStatus()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: mldCacheStatus.setDescription("The status of this row, by which new entries may be\ncreated, or existing entries deleted from this table.")
mldMIBConformance = MibIdentifier((1, 3, 6, 1, 2, 1, 91, 2))
mldMIBCompliances = MibIdentifier((1, 3, 6, 1, 2, 1, 91, 2, 1))
mldMIBGroups = MibIdentifier((1, 3, 6, 1, 2, 1, 91, 2, 2))

# Augmentions

# Groups

mldBaseMIBGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 91, 2, 2, 1)).setObjects(*(("IPV6-MLD-MIB", "mldCacheStatus"), ("IPV6-MLD-MIB", "mldInterfaceStatus"), ("IPV6-MLD-MIB", "mldCacheSelf"), ) )
if mibBuilder.loadTexts: mldBaseMIBGroup.setDescription("The basic collection of objects providing management of\nMLD.  The mldBaseMIBGroup is designed to allow for the\nmanager creation and deletion of MLD cache entries.")
mldRouterMIBGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 91, 2, 2, 2)).setObjects(*(("IPV6-MLD-MIB", "mldInterfaceQuerierExpiryTime"), ("IPV6-MLD-MIB", "mldInterfaceQueryInterval"), ("IPV6-MLD-MIB", "mldInterfaceVersion"), ("IPV6-MLD-MIB", "mldInterfaceQuerierUpTime"), ("IPV6-MLD-MIB", "mldCacheUpTime"), ("IPV6-MLD-MIB", "mldInterfaceQuerier"), ("IPV6-MLD-MIB", "mldCacheLastReporter"), ("IPV6-MLD-MIB", "mldInterfaceGroups"), ("IPV6-MLD-MIB", "mldInterfaceJoins"), ("IPV6-MLD-MIB", "mldCacheExpiryTime"), ("IPV6-MLD-MIB", "mldInterfaceRobustness"), ("IPV6-MLD-MIB", "mldInterfaceQueryMaxResponseDelay"), ("IPV6-MLD-MIB", "mldInterfaceLastListenQueryIntvl"), ) )
if mibBuilder.loadTexts: mldRouterMIBGroup.setDescription("A collection of additional objects for management of MLD\nin routers.")
mldHostMIBGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 91, 2, 2, 3)).setObjects(*(("IPV6-MLD-MIB", "mldInterfaceQuerier"), ) )
if mibBuilder.loadTexts: mldHostMIBGroup.setDescription("A collection of additional objects for management of MLD\nin hosts.")
mldProxyMIBGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 91, 2, 2, 4)).setObjects(*(("IPV6-MLD-MIB", "mldInterfaceProxyIfIndex"), ) )
if mibBuilder.loadTexts: mldProxyMIBGroup.setDescription("A collection of additional objects for management of MLD\nproxy devices.")

# Compliances

mldHostMIBCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 91, 2, 1, 1)).setObjects(*(("IPV6-MLD-MIB", "mldBaseMIBGroup"), ("IPV6-MLD-MIB", "mldHostMIBGroup"), ) )
if mibBuilder.loadTexts: mldHostMIBCompliance.setDescription("The compliance statement for hosts running MLD and\nimplementing the MLD MIB.")
mldRouterMIBCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 91, 2, 1, 2)).setObjects(*(("IPV6-MLD-MIB", "mldBaseMIBGroup"), ("IPV6-MLD-MIB", "mldRouterMIBGroup"), ) )
if mibBuilder.loadTexts: mldRouterMIBCompliance.setDescription("The compliance statement for routers running MLD and\nimplementing the MLD MIB.")

# Exports

# Module identity
mibBuilder.exportSymbols("IPV6-MLD-MIB", PYSNMP_MODULE_ID=mldMIB)

# Objects
mibBuilder.exportSymbols("IPV6-MLD-MIB", mldMIB=mldMIB, mldMIBObjects=mldMIBObjects, mldInterfaceTable=mldInterfaceTable, mldInterfaceEntry=mldInterfaceEntry, mldInterfaceIfIndex=mldInterfaceIfIndex, mldInterfaceQueryInterval=mldInterfaceQueryInterval, mldInterfaceStatus=mldInterfaceStatus, mldInterfaceVersion=mldInterfaceVersion, mldInterfaceQuerier=mldInterfaceQuerier, mldInterfaceQueryMaxResponseDelay=mldInterfaceQueryMaxResponseDelay, mldInterfaceJoins=mldInterfaceJoins, mldInterfaceGroups=mldInterfaceGroups, mldInterfaceRobustness=mldInterfaceRobustness, mldInterfaceLastListenQueryIntvl=mldInterfaceLastListenQueryIntvl, mldInterfaceProxyIfIndex=mldInterfaceProxyIfIndex, mldInterfaceQuerierUpTime=mldInterfaceQuerierUpTime, mldInterfaceQuerierExpiryTime=mldInterfaceQuerierExpiryTime, mldCacheTable=mldCacheTable, mldCacheEntry=mldCacheEntry, mldCacheAddress=mldCacheAddress, mldCacheIfIndex=mldCacheIfIndex, mldCacheSelf=mldCacheSelf, mldCacheLastReporter=mldCacheLastReporter, mldCacheUpTime=mldCacheUpTime, mldCacheExpiryTime=mldCacheExpiryTime, mldCacheStatus=mldCacheStatus, mldMIBConformance=mldMIBConformance, mldMIBCompliances=mldMIBCompliances, mldMIBGroups=mldMIBGroups)

# Groups
mibBuilder.exportSymbols("IPV6-MLD-MIB", mldBaseMIBGroup=mldBaseMIBGroup, mldRouterMIBGroup=mldRouterMIBGroup, mldHostMIBGroup=mldHostMIBGroup, mldProxyMIBGroup=mldProxyMIBGroup)

# Compliances
mibBuilder.exportSymbols("IPV6-MLD-MIB", mldHostMIBCompliance=mldHostMIBCompliance, mldRouterMIBCompliance=mldRouterMIBCompliance)
