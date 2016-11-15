# coding: utf-8
#--
# Copyright (c) 2008-2013 Net-ng.
# All rights reserved.
#
# This software is licensed under the BSD License, as described in
# the file LICENSE.txt, which you should have received as part of
# this distribution.
#--

import datetime
import decimal

import pytz
from nose import with_setup

from nagare import i18n


"""Tests are working with Babel == 2.3.4"""


class Translation(dict):
    def gettext(self, msg):
        return self[msg]

    def ugettext(self, msg):
        return unicode(self.gettext(msg))

    def ngettext(self, singular, plural, n):
        return self[singular if n == 1 else plural]

    def ungettext(self, singular, plural, n):
        return unicode(self.ngettext(singular, plural, n))


class Locale(i18n.Locale):
    def _get_translation(self, domain=None):
        translation = Translation({
            'hello': 'bonjour',
            'Holidays': 'Vacances %(year)d',
            'horse': 'cheval',
            'horses': 'chevaux'
        })
        return translation


def setup():
    i18n.set_locale(Locale('fr', 'FR'))


def teardown():
    pass

# -----------------------------------------------------------------------------

@with_setup(setup, teardown)
def test_gettext():
    s = i18n.gettext('hello')
    assert isinstance(s, str) and (s == 'bonjour')


@with_setup(setup, teardown)
def test_gettext_params():
    s = i18n.gettext('Holidays', year=2010)
    assert isinstance(s, str) and (s == 'Vacances 2010')


def test_gettext_unknown():
    i18n.set_locale(i18n.Locale('fr', 'FR'))
    s = i18n.gettext('unknown')
    assert isinstance(s, str) and (s == 'unknown')


@with_setup(setup, teardown)
def test_ugettext():
    s = i18n.ugettext('hello')
    assert isinstance(s, unicode) and (s == u'bonjour')


@with_setup(setup, teardown)
def test_ugettext_params():
    s = i18n.ugettext('Holidays', year=2010)
    assert isinstance(s, unicode) and (s == u'Vacances 2010')


def test_ugettext_unknown():
    i18n.set_locale(i18n.Locale('fr', 'FR'))
    s = i18n.ugettext('unknown')
    assert isinstance(s, unicode) and (s == u'unknown')


@with_setup(setup, teardown)
def test__():
    s = i18n._('hello')
    assert isinstance(s, unicode) and (s == u'bonjour')


@with_setup(setup, teardown)
def test_ngettext_singular():
    s = i18n.ngettext('horse', 'horses', 1)
    assert isinstance(s, str) and (s == 'cheval')


@with_setup(setup, teardown)
def test_ngettext_plural():
    s = i18n.ngettext('horse', 'horses', 3)
    assert isinstance(s, str) and (s == 'chevaux')


def test_ngettext_singular_unknown():
    i18n.set_locale(i18n.Locale('fr', 'FR'))
    s = i18n.ngettext('unknown1', 'unknown2', 1)
    assert isinstance(s, str) and (s == 'unknown1')


def test_ngettext_plural_unknown():
    i18n.set_locale(i18n.Locale('fr_FR'))
    s = i18n.ngettext('unknown1', 'unknown2', 3)
    assert isinstance(s, str) and (s == 'unknown2')


@with_setup(setup, teardown)
def test_ungettext_singular():
    s = i18n.ungettext('horse', 'horses', 1)
    assert isinstance(s, unicode) and (s == u'cheval')


@with_setup(setup, teardown)
def test_ungettext_plural():
    s = i18n.ungettext('horse', 'horses', 3)
    assert isinstance(s, unicode) and (s == u'chevaux')


def test_ungettext_singular_unknown():
    i18n.set_locale(i18n.Locale('fr', 'FR'))
    s = i18n.ungettext('unknown1', 'unknown2', 1)
    assert isinstance(s, unicode) and (s == u'unknown1')


def test_ungettext_plural_unknown():
    i18n.set_locale(i18n.Locale('fr', 'FR'))
    s = i18n.ungettext('unknown1', 'unknown2', 3)
    assert isinstance(s, unicode) and (s == u'unknown2')


@with_setup(setup, teardown)
def test_N_singular():
    s = i18n._N('horse', 'horses', 1)
    assert isinstance(s, unicode) and (s == u'cheval')


