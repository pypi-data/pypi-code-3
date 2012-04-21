# PySNMP SMI module. Autogenerated from smidump -f python IANA-IPPM-METRICS-REGISTRY-MIB
# by libsmi2pysnmp-0.1.3 at Mon Apr  2 20:39:06 2012,
# Python version sys.version_info(major=2, minor=7, micro=2, releaselevel='final', serial=0)

# Imports

( Integer, ObjectIdentifier, OctetString, ) = mibBuilder.importSymbols("ASN1", "Integer", "ObjectIdentifier", "OctetString")
( NamedValues, ) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
( ConstraintsIntersection, ConstraintsUnion, SingleValueConstraint, ValueRangeConstraint, ValueSizeConstraint, ) = mibBuilder.importSymbols("ASN1-REFINEMENT", "ConstraintsIntersection", "ConstraintsUnion", "SingleValueConstraint", "ValueRangeConstraint", "ValueSizeConstraint")
( Bits, Integer32, ModuleIdentity, MibIdentifier, ObjectIdentity, TimeTicks, mib_2, ) = mibBuilder.importSymbols("SNMPv2-SMI", "Bits", "Integer32", "ModuleIdentity", "MibIdentifier", "ObjectIdentity", "TimeTicks", "mib-2")

# Objects

ianaIppmMetricsRegistry = ModuleIdentity((1, 3, 6, 1, 2, 1, 128)).setRevisions(("2006-12-04 00:00","2005-04-12 00:00",))
if mibBuilder.loadTexts: ianaIppmMetricsRegistry.setOrganization("IANA")
if mibBuilder.loadTexts: ianaIppmMetricsRegistry.setContactInfo("Internet Assigned Numbers Authority\n\nPostal: ICANN\n    4676 Admiralty Way, Suite 330\n    Marina del Rey, CA 90292\n\nTel:    +1 310 823 9358\nE-Mail: iana&iana.org")
if mibBuilder.loadTexts: ianaIppmMetricsRegistry.setDescription("This module defines a registry for IP Performance Metrics.\n\nRegistrations are done sequentially by IANA in the ianaIppmMetrics\nsubtree on the bases of 'Specification Required' as defined in\n[RFC2434].\n\nThe reference of the specification must point to a stable document\nincluding a title, a revision and a date.\n\nThe name always starts with the name of the organization and must\nrespect the SMIv2 rules for descriptors defined in the section 3.1\nof [RFC2578];\n\nA document that creates new metrics would have an IANA\nconsiderations section in which it would describe new metrics to\nregister.\n\nAn OBJECT IDENTITY assigned to a metric is definitive and cannot\nbe reused.  If a new version of a metric is produced then it is\nassigned with a new name and a new identifier.\n\nCopyright (C) The Internet Society (2005).  The initial version of\nthis MIB module was published in RFC 4148; for full legal notices\nsee the RFC itself or see:\nhttp://www.ietf.org/copyrights/ianamib.html.  ")
ianaIppmMetrics = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1))
if mibBuilder.loadTexts: ianaIppmMetrics.setDescription("Registration point for IP Performance Metrics.")
ietfInstantUnidirConnectivity = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 1))
if mibBuilder.loadTexts: ietfInstantUnidirConnectivity.setDescription("Type-P-Instantaneous-Unidirectional-Connectivity")
ietfInstantBidirConnectivity = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 2))
if mibBuilder.loadTexts: ietfInstantBidirConnectivity.setDescription("Type-P-Instantaneous-Bidirectional-Connectivity")
ietfIntervalUnidirConnectivity = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 3))
if mibBuilder.loadTexts: ietfIntervalUnidirConnectivity.setDescription("Type-P-Interval-Unidirectional-Connectivity")
ietfIntervalBidirConnectivity = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 4))
if mibBuilder.loadTexts: ietfIntervalBidirConnectivity.setDescription("Type-P-Interval-Bidirectional-Connectivity")
ietfIntervalTemporalConnectivity = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 5))
if mibBuilder.loadTexts: ietfIntervalTemporalConnectivity.setDescription("Type-P1-P2-Interval-Temporal-Connectivity")
ietfOneWayDelay = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 6))
if mibBuilder.loadTexts: ietfOneWayDelay.setDescription("Type-P-One-way-Delay")
ietfOneWayDelayPoissonStream = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 7))
if mibBuilder.loadTexts: ietfOneWayDelayPoissonStream.setDescription("Type-P-One-way-Delay-Poisson-Stream")
ietfOneWayDelayPercentile = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 8))
if mibBuilder.loadTexts: ietfOneWayDelayPercentile.setDescription("Type-P-One-way-Delay-Percentile")
ietfOneWayDelayMedian = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 9))
if mibBuilder.loadTexts: ietfOneWayDelayMedian.setDescription("Type-P-One-way-Delay-Median")
ietfOneWayDelayMinimum = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 10))
if mibBuilder.loadTexts: ietfOneWayDelayMinimum.setDescription("Type-P-One-way-Delay-Minimum")
ietfOneWayDelayInversePercentile = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 11))
if mibBuilder.loadTexts: ietfOneWayDelayInversePercentile.setDescription("Type-P-One-way-Delay-Inverse-Percentile")
ietfOneWayPktLoss = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 12))
if mibBuilder.loadTexts: ietfOneWayPktLoss.setDescription("Type-P-One-way-Packet-Loss")
ietfOneWayPktLossPoissonStream = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 13))
if mibBuilder.loadTexts: ietfOneWayPktLossPoissonStream.setDescription("Type-P-One-way-Packet-Loss-Poisson-Stream")
ietfOneWayPktLossAverage = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 14))
if mibBuilder.loadTexts: ietfOneWayPktLossAverage.setDescription("Type-P-One-way-Packet-Loss-Average")
ietfRoundTripDelay = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 15))
if mibBuilder.loadTexts: ietfRoundTripDelay.setDescription("Type-P-Round-trip-Delay")
ietfRoundTripDelayPoissonStream = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 16))
if mibBuilder.loadTexts: ietfRoundTripDelayPoissonStream.setDescription("Type-P-Round-trip-Delay-Poisson-Stream")
ietfRoundTripDelayPercentile = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 17))
if mibBuilder.loadTexts: ietfRoundTripDelayPercentile.setDescription("Type-P-Round-trip-Delay-Percentile")
ietfRoundTripDelayMedian = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 18))
if mibBuilder.loadTexts: ietfRoundTripDelayMedian.setDescription("Type-P-Round-trip-Delay-Median")
ietfRoundTripDelayMinimum = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 19))
if mibBuilder.loadTexts: ietfRoundTripDelayMinimum.setDescription("Type-P-Round-trip-Delay-Minimum")
ietfRoundTripDelayInvPercentile = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 20))
if mibBuilder.loadTexts: ietfRoundTripDelayInvPercentile.setDescription("Type-P-Round-trip-Inverse-Percentile")
ietfOneWayLossDistanceStream = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 21))
if mibBuilder.loadTexts: ietfOneWayLossDistanceStream.setDescription("Type-P-One-Way-Loss-Distance-Stream")
ietfOneWayLossPeriodStream = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 22))
if mibBuilder.loadTexts: ietfOneWayLossPeriodStream.setDescription("Type-P-One-Way-Loss-Period-Stream")
ietfOneWayLossNoticeableRate = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 23))
if mibBuilder.loadTexts: ietfOneWayLossNoticeableRate.setDescription("Type-P-One-Way-Loss-Noticeable-Rate")
ietfOneWayLossPeriodTotal = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 24))
if mibBuilder.loadTexts: ietfOneWayLossPeriodTotal.setDescription("Type-P-One-Way-Loss-Period-Total")
ietfOneWayLossPeriodLengths = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 25))
if mibBuilder.loadTexts: ietfOneWayLossPeriodLengths.setDescription("Type-P-One-Way-Loss-Period-Lengths")
ietfOneWayInterLossPeriodLengths = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 26))
if mibBuilder.loadTexts: ietfOneWayInterLossPeriodLengths.setDescription("Type-P-One-Way-Inter-Loss-Period-Lengths")
ietfOneWayIpdv = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 27))
if mibBuilder.loadTexts: ietfOneWayIpdv.setDescription("Type-P-One-way-ipdv")
ietfOneWayIpdvPoissonStream = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 28))
if mibBuilder.loadTexts: ietfOneWayIpdvPoissonStream.setDescription("Type-P-One-way-ipdv-Poisson-stream")
ietfOneWayIpdvPercentile = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 29))
if mibBuilder.loadTexts: ietfOneWayIpdvPercentile.setDescription("Type-P-One-way-ipdv-percentile")
ietfOneWayIpdvInversePercentile = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 30))
if mibBuilder.loadTexts: ietfOneWayIpdvInversePercentile.setDescription("Type-P-One-way-ipdv-inverse-percentile")
ietfOneWayIpdvJitter = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 31))
if mibBuilder.loadTexts: ietfOneWayIpdvJitter.setDescription("Type-P-One-way-ipdv-jitter")
ietfOneWayPeakToPeakIpdv = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 32))
if mibBuilder.loadTexts: ietfOneWayPeakToPeakIpdv.setDescription("Type-P-One-way-peak-to-peak-ipdv")
ietfOneWayDelayPeriodicStream = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 33))
if mibBuilder.loadTexts: ietfOneWayDelayPeriodicStream.setDescription("Type-P-One-way-Delay-Periodic-Stream")
ietfReorderedSingleton = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 34))
if mibBuilder.loadTexts: ietfReorderedSingleton.setDescription("Type-P-Reordered")
ietfReorderedPacketRatio = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 35))
if mibBuilder.loadTexts: ietfReorderedPacketRatio.setDescription("Type-P-Reordered-Ratio-Stream")
ietfReorderingExtent = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 36))
if mibBuilder.loadTexts: ietfReorderingExtent.setDescription("Type-P-Packet-Reordering-Extent-Stream")
ietfReorderingLateTimeOffset = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 37))
if mibBuilder.loadTexts: ietfReorderingLateTimeOffset.setDescription("Type-P-Packet-Late-Time-Stream")
ietfReorderingByteOffset = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 38))
if mibBuilder.loadTexts: ietfReorderingByteOffset.setDescription("Type-P-Packet-Byte-Offset-Stream")
ietfReorderingGap = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 39))
if mibBuilder.loadTexts: ietfReorderingGap.setDescription("Type-P-Packet-Reordering-Gap-Stream")
ietfReorderingGapTime = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 40))
if mibBuilder.loadTexts: ietfReorderingGapTime.setDescription("Type-P-Packet-Reordering-GapTime-Stream")
ietfReorderingFreeRunx = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 41))
if mibBuilder.loadTexts: ietfReorderingFreeRunx.setDescription("Type-P-Packet-Reordering-Free-Run-x-numruns-Stream")
ietfReorderingFreeRunq = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 42))
if mibBuilder.loadTexts: ietfReorderingFreeRunq.setDescription("Type-P-Packet-Reordering-Free-Run-q-squruns-Stream")
ietfReorderingFreeRunp = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 43))
if mibBuilder.loadTexts: ietfReorderingFreeRunp.setDescription("Type-P-Packet-Reordering-Free-Run-p-numpkts-Stream")
ietfReorderingFreeRuna = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 44))
if mibBuilder.loadTexts: ietfReorderingFreeRuna.setDescription("Type-P-Packet-Reordering-Free-Run-a-accpkts-Stream")
ietfnReordering = ObjectIdentity((1, 3, 6, 1, 2, 1, 128, 1, 45))
if mibBuilder.loadTexts: ietfnReordering.setDescription("Type-P-Packet-n-Reordering-Stream")

