# -*- coding: utf-8 -*-
import re
import os
import uuid

import pytest
import popquotes.pmxbot

from pmxbot import pmxbot
from pmxbot import karma

def pytest_generate_tests(metafunc):
	# any test that takes the iter_ parameter should be executed 100 times
	if "iter_" in metafunc.funcargnames:
		for i in range(100):
			metafunc.addcall(funcargs=dict(iter_=i))

class Empty(object):
	"""
	Passed in to the individual commands instead of a client/event because
	we don't normally care about them
	"""
	pass

c = Empty()
e = Empty()


def logical_xor(a, b):
	return bool(a) ^ bool(b)

def onetrue(*args):
	truthiness = filter(bool, args)
	if len(truthiness) == 1:
		return True
	else:
		return False

class TestCommands(object):
	@classmethod
	def setup_class(self):
		path = os.path.dirname(os.path.abspath(__file__))
		configfile = os.path.join(path, 'testconf.yaml')
		pmxbot.run(configFile=configfile, start=False)
		pmxbot.botbase.logger.message("logged", "testrunner", "some text")

	@classmethod
	def teardown_class(self):
		pmxbot._cleanup()
		path = os.path.dirname(os.path.abspath(__file__))
		os.remove(os.path.join(path, 'pmxbot.sqlite'))

	@pytest.has_internet
	def test_google(self):
		"""
		Basic google search for "pmxbot". Result must contain a link.
		"""
		res = pmxbot.google(c, e, "#test", "testrunner", "pmxbot")
		print res
		assert "http" in res

	@pytest.has_internet
	def test_googlecalc_simple(self):
		"""
		Basic google calculator command - 1+1 must include 2 in results
		"""
		res = pmxbot.googlecalc(c, e, "#test", "testrunner", "1+1")
		print res
		assert "2" in res

	@pytest.has_internet
	def test_googlecalc_complicated(self):
		"""
		More complicated google calculator command - 40 gallons in liters must
		include 151.4 in results
		"""
		res = pmxbot.googlecalc(c, e, "#test", "testrunner", "40 gallons in liters")
		print res
		assert "151.4" in res

	@pytest.has_internet
	def test_googlecalc_supercomplicated(self):
		"""
		Supercomplicated google calculator command - 502 hogsheads per mile in
		litres per km includes 74 and 388.9641 in results
		"""
		res = pmxbot.googlecalc(c, e, "#test", "testrunner",
			"502 hogsheads per mile in litres per km")
		assert "388.9641" in res and "74" in res

	@pytest.has_internet
	def test_googlecalc_currency_usd_gbp(self):
		"""
		Test that google calculator for a currency conversion: 1 USD in GBP
		"""
		res = pmxbot.googlecalc(c, e, "#test", "testrunner", "1 USD in GBP")
		print res
		assert re.match(r"""1 (?:US|U\.S\.) dollars? = \d\.\d+ British pounds?(?: sterling)?""", res)

	@pytest.has_internet
	def test_googlecalc_currency_czk_euro(self):
		"""
		Test that google calculator for a currency conversion: 12 CZK in euros
		"""
		res = pmxbot.googlecalc(c, e, "#test", "testrunner", "12 CZK in euros")
		print res
		assert re.match(r"""12 Czech(?: Republic)? [Kk]orun(?:a|y)s? = \d\.\d+ [Ee]uros?""", res)

	# time patterns come as 4:20pm when queried from the U.S. and 16:20
	#  when queried from (at least some) other locales.
	time_pattern = re.compile(r'^[0-9]{1,2}:[0-9]{2}(?:am|pm)?')

	@pytest.has_internet
	def test_time_one(self):
		"""
		Check the time in Washington, DC. Must match time_pattern.
		"""
		res = pmxbot.googletime(c, e, "#test", "testrunner", "Washington, DC")
		assert res
		i = 0
		for line in res:
			print line
			i += 1
			assert self.time_pattern.match(line)
		assert i == 1

	@pytest.has_internet
	def test_time_three(self):
		"""
		Check the time in three cities. Must include something that
		matches the time pattern on each line
		"""
		res = pmxbot.googletime(c, e, "#test", "testrunner",
			"Washington, DC | Palo Alto, CA | London")
		assert res
		i = 0
		for line in res:
			print line
			i += 1
			assert self.time_pattern.match(line)
		assert i == 3

	@pytest.has_internet
	def test_time_all(self):
		"""
		Check the time in "all" cities. Must include something that
		matches the time pattern on each line
		"""
		res = pmxbot.googletime(c, e, "#test", "testrunner", "all")
		assert res
		i = 0
		for line in res:
			print line
			i += 1
			assert self.time_pattern.match(line)
		assert i == 4

	def test_weather_one(self):
		"""
		Check the weather in Washington, DC. Must include something that looks like a weather XX:XX(AM/PM)
		"""
		res = pmxbot.weather(c, e, "#test", "testrunner", "Washington, DC")
		for line in res:
			print line
			assert re.match(r""".+\. Currently: (?:-)?[0-9]{1,3}F/(?:-)?[0-9]{1,2}C, .+\.\W+[A-z]{3}: (?:-)?[0-9]{1,3}F/(?:-)?[0-9]{1,2}C, """, line)

	def test_weather_three(self):
		"""
		Check the weather in three cities. Must include something that looks like
		a weather XX:XX(AM/PM) on each line
		"""
		res = pmxbot.weather(c, e, "#test", "testrunner", "Washington, DC | Palo Alto, CA | London")
		for line in res:
			print line
			assert re.match(r""".+\. Currently: (?:-)?[0-9]{1,3}F/(?:-)?[0-9]{1,2}C, .+\.\W+[A-z]{3}: (?:-)?[0-9]{1,3}F/(?:-)?[0-9]{1,2}C, """, line)

	def test_weather_all(self):
		"""
		Check the weather in "all" cities. Must include something that looks like
		a weather XX:XX(AM/PM) on each line
		"""
		res = pmxbot.weather(c, e, "#test", "testrunner", "all")
		for line in res:
			print line
			assert re.match(r""".+\. Currently: (?:-)?[0-9]{1,3}F/(?:-)?[0-9]{1,2}C, .+\.\W+[A-z]{3}: (?:-)?[0-9]{1,3}F/(?:-)?[0-9]{1,2}C, """, line)

	def test_boo(self):
		"""
		Test "boo foo"
		"""
		subject = "foo"
		pre = karma.Karma.store.lookup(subject)
		res = pmxbot.boo(c, e, "#test", "testrunner", subject)
		assert res == "/me BOOO %s!!! BOOO!!!" % subject
		post = karma.Karma.store.lookup(subject)
		assert post == pre - 1

	def test_troutslap(self):
		"""
		Test "troutslap foo"
		"""
		subject = "foo"
		pre = karma.Karma.store.lookup(subject)
		res = pmxbot.troutslap(c, e, "#test", "testrunner", subject)
		assert res == "/me slaps %s around a bit with a large trout" % subject
		post = karma.Karma.store.lookup(subject)
		assert post == pre - 1

	def test_keelhaul(self):
		"""
		Test "keelhaul foo"
		"""
		subject = "foo"
		pre = karma.Karma.store.lookup(subject)
		res = pmxbot.keelhaul(c, e, "#test", "testrunner", subject)
		assert res == "/me straps %s to a dirty rope, tosses 'em overboard and pulls with great speed. Yarrr!" % subject
		post = karma.Karma.store.lookup(subject)
		assert post == pre - 1

	def test_motivate(self):
		"""
		Test that motivate actually works.
		"""
		subject = "foo"
		pre = karma.Karma.store.lookup(subject)
		res = pmxbot.motivate(c, e, "#test", "testrunner", subject)
		assert res == "you're doing good work, %s!" % subject
		post = karma.Karma.store.lookup(subject)
		assert post == pre + 1

	def test_motivate_with_spaces(self):
		"""
		Test that motivate strips beginning and ending whitespace
		"""
		subject = "foo"
		pre = karma.Karma.store.lookup(subject)
		res = pmxbot.motivate(c, e, "#test", "testrunner", "   %s 	  " % subject)
		assert res == "you're doing good work, %s!" % subject
		post = karma.Karma.store.lookup(subject)
		assert post == pre + 1

	def test_demotivate(self):
		"""
		Test that demotivate actually works.
		"""
		subject = "foo"
		pre = karma.Karma.store.lookup(subject)
		res = pmxbot.demotivate(c, e, "#test", "testrunner", subject)
		assert res == "you're doing horrible work, %s!" % subject
		post = karma.Karma.store.lookup(subject)
		assert post == pre - 1

	def test_imotivate(self):
		"""
		Test that ironic/sarcastic motivate actually works.
		"""
		subject = "foo"
		pre = karma.Karma.store.lookup(subject)
		res = pmxbot.imotivate(c, e, "#test", "testrunner", subject)
		assert res == """you're "doing" "good" "work", %s!""" % subject
		post = karma.Karma.store.lookup(subject)
		assert post == pre - 1

	def test_add_quote(self):
		"""
		Try adding a quote
		"""
		quote = "And then she said %s" % str(uuid.uuid4())
		res = pmxbot.quote(c, e, "#test", "testrunner", "add %s" % quote)
		assert res == "Quote added!"
		cursor = pmxbot.botbase.logger.db.cursor()
		cursor.execute("select count(*) from quotes where library = 'pmx' and quote = ?", (quote,))
		numquotes = cursor.fetchone()[0]
		assert numquotes == 1

	def test_add_and_retreive_quote(self):
		"""
		Try adding a quote, then retrieving it
		"""
		id = str(uuid.uuid4())
		quote = "So I says to Mabel, I says, %s" % id
		res = pmxbot.quote(c, e, "#test", "testrunner", "add %s" % quote)
		assert res == "Quote added!"
		cursor = pmxbot.botbase.logger.db.cursor()
		cursor.execute("select count(*) from quotes where library = 'pmx' and quote = ?", (quote,))
		numquotes = cursor.fetchone()[0]
		assert numquotes == 1

		res = pmxbot.quote(c, e, "#test", "testrunner", id)
		assert res == "(1/1): %s" % quote

	def test_roll(self):
		"""
		Roll a die, both with no arguments and with some numbers
		"""
		res = int(pmxbot.roll(c, e, "#test", "testrunner", "").split()[-1])
		assert res >= 0 and res <= 100
		n = 6668

		res = int(pmxbot.roll(c, e, "#test", "testrunner", "%s" % n).split()[-1])
		assert res >= 0 and res <= n

	@pytest.has_internet
	def test_ticker_goog(self):
		"""
		Get the current stock price of Google.

		GOOG at 4:00pm (ET): 484.81 (1.5%)
		"""
		res = pmxbot.ticker(c, e, "#test", "testrunner", "goog")
		print res
		assert re.match(r"""^GOOG at \d{1,2}:\d{2}(?:am|pm) \([A-z]{1,3}\): \d{2,4}.\d{1,4} \(\-?\d{1,3}.\d%\)$""", res), res

	@pytest.has_internet
	def test_ticker_yougov(self):
		"""
		Get the current stock price of YouGov.

		YOU.L at 10:37am (ET): 39.40 (0.4%)
		"""
		res = pmxbot.ticker(c, e, "#test", "testrunner", "you.l")
		print res
		assert re.match(r"""^YOU.L at \d{1,2}:\d{2}(?:am|pm) \([A-z]{1,3}\): \d{1,4}.\d{2,4} \(\-?\d{1,3}.\d%\)$""", res), res

	@pytest.has_internet
	def test_ticker_nasdaq(self):
		"""
		Get the current stock price of the NASDAQ.

		^IXIC at 10:37am (ET): 2490.40 (0.4%)
		"""
		res = pmxbot.ticker(c, e, "#test", "testrunner", "^ixic")
		print res
		assert re.match(r"""^\^IXIC at \d{1,2}:\d{2}(?:am|pm) \([A-z]{1,3}\): \d{4,5}.\d{2} \(\-?\d{1,3}.\d%\)$""", res), res

	def test_pick_or(self):
		"""
		Test the pick command with a simple or expression
		"""
		res = pmxbot.pick(c, e, "#test", "testrunner", "fire or acid")
		assert logical_xor("fire" in res, "acid" in res)
		assert " or " not in res

	def test_pick_or_intro(self):
		"""
		Test the pick command with an intro and a simple "or" expression
		"""
		res = pmxbot.pick(c, e, "#test", "testrunner", "how would you like to die, pmxbot: fire or acid")
		assert logical_xor("fire" in res, "acid" in res)
		assert "die" not in res and "pmxbot" not in res and " or " not in res

	def test_pick_comma(self):
		"""
		Test the pick command with two options separated by commas
		"""
		res = pmxbot.pick(c, e, "#test", "testrunner", "fire, acid")
		assert logical_xor("fire" in res, "acid" in res)

	def test_pick_comma_intro(self):
		"""
		Test the pick command with an intro followed by two options separted by commas
		"""
		res = pmxbot.pick(c, e, "#test", "testrunner", "how would you like to die, pmxbot: fire, acid")
		assert logical_xor("fire" in res, "acid" in res)
		assert "die" not in res and "pmxbot" not in res

	def test_pick_comma_or_intro(self):
		"""
		Test the pick command with an intro followed by options with commands and ors
		"""
		res = pmxbot.pick(c, e, "#test", "testrunner", "how would you like to die, pmxbot: gun, fire, acid or defenestration")
		assert onetrue("gun" in res, "fire" in res, "acid" in res, "defenestration" in res)
		assert "die" not in res and "pmxbot" not in res and " or " not in res

	def test_lunch(self):
		"""
		Test that the lunch command selects one of the list options
		"""
		res = pmxbot.lunch(c, e, "#test", "testrunner", "PA")
		assert res in ["Pasta?", "Thaiphoon", "Pluto's", "Penninsula Creamery", "Kan Zeman"]

	def test_karma_check_self_blank(self):
		"""
		Determine your own, blank, karma.
		"""
		id = str(uuid.uuid4())[:15]
		res = pmxbot.karma(c, e, "#test", id, "")
		assert re.match(r"^%s has 0 karmas$" % id, res)

	def test_karma_check_other_blank(self):
		"""
		Determine some else's blank/new karma.
		"""
		id = str(uuid.uuid4())
		res = pmxbot.karma(c, e, "#test", "testrunner", id)
		assert re.match("^%s has 0 karmas$" % id, res)

	def test_karma_set_and_check(self):
		"""
		Take a new entity, give it some karma, check that it has more
		"""
		id = str(uuid.uuid4())
		res = pmxbot.karma(c, e, "#test", "testrunner", id)
		assert re.match("^%s has 0 karmas$" % id, res)
		res = pmxbot.karma(c, e, "#test", "testrunner", "%s++" %id)
		res = pmxbot.karma(c, e, "#test", "testrunner", "%s++" %id)
		res = pmxbot.karma(c, e, "#test", "testrunner", "%s++" %id)
		res = pmxbot.karma(c, e, "#test", "testrunner", "%s--" %id)
		res = pmxbot.karma(c, e, "#test", "testrunner", id)
		assert re.match(r"^%s has 2 karmas$" % id, res)

	def test_karma_set_and_check_with_space(self):
		"""
		Take a new entity that has a space in it's name, give it some karma, check that it has more
		"""
		id = str(uuid.uuid4()).replace("-", " ")
		res = pmxbot.karma(c, e, "#test", "testrunner", id)
		assert re.match("^%s has 0 karmas$" % id, res)
		res = pmxbot.karma(c, e, "#test", "testrunner", "%s++" %id)
		res = pmxbot.karma(c, e, "#test", "testrunner", "%s++" %id)
		res = pmxbot.karma(c, e, "#test", "testrunner", "%s++" %id)
		res = pmxbot.karma(c, e, "#test", "testrunner", "%s--" %id)
		res = pmxbot.karma(c, e, "#test", "testrunner", id)
		assert re.match(r"^%s has 2 karmas$" % id, res)

	def test_karma_randomchange(self):
		"""
		Take a new entity that has a space in it's name, give it some karma, check that it has more
		"""
		id = str(uuid.uuid4())
		flags = {}
		i = 0
		karmafetch = re.compile(r"^%s has (\-?\d+) karmas$" % id)
		while len(flags) < 3 and i <= 30:
			res = pmxbot.karma(c, e, "#test", "testrunner", id)
			prekarma = int(karmafetch.findall(res)[0])
			change = pmxbot.karma(c, e, "#test", "testrunner", "%s~~" % id)
			assert change in ["%s karma++" % id, "%s karma--" % id, "%s karma shall remain the same" % id]
			if change.endswith('karma++'):
				flags['++'] = True
				res = pmxbot.karma(c, e, "#test", "testrunner", id)
				postkarma = int(karmafetch.findall(res)[0])
				assert postkarma == prekarma + 1
			elif change.endswith('karma--'):
				flags['--'] = True
				res = pmxbot.karma(c, e, "#test", "testrunner", id)
				postkarma = int(karmafetch.findall(res)[0])
				assert postkarma == prekarma - 1
			elif change.endswith('karma shall remain the same'):
				flags['same'] = True
				res = pmxbot.karma(c, e, "#test", "testrunner", id)
				postkarma = int(karmafetch.findall(res)[0])
				assert postkarma == prekarma
			i+=1
		assert len(flags) == 3
		assert i < 30

	def test_calc_simple(self):
		"""
		Test the built-in python calculator with a simple expression - 2+2
		"""
		res = pmxbot.calc(c, e, "#test", "testrunner", "2+2")
		print res
		assert res == "4"

	def test_calc_complex(self):
		"""
		Test the built-in python calculator with a more complicated formula
		((((781**2)*5)/92835.3)+4)**0.5
		"""
		res = pmxbot.calc(c, e, "#test", "testrunner", "((((781**2)*5)/92835.3)+4)**0.5")
		print res
		assert res.startswith("6.070566")

	@pytest.has_internet
	def test_define_keyboard(self):
		"""
		Test the dictionary with the word keyboard.
		"""
		res = pmxbot.defit(c, e, "#test", "testrunner", "keyboard")
		assert isinstance(res, unicode)
		assert res == ("Wordnik says: A set of keys, as on a computer "
			"terminal, word processor, typewriter, or piano.")

	@pytest.has_internet
	def test_define_irc(self):
		"""
		Test the dictionary with the word IRC.
		"""
		res = pmxbot.defit(c, e, "#test", "testrunner", "  IRC \t")
		assert isinstance(res, unicode)
		assert res == "Wordnik says: An international computer network of Internet servers, using its own protocol through which individual users can hold real-time online conversations."

	@pytest.has_internet
	def test_define_notaword(self):
		"""
		Test the dictionary with a nonsense word.
		"""
		res = pmxbot.defit(c, e, "#test", "testrunner", "notaword")
		assert isinstance(res, unicode)
		assert res == "Wordnik does not have a definition for that."

	@pytest.has_internet
	def test_urb_irc(self):
		"""
		Test the urban dictionary with the word IRC.
		"""
		res = pmxbot.urbandefit(c, e, "#test", "testrunner", "irc")
		assert "Internet Relay Chat" in res
		assert "protocol" in res.lower()

	@pytest.has_internet
	def test_acronym_irc(self):
		"""
		Test acronym finder with the word IRC.
		"""
		res = pmxbot.acit(c, e, "#test", "testrunner", "irc")
		assert "Internet Relay Chat" in res
		assert "|" in res

	def test_progress(self):
		"""
		Test the progress bar
		"""
		res = pmxbot.progress(c, e, "#test", "testrunner", "1|98123|30")
		print res
		assert res == "1 [===       ] 98123"

	def test_strategy(self):
		"""
		Test the social strategy thingie
		"""
		res = pmxbot.strategy(c, e, "#test", "testrunner", "")
		print res
		assert res != ""

	@pytest.has_internet
	def test_paste_newuser(self):
		"""
		Test the pastebin with an unknown user
		"""
		person = str(uuid.uuid4())[:9]
		res = pmxbot.paste(c, e, '#test', person, '')
		print res
		assert res == "hmm.. I didn't find a recent paste of yours, %s. Checkout http://a.libpa.st/" % person

	@pytest.has_internet
	def test_paste_real_user(self):
		"""
		Test the pastebin with a valid user with an existing paste
		"""
		person = 'vbSptH3ByfQQ6h'
		res = pmxbot.paste(c, e, '#test', person, '')
		assert res == "http://a.libpa.st/40a4345a-4e4b-40d8-ad06-c0a22a26b282"

	def test_qbiu_person(self):
		"""
		Test the qbiu function with a specified person.
		"""
		bitcher = "all y'all"
		res = pmxbot.bitchingisuseless(c, e, '#test', 'testrunner', bitcher)
		print res
		assert res == "Quiet bitching is useless, all y'all. Do something about it."

	def test_qbiu_blank(self):
		"""
		Test the qbiu function with a specified person.
		"""
		res = pmxbot.bitchingisuseless(c, e, '#test', 'testrunner', '')
		print res
		assert res == "Quiet bitching is useless, foo'. Do something about it."

	def test_excuse(self):
		import excuses
		gen = excuses.RandomExcuseGenerator.create_local()
		gen.pmxbot_excuse(c, e, '#test', 'testrunner', '')

	def test_popquotes(self):
		popquotes.pmxbot.install_commands()
		res = popquotes.pmxbot.bender(c, e, '#test', 'testrunner', '')
		assert len(res) > 5

	def test_rand_bot(self, iter_):
		res = pmxbot.rand_bot(c, e, '#test', 'testrunner', '')
		if res is None: return
		if not isinstance(res, basestring):
			res = u''.join(res)
		assert len(res)