@with_setup(setup, teardown)
def test_N_plural():
    s = i18n._N('horse', 'horses', 3)
    assert isinstance(s, unicode) and (s == u'chevaux')


@with_setup(setup, teardown)
def test_lazy_gettext():
    s = i18n.lazy_gettext('hello')
    assert s.__class__.__name__ == 'LazyProxy'
    assert isinstance(s.value, str) and (s == 'bonjour')


@with_setup(setup, teardown)
def test_lazy_gettext_params():
    s = i18n.lazy_gettext('Holidays', year=2010)
    assert s.__class__.__name__ == 'LazyProxy'
    assert isinstance(s.value, str) and (s == 'Vacances 2010')


@with_setup(setup, teardown)
def test_lazy_gettext():
    s = i18n.lazy_gettext('hello')
    assert s.__class__.__name__ == 'LazyProxy'
    assert isinstance(s.value, str) and (s == 'bonjour')


@with_setup(setup, teardown)
def test_lazy_gettext_params():
    s = i18n.lazy_gettext('Holidays', year=2010)
    assert s.__class__.__name__ == 'LazyProxy'
    assert isinstance(s.value, str) and (s == 'Vacances 2010')


@with_setup(setup, teardown)
def test_lazy_ugettext():
    s = i18n.lazy_ugettext('hello')
    assert s.__class__.__name__ == 'LazyProxy'
    assert isinstance(s.value, unicode) and (s == u'bonjour')


@with_setup(setup, teardown)
def test_lazy_ugettext_params():
    s = i18n.lazy_ugettext('Holidays', year=2010)
    assert s.__class__.__name__ == 'LazyProxy'
    assert isinstance(s.value, unicode) and (s == u'Vacances 2010')


@with_setup(setup, teardown)
def test_L_ugettext():
    s = i18n._L('hello')
    assert s.__class__.__name__ == 'LazyProxy'
    assert isinstance(s.value, unicode) and (s == u'bonjour')


@with_setup(setup, teardown)
def test_lazy_ngettext_singular():
    s = i18n.lazy_ngettext('horse', 'horses', 1)
    assert s.__class__.__name__ == 'LazyProxy'
    assert isinstance(s.value, str) and (s == 'cheval')


@with_setup(setup, teardown)
def test_lazy_ngettext_plural():
    s = i18n.lazy_ngettext('horse', 'horses', 3)
    assert s.__class__.__name__ == 'LazyProxy'
    assert isinstance(s.value, str) and (s == 'chevaux')


@with_setup(setup, teardown)
def test_lazy_ungettext_singular():
    s = i18n.lazy_ungettext('horse', 'horses', 1)
    assert s.__class__.__name__ == 'LazyProxy'
    assert isinstance(s.value, unicode) and (s == u'cheval')


@with_setup(setup, teardown)
def test_lazy_ungettext_plural():
    s = i18n.lazy_ungettext('horse', 'horses', 3)
    assert s.__class__.__name__ == 'LazyProxy'
    assert isinstance(s.value, unicode) and (s == u'chevaux')


@with_setup(setup, teardown)
def test_LN_ungettext_singular():
    s = i18n._LN('horse', 'horses', 1)
    assert s.__class__.__name__ == 'LazyProxy'
    assert isinstance(s.value, unicode) and (s == u'cheval')


@with_setup(setup, teardown)
def test_LN_ungettext_plural():
    s = i18n._LN('horse', 'horses', 3)
    assert s.__class__.__name__ == 'LazyProxy'
    assert isinstance(s.value, unicode) and (s == u'chevaux')

# -----------------------------------------------------------------------------


def setup():
    i18n.set_locale(i18n.Locale('fr', 'FR'))


def setup_en():
    i18n.set_locale(i18n.Locale('en', 'US'))


def teardown():
    pass


@with_setup(setup, teardown)
def test_get_period_names():
    assert i18n.get_period_names() == {'afternoon1': u'après-midi',
                                       'am': u'AM',
                                       'evening1': u'soir',
                                       'midnight': u'minuit',
                                       'morning1': u'matin',
                                       'night1': u'nuit',
                                       'noon': u'midi',
                                       'pm': u'PM'}

