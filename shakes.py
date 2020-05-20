from urllib.request import urlopen
import random
from statistics import mean
#from 'oxford_dictionary.py' import *

###########
#### API REQUEST MODULE
import requests
import json
app_id = "ff1366d1"
app_key = "2570c76c5136c6a51f084384d5ae91c2"
language = "en-gb"
delims = ['.',';',':',',','?','!','*','(',')','}','{','|']
def get_word_type(word):
	for i in delims:
		if i in word:
			return 'rejected'
	if word in dictionary.values():
		print("yolo")
		return [x for x in dictionary.keys() if word in dictionary[x]][0]
	word_id = str(word)
	url = "https://od-api.oxforddictionaries.com:443/api/v2/entries/" + language + "/" + word_id.lower()
	r = requests.get(url, headers={"app_id": app_id, "app_key": app_key})
	return dict(r.json())['results'][0]['lexicalEntries'][0]['lexicalCategory']['id'] #--> gives type
####
###########

#flask
#bootstrap
#word to vec


#### HAIKU GENERATION MODULE

shakespeare = urlopen('http://composingprograms.com/shakespeare.txt')
wordshake = list(shakespeare.read().decode().split())
words = [word for word in wordshake if word not in delims]
seasonal  = ['horses','Porsche','love','hope','forsooth','melancholy','midsummer','autumn','fall','tree','nature','mercy']
fillers = ['a','the','but','so','and','or','ho']
pronouns = ['thou','thine','you','me','thy','thee']
lyrics = list(open("lyrics.txt").read().split())
#words = list(lyrics)



#### HAIKU GENERATION MODULE

def clean(stringy):
	out = ""
	for i in range(0,len(stringy)):
		if i==0:
			out+=stringy[i].upper()
		elif stringy[i].isupper():
			out+=stringy[i].lower()
		else:
			out+=stringy[i]
	return out


def create_random_haiku():
	'''
	Basic structure of haiku

	17 syllables total
	5 in first
	7 in second
	5 in third

	'''
	'''

	line1 = clean(generate_random_line(4))
	line2 = clean(generate_random_line(6))
	line3 = clean(generate_random_line(4))
	'''

	### Formatting

	return clean(generate_random_line(4))+", " + clean(generate_random_line(6))+", " + clean(generate_random_line(4))
	#return line1+", "+line2+", "+line3+"."


def inf_gen():
	while True:
		yield new_line()+"."

def generate_random_line(num_syll):
	d = make_structure('sentence')
	if num_syllables(d)==(num_syll-1):
		return print_string(d)
	else :
		return generate_random_line(num_syll)

def new_line():
	return clean(print_string(make_structure('sentence')))

### NATURAL LANGUAGE MODULE

vowels = ['a','e','i','o','u']
def count_syllables(stringy):
	num_syl = 0
	for i in range(0,len(stringy)):
		if stringy[i] in vowels:
			num_syl+=1
			if stringy[i-1] in vowels:
				num_syl-=1
			elif stringy[i-1] == 'y':
				num_syl-=1
		elif stringy[i]=='y':
			if stringy[i-1] in vowels: 
				num_syl-=1
	return num_syl


rules = {'sentence':[['nounphrase','verbphrase'],['nounphrase','joinerphrase','verbphrase']],
	'nounphrase':[['noun'],['adjective','noun'],['articlephrase','noun']],
	'verbphrase':[['verb'],['verb','nounphrase'],['adverb','verbphrase']],
	'joinerphrase':[['joiner']],
	'articlephrase':[['possessive'],['article']]
}

word_types = ['noun','verb','adjective','adverb','joiner','article']

dictionary = {
	'noun': ['thou'],#['tree','cow','grass','couch','goose','buffalo'],
	'verb': [],#['eats','attacks','charges','investigates'],
	'adjective': ['green','good'],
	'adverb': ['fiercely','cheerfully'],
	'joiner':['and','for','because','that','so that'],
	'article':['the'],
	'possessive':['thine','thy']
}

#lru cache- to store what's already classified
def my_classify(wordy):
	if len(wordy)<=4:
		return None
	elif 'ing' in wordy[(len(wordy)-4):]:
		return 'verb'
	elif 'ion' in wordy:
		return 'noun'
	elif 'ly' in wordy[(len(wordy)-3):]:
		return 'adverb'
	elif 'ish' in wordy[(len(wordy)-3):]:
		return 'adjective'
	else:
		return None

for wordy in words:
	x = my_classify(wordy)
	if x:
		if wordy not in dictionary[x]:
			dictionary[x].append(wordy)
#######
### Phrase Data Abstraction ###
#######

class Phrase():
	def __init__(self,cat,subphrases=[]):
		assert cat in rules.keys()
		for x in subphrases:
			assert type(x)==Phrase or type(x)==Word
		self.cat = cat
		self.subphrases = subphrases

class Word():
	created_words = []
	def __init__(self,cat,label=""):
		assert type(label)==str
		self.cat=cat
		wordy = dictionary[cat][random.randint(0,len(dictionary[cat])-1)]
		fin = ""
		for a in wordy:
			if a not in delims:
				fin+=a
		self.label=fin
		# same word not twice


def num_words(phrase):
	if type(phrase) == Word:
		return 1
	else:
		return sum([num_words(s) for s in phrase.subphrases])

def num_syllables(phrase):
	if type(phrase) == Word:
		return count_syllables(phrase.label)
	else :
		return sum([num_syllables(s) for s in phrase.subphrases])


def make_structure(cat):
	if cat in dictionary.keys():
		return Word(cat)
	structurey = rules[cat]
	structure = structurey[random.randint(0,(len(structurey)-1))]
	# replace 0 with random integer later
	s = []
	for i in structure:
		s+=[make_structure(i)]
	return Phrase(cat,s)

def print_structure(phrase):
	if type(phrase)==Word:
		return phrase.cat+" "
	else:
		stringy = ""
		for x in phrase.subphrases:
			stringy+=print_structure(x)
		return stringy

def print_string(phrase):
	if type(phrase)==Word:
		return phrase.label+" "
	else:
		stringy = ""
		for x in phrase.subphrases:
			stringy+=print_string(x)
		return stringy




