# PySNMP SMI module. Autogenerated from smidump -f python RADIUS-DYNAUTH-SERVER-MIB
# by libsmi2pysnmp-0.1.3 at Mon Apr  2 20:39:31 2012,
# Python version sys.version_info(major=2, minor=7, micro=2, releaselevel='final', serial=0)

# Imports

( Integer, ObjectIdentifier, OctetString, ) = mibBuilder.importSymbols("ASN1", "Integer", "ObjectIdentifier", "OctetString")
( NamedValues, ) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
( ConstraintsIntersection, ConstraintsUnion, SingleValueConstraint, ValueRangeConstraint, ValueSizeConstraint, ) = mibBuilder.importSymbols("ASN1-REFINEMENT", "ConstraintsIntersection", "ConstraintsUnion", "SingleValueConstraint", "ValueRangeConstraint", "ValueSizeConstraint")
( InetAddress, InetAddressType, ) = mibBuilder.importSymbols("INET-ADDRESS-MIB", "InetAddress", "InetAddressType")
( SnmpAdminString, ) = mibBuilder.importSymbols("SNMP-FRAMEWORK-MIB", "SnmpAdminString")
( ModuleCompliance, ObjectGroup, ) = mibBuilder.importSymbols("SNMPv2-CONF", "ModuleCompliance", "ObjectGroup")
( Bits, Counter32, Integer32, Integer32, ModuleIdentity, MibIdentifier, MibScalar, MibTable, MibTableRow, MibTableColumn, TimeTicks, TimeTicks, mib_2, ) = mibBuilder.importSymbols("SNMPv2-SMI", "Bits", "Counter32", "Integer32", "Integer32", "ModuleIdentity", "MibIdentifier", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "TimeTicks", "TimeTicks", "mib-2")

# Objects

radiusDynAuthServerMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 146)).setRevisions(("2006-08-29 00:00",))
if mibBuilder.loadTexts: radiusDynAuthServerMIB.setOrganization("IETF RADEXT Working Group")
if mibBuilder.loadTexts: radiusDynAuthServerMIB.setContactInfo(" Stefaan De Cnodder\nAlcatel\nFrancis Wellesplein 1\nB-2018 Antwerp\nBelgium\n\nPhone: +32 3 240 85 15\nEMail: stefaan.de_cnodder@alcatel.be\n\nNagi Reddy Jonnala\nCisco Systems, Inc.\nDivyasree Chambers, B Wing,\nO'Shaugnessy Road,\nBangalore-560027, India.\n\nPhone: +91 94487 60828\nEMail: njonnala@cisco.com\n\nMurtaza Chiba\nCisco Systems, Inc.\n170 West Tasman Dr.\nSan Jose CA, 95134\n\nPhone: +1 408 525 7198\nEMail: mchiba@cisco.com ")
if mibBuilder.loadTexts: radiusDynAuthServerMIB.setDescription("The MIB module for entities implementing the server\nside of the Dynamic Authorization Extensions to the\nRemote Authentication Dial-In User Service (RADIUS)\nprotocol.  Copyright (C) The Internet Society (2006).\n\n\n\nInitial version as published in RFC 4673; for full\nlegal notices see the RFC itself.")
radiusDynAuthServerMIBObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 146, 1))
radiusDynAuthServerScalars = MibIdentifier((1, 3, 6, 1, 2, 1, 146, 1, 1))
radiusDynAuthServerDisconInvalidClientAddresses = MibScalar((1, 3, 6, 1, 2, 1, 146, 1, 1, 1), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServerDisconInvalidClientAddresses.setDescription("The number of Disconnect-Request packets received from\nunknown addresses.  This counter may experience a\ndiscontinuity when the DAS module (re)starts, as\nindicated by the value of\nradiusDynAuthServerCounterDiscontinuity.")
radiusDynAuthServerCoAInvalidClientAddresses = MibScalar((1, 3, 6, 1, 2, 1, 146, 1, 1, 2), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServerCoAInvalidClientAddresses.setDescription("The number of CoA-Request packets received from unknown\naddresses.  This counter may experience a discontinuity\nwhen the DAS module (re)starts, as indicated by the\nvalue of radiusDynAuthServerCounterDiscontinuity.")
radiusDynAuthServerIdentifier = MibScalar((1, 3, 6, 1, 2, 1, 146, 1, 1, 3), SnmpAdminString()).setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServerIdentifier.setDescription("The NAS-Identifier of the RADIUS Dynamic Authorization\nServer.  This is not necessarily the same as sysName in\nMIB II.")
radiusDynAuthClientTable = MibTable((1, 3, 6, 1, 2, 1, 146, 1, 2))
if mibBuilder.loadTexts: radiusDynAuthClientTable.setDescription("The (conceptual) table listing the RADIUS Dynamic\nAuthorization Clients with which the server shares a\nsecret.")
radiusDynAuthClientEntry = MibTableRow((1, 3, 6, 1, 2, 1, 146, 1, 2, 1)).setIndexNames((0, "RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthClientIndex"))
if mibBuilder.loadTexts: radiusDynAuthClientEntry.setDescription("An entry (conceptual row) representing one Dynamic\nAuthorization Client with which the server shares a\nsecret.")
radiusDynAuthClientIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647))).setMaxAccess("noaccess")
if mibBuilder.loadTexts: radiusDynAuthClientIndex.setDescription("A number uniquely identifying each RADIUS Dynamic\nAuthorization Client with which this Dynamic\nAuthorization Server communicates.  This number is\nallocated by the agent implementing this MIB module\nand is unique in this context.")
radiusDynAuthClientAddressType = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 2), InetAddressType()).setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthClientAddressType.setDescription("The type of IP address of the RADIUS Dynamic\nAuthorization Client referred to in this table entry.")
radiusDynAuthClientAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 3), InetAddress()).setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthClientAddress.setDescription("The IP address value of the RADIUS Dynamic\nAuthorization Client referred to in this table entry,\nusing the version neutral IP address format.  The type\nof this address is determined by the value of\nthe radiusDynAuthClientAddressType object.")
radiusDynAuthServDisconRequests = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 4), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServDisconRequests.setDescription("The number of RADIUS Disconnect-Requests received\nfrom this Dynamic Authorization Client.  This also\nincludes the RADIUS Disconnect-Requests that have a\nService-Type attribute with value 'Authorize Only'.\nThis counter may experience a discontinuity when the\n\n\n\nDAS module (re)starts as indicated by the value of\nradiusDynAuthServerCounterDiscontinuity.")
radiusDynAuthServDisconAuthOnlyRequests = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 5), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServDisconAuthOnlyRequests.setDescription("The number of RADIUS Disconnect-Requests that include\na Service-Type attribute with value 'Authorize Only'\nreceived from this Dynamic Authorization Client.  This\ncounter may experience a discontinuity when the DAS\nmodule (re)starts, as indicated by the value of\nradiusDynAuthServerCounterDiscontinuity.")
radiusDynAuthServDupDisconRequests = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 6), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServDupDisconRequests.setDescription("The number of duplicate RADIUS Disconnect-Request\npackets received from this Dynamic Authorization\nClient.  This counter may experience a discontinuity\nwhen the DAS module (re)starts, as indicated by the\nvalue of radiusDynAuthServerCounterDiscontinuity.")
radiusDynAuthServDisconAcks = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 7), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServDisconAcks.setDescription("The number of RADIUS Disconnect-ACK packets sent to\nthis Dynamic Authorization Client.  This counter may\nexperience a discontinuity when the DAS module\n(re)starts, as indicated by the value of\nradiusDynAuthServerCounterDiscontinuity.")
radiusDynAuthServDisconNaks = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 8), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServDisconNaks.setDescription("The number of RADIUS Disconnect-NAK packets\nsent to this Dynamic Authorization Client.  This\nincludes the RADIUS Disconnect-NAK packets sent\nwith a Service-Type attribute with value 'Authorize\nOnly' and the RADIUS Disconnect-NAK packets sent\nbecause no session context was found.  This counter\nmay experience a discontinuity when the DAS module\n(re)starts, as indicated by the value of\nradiusDynAuthServerCounterDiscontinuity.")
radiusDynAuthServDisconNakAuthOnlyRequests = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 9), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServDisconNakAuthOnlyRequests.setDescription("The number of RADIUS Disconnect-NAK packets that\ninclude a Service-Type attribute with value\n'Authorize Only' sent to this Dynamic Authorization\nClient.  This counter may experience a discontinuity\nwhen the DAS module (re)starts, as indicated by the\nvalue of radiusDynAuthServerCounterDiscontinuity.")
radiusDynAuthServDisconNakSessNoContext = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 10), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServDisconNakSessNoContext.setDescription("The number of RADIUS Disconnect-NAK packets\nsent to this Dynamic Authorization Client\nbecause no session context was found.  This counter may\n\n\n\nexperience a discontinuity when the DAS module\n(re)starts, as indicated by the value of\nradiusDynAuthServerCounterDiscontinuity.")
radiusDynAuthServDisconUserSessRemoved = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 11), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServDisconUserSessRemoved.setDescription("The number of user sessions removed for the\nDisconnect-Requests received from this\nDynamic Authorization Client.  Depending on site-\nspecific policies, a single Disconnect request\ncan remove multiple user sessions.  In cases where\nthis Dynamic Authorization Server has no\nknowledge of the number of user sessions that\nare affected by a single request, each such\nDisconnect-Request will count as a single\naffected user session only.  This counter may experience\na discontinuity when the DAS module (re)starts, as\nindicated by the value of\nradiusDynAuthServerCounterDiscontinuity.")
radiusDynAuthServMalformedDisconRequests = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 12), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServMalformedDisconRequests.setDescription("The number of malformed RADIUS Disconnect-Request\npackets received from this Dynamic Authorization\nClient.  Bad authenticators and unknown types are not\nincluded as malformed Disconnect-Requests.  This counter\nmay experience a discontinuity when the DAS module\n(re)starts, as indicated by the value of\nradiusDynAuthServerCounterDiscontinuity.")
radiusDynAuthServDisconBadAuthenticators = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 13), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServDisconBadAuthenticators.setDescription("The number of RADIUS Disconnect-Request packets\nthat contained an invalid Authenticator field\nreceived from this Dynamic Authorization Client.  This\ncounter may experience a discontinuity when the DAS\nmodule (re)starts, as indicated by the value of\nradiusDynAuthServerCounterDiscontinuity.")
radiusDynAuthServDisconPacketsDropped = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 14), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServDisconPacketsDropped.setDescription("The number of incoming Disconnect-Requests\nfrom this Dynamic Authorization Client silently\ndiscarded by the server application for some reason\nother than malformed, bad authenticators, or unknown\ntypes.  This counter may experience a discontinuity\nwhen the DAS module (re)starts, as indicated by the\nvalue of radiusDynAuthServerCounterDiscontinuity.")
radiusDynAuthServCoARequests = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 15), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServCoARequests.setDescription("The number of RADIUS CoA-requests received from this\nDynamic Authorization Client.  This also includes\nthe CoA requests that have a Service-Type attribute\nwith value 'Authorize Only'.  This counter may\nexperience a discontinuity when the DAS module\n(re)starts, as indicated by the value of\nradiusDynAuthServerCounterDiscontinuity.")
radiusDynAuthServCoAAuthOnlyRequests = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 16), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServCoAAuthOnlyRequests.setDescription("The number of RADIUS CoA-requests that include a\nService-Type attribute with value 'Authorize Only'\nreceived from this Dynamic Authorization Client.  This\ncounter may experience a discontinuity when the DAS\nmodule (re)starts, as indicated by the value of\nradiusDynAuthServerCounterDiscontinuity.")
radiusDynAuthServDupCoARequests = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 17), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServDupCoARequests.setDescription("The number of duplicate RADIUS CoA-Request packets\nreceived from this Dynamic Authorization Client.  This\ncounter may experience a discontinuity when the DAS\nmodule (re)starts, as indicated by the value of\nradiusDynAuthServerCounterDiscontinuity.")
radiusDynAuthServCoAAcks = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 18), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServCoAAcks.setDescription("The number of RADIUS CoA-ACK packets sent to this\nDynamic Authorization Client.  This counter may\nexperience a discontinuity when the DAS module\n\n\n\n(re)starts, as indicated by the value of\nradiusDynAuthServerCounterDiscontinuity.")
radiusDynAuthServCoANaks = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 19), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServCoANaks.setDescription("The number of RADIUS CoA-NAK packets sent to\nthis Dynamic Authorization Client.  This includes\nthe RADIUS CoA-NAK packets sent with a Service-Type\nattribute with value 'Authorize Only' and the RADIUS\nCoA-NAK packets sent because no session context was\nfound.  This counter may experience a discontinuity\nwhen the DAS module (re)starts, as indicated by the\nvalue of radiusDynAuthServerCounterDiscontinuity.")
radiusDynAuthServCoANakAuthOnlyRequests = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 20), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServCoANakAuthOnlyRequests.setDescription("The number of RADIUS CoA-NAK packets that include a\nService-Type attribute with value 'Authorize Only'\nsent to this Dynamic Authorization Client.  This counter\nmay experience a discontinuity when the DAS module\n(re)starts, as indicated by the value of\nradiusDynAuthServerCounterDiscontinuity.")
radiusDynAuthServCoANakSessNoContext = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 21), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServCoANakSessNoContext.setDescription("The number of RADIUS CoA-NAK packets sent to this\nDynamic Authorization Client because no session context\nwas found.  This counter may experience a discontinuity\nwhen the DAS module (re)starts, as indicated by the\nvalue of radiusDynAuthServerCounterDiscontinuity.")
radiusDynAuthServCoAUserSessChanged = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 22), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServCoAUserSessChanged.setDescription("The number of user sessions authorization\nchanged for the CoA-Requests received from this\nDynamic Authorization Client.  Depending on site-\nspecific policies, a single CoA request can change\nmultiple user sessions' authorization.  In cases where\nthis Dynamic Authorization Server has no knowledge of\nthe number of user sessions that are affected by a\nsingle request, each such CoA-Request will\ncount as a single affected user session only.  This\ncounter may experience a discontinuity when the DAS\nmodule (re)starts, as indicated by the value of\nradiusDynAuthServerCounterDiscontinuity.")
radiusDynAuthServMalformedCoARequests = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 23), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServMalformedCoARequests.setDescription("The number of malformed RADIUS CoA-Request packets\nreceived from this Dynamic Authorization Client.  Bad\nauthenticators and unknown types are not included as\nmalformed CoA-Requests.  This counter may experience a\ndiscontinuity when the DAS module (re)starts, as\nindicated by the value of\nradiusDynAuthServerCounterDiscontinuity.")
radiusDynAuthServCoABadAuthenticators = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 24), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServCoABadAuthenticators.setDescription("The number of RADIUS CoA-Request packets that\ncontained an invalid Authenticator field received\nfrom this Dynamic Authorization Client.  This counter\nmay experience a discontinuity when the DAS module\n(re)starts, as indicated by the value of\n  radiusDynAuthServerCounterDiscontinuity.")
radiusDynAuthServCoAPacketsDropped = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 25), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServCoAPacketsDropped.setDescription("The number of incoming CoA packets from this\nDynamic Authorization Client silently discarded\nby the server application for some reason other than\nmalformed, bad authenticators, or unknown types.  This\ncounter may experience a discontinuity when the DAS\nmodule (re)starts, as indicated by the value of\nradiusDynAuthServerCounterDiscontinuity.")
radiusDynAuthServUnknownTypes = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 26), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServUnknownTypes.setDescription("The number of incoming packets of unknown types that\nwere received on the Dynamic Authorization port.  This\ncounter may experience a discontinuity when the DAS\n\n\n\nmodule (re)starts, as indicated by the value of\nradiusDynAuthServerCounterDiscontinuity.")
radiusDynAuthServerCounterDiscontinuity = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 27), TimeTicks()).setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServerCounterDiscontinuity.setDescription("The time (in hundredths of a second) since the\nlast counter discontinuity.  A discontinuity may\nbe the result of a reinitialization of the DAS\nmodule within the managed entity.")
radiusDynAuthServerMIBConformance = MibIdentifier((1, 3, 6, 1, 2, 1, 146, 2))
radiusDynAuthServerMIBCompliances = MibIdentifier((1, 3, 6, 1, 2, 1, 146, 2, 1))
radiusDynAuthServerMIBGroups = MibIdentifier((1, 3, 6, 1, 2, 1, 146, 2, 2))