@with_setup(setup, teardown)
def test_get_day_names():
    assert i18n.get_day_names() == {0: u'lundi', 1: u'mardi', 2: u'mercredi', 3: u'jeudi', 4: u'vendredi', 5: u'samedi', 6: u'dimanche'}
    assert i18n.get_day_names(width='wide') == {0: u'lundi', 1: u'mardi', 2: u'mercredi', 3: u'jeudi', 4: u'vendredi', 5: u'samedi', 6: u'dimanche'}
    assert i18n.get_day_names(width='abbreviated') == {0: u'lun.', 1: u'mar.', 2: u'mer.', 3: u'jeu.', 4: u'ven.', 5: u'sam.', 6: u'dim.'}
    assert i18n.get_day_names(width='narrow') == {0: u'L', 1: u'M', 2: u'M', 3: u'J', 4: u'V', 5: u'S', 6: u'D'}


@with_setup(setup, teardown)
def test_get_month_names():
    assert i18n.get_month_names() == {1: u'janvier', 2: u'f\xe9vrier', 3: u'mars', 4: u'avril', 5: u'mai', 6: u'juin', 7: u'juillet', 8: u'ao\xfbt', 9: u'septembre', 10: u'octobre', 11: u'novembre', 12: u'd\xe9cembre'}
    assert i18n.get_month_names(width='wide') == {1: u'janvier', 2: u'f\xe9vrier', 3: u'mars', 4: u'avril', 5: u'mai', 6: u'juin', 7: u'juillet', 8: u'ao\xfbt', 9: u'septembre', 10: u'octobre', 11: u'novembre', 12: u'd\xe9cembre'}
    assert i18n.get_month_names(width='abbreviated') == {1: u'janv.', 2: u'f\xe9vr.', 3: u'mars', 4: u'avr.', 5: u'mai', 6: u'juin', 7: u'juil.', 8: u'ao\xfbt', 9: u'sept.', 10: u'oct.', 11: u'nov.', 12: u'd\xe9c.'}
    assert i18n.get_month_names(width='narrow') == {1: u'J', 2: u'F', 3: u'M', 4: u'A', 5: u'M', 6: u'J', 7: u'J', 8: u'A', 9: u'S', 10: u'O', 11: u'N', 12: u'D'}


@with_setup(setup_en, teardown)
def test_get_quarter_names():
    assert i18n.get_quarter_names() == {1: u'1st quarter', 2: u'2nd quarter', 3: u'3rd quarter', 4: u'4th quarter'}
    assert i18n.get_quarter_names(width='wide') == {1: u'1st quarter', 2: u'2nd quarter', 3: u'3rd quarter', 4: u'4th quarter'}
    assert i18n.get_quarter_names(width='abbreviated') == {1: u'Q1', 2: u'Q2', 3: u'Q3', 4: u'Q4'}
    assert i18n.get_quarter_names(width='abbreviated') == {1: u'Q1', 2: u'Q2', 3: u'Q3', 4: u'Q4'}


@with_setup(setup_en, teardown)
def test_get_era_names():
    assert i18n.get_era_names() == {0: u'Before Christ', 1: u'Anno Domini'}
    assert i18n.get_era_names(width='abbreviated') == {0: u'BC', 1: u'AD'}
    assert i18n.get_era_names(width='narrow') == {0: u'B', 1: u'A'}


@with_setup(setup, teardown)
def test_get_date_format():
    assert i18n.get_date_format(format='full').pattern == 'EEEE d MMMM y'
    assert i18n.get_date_format(format='long').pattern == 'd MMMM y'
    assert i18n.get_date_format().pattern == 'd MMM y'
    assert i18n.get_date_format(format='medium').pattern == 'd MMM y'
    assert i18n.get_date_format(format='short').pattern == 'dd/MM/y'


@with_setup(setup, teardown)
def test_get_datetime_format():
    assert i18n.get_datetime_format(format='full') == u"{1} 'à' {0}"
    assert i18n.get_datetime_format(format='long') == u"{1} 'à' {0}"
    assert i18n.get_datetime_format() == u"{1} 'à' {0}"
    assert i18n.get_datetime_format(format='medium') == u"{1} 'à' {0}"
    assert i18n.get_datetime_format(format='short') == u'{1} {0}'


