# PySNMP SMI module. Autogenerated from smidump -f python DIFFSERV-CONFIG-MIB
# by libsmi2pysnmp-0.1.3 at Mon Apr  2 20:38:47 2012,
# Python version sys.version_info(major=2, minor=7, micro=2, releaselevel='final', serial=0)

# Imports

( Integer, ObjectIdentifier, OctetString, ) = mibBuilder.importSymbols("ASN1", "Integer", "ObjectIdentifier", "OctetString")
( NamedValues, ) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
( ConstraintsIntersection, ConstraintsUnion, SingleValueConstraint, ValueRangeConstraint, ValueSizeConstraint, ) = mibBuilder.importSymbols("ASN1-REFINEMENT", "ConstraintsIntersection", "ConstraintsUnion", "SingleValueConstraint", "ValueRangeConstraint", "ValueSizeConstraint")
( SnmpAdminString, ) = mibBuilder.importSymbols("SNMP-FRAMEWORK-MIB", "SnmpAdminString")
( ModuleCompliance, ObjectGroup, ) = mibBuilder.importSymbols("SNMPv2-CONF", "ModuleCompliance", "ObjectGroup")
( Bits, Integer32, ModuleIdentity, MibIdentifier, MibScalar, MibTable, MibTableRow, MibTableColumn, TimeTicks, mib_2, zeroDotZero, ) = mibBuilder.importSymbols("SNMPv2-SMI", "Bits", "Integer32", "ModuleIdentity", "MibIdentifier", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "TimeTicks", "mib-2", "zeroDotZero")
( DateAndTime, RowPointer, RowStatus, StorageType, ) = mibBuilder.importSymbols("SNMPv2-TC", "DateAndTime", "RowPointer", "RowStatus", "StorageType")

# Objects

diffServConfigMib = ModuleIdentity((1, 3, 6, 1, 2, 1, 108)).setRevisions(("2004-01-22 00:00",))
if mibBuilder.loadTexts: diffServConfigMib.setOrganization("SNMPCONF WG")
if mibBuilder.loadTexts: diffServConfigMib.setContactInfo("SNMPCONF Working Group\nhttp://www.ietf.org/html.charters/snmpconf-charter.html\nWG mailing list: snmpconf@snmp.com\n\nEditors:\nHarrie Hazewinkel\nI.Net\nvia Darwin 85\n20019 - Settimo Milanese (MI)\nItaly\nEMail: harrie@inet.it\n\nDavid Partain\nEricsson AB\nP.O. Box 1248\nSE-581 12 Linkoping\nSweden\nE-mail: David.Partain@ericsson.com")
if mibBuilder.loadTexts: diffServConfigMib.setDescription("This MIB module contains differentiated services\nspecific managed objects to perform higher-level\nconfiguration management.  This MIB allows policies\nto use 'templates' to instantiate Differentiated\nServices functional datapath configurations to\nbe assigned (associated with an interface and\ndirection) when a policy is activated.\n\nCopyright (C) The Internet Society (2004).  This version\nof this MIB module is part of RFC 3747;  see the RFC\nitself for full legal notices.")
diffServConfigMIBObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 108, 1))
diffServConfigTable = MibTable((1, 3, 6, 1, 2, 1, 108, 1, 2))
if mibBuilder.loadTexts: diffServConfigTable.setDescription("A table which defines the various per-hop-behaviors\nfor which the system has default 'templates'.")
diffServConfigEntry = MibTableRow((1, 3, 6, 1, 2, 1, 108, 1, 2, 1)).setIndexNames((0, "DIFFSERV-CONFIG-MIB", "diffServConfigId"))
if mibBuilder.loadTexts: diffServConfigEntry.setDescription("An entry defining a per-hop-behavior.  Each entry in\nthis table combines the various parameters (entries)\ninto a specific per-hop-behavior.  Entries in this\ntable might be defined by a vendor (pre-configured)\nor defined by a management application.")
diffServConfigId = MibTableColumn((1, 3, 6, 1, 2, 1, 108, 1, 2, 1, 1), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(1, 116))).setMaxAccess("noaccess")
if mibBuilder.loadTexts: diffServConfigId.setDescription("A unique id for the per-hop-behavior policy for at\nleast the SNMP agent.  For ease of administration the\nvalue may be unique within an administrative domain,\nbut this is not required.\n\nThe range of up to 116 octets is chosen to stay within\nthe SMI limit of 128 sub-identifiers in an object\nidentifier.")
diffServConfigDescr = MibTableColumn((1, 3, 6, 1, 2, 1, 108, 1, 2, 1, 2), SnmpAdminString()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: diffServConfigDescr.setDescription("A human-readable description to identify this defined\nper-hop-behavior.  Note that this is an SnmpAdminString,\nwhich permits UTF-8 strings.  An administratively assigned\nidentifier for a template that would be unique within\nan administrative domain.  It is up to the management\napplications to agree how these are assigned within the\nadministrative domain.  Once a description, such as\n'EF' is assigned, that has a certain set of parameters\nthat achieve 'EF' from box to box. Management\napplication code or script code can then scan\nthe table to find the proper template and then\nassign it.")
diffServConfigOwner = MibTableColumn((1, 3, 6, 1, 2, 1, 108, 1, 2, 1, 3), SnmpAdminString()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: diffServConfigOwner.setDescription("The owner who created this entry.")
diffServConfigLastChange = MibTableColumn((1, 3, 6, 1, 2, 1, 108, 1, 2, 1, 4), DateAndTime()).setMaxAccess("readonly")
if mibBuilder.loadTexts: diffServConfigLastChange.setDescription("The date and time when this entry was last changed.")
diffServConfigStart = MibTableColumn((1, 3, 6, 1, 2, 1, 108, 1, 2, 1, 5), RowPointer().clone('0.0')).setMaxAccess("readcreate")
if mibBuilder.loadTexts: diffServConfigStart.setDescription("The pointer to a functional datapath configuration template as\nset up in the DIFFSERV-MIB.  This RowPointer should\npoint to an instance of one of:\n  diffServClfrEntry\n  diffServMeterEntry\n  diffServActionEntry\n  diffServAlgDropEntry\n  diffServQEntry\n\n\n\n\nA value of zeroDotZero in this attribute indicates no\nfurther Diffserv treatment is performed on traffic of\nthis functional datapath.  This also means that the\ntemplate described by this row is not defined.\n\nIf the row pointed to does not exist, the treatment\nis as if this attribute contains a value of zeroDotZero.")
diffServConfigStorage = MibTableColumn((1, 3, 6, 1, 2, 1, 108, 1, 2, 1, 6), StorageType().clone('nonVolatile')).setMaxAccess("readcreate")
if mibBuilder.loadTexts: diffServConfigStorage.setDescription("The type of storage used for this row.\n\nSince an entry in this table serves as a starting\npoint for a configuration, it is recommended that\nall entries comprising the configuration started by\ndiffServConfigStart follow the storage type of this\nentry.  Otherwise, after agent reboots a configuration\nmay differ.  It may very well be that the agent is\nnot capable of detecting such changes and therefore,\nthe management application should verify the correct\nconfiguration after a reboot.  Rows with a StorageType\nof 'permanent' do not need to allow write access to\nany of the columnar objects in that row.")
diffServConfigStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 108, 1, 2, 1, 7), RowStatus().clone('notInService')).setMaxAccess("readcreate")
if mibBuilder.loadTexts: diffServConfigStatus.setDescription("RowStatus object used for creation and deletion of\nrows in this table.  All writable objects in this row\nmay be modified at any time.")
diffServConfigMIBConformance = MibIdentifier((1, 3, 6, 1, 2, 1, 108, 2))
diffServConfigMIBCompliances = MibIdentifier((1, 3, 6, 1, 2, 1, 108, 2, 1))
diffServConfigMIBGroups = MibIdentifier((1, 3, 6, 1, 2, 1, 108, 2, 2))

