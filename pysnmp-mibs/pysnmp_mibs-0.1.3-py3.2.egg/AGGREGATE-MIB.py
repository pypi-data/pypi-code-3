# PySNMP SMI module. Autogenerated from smidump -f python AGGREGATE-MIB
# by libsmi2pysnmp-0.1.3 at Mon Apr  2 20:38:39 2012,
# Python version sys.version_info(major=2, minor=7, micro=2, releaselevel='final', serial=0)

# Imports

( Integer, ObjectIdentifier, OctetString, ) = mibBuilder.importSymbols("ASN1", "Integer", "ObjectIdentifier", "OctetString")
( NamedValues, ) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
( ConstraintsIntersection, ConstraintsUnion, SingleValueConstraint, ValueRangeConstraint, ValueSizeConstraint, ) = mibBuilder.importSymbols("ASN1-REFINEMENT", "ConstraintsIntersection", "ConstraintsUnion", "SingleValueConstraint", "ValueRangeConstraint", "ValueSizeConstraint")
( OwnerString, ) = mibBuilder.importSymbols("RMON-MIB", "OwnerString")
( SnmpAdminString, ) = mibBuilder.importSymbols("SNMP-FRAMEWORK-MIB", "SnmpAdminString")
( ModuleCompliance, ObjectGroup, ) = mibBuilder.importSymbols("SNMPv2-CONF", "ModuleCompliance", "ObjectGroup")
( Bits, Integer32, ModuleIdentity, MibIdentifier, MibScalar, MibTable, MibTableRow, MibTableColumn, Opaque, TimeTicks, Unsigned32, experimental, ) = mibBuilder.importSymbols("SNMPv2-SMI", "Bits", "Integer32", "ModuleIdentity", "MibIdentifier", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "Opaque", "TimeTicks", "Unsigned32", "experimental")
( RowStatus, StorageType, TextualConvention, ) = mibBuilder.importSymbols("SNMPv2-TC", "RowStatus", "StorageType", "TextualConvention")

# Types

class AggrMOCompressedValue(OctetString):
    subtypeSpec = OctetString.subtypeSpec+ValueSizeConstraint(0,1024)
    
class AggrMOErrorStatus(Opaque):
    subtypeSpec = Opaque.subtypeSpec+ValueSizeConstraint(0,1024)
    
class AggrMOValue(Opaque):
    subtypeSpec = Opaque.subtypeSpec+ValueSizeConstraint(0,1024)
    

# Objects