@with_setup(setup, teardown)
def test_get_time_format():
    assert i18n.get_time_format(format='full').pattern == 'HH:mm:ss zzzz'
    assert i18n.get_time_format(format='long').pattern == 'HH:mm:ss z'
    assert i18n.get_time_format().pattern == 'HH:mm:ss'
    assert i18n.get_time_format(format='medium').pattern == 'HH:mm:ss'
    assert i18n.get_time_format(format='short').pattern == 'HH:mm'


@with_setup(setup, teardown)
def test_get_timezone_gmt():
    tz = pytz.timezone('Pacific/Pitcairn')
    d = tz.localize(datetime.datetime(2007, 4, 1, 15, 30))

    assert i18n.get_timezone_gmt(d, width='long') == 'UTC-08:00'
    assert i18n.get_timezone_gmt(d) == 'UTC-08:00'
    assert i18n.get_timezone_gmt(d, width='short') == '-0800'

    setup_en()

    assert i18n.get_timezone_gmt(d, width='long') == 'GMT-08:00'
    assert i18n.get_timezone_gmt(d) == 'GMT-08:00'
    assert i18n.get_timezone_gmt(d, width='short') == '-0800'


@with_setup(setup, teardown)
def test_get_timezone_location():
    tz = pytz.timezone('Africa/Bamako')
    assert i18n.get_timezone_location(tz) == 'heure : Mali'


@with_setup(setup_en, teardown)
def test_get_timezone_name():
    tz = pytz.timezone('Pacific/Pitcairn')
    d = tz.localize(datetime.datetime(2007, 4, 1, 15, 30))

    assert i18n.get_timezone_name(d, width='long') == 'Pitcairn Time'
    assert i18n.get_timezone_name(d) == 'Pitcairn Time'
    assert i18n.get_timezone_name(d, width='short') == '-0800'

# -----------------------------------------------------------------------------

@with_setup(setup_en, teardown)
def test_get_currency_name():
    assert i18n.get_currency_name('USD') == 'US Dollar'


@with_setup(setup, teardown)
def test_get_currency_symbol():
    assert i18n.get_currency_symbol('USD') == '$US'


@with_setup(setup, teardown)
def test_get_decimal_symbol():
    assert i18n.get_decimal_symbol() == ','


@with_setup(setup, teardown)
def test_get_plus_sign_symbol():
    assert i18n.get_plus_sign_symbol() == '+'


@with_setup(setup, teardown)
def test_get_minus_sign_symbol():
    assert i18n.get_minus_sign_symbol() == '-'


@with_setup(setup, teardown)
def test_get_exponential_symbol():
    assert i18n.get_exponential_symbol() == 'E'


@with_setup(setup, teardown)
def test_get_group_symbol():
    assert i18n.get_group_symbol() == u'\N{NO-BREAK SPACE}'


@with_setup(setup, teardown)
def test_format_number():
    assert i18n.format_number(1099) == u'1\N{NO-BREAK SPACE}099'


@with_setup(setup, teardown)
def test_format_decimal():
    assert i18n.format_decimal(1236.1236) == u'1\N{NO-BREAK SPACE}236,124'


@with_setup(setup, teardown)
def test_format_currency():
    assert i18n.format_currency(1236.126, 'EUR') == u'1\N{NO-BREAK SPACE}236,13\N{NO-BREAK SPACE}\N{EURO SIGN}'


@with_setup(setup, teardown)
def test_format_percent():
    assert i18n.format_percent(24.1234) == u'2\N{NO-BREAK SPACE}412\N{NO-BREAK SPACE}%'


@with_setup(setup, teardown)
def test_format_scientific():
    assert i18n.format_scientific(10000) == '1E4'
    assert i18n.format_scientific(1234567, u'##0E00') == '1.23E06'


@with_setup(setup, teardown)
def test_parse_number():
    assert i18n.parse_number(u'1\N{NO-BREAK SPACE}099') == 1099


@with_setup(setup, teardown)
def test_parse_decimal():
    assert i18n.parse_decimal(u'1\N{NO-BREAK SPACE}099,1234') == decimal.Decimal('1099.1234')

# -----------------------------------------------------------------------------