# Augmentions

# Groups

diffServConfigMIBConfigGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 108, 2, 2, 1)).setObjects(*(("DIFFSERV-CONFIG-MIB", "diffServConfigDescr"), ("DIFFSERV-CONFIG-MIB", "diffServConfigStatus"), ("DIFFSERV-CONFIG-MIB", "diffServConfigStorage"), ("DIFFSERV-CONFIG-MIB", "diffServConfigLastChange"), ("DIFFSERV-CONFIG-MIB", "diffServConfigOwner"), ("DIFFSERV-CONFIG-MIB", "diffServConfigStart"), ) )
if mibBuilder.loadTexts: diffServConfigMIBConfigGroup.setDescription("The per-hop-behavior Group defines the MIB objects that\ndescribe the configuration template for the per-hop-behavior.")

# Compliances

diffServConfigMIBFullCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 108, 2, 1, 1)).setObjects(*(("DIFFSERV-CONFIG-MIB", "diffServConfigMIBConfigGroup"), ) )
if mibBuilder.loadTexts: diffServConfigMIBFullCompliance.setDescription("The full compliance for this MIB module.\n\nFor this compliance level the 'diffServMIBFullCompliance'\nmust be met, since this MIB module depends on it in order\nto provide the configuration entries.")

# Exports

# Module identity
mibBuilder.exportSymbols("DIFFSERV-CONFIG-MIB", PYSNMP_MODULE_ID=diffServConfigMib)

# Objects
mibBuilder.exportSymbols("DIFFSERV-CONFIG-MIB", diffServConfigMib=diffServConfigMib, diffServConfigMIBObjects=diffServConfigMIBObjects, diffServConfigTable=diffServConfigTable, diffServConfigEntry=diffServConfigEntry, diffServConfigId=diffServConfigId, diffServConfigDescr=diffServConfigDescr, diffServConfigOwner=diffServConfigOwner, diffServConfigLastChange=diffServConfigLastChange, diffServConfigStart=diffServConfigStart, diffServConfigStorage=diffServConfigStorage, diffServConfigStatus=diffServConfigStatus, diffServConfigMIBConformance=diffServConfigMIBConformance, diffServConfigMIBCompliances=diffServConfigMIBCompliances, diffServConfigMIBGroups=diffServConfigMIBGroups)

# Groups
mibBuilder.exportSymbols("DIFFSERV-CONFIG-MIB", diffServConfigMIBConfigGroup=diffServConfigMIBConfigGroup)

# Compliances
mibBuilder.exportSymbols("DIFFSERV-CONFIG-MIB", diffServConfigMIBFullCompliance=diffServConfigMIBFullCompliance)