aggrMIB = ModuleIdentity((1, 3, 6, 1, 3, 123)).setRevisions(("2006-04-27 00:00",))
if mibBuilder.loadTexts: aggrMIB.setOrganization("Cyber Solutions Inc. NetMan Working Group")
if mibBuilder.loadTexts: aggrMIB.setContactInfo("                      Glenn Mansfield Keeni\nPostal: Cyber Solutions Inc.\n        6-6-3, Minami Yoshinari\n        Aoba-ku, Sendai, Japan 989-3204.\n   Tel: +81-22-303-4012\n   Fax: +81-22-303-4015\nE-mail: glenn@cysols.com\n\nSupport Group E-mail: mibsupport@cysols.com")
if mibBuilder.loadTexts: aggrMIB.setDescription("The MIB for servicing aggregate objects.\n\nCopyright (C) The Internet Society (2006).  This\nversion of this MIB module is part of RFC 4498;\nsee the RFC itself for full legal notices.")
aggrCtlTable = MibTable((1, 3, 6, 1, 3, 123, 1))
if mibBuilder.loadTexts: aggrCtlTable.setDescription("A table that controls the aggregation of the MOs.")
aggrCtlEntry = MibTableRow((1, 3, 6, 1, 3, 123, 1, 1)).setIndexNames((0, "AGGREGATE-MIB", "aggrCtlEntryID"))
if mibBuilder.loadTexts: aggrCtlEntry.setDescription("A row of the control table that defines one aggregated\nMO.\n\n\n\n\n\nEntries in this table are required to survive a reboot\nof the managed entity depending on the value of the\ncorresponding aggrCtlEntryStorageType instance.")
aggrCtlEntryID = MibTableColumn((1, 3, 6, 1, 3, 123, 1, 1, 1), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(1, 32))).setMaxAccess("noaccess")
if mibBuilder.loadTexts: aggrCtlEntryID.setDescription("A locally unique, administratively assigned name\nfor this aggregated MO.  It is used as an index to\nuniquely identify this row in the table.")
aggrCtlMOIndex = MibTableColumn((1, 3, 6, 1, 3, 123, 1, 1, 2), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647))).setMaxAccess("readcreate")
if mibBuilder.loadTexts: aggrCtlMOIndex.setDescription("A pointer to a group of MOs identified by aggrMOEntryID\nin the aggrMOTable.  This is the group of MOs that will\nbe aggregated.")
aggrCtlMODescr = MibTableColumn((1, 3, 6, 1, 3, 123, 1, 1, 3), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(0, 64))).setMaxAccess("readcreate")
if mibBuilder.loadTexts: aggrCtlMODescr.setDescription("A textual description of the object that is\nbeing aggregated.")
aggrCtlCompressionAlgorithm = MibTableColumn((1, 3, 6, 1, 3, 123, 1, 1, 4), Integer().subtype(subtypeSpec=SingleValueConstraint(1,2,)).subtype(namedValues=NamedValues(("none", 1), ("deflate", 2), )).clone(1)).setMaxAccess("readcreate")
if mibBuilder.loadTexts: aggrCtlCompressionAlgorithm.setDescription("The compression algorithm that will be used by\nthe agent to compress the value of the aggregated\nobject.\nThe deflate algorithm and corresponding data format\nspecification is described in RFC 1951.  It is\ncompatible with the widely used gzip utility.")
aggrCtlEntryOwner = MibTableColumn((1, 3, 6, 1, 3, 123, 1, 1, 5), OwnerString()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: aggrCtlEntryOwner.setDescription("The entity that created this entry.")
aggrCtlEntryStorageType = MibTableColumn((1, 3, 6, 1, 3, 123, 1, 1, 6), StorageType()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: aggrCtlEntryStorageType.setDescription("This object defines whether the parameters defined in\nthis row are kept in volatile storage and lost upon\nreboot or backed up by non-volatile (permanent)\nstorage.\n\nConceptual rows having the value 'permanent' need not\nallow write-access to any columnar objects in the row.")
aggrCtlEntryStatus = MibTableColumn((1, 3, 6, 1, 3, 123, 1, 1, 7), RowStatus()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: aggrCtlEntryStatus.setDescription("The row status variable, used according to row\ninstallation and removal conventions.\nObjects in a row can be modified only when the value of\nthis object in the corresponding conceptual row is not\n'active'.\nThus, to modify one or more of the objects in this\nconceptual row,\n  a. change the row status to 'notInService',\n  b. change the values of the row, and\n  c. change the row status to 'active'.\nThe aggrCtlEntryStatus may be changed to 'active' if\nall the MOs in the conceptual row have been assigned\nvalid values.")
aggrMOTable = MibTable((1, 3, 6, 1, 3, 123, 2))
if mibBuilder.loadTexts: aggrMOTable.setDescription("The table of primary(simple) MOs that will be aggregated.\nEach row in this table represents a MO that will be\naggregated.  The aggrMOEntryID index is used to identify\nthe group of MOs that will be aggregated.  The\naggrMOIndex instance in the corresponding row of the\naggrCtlTable will have a value equal to the value of\naggrMOEntryID.  The aggrMOEntryMOID index is used to\nidentify an MO in the group.")
aggrMOEntry = MibTableRow((1, 3, 6, 1, 3, 123, 2, 1)).setIndexNames((0, "AGGREGATE-MIB", "aggrMOEntryID"), (0, "AGGREGATE-MIB", "aggrMOEntryMOID"))
if mibBuilder.loadTexts: aggrMOEntry.setDescription("A row of the table that specifies one MO.\nEntries in this table are required to survive a reboot\nof the managed entity depending on the value of the\ncorresponding aggrMOEntryStorageType instance.")
aggrMOEntryID = MibTableColumn((1, 3, 6, 1, 3, 123, 2, 1, 1), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647))).setMaxAccess("noaccess")
if mibBuilder.loadTexts: aggrMOEntryID.setDescription("An index uniquely identifying a group of MOs\nthat will be aggregated.")
aggrMOEntryMOID = MibTableColumn((1, 3, 6, 1, 3, 123, 2, 1, 2), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess("noaccess")
if mibBuilder.loadTexts: aggrMOEntryMOID.setDescription("An index to uniquely identify an MO instance in the\ngroup of MO instances that will be aggregated.")
aggrMOInstance = MibTableColumn((1, 3, 6, 1, 3, 123, 2, 1, 3), ObjectIdentifier()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: aggrMOInstance.setDescription("The OID of the MO instance, the value of which will\nbe sampled by the agent.")
aggrMODescr = MibTableColumn((1, 3, 6, 1, 3, 123, 2, 1, 4), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(0, 64))).setMaxAccess("readcreate")
if mibBuilder.loadTexts: aggrMODescr.setDescription("A textual description of the object that will\nbe aggregated.")
aggrMOEntryStorageType = MibTableColumn((1, 3, 6, 1, 3, 123, 2, 1, 5), StorageType()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: aggrMOEntryStorageType.setDescription("This object defines whether the parameters defined in\nthis row are kept in volatile storage and lost upon\nreboot or backed up by non-volatile (permanent)\nstorage.\nConceptual rows having the value 'permanent' need not\nallow write-access to any columnar objects in the row.")
aggrMOEntryStatus = MibTableColumn((1, 3, 6, 1, 3, 123, 2, 1, 6), RowStatus()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: aggrMOEntryStatus.setDescription("The row status variable, used according to row\ninstallation and removal conventions.\nObjects in a row can be modified only when the value of\nthis object in the corresponding conceptual row is not\n'active'.\nThus, to modify one or more of the objects in this\nconceptual row,\n  a. change the row status to 'notInService',\n  b. change the values of the row, and\n  c. change the row status to 'active'.\nThe aggrMOEntryStatus may be changed to 'active' iff\nall the MOs in the conceptual row have been assigned\nvalid values.")
aggrDataTable = MibTable((1, 3, 6, 1, 3, 123, 3))
if mibBuilder.loadTexts: aggrDataTable.setDescription("Each row of this table contains information\nabout an aggregateMO indexed by aggrCtlEntryID.")
aggrDataEntry = MibTableRow((1, 3, 6, 1, 3, 123, 3, 1)).setIndexNames((0, "AGGREGATE-MIB", "aggrCtlEntryID"))
if mibBuilder.loadTexts: aggrDataEntry.setDescription("Entry containing information pertaining to\nan aggregate MO.")
aggrDataRecord = MibTableColumn((1, 3, 6, 1, 3, 123, 3, 1, 1), AggrMOValue()).setMaxAccess("readonly")
if mibBuilder.loadTexts: aggrDataRecord.setDescription("The snapshot value of the aggregated MO.\nNote that the access privileges to this object will be\ngoverned by the access privileges of the component\nobjects.  Thus, an entity attempting to access an\ninstance of this MO MUST have access rights to all the\ncomponent instance objects and this MO instance.")
aggrDataRecordCompressed = MibTableColumn((1, 3, 6, 1, 3, 123, 3, 1, 2), AggrMOCompressedValue()).setMaxAccess("readonly")
if mibBuilder.loadTexts: aggrDataRecordCompressed.setDescription("The compressed value of the aggregated MO.\nThe compression algorithm will depend on the\naggrCtlCompressionAlgorithm given in the corresponding\naggrCtlEntry.  If the value of the corresponding\naggrCtlCompressionAlgorithm is (1) 'none', then the value\nof all instances of this object will be a string of zero\nlength.\nNote that the access privileges to this object will be\ngoverned by the access privileges of the component\nobjects.  Thus, an entity attempting to access an instance\nof this MO MUST have access rights to all the component\ninstance objects and this MO instance.")
aggrDataErrorRecord = MibTableColumn((1, 3, 6, 1, 3, 123, 3, 1, 3), AggrMOErrorStatus()).setMaxAccess("readonly")
if mibBuilder.loadTexts: aggrDataErrorRecord.setDescription("The error status corresponding to the MO instances\naggregated in aggrDataRecord (and\naggrDataRecordCompressed).")
aggrConformance = MibIdentifier((1, 3, 6, 1, 3, 123, 4))
aggrGroups = MibIdentifier((1, 3, 6, 1, 3, 123, 4, 1))
aggrCompliances = MibIdentifier((1, 3, 6, 1, 3, 123, 4, 2))

# Augmentions

# Groups

aggrMibBasicGroup = ObjectGroup((1, 3, 6, 1, 3, 123, 4, 1, 1)).setObjects(*(("AGGREGATE-MIB", "aggrCtlEntryStatus"), ("AGGREGATE-MIB", "aggrDataRecord"), ("AGGREGATE-MIB", "aggrCtlEntryOwner"), ("AGGREGATE-MIB", "aggrCtlMODescr"), ("AGGREGATE-MIB", "aggrMOInstance"), ("AGGREGATE-MIB", "aggrMOEntryStorageType"), ("AGGREGATE-MIB", "aggrCtlCompressionAlgorithm"), ("AGGREGATE-MIB", "aggrCtlEntryStorageType"), ("AGGREGATE-MIB", "aggrMODescr"), ("AGGREGATE-MIB", "aggrCtlMOIndex"), ("AGGREGATE-MIB", "aggrMOEntryStatus"), ("AGGREGATE-MIB", "aggrDataErrorRecord"), ("AGGREGATE-MIB", "aggrDataRecordCompressed"), ) )
if mibBuilder.loadTexts: aggrMibBasicGroup.setDescription("A collection of objects for aggregation of MOs.")

# Compliances

aggrMibCompliance = ModuleCompliance((1, 3, 6, 1, 3, 123, 4, 2, 1)).setObjects(*(("AGGREGATE-MIB", "aggrMibBasicGroup"), ) )
if mibBuilder.loadTexts: aggrMibCompliance.setDescription("The compliance statement for SNMP entities\nthat implement the AGGREGATE-MIB.")

# Exports

# Module identity
mibBuilder.exportSymbols("AGGREGATE-MIB", PYSNMP_MODULE_ID=aggrMIB)

# Types
mibBuilder.exportSymbols("AGGREGATE-MIB", AggrMOCompressedValue=AggrMOCompressedValue, AggrMOErrorStatus=AggrMOErrorStatus, AggrMOValue=AggrMOValue)

# Objects
mibBuilder.exportSymbols("AGGREGATE-MIB", aggrMIB=aggrMIB, aggrCtlTable=aggrCtlTable, aggrCtlEntry=aggrCtlEntry, aggrCtlEntryID=aggrCtlEntryID, aggrCtlMOIndex=aggrCtlMOIndex, aggrCtlMODescr=aggrCtlMODescr, aggrCtlCompressionAlgorithm=aggrCtlCompressionAlgorithm, aggrCtlEntryOwner=aggrCtlEntryOwner, aggrCtlEntryStorageType=aggrCtlEntryStorageType, aggrCtlEntryStatus=aggrCtlEntryStatus, aggrMOTable=aggrMOTable, aggrMOEntry=aggrMOEntry, aggrMOEntryID=aggrMOEntryID, aggrMOEntryMOID=aggrMOEntryMOID, aggrMOInstance=aggrMOInstance, aggrMODescr=aggrMODescr, aggrMOEntryStorageType=aggrMOEntryStorageType, aggrMOEntryStatus=aggrMOEntryStatus, aggrDataTable=aggrDataTable, aggrDataEntry=aggrDataEntry, aggrDataRecord=aggrDataRecord, aggrDataRecordCompressed=aggrDataRecordCompressed, aggrDataErrorRecord=aggrDataErrorRecord, aggrConformance=aggrConformance, aggrGroups=aggrGroups, aggrCompliances=aggrCompliances)

# Groups
mibBuilder.exportSymbols("AGGREGATE-MIB", aggrMibBasicGroup=aggrMibBasicGroup)

# Compliances
mibBuilder.exportSymbols("AGGREGATE-MIB", aggrMibCompliance=aggrMibCompliance)