def test_to_timezone_no_timezone_datetime():
    d = datetime.datetime(2007, 4, 1, 15, 30)

    i18n.set_locale(i18n.Locale('fr', 'FR'))
    d2 = i18n.to_timezone(d)
    assert (d2.tzinfo is None) and (d2.strftime('%H:%M') == '15:30')

    i18n.set_locale(i18n.Locale('fr', 'FR', timezone='Africa/Niamey'))
    d2 = i18n.to_timezone(d)
    assert (str(d2.tzinfo) == 'Africa/Niamey') and (d2.strftime('%H:%M') == '15:30')

    i18n.set_locale(i18n.Locale('fr', 'FR', timezone='Africa/Niamey', default_timezone=pytz.UTC))
    d2 = i18n.to_timezone(d)
    assert (str(d2.tzinfo) == 'Africa/Niamey') and (d2.strftime('%H:%M') == '16:30')


def test_to_timezone_utc_datetime():
    d = pytz.UTC.localize(datetime.datetime(2007, 4, 1, 15, 30))

    i18n.set_locale(i18n.Locale('fr', 'FR'))
    d2 = i18n.to_timezone(d)
    assert (str(d2.tzinfo) == 'UTC') and (d2.strftime('%H:%M') == '15:30')

    i18n.set_locale(i18n.Locale('fr', 'FR', timezone='Africa/Niamey'))
    d2 = i18n.to_timezone(d)
    assert (str(d2.tzinfo) == 'Africa/Niamey') and (d2.strftime('%H:%M') == '16:30')

    i18n.set_locale(i18n.Locale('fr', 'FR', timezone='Africa/Niamey', default_timezone=pytz.UTC))
    d2 = i18n.to_timezone(d)
    assert (str(d2.tzinfo) == 'Africa/Niamey') and (d2.strftime('%H:%M') == '16:30')


def test_to_timezone_local_datetime():
    tz = pytz.timezone('Pacific/Pitcairn')
    d = tz.localize(datetime.datetime(2007, 4, 1, 15, 30))

    i18n.set_locale(i18n.Locale('fr', 'FR'))
    d2 = i18n.to_timezone(d)
    assert (str(d2.tzinfo) == 'Pacific/Pitcairn') and (d2.strftime('%H:%M') == '15:30')

    i18n.set_locale(i18n.Locale('fr', 'FR', timezone='Africa/Niamey'))
    d2 = i18n.to_timezone(d)
    assert (str(d2.tzinfo) == 'Africa/Niamey') and (d2.strftime('%H:%M') == '00:30')

    i18n.set_locale(i18n.Locale('fr', 'FR', timezone='Africa/Niamey', default_timezone=pytz.UTC))
    d2 = i18n.to_timezone(d)
    assert (str(d2.tzinfo) == 'Africa/Niamey') and (d2.strftime('%H:%M') == '00:30')


def test_to_utc_no_timezone_datetime():
    d = datetime.datetime(2007, 4, 1, 15, 30)

    i18n.set_locale(i18n.Locale('fr', 'FR'))
    d2 = i18n.to_utc(d)
    assert (str(d2.tzinfo) == 'UTC') and (d2.strftime('%H:%M') == '15:30')

    i18n.set_locale(i18n.Locale('fr', 'FR', timezone='Africa/Niamey'))
    d2 = i18n.to_utc(d)
    assert (str(d2.tzinfo) == 'UTC') and (d2.strftime('%H:%M') == '14:30')

    i18n.set_locale(i18n.Locale('fr', 'FR', timezone='Africa/Niamey', default_timezone=pytz.UTC))
    d2 = i18n.to_utc(d)
    assert (str(d2.tzinfo) == 'UTC') and (d2.strftime('%H:%M') == '15:30')


def test_to_utc_utc_datetime():
    d = pytz.UTC.localize(datetime.datetime(2007, 4, 1, 15, 30))

    i18n.set_locale(i18n.Locale('fr', 'FR'))
    d2 = i18n.to_utc(d)
    assert (str(d2.tzinfo) == 'UTC') and (d2.strftime('%H:%M') == '15:30')

    i18n.set_locale(i18n.Locale('fr', 'FR', timezone='Africa/Niamey'))
    d2 = i18n.to_utc(d)
    assert (str(d2.tzinfo) == 'UTC') and (d2.strftime('%H:%M') == '15:30')

    i18n.set_locale(i18n.Locale('fr', 'FR', timezone='Africa/Niamey', default_timezone=pytz.UTC))
    d2 = i18n.to_utc(d)
    assert (str(d2.tzinfo) == 'UTC') and (d2.strftime('%H:%M') == '15:30')


