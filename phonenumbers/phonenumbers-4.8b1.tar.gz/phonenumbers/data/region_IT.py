"""Auto-generated file, do not edit by hand. IT metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_IT = PhoneMetadata(id='IT', country_code=39, international_prefix='00',
    general_desc=PhoneNumberDesc(national_number_pattern='[0189]\\d{5,10}|3(?:[12457-9]\\d{8}|[36]\\d{7,9})', possible_number_pattern='\\d{6,11}'),
    fixed_line=PhoneNumberDesc(national_number_pattern='0(?:[26]\\d{4,9}|[13-57-9](?:[0159]\\d{4,8}|[2-46-8]\\d{5,8}))', possible_number_pattern='\\d{6,11}', example_number='0212345678'),
    mobile=PhoneNumberDesc(national_number_pattern='3(?:[12457-9]\\d{8}|6\\d{7,8}|3\\d{7,9})', possible_number_pattern='\\d{9,11}', example_number='3123456789'),
    toll_free=PhoneNumberDesc(national_number_pattern='80(?:0\\d{6}|3\\d{3})', possible_number_pattern='\\d{6,9}', example_number='800123456'),
    premium_rate=PhoneNumberDesc(national_number_pattern='0878\\d{5}|1(?:44|6[346])\\d{6}|89(?:2\\d{3}|9\\d{6})', possible_number_pattern='\\d{6,9}', example_number='899123456'),
    shared_cost=PhoneNumberDesc(national_number_pattern='84[78]\\d{6,7}', possible_number_pattern='\\d{9,10}', example_number='8481234567'),
    personal_number=PhoneNumberDesc(national_number_pattern='178\\d{6,7}', possible_number_pattern='\\d{9,10}', example_number='1781234567'),
    voip=PhoneNumberDesc(national_number_pattern='NA', possible_number_pattern='NA'),
    pager=PhoneNumberDesc(national_number_pattern='NA', possible_number_pattern='NA'),
    uan=PhoneNumberDesc(national_number_pattern='NA', possible_number_pattern='NA'),
    emergency=PhoneNumberDesc(national_number_pattern='11[2358]', possible_number_pattern='\\d{3}', example_number='112'),
    voicemail=PhoneNumberDesc(national_number_pattern='NA', possible_number_pattern='NA'),
    no_international_dialling=PhoneNumberDesc(national_number_pattern='848\\d{6,7}', possible_number_pattern='\\d{9,10}', example_number='8481234567'),
    number_format=[NumberFormat(pattern='(0[26])(\\d{3,4})(\\d{4})', format=u'\\1 \\2 \\3', leading_digits_pattern=['0[26]']),
        NumberFormat(pattern='(0[26])(\\d{4})(\\d{5})', format=u'\\1 \\2 \\3', leading_digits_pattern=['0[26]']),
        NumberFormat(pattern='(0[26])(\\d{4,6})', format=u'\\1 \\2', leading_digits_pattern=['0[26]']),
        NumberFormat(pattern='(0\\d{2})(\\d{3,4})(\\d{4})', format=u'\\1 \\2 \\3', leading_digits_pattern=['0[13-57-9][0159]']),
        NumberFormat(pattern='(0\\d{2})(\\d{4,6})', format=u'\\1 \\2', leading_digits_pattern=['0[13-57-9][0159]']),
        NumberFormat(pattern='(0\\d{3})(\\d{3})(\\d{4})', format=u'\\1 \\2 \\3', leading_digits_pattern=['0[13-57-9][2-46-8]']),
        NumberFormat(pattern='(0\\d{3})(\\d{4,6})', format=u'\\1 \\2', leading_digits_pattern=['0[13-57-9][2-46-8]']),
        NumberFormat(pattern='(\\d{3})(\\d{3})(\\d{3,4})', format=u'\\1 \\2 \\3', leading_digits_pattern=['[13]|8(?:00|4[78]|99)']),
        NumberFormat(pattern='(\\d{3})(\\d{4})(\\d{4})', format=u'\\1 \\2 \\3', leading_digits_pattern=['3']),
        NumberFormat(pattern='(\\d{3})(\\d{3,6})', format=u'\\1 \\2', leading_digits_pattern=['8(?:03|92)'])],
    leading_zero_possible=True)
