"""Auto-generated file, do not edit by hand. AR metadata"""
from phonenumbers.phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_AR = PhoneMetadata(id='AR', country_code=54, international_prefix='00',
    general_desc=PhoneNumberDesc(national_number_pattern='[1-3689]\\d{9,10}', possible_number_pattern='\\d{6,11}'),
    fixed_line=PhoneNumberDesc(national_number_pattern='[1-3]\\d{9}', possible_number_pattern='\\d{6,10}'),
    mobile=PhoneNumberDesc(national_number_pattern='9\\d{10}|[1-3]\\d{9}', possible_number_pattern='\\d{10,11}'),
    toll_free=PhoneNumberDesc(national_number_pattern='80\\d{8}', possible_number_pattern='\\d{10}'),
    premium_rate=PhoneNumberDesc(national_number_pattern='6(0\\d|10)\\d{7}', possible_number_pattern='\\d{10}'),
    shared_cost=PhoneNumberDesc(national_number_pattern='NA', possible_number_pattern='NA'),
    personal_number=PhoneNumberDesc(national_number_pattern='NA', possible_number_pattern='NA'),
    voip=PhoneNumberDesc(national_number_pattern='NA', possible_number_pattern='NA'),
    pager=PhoneNumberDesc(national_number_pattern='NA', possible_number_pattern='NA'),
    uan=PhoneNumberDesc(national_number_pattern='NA', possible_number_pattern='NA'),
    emergency=PhoneNumberDesc(national_number_pattern='NA', possible_number_pattern='NA'),
    voicemail=PhoneNumberDesc(national_number_pattern='NA', possible_number_pattern='NA'),
    no_international_dialling=PhoneNumberDesc(national_number_pattern='NA', possible_number_pattern='NA'),
    national_prefix='0',
    national_prefix_for_parsing='0(?:(11|343|3715)15)?',
    national_prefix_transform_rule=u'9\\1',
    number_format=[NumberFormat(pattern='(\\d{2})(\\d{4})(\\d{4})', format=u'\\1 \\2-\\3', leading_digits_pattern=['11'], national_prefix_formatting_rule=u'0\\1'),
        NumberFormat(pattern='(\\d{4})(\\d{2})(\\d{4})', format=u'\\1 \\2-\\3', leading_digits_pattern=['1[02-9]|[23]'], national_prefix_formatting_rule=u'0\\1'),
        NumberFormat(pattern='(9)(11)(\\d{4})(\\d{4})', format=u'\\2 15 \\3-\\4', leading_digits_pattern=['911'], national_prefix_formatting_rule=u'0\\1'),
        NumberFormat(pattern='(9)(\\d{4})(\\d{2})(\\d{4})', format=u'\\2 \\3-\\4', leading_digits_pattern=['9(?:1[02-9]|[23])'], national_prefix_formatting_rule=u'0\\1', domestic_carrier_code_formatting_rule=u'0\\1 $CC'),
        NumberFormat(pattern='(\\d{3})(\\d{3})(\\d{4})', format=u'\\1-\\2-\\3', leading_digits_pattern=['[68]'], national_prefix_formatting_rule=u'0\\1')],
    intl_number_format=[NumberFormat(pattern='(\\d{2})(\\d{4})(\\d{4})', format=u'\\1 \\2-\\3', leading_digits_pattern=['11']),
        NumberFormat(pattern='(\\d{4})(\\d{2})(\\d{4})', format=u'\\1 \\2-\\3', leading_digits_pattern=['1[02-9]|[23]']),
        NumberFormat(pattern='(9)(11)(\\d{4})(\\d{4})', format=u'\\1 \\2 \\3 \\4', leading_digits_pattern=['911']),
        NumberFormat(pattern='(9)(\\d{4})(\\d{2})(\\d{4})', format=u'\\1 \\2 \\3 \\4', leading_digits_pattern=['9(?:1[02-9]|[23])']),
        NumberFormat(pattern='(\\d{3})(\\d{3})(\\d{4})', format=u'\\1-\\2-\\3', leading_digits_pattern=['[68]'])])