def test_to_utc_local_datetime():
    tz = pytz.timezone('Pacific/Pitcairn')
    d = tz.localize(datetime.datetime(2007, 4, 1, 15, 30))

    i18n.set_locale(i18n.Locale('fr', 'FR'))
    d2 = i18n.to_utc(d)
    assert (str(d2.tzinfo) == 'UTC') and (d2.strftime('%H:%M') == '23:30')

    i18n.set_locale(i18n.Locale('fr', 'FR', timezone='Africa/Niamey'))
    d2 = i18n.to_utc(d)
    assert (str(d2.tzinfo) == 'UTC') and (d2.strftime('%H:%M') == '23:30')

    i18n.set_locale(i18n.Locale('fr', 'FR', timezone='Africa/Niamey', default_timezone=pytz.UTC))
    d2 = i18n.to_utc(d)
    assert (str(d2.tzinfo) == 'UTC') and (d2.strftime('%H:%M') == '23:30')


def test_format_time_time_fr1():
    i18n.set_locale(i18n.Locale('fr', 'FR'))

    t = datetime.time(15, 30)

    assert i18n.format_time(t, format='full') == '15:30:00 UTC+00:00'
    assert i18n.format_time(t, format='long') == '15:30:00 +0000'
    assert i18n.format_time(t, format='medium') == '15:30:00'
    assert i18n.format_time(t) == '15:30:00'
    assert i18n.format_time(t, format='short') == '15:30'


def test_format_time_time_fr2():
    i18n.set_locale(i18n.Locale('fr', 'FR', timezone='Africa/Niamey'))

    t = datetime.time(15, 30)

    assert i18n.format_time(t, format='full') == u'15:30:00 heure normale d’Afrique de l’Ouest'
    assert i18n.format_time(t, format='long') == '15:30:00 +0100'
    assert i18n.format_time(t, format='medium') == '15:30:00'
    assert i18n.format_time(t) == '15:30:00'
    assert i18n.format_time(t, format='short') == '15:30'


def test_format_time_time_fr3():
    i18n.set_locale(i18n.Locale('fr', 'FR'))

    t = datetime.time(15, 30, tzinfo=pytz.timezone('Pacific/Pitcairn'))

    assert i18n.format_time(t, format='full') == '15:30:00 UTC+00:00'
    assert i18n.format_time(t, format='long') == '15:30:00 +0000'
    assert i18n.format_time(t, format='medium') == '15:30:00'
    assert i18n.format_time(t) == '15:30:00'
    assert i18n.format_time(t, format='short') == '15:30'


def test_format_time_time_fr4():
    i18n.set_locale(i18n.Locale('fr', 'FR', timezone='Africa/Niamey'))

    t = datetime.time(15, 30, tzinfo=pytz.timezone('Pacific/Pitcairn'))

    assert i18n.format_time(t, format='full') == u'15:30:00 heure normale d’Afrique de l’Ouest'
    assert i18n.format_time(t, format='long') == '15:30:00 +0100'
    assert i18n.format_time(t, format='medium') == '15:30:00'
    assert i18n.format_time(t) == '15:30:00'
    assert i18n.format_time(t, format='short') == '15:30'


def test_format_time_time_en():
    i18n.set_locale(i18n.Locale('en', 'US', timezone='Pacific/Pitcairn'))

    t = datetime.time(15, 30)

    assert i18n.format_time(t, format='full') == '3:30:00 PM Pitcairn Time'
    assert i18n.format_time(t, format='long') == '3:30:00 PM -0800'
    assert i18n.format_time(t, format='medium') == '3:30:00 PM'
    assert i18n.format_time(t) == '3:30:00 PM'
    assert i18n.format_time(t, format='short') == '3:30 PM'


def test_format_time_time_with_format():
    i18n.set_locale(i18n.Locale('en', 'US', timezone='Pacific/Pitcairn'))

    t = datetime.time(15, 30)
    assert i18n.format_time(t, format="hh 'o''clock' a, zzzz") == "03 o'clock PM, Pitcairn Time"

    t = datetime.time(15, 30, tzinfo=pytz.timezone('Africa/Niamey'))
    assert i18n.format_time(t, format="hh 'o''clock' a, zzzz") == "03 o'clock PM, Pitcairn Time"