# Augmentions

# Exports

# Module identity
mibBuilder.exportSymbols("IANA-IPPM-METRICS-REGISTRY-MIB", PYSNMP_MODULE_ID=ianaIppmMetricsRegistry)

# Objects
mibBuilder.exportSymbols("IANA-IPPM-METRICS-REGISTRY-MIB", ianaIppmMetricsRegistry=ianaIppmMetricsRegistry, ianaIppmMetrics=ianaIppmMetrics, ietfInstantUnidirConnectivity=ietfInstantUnidirConnectivity, ietfInstantBidirConnectivity=ietfInstantBidirConnectivity, ietfIntervalUnidirConnectivity=ietfIntervalUnidirConnectivity, ietfIntervalBidirConnectivity=ietfIntervalBidirConnectivity, ietfIntervalTemporalConnectivity=ietfIntervalTemporalConnectivity, ietfOneWayDelay=ietfOneWayDelay, ietfOneWayDelayPoissonStream=ietfOneWayDelayPoissonStream, ietfOneWayDelayPercentile=ietfOneWayDelayPercentile, ietfOneWayDelayMedian=ietfOneWayDelayMedian, ietfOneWayDelayMinimum=ietfOneWayDelayMinimum, ietfOneWayDelayInversePercentile=ietfOneWayDelayInversePercentile, ietfOneWayPktLoss=ietfOneWayPktLoss, ietfOneWayPktLossPoissonStream=ietfOneWayPktLossPoissonStream, ietfOneWayPktLossAverage=ietfOneWayPktLossAverage, ietfRoundTripDelay=ietfRoundTripDelay, ietfRoundTripDelayPoissonStream=ietfRoundTripDelayPoissonStream, ietfRoundTripDelayPercentile=ietfRoundTripDelayPercentile, ietfRoundTripDelayMedian=ietfRoundTripDelayMedian, ietfRoundTripDelayMinimum=ietfRoundTripDelayMinimum, ietfRoundTripDelayInvPercentile=ietfRoundTripDelayInvPercentile, ietfOneWayLossDistanceStream=ietfOneWayLossDistanceStream, ietfOneWayLossPeriodStream=ietfOneWayLossPeriodStream, ietfOneWayLossNoticeableRate=ietfOneWayLossNoticeableRate, ietfOneWayLossPeriodTotal=ietfOneWayLossPeriodTotal, ietfOneWayLossPeriodLengths=ietfOneWayLossPeriodLengths, ietfOneWayInterLossPeriodLengths=ietfOneWayInterLossPeriodLengths, ietfOneWayIpdv=ietfOneWayIpdv, ietfOneWayIpdvPoissonStream=ietfOneWayIpdvPoissonStream, ietfOneWayIpdvPercentile=ietfOneWayIpdvPercentile, ietfOneWayIpdvInversePercentile=ietfOneWayIpdvInversePercentile, ietfOneWayIpdvJitter=ietfOneWayIpdvJitter, ietfOneWayPeakToPeakIpdv=ietfOneWayPeakToPeakIpdv, ietfOneWayDelayPeriodicStream=ietfOneWayDelayPeriodicStream, ietfReorderedSingleton=ietfReorderedSingleton, ietfReorderedPacketRatio=ietfReorderedPacketRatio, ietfReorderingExtent=ietfReorderingExtent, ietfReorderingLateTimeOffset=ietfReorderingLateTimeOffset, ietfReorderingByteOffset=ietfReorderingByteOffset, ietfReorderingGap=ietfReorderingGap, ietfReorderingGapTime=ietfReorderingGapTime, ietfReorderingFreeRunx=ietfReorderingFreeRunx, ietfReorderingFreeRunq=ietfReorderingFreeRunq, ietfReorderingFreeRunp=ietfReorderingFreeRunp, ietfReorderingFreeRuna=ietfReorderingFreeRuna, ietfnReordering=ietfnReordering)

