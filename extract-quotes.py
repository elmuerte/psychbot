#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2023 Michiel Hendriks
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys, pathlib, re, textwrap, sqlite3

# ASGD027GL
# \  /\ /\/
#  |   |  `- defines the character talking!
#  |   `---- some unique number
#  `-------- level/movie/.. reference

characters = {}
characters["AN"] = "Wrestling Announcer"
characters["BD"] = "Bulldog"
characters["BE"] = "Becky Houndstooth"
characters["BN"] = "Benny Fideleo"
characters["BO"] = "Boyd Cooper"
characters["BU"] = "The Butcher"
characters["BT"] = "Bonita Soleil"
characters["BY"] = "Underground Rapid Transit System"
characters["BZ"] = "Bobby Zilch"
characters["CB"] = "Cobra"
characters["CF"] = "Crystal Flowers Snagrash"
characters["CH"] = "Chloe Barge"
characters["CL"] = "Collie"
characters["CM"] = "Clem Foote"
characters["CN"] = "Carpenter"
characters["CO"] = "Coach Oleander"
characters["CP"] = "Melvin \"Chops\" Sweetwind"
characters["CR"] = "Crispin Whytehead"
characters["DA"] = "Dalmatian"
characters["DI"] = "Dingo Inflagrante"
characters["DN"] = "Dancer"
characters["DM"] = "Den Mother"
characters["DO"] = "Dogen Boole"
characters["DR"] = "Dragon"
characters["EA"] = "Eagle"
characters["ED"] = "Edgar Teglee"
characters["EF"] = "Elton Fir"
characters["EL"] = "Elka Doom"
characters["EV"] = "Evil Augustus"
characters["KI"] = "Kitty Bubai"
characters["LF"] = "Linda"
characters["FA"] = "Franke Athens"
characters["FF"] = "Orange flower"
characters["FT"] = "Thistle"
characters["FR"] = "Fred Bonaparte"
characters["FO"] = "Ford Cruller"
characters["GD"] = "Augustus Aquato"
characters["GM"] = "G-Man"
characters["HF"] = "Blue flower"
characters["HT"] = "Head thistle"
characters["JA"] = "Jasper Rolls"
characters["JT"] = "J. T. Hoofburger"
characters["KN"] = "Hearty Knight"
characters["LA"] = "Lampita Pasionado"
characters["LC"] = "Lungfish Citizen"
characters["LI"] = "Lili Zanotto"
characters["LO"] = "Dr. Loboto" # Dr. Caligosto Loboto
characters["LP"] = "Officer O'Lungfish"
characters["LR"] = "Lungfish Citizen"
characters["LY"] = "Lungfish Citizen"
characters["GL"] = "Gloria Von Gouten"
characters["MA"] = "Dingo Inflagrante"
characters["MD"] = "Dancer"
characters["MF"] = "Maloof Canola"
characters["MH"] = "Mikhail Bulgakov"
characters["MI"] = "Milla Vodello"
characters["MM"] = "Militiaman"
characters["MP"] = "Milka Phage"
characters["NI"] = "Nils Lutefisk"
characters["NP"] = "Napoleon Bonaparte"
characters["OL"] = "Morceau \"Oly\" Oleander"
characters["P1"] = "Peasant"
characters["P2"] = "Peasant"
characters["P3"] = "Peasant"
characters["PH"] = "Phoebe Love"
characters["PL"] = "Mr. Pokeylope"
characters["PT"] = "The Phantom"
characters["QU"] = "Quentin Hedgemouse"
characters["RA"] = "Raz"
characters["RQ"] = "Rainbow Squirt"
characters["RS"] = "Rainbow Squirt"
characters["SA"] = "Sasha Nein"
characters["SB"] = "St. Bernard"
characters["SD"] = "Soldier"
characters["SF"] = "Pink flower"
characters["SH"] = "Sheegor"
characters["SN"] = "Snails"
characters["ST"] = "Small thistle"
characters["TI"] = "Tiger"
characters["TO"] = "" # Inventory / Help text
characters["VE"] = "Vernon Tripe"

class StringsFile:
	def __init__(self, source):
		self.source = source

	def __enter__(self):
		self._fp = open(self.source, "rt", encoding="cp1252", errors="ignore")
		self._more = True
		self.line = ""
		self.id = None
		return self

	def __exit__(self, *args):
		self._fp.close()

	def has_next(self):
		return self._more

	def next(self):
		if not self._more:
			return False
		if (ln := self._fp.readline()):
			self.line = ln
			self.id = re.match("^(([A-Z]{4})([0-9]{3})([A-Z]{2}))\n$", ln)
		else:
			self._more = False
		return self._more

	def is_id(self):
		return self.id

	def next_id(self):
		while self.has_next():
			self.next()
			if self.is_id():
				return

def add_quote(id, text):
	text = text.strip()
	if not text:
		return
	print("Quote", id.group(1), text)
	speaker = characters[id.group(4)]
	db.execute(
		"""
		insert into quotes (id, speaker, message) values (?, ?, ?)
		on conflict(id) do update set speaker = ?, message = ?
		""",
		(id.group(1), speaker, text, speaker, text)
	)

def proc_entry(fp):
	id = fp.id
	fp.next()
	if fp.is_id():
		return
	text = fp.line
	add_quote(id, text)

def proc_file(fp):
	while fp.has_next():
		if fp.is_id():
			proc_entry(fp)
		else:
			fp.next_id()

def init_db():
	db.execute('''
		create table if not exists quotes (
			id text primary key,
			speaker text,
			message text,
			enabled boolean not null default true,
			last_used timestamp
		)
	''')

db_conn = sqlite3.connect('quotes.db')
db = db_conn.cursor()
init_db()

try:
	with StringsFile(sys.argv[1]) as fp:
		proc_file(fp)
	db_conn.commit()
finally:
	db.close()
	db_conn.close()