def test_format_time_datetime_fr1():
    i18n.set_locale(i18n.Locale('fr', 'FR'))

    d = datetime.datetime(2007, 4, 1, 15, 30)

    assert i18n.format_time(d, format='full') == '15:30:00 UTC+00:00'
    assert i18n.format_time(d, format='long') == '15:30:00 +0000'
    assert i18n.format_time(d, format='medium') == '15:30:00'
    assert i18n.format_time(d) == '15:30:00'
    assert i18n.format_time(d, format='short') == '15:30'


def test_format_time_datetime_fr2():
    i18n.set_locale(i18n.Locale('fr', 'FR', timezone='Africa/Niamey'))

    d = datetime.datetime(2007, 4, 1, 15, 30)

    assert i18n.format_time(d, format='full') == u'15:30:00 heure normale d’Afrique de l’Ouest'
    assert i18n.format_time(d, format='long') == '15:30:00 +0100'
    assert i18n.format_time(d, format='medium') == '15:30:00'
    assert i18n.format_time(d) == '15:30:00'
    assert i18n.format_time(d, format='short') == '15:30'


def test_format_time_datetime_fr3():
    i18n.set_locale(i18n.Locale('fr', 'FR', timezone='Africa/Niamey', default_timezone=pytz.UTC))

    d = datetime.datetime(2007, 4, 1, 15, 30)

    assert i18n.format_time(d, format='full') == u'16:30:00 heure normale d’Afrique de l’Ouest'
    assert i18n.format_time(d, format='long') == '16:30:00 +0100'
    assert i18n.format_time(d, format='medium') == '16:30:00'
    assert i18n.format_time(d) == '16:30:00'
    assert i18n.format_time(d, format='short') == '16:30'


def test_format_time_datetime_fr4():
    i18n.set_locale(i18n.Locale('fr', 'FR'))

    tz = pytz.timezone('Pacific/Pitcairn')
    d = tz.localize(datetime.datetime(2007, 4, 1, 15, 30))

    assert i18n.format_time(d, format='full') == '23:30:00 UTC+00:00'
    assert i18n.format_time(d, format='long') == '23:30:00 +0000'
    assert i18n.format_time(d, format='medium') == '23:30:00'
    assert i18n.format_time(d) == '23:30:00'
    assert i18n.format_time(d, format='short') == '23:30'


def test_format_time_datetime_fr5():
    i18n.set_locale(i18n.Locale('fr', 'FR', timezone='Africa/Niamey'))

    tz = pytz.timezone('Pacific/Pitcairn')
    d = tz.localize(datetime.datetime(2007, 4, 1, 15, 30))

    assert i18n.format_time(d, format='full') == u'00:30:00 heure normale d’Afrique de l’Ouest'
    assert i18n.format_time(d, format='long') == '00:30:00 +0100'
    assert i18n.format_time(d, format='medium') == '00:30:00'
    assert i18n.format_time(d) == '00:30:00'
    assert i18n.format_time(d, format='short') == '00:30'


def test_format_time_datetime_with_format():
    i18n.set_locale(i18n.Locale('en', 'US', timezone='Pacific/Pitcairn'))

    d = datetime.datetime(2007, 4, 1, 15, 30)
    assert i18n.format_time(d, format="hh 'o''clock' a, zzzz") == "03 o'clock PM, Pitcairn Time"

    tz = pytz.timezone('Africa/Niamey')
    d = tz.localize(datetime.datetime(2007, 4, 1, 15, 30))
    assert i18n.format_time(d, format="hh 'o''clock' a, zzzz") == "06 o'clock AM, Pitcairn Time"


@with_setup(setup, teardown)
def test_format_date_date():
    d = datetime.date(2007, 4, 1)

    assert i18n.format_date(d, format='full') == 'dimanche 1 avril 2007'
    assert i18n.format_date(d, format='long') == '1 avril 2007'
    assert i18n.format_date(d, format='medium') == '1 avr. 2007'
    assert i18n.format_date(d) == '1 avr. 2007'
    assert i18n.format_date(d, format='short') == '01/04/2007'