# Augmentions

# Groups

radiusDynAuthServerMIBGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 146, 2, 2, 1)).setObjects(*(("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServDisconPacketsDropped"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServDisconUserSessRemoved"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServMalformedDisconRequests"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServCoABadAuthenticators"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthClientAddressType"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServMalformedCoARequests"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServDisconBadAuthenticators"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServerCoAInvalidClientAddresses"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServDisconAcks"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServerCounterDiscontinuity"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServCoAAcks"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServCoANaks"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServDupDisconRequests"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServDupCoARequests"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServUnknownTypes"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthClientAddress"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServerIdentifier"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServCoAPacketsDropped"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServCoARequests"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServCoAUserSessChanged"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServerDisconInvalidClientAddresses"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServDisconRequests"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServDisconNaks"), ) )
if mibBuilder.loadTexts: radiusDynAuthServerMIBGroup.setDescription("The collection of objects providing management of\na RADIUS Dynamic Authorization Server.")
radiusDynAuthServerAuthOnlyGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 146, 2, 2, 2)).setObjects(*(("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServDisconNakAuthOnlyRequests"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServCoAAuthOnlyRequests"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServCoANakAuthOnlyRequests"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServDisconAuthOnlyRequests"), ) )
if mibBuilder.loadTexts: radiusDynAuthServerAuthOnlyGroup.setDescription("The collection of objects supporting the RADIUS\nmessages including Service-Type attribute with\nvalue 'Authorize Only'.")
radiusDynAuthServerNoSessGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 146, 2, 2, 3)).setObjects(*(("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServDisconNakSessNoContext"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServCoANakSessNoContext"), ) )
if mibBuilder.loadTexts: radiusDynAuthServerNoSessGroup.setDescription("The collection of objects supporting the RADIUS\nmessages that are referring to non-existing sessions.")

# Compliances

radiusAuthServerMIBCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 146, 2, 1, 1)).setObjects(*(("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServerAuthOnlyGroup"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServerMIBGroup"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServerNoSessGroup"), ) )
if mibBuilder.loadTexts: radiusAuthServerMIBCompliance.setDescription("The compliance statement for entities implementing\nthe RADIUS Dynamic Authorization Server.  Implementation\nof this module is for entities that support IPv4 and/or\nIPv6.")

# Exports

# Module identity
mibBuilder.exportSymbols("RADIUS-DYNAUTH-SERVER-MIB", PYSNMP_MODULE_ID=radiusDynAuthServerMIB)

# Objects
mibBuilder.exportSymbols("RADIUS-DYNAUTH-SERVER-MIB", radiusDynAuthServerMIB=radiusDynAuthServerMIB, radiusDynAuthServerMIBObjects=radiusDynAuthServerMIBObjects, radiusDynAuthServerScalars=radiusDynAuthServerScalars, radiusDynAuthServerDisconInvalidClientAddresses=radiusDynAuthServerDisconInvalidClientAddresses, radiusDynAuthServerCoAInvalidClientAddresses=radiusDynAuthServerCoAInvalidClientAddresses, radiusDynAuthServerIdentifier=radiusDynAuthServerIdentifier, radiusDynAuthClientTable=radiusDynAuthClientTable, radiusDynAuthClientEntry=radiusDynAuthClientEntry, radiusDynAuthClientIndex=radiusDynAuthClientIndex, radiusDynAuthClientAddressType=radiusDynAuthClientAddressType, radiusDynAuthClientAddress=radiusDynAuthClientAddress, radiusDynAuthServDisconRequests=radiusDynAuthServDisconRequests, radiusDynAuthServDisconAuthOnlyRequests=radiusDynAuthServDisconAuthOnlyRequests, radiusDynAuthServDupDisconRequests=radiusDynAuthServDupDisconRequests, radiusDynAuthServDisconAcks=radiusDynAuthServDisconAcks, radiusDynAuthServDisconNaks=radiusDynAuthServDisconNaks, radiusDynAuthServDisconNakAuthOnlyRequests=radiusDynAuthServDisconNakAuthOnlyRequests, radiusDynAuthServDisconNakSessNoContext=radiusDynAuthServDisconNakSessNoContext, radiusDynAuthServDisconUserSessRemoved=radiusDynAuthServDisconUserSessRemoved, radiusDynAuthServMalformedDisconRequests=radiusDynAuthServMalformedDisconRequests, radiusDynAuthServDisconBadAuthenticators=radiusDynAuthServDisconBadAuthenticators, radiusDynAuthServDisconPacketsDropped=radiusDynAuthServDisconPacketsDropped, radiusDynAuthServCoARequests=radiusDynAuthServCoARequests, radiusDynAuthServCoAAuthOnlyRequests=radiusDynAuthServCoAAuthOnlyRequests, radiusDynAuthServDupCoARequests=radiusDynAuthServDupCoARequests, radiusDynAuthServCoAAcks=radiusDynAuthServCoAAcks, radiusDynAuthServCoANaks=radiusDynAuthServCoANaks, radiusDynAuthServCoANakAuthOnlyRequests=radiusDynAuthServCoANakAuthOnlyRequests, radiusDynAuthServCoANakSessNoContext=radiusDynAuthServCoANakSessNoContext, radiusDynAuthServCoAUserSessChanged=radiusDynAuthServCoAUserSessChanged, radiusDynAuthServMalformedCoARequests=radiusDynAuthServMalformedCoARequests, radiusDynAuthServCoABadAuthenticators=radiusDynAuthServCoABadAuthenticators, radiusDynAuthServCoAPacketsDropped=radiusDynAuthServCoAPacketsDropped, radiusDynAuthServUnknownTypes=radiusDynAuthServUnknownTypes, radiusDynAuthServerCounterDiscontinuity=radiusDynAuthServerCounterDiscontinuity, radiusDynAuthServerMIBConformance=radiusDynAuthServerMIBConformance, radiusDynAuthServerMIBCompliances=radiusDynAuthServerMIBCompliances, radiusDynAuthServerMIBGroups=radiusDynAuthServerMIBGroups)

# Groups
mibBuilder.exportSymbols("RADIUS-DYNAUTH-SERVER-MIB", radiusDynAuthServerMIBGroup=radiusDynAuthServerMIBGroup, radiusDynAuthServerAuthOnlyGroup=radiusDynAuthServerAuthOnlyGroup, radiusDynAuthServerNoSessGroup=radiusDynAuthServerNoSessGroup)

# Compliances
mibBuilder.exportSymbols("RADIUS-DYNAUTH-SERVER-MIB", radiusAuthServerMIBCompliance=radiusAuthServerMIBCompliance)
