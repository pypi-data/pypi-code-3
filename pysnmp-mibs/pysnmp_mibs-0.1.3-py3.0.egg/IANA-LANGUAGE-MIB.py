# PySNMP SMI module. Autogenerated from smidump -f python IANA-LANGUAGE-MIB
# by libsmi2pysnmp-0.1.3 at Mon Apr  2 20:39:06 2012,
# Python version sys.version_info(major=2, minor=7, micro=2, releaselevel='final', serial=0)

# Imports

( Integer, ObjectIdentifier, OctetString, ) = mibBuilder.importSymbols("ASN1", "Integer", "ObjectIdentifier", "OctetString")
( NamedValues, ) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
( ConstraintsIntersection, ConstraintsUnion, SingleValueConstraint, ValueRangeConstraint, ValueSizeConstraint, ) = mibBuilder.importSymbols("ASN1-REFINEMENT", "ConstraintsIntersection", "ConstraintsUnion", "SingleValueConstraint", "ValueRangeConstraint", "ValueSizeConstraint")
( Bits, Integer32, ModuleIdentity, MibIdentifier, ObjectIdentity, TimeTicks, mib_2, ) = mibBuilder.importSymbols("SNMPv2-SMI", "Bits", "Integer32", "ModuleIdentity", "MibIdentifier", "ObjectIdentity", "TimeTicks", "mib-2")

# Objects

ianaLanguages = ModuleIdentity((1, 3, 6, 1, 2, 1, 73)).setRevisions(("2000-05-10 00:00","1999-09-09 09:00",))
if mibBuilder.loadTexts: ianaLanguages.setOrganization("IANA")
if mibBuilder.loadTexts: ianaLanguages.setContactInfo("Internet Assigned Numbers Authority (IANA)\n\nPostal: ICANN\n        4676 Admiralty Way, Suite 330\n        Marina del Rey, CA 90292\n\nTel:    +1 310 823 9358 x20\nE-Mail: iana&iana.org")
if mibBuilder.loadTexts: ianaLanguages.setDescription("The MIB module registers object identifier values for\nwell-known programming and scripting languages. Every\nlanguage registration MUST describe the format used\nwhen transferring scripts written in this language.\n\nAny additions or changes to the contents of this MIB\nmodule require Designated Expert Review as defined in\nthe Guidelines for Writing IANA Considerations Section\ndocument. The Designated Expert will be selected by\nthe IESG Area Director of the OPS Area.\n\nNote, this module does not have to register all possible\nlanguages since languages are identified by object\nidentifier values. It is therefore possible to registered \nlanguages in private OID trees. The references given below are not\nnormative with regard to the language version. Other\nreferences might be better suited to describe some newer \nversions of this language. The references are only\nprovided as `a pointer into the right direction'.")
ianaLangJavaByteCode = ObjectIdentity((1, 3, 6, 1, 2, 1, 73, 1))
if mibBuilder.loadTexts: ianaLangJavaByteCode.setDescription("Java byte code to be processed by a Java virtual machine.\nA script written in Java byte code is transferred by using\nthe Java archive file format (JAR).")
ianaLangTcl = ObjectIdentity((1, 3, 6, 1, 2, 1, 73, 2))
if mibBuilder.loadTexts: ianaLangTcl.setDescription("The Tool Command Language (Tcl). A script written in the\nTcl language is transferred in Tcl source code format.")
ianaLangPerl = ObjectIdentity((1, 3, 6, 1, 2, 1, 73, 3))
if mibBuilder.loadTexts: ianaLangPerl.setDescription("The Perl language. A script written in the Perl language\nis transferred in Perl source code format.")
ianaLangScheme = ObjectIdentity((1, 3, 6, 1, 2, 1, 73, 4))
if mibBuilder.loadTexts: ianaLangScheme.setDescription("The Scheme language. A script written in the Scheme\nlanguage is transferred in Scheme source code format.")
ianaLangSRSL = ObjectIdentity((1, 3, 6, 1, 2, 1, 73, 5))
if mibBuilder.loadTexts: ianaLangSRSL.setDescription("The SNMP Script Language defined by SNMP Research. A\nscript written in the SNMP Script Language is transferred\nin the SNMP Script Language source code format.")
ianaLangPSL = ObjectIdentity((1, 3, 6, 1, 2, 1, 73, 6))
if mibBuilder.loadTexts: ianaLangPSL.setDescription("The Patrol Script Language defined by BMC Software. A script\nwritten in the Patrol Script Language is transferred in the\nPatrol Script Language source code format.")
ianaLangSMSL = ObjectIdentity((1, 3, 6, 1, 2, 1, 73, 7))
if mibBuilder.loadTexts: ianaLangSMSL.setDescription("The Systems Management Scripting Language. A script written\nin the SMSL language is transferred in the SMSL source code\nformat.")

# Augmentions

# Exports

# Module identity
mibBuilder.exportSymbols("IANA-LANGUAGE-MIB", PYSNMP_MODULE_ID=ianaLanguages)

# Objects
mibBuilder.exportSymbols("IANA-LANGUAGE-MIB", ianaLanguages=ianaLanguages, ianaLangJavaByteCode=ianaLangJavaByteCode, ianaLangTcl=ianaLangTcl, ianaLangPerl=ianaLangPerl, ianaLangScheme=ianaLangScheme, ianaLangSRSL=ianaLangSRSL, ianaLangPSL=ianaLangPSL, ianaLangSMSL=ianaLangSMSL)