@with_setup(setup, teardown)
def test_format_date_datetime():
    tz = pytz.timezone('Pacific/Pitcairn')
    d = tz.localize(datetime.datetime(2007, 4, 1, 15, 30))

    assert i18n.format_date(d, format='full') == 'dimanche 1 avril 2007'
    assert i18n.format_date(d, format='long') == '1 avril 2007'
    assert i18n.format_date(d, format='medium') == '1 avr. 2007'
    assert i18n.format_date(d) == '1 avr. 2007'
    assert i18n.format_date(d, format='short') == '01/04/2007'


@with_setup(setup, teardown)
def test_format_date_date_with_format():
    d = datetime.date(2007, 4, 1)

    assert i18n.format_date(d, 'EEE, MMM d, yy') == 'dim., avr. 1, 07'


@with_setup(setup, teardown)
def test_format_datetime():
    i18n.set_locale(i18n.Locale('fr', 'FR', timezone='Africa/Niamey'))

    tz = pytz.timezone('Pacific/Pitcairn')
    d = tz.localize(datetime.datetime(2007, 4, 1, 15, 30))

    assert i18n.format_datetime(d, format='full') == u'lundi 2 avril 2007 à 00:30:00 heure normale d’Afrique de l’Ouest'
    assert i18n.format_datetime(d, format='long') == u'2 avril 2007 à 00:30:00 +0100'
    assert i18n.format_datetime(d, format='medium') == u'2 avr. 2007 à 00:30:00'
    assert i18n.format_datetime(d) == u'2 avr. 2007 à 00:30:00'
    assert i18n.format_datetime(d, format='short') == u'02/04/2007 00:30'


def test_format_datetime_with_format():
    i18n.set_locale(i18n.Locale('en', 'US', timezone='Pacific/Pitcairn'))

    d = datetime.datetime(2007, 4, 1, 15, 30)
    assert i18n.format_datetime(d, format="yyyy.MM.dd G 'at' HH:mm:ss zzz") == '2007.04.01 AD at 15:30:00 -0800'

    tz = pytz.timezone('Africa/Niamey')
    d = tz.localize(datetime.datetime(2007, 4, 1, 15, 30))
    assert i18n.format_datetime(d, format="yyyy.MM.dd G 'at' HH:mm:ss zzz") == '2007.04.01 AD at 06:30:00 -0800'


@with_setup(setup, teardown)
def test_parse_time_fr():
    t = i18n.parse_time('15:30:10')
    assert isinstance(t, datetime.time)
    assert (t.hour == 15) and (t.minute == 30) and (t.second == 10)

@with_setup(setup_en, teardown)
def test_parse_time_en():
    t = i18n.parse_time('15:30:10')
    assert isinstance(t, datetime.time)
    assert (t.hour == 15) and (t.minute == 30) and (t.second == 10)

@with_setup(setup, teardown)
def test_parse_date_fr():
    d = i18n.parse_date('4/1/04')
    assert isinstance(d, datetime.date)
    assert (d.year == 2004) and (d.month == 1) and (d.day == 4)

    d = i18n.parse_date('4/1/2004')
    assert isinstance(d, datetime.date)
    assert (d.year == 2004) and (d.month == 1) and (d.day == 4)


@with_setup(setup_en, teardown)
def test_parse_date_en():
    d = i18n.parse_date('4/1/04')
    assert isinstance(d, datetime.date)
    assert (d.year == 2004) and (d.month == 4) and (d.day == 1)

    d = i18n.parse_date('4/1/2004')
    assert isinstance(d, datetime.date)
    assert (d.year == 2004) and (d.month == 4) and (d.day == 1)


def test_context_manager():
    locale1 = i18n.Locale('fr', 'FR', domain='domain1')
    locale2 = i18n.Locale('fr', 'FR', domain='domain2')
    i18n.set_locale(locale1)
    assert i18n.get_locale().domain == 'domain1', i18n.get_locale().domain
    with locale2:
        assert i18n.get_locale().domain == 'domain2', i18n.get_locale().domain
        with locale2:
            assert i18n.get_locale().domain == 'domain2', i18n.get_locale().domain

    assert i18n.get_locale().domain == 'domain1', i18n.get_locale().domain
