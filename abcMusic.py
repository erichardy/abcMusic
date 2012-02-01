#!/Library/Frameworks/Python.framework/Versions/Current/bin/python
# -*- coding: utf-8 -*-
"""
Class abcTune :
	c'est un morceau de musique au format abc qui pourra être
	- chargé à partir d'un fichier
	- défini/contruit dynamiquement
	- joué par une application ou via son API
	- visualisé en PS ou PDF
Une vérification de sa syntaxe devra être opérée avant traitement... ou alors en utilisant
les outils abc déjà développés...
voir le site http://www.abc-notation.com/
abcMIDI
abcm2ps
abctab2ps
tclabc
abcpp : preprocessor

les tags ci-dessous peuvent apparaître aussi bien dans l'entête du morceau que dans
le morceau lui-même
E: K: L: M: P: Q: T: V: W: w: 

pour description complète de la syntaxe,
voir http://www.tradfrance.com/abcf.txt (en français)
et le texte original : http://www.walshaw.plus.com/abc/abc2mtex/abc.txt
"""
import os,sys,re

class abcFormatException(Exception):
    def __init__(self,raison):
	    self.raison = raison
			        
    def __str__(self):
	    return self.raison

class abcTune:
	"""
	une classe de piece de musique au format abc"
	T: il peut y avoir plusieurs titres a un morceau
	"""
	X = ""
	T = []
	Q = ""
	L = ""
	A = B = C = D = E = G = H = I = ""
	# Header est une liste qui contient les lignes jusqu'au premier K: (exclu).
	# C'est l'entête globale
	Header = []
	HeaderComments = []

	def __init__(self):
		self.data = []
		self.dataNoComments = []
		self.A = self.B = self.C = self.D = self.E = ""
		self.F = self.G = self.H = self.I = ""
		self.M = self.N = self.O = self.P = self.Q = ""
		self.R = self.S = self.W = self.X = self.Z = ""
		self.T = []
		self.HeaderComments = []

	def headers(pattern):
		"""
		affecte les variables d'objet liées à l'entête du morceau (self.T, self.X, ...)
		c'est à dire jusqu'au premier K: non inclu qui est
		    une entête de partie (même s'il y a une partie unique)
		Il s'agit des entêtes globales du morceau.
		Les entêtes spécifiques aux parties sont traitées ailleurs.
		"""
		pass

	def abcPrint(self):
		if ((self.X != "") & (self.T != "")):
			print "================================"
			print 'X:' + self.X
			for t in self.T:
				print 'T: ' + t
			for c in self.HeaderComments:
				print c
			if self.A != "":
				print 'A:' + self.A
			if self.B != "":
				print 'B:' + self.B
			if self.C != "":
				print 'C:' + self.C
			if self.D != "":
				print 'D:' + self.D
			if self.E != "":
				print 'E:' + self.E
			if self.F != "":
				print 'F:' + self.F
			if self.G != "":
				print 'G:' + self.G
			if self.I != "":
				print 'I:' + self.I
			if self.L != "":
				print 'L:' + self.L
			if self.M != "":
				print 'M:' + self.M
			if self.N != "":
				print 'N:' + self.N
			if self.O != "":
				print 'O:' + self.O
			if self.P != "":
				print 'P:' + self.P
			if self.Q != "":
				print 'Q:' + self.Q
			if self.R != "":
				print 'R:' + self.R
			if self.S != "":
				print 'S:' + self.S
			if self.W != "":
				print 'W:' + self.W
			if self.Z != "":
				print 'Z:' + self.Z
			if self.G != "":
				print 'G:' + self.G
			if self.parts[2] == 'uniqPart':
				for l in self.parts[3]:
					print self.data[l]
			else:
				# cette partie à revoir quand on aura la possibilité de déterminer le nombre de parties...
				for n in [2,4,6,8,10,12,14,16,18,20]:
					try:
						for l in self.parts[n]:
							print self.data[l]
					except:
						pass

			print "================================"
		else:
			raise abcFormatException('X: or T: field missing')


	def abcPrintSource(self):
		for l in self.data:
			print l

	def analyseOnLoad(self):
		"""
		analyse de la composition d'un morceau qui vient d'être lu dans un fichier
		qui ne contient qu'un seul morceau (typiquement ceux de shabc)
		il s'agit ici seulement de distinguer l'entête et chacune
		des parties d'un morceau
		une liste contruite par :
		- permier élément : le mot 'headers'
		- deuxième élément : les entetes globales, c'est-a-dire celles avant le debut desd parties
		- s'il n'y a pas de champ P:, le troisième élément
		  est 'uniqPart' et l'élément suivant, qui est le dernier
		  est la liste des N° de ligne contenant le morceau
		- s'il y a un champ P:, les champs à partir du troisème
		  vont par paires, les champs d'indice pair sont les noms
		  des parties (P:Z, P:A, P:B,...) et les champs d'indice
		  impair sont les listes des N° de ligne contenant les
		  parties dont le nom est dans le champ d'indice impair
		  immédiatement inférieur
		**** Il reste a verifier que, s'il y a une declaration d'un champ P dans
		     l'entete, il FAUT que les parties declarees dans ce champ soient bien presentes
		     dans les declarations de parties
		"""
		if not re.match("^X:" , self.dataNoComments[0]):
			raise abcFormatException('X: field missing at the first line')
		if not re.match("^T:" , self.dataNoComments[1]):
			raise abcFormatException('T: field missing at the second line')
		self.X = self.dataNoComments[0].split(':')[1].strip()
		self.T.append(self.dataNoComments[1].split(':')[1].strip())
		nLigne = 0
		l = self.data[nLigne]
		self.parts = []
		"""
		Dans la spécification, on sait qu'un champ K: est le dernier avant les premières
		notes (même si il peut y avoir d'autres champs K: en cours de morceau).
		Donc, le parcours des entêtes peut s'arrêter juste après le premier champ K:
		NON NON NON : le parcours des entêtes DOIT s'arrêter AVANT le premier champ K:
		rencontré car celui-ci fait partie de la première partie rencontrée
		"""
		"""
		Mais probleme : si on a un champ K:, on peut aussi avoir un autre champ P: qui indique le debut
		d'une partie et qui se situe AVANT ce champ K: qui DOIT etre le dernier avant le debut des notes
		d'une partie.
		Peut-etre qu'il faudrait faire une premier passage d'analyse du morceau pour determiner combien de parties
		il y a en tout.... et elucider la question des champs P: car un champ P: peut signaler la facon de jouer
		le morceau OU le debut d'une partie !!!!
		Ce qui distingue ces deux types de champs P: c'est si sa valeur contient UN ou deux nom de partie 
		ex : P: ABAB ou P:A
		ECRIRE une methode de 'pre-processing' du morceau qui va determiner le nombre de parties en fonction
		- des champs P:
		- de la valeur de ces champs P: (sachant qu'un champ P: peut avoir une valeur unique pour indiquer que l'on
		ne doit jouer qu'une seule partie une seule fois)
		- il faut donc determiner le NOMBRE de champs P: et leur position
		MAIS la specification n'est pas tres nette sur ce point, et quand, dans un morceau on met un champ P: avant
		un champ K: il y a une erreur de abc2midi : P: field in header should go after K: field
		alors qu'il est bien spécifié que le champ K: DOIT etre le dernier !
		DONC un champ P: peut etre apres un champ K: s'il determine une partie.
		NB: Dans la cas ou on met un champ P: avant un champ K: dans une Nieme partie (par ex P: B) abc2midi accepte
		a la compilation, mais abc2mps met les deux types d'alterations en début de portee.
		C'est donc bien confirme, on a bien l'ordre :
		X:1
		... autres entetes
		P:ABAB
		....autres entetes
		K:G
		P:A
		musique....
		K:D
		P:B
		Si on a un champ P: avant un champ K:, il faut imperatibement avoir au moins un champ P: apres K: car le
		premier declare les parties a jouer qui DOIVENT etre declarees aussi.
		"""
		lignes = []
		while not re.match("^K:" , self.data[nLigne]):
			lignes.append(self.data[nLigne])
			self.Header.append(self.data[nLigne])
			if re.match("^A:" , self.data[nLigne]):
				self.A = self.data[nLigne].split(':')[1].strip()
			if re.match("^B:" , self.data[nLigne]):
				self.B = self.data[nLigne].split(':')[1].strip()
			if re.match("^C:" , self.data[nLigne]):
				self.C = self.data[nLigne].split(':')[1].strip()
			if re.match("^D:" , self.data[nLigne]):
				self.D = self.data[nLigne].split(':')[1].strip()
			if re.match("^E:" , self.data[nLigne]):
				self.E = self.data[nLigne].split(':')[1].strip()
			if re.match("^F:" , self.data[nLigne]):
				self.F = self.data[nLigne].split(':')[1].strip()
			if re.match("^G:" , self.data[nLigne]):
				self.G = self.data[nLigne].split(':')[1].strip()
			if re.match("^H:" , self.data[nLigne]):
				self.H = self.data[nLigne].split(':')[1].strip()
			if re.match("^I:" , self.data[nLigne]):
				self.I = self.data[nLigne].split(':')[1].strip()
			if re.match("^L:" , self.data[nLigne]):
				self.L = self.data[nLigne].split(':')[1].strip()
			if re.match("^M:" , self.data[nLigne]):
				self.M = self.data[nLigne].split(':')[1].strip()
			if re.match("^O:" , self.data[nLigne]):
				self.O = self.data[nLigne].split(':')[1].strip()
			if re.match("^P:" , self.data[nLigne]):
				self.P = self.data[nLigne].split(':')[1].strip()
			if re.match("^Q:" , self.data[nLigne]):
				self.Q = self.data[nLigne].split(':')[1].strip()
			if re.match("^R:" , self.data[nLigne]):
				self.R = self.data[nLigne].split(':')[1].strip()
			if re.match("^S:" , self.data[nLigne]):
				self.S = self.data[nLigne].split(':')[1].strip()
			if re.match("^T:" , self.data[nLigne]):
				xT = self.data[nLigne].split(':')[1].strip()
				if xT != self.T[0]:
					self.T.append(self.data[nLigne].split(':')[1].strip())
			if re.match("^W:" , self.data[nLigne]):
				self.W = self.data[nLigne].split(':')[1].strip()
			if re.match("^Z:" , self.data[nLigne]):
				self.Z = self.data[nLigne].split(':')[1].strip()
			if re.match("^%" , self.data[nLigne]):
				self.HeaderComments.append(self.data[nLigne].strip())
			nLigne += 1
		# lignes.append(nLigne) : pour que le premier champ K: ne fasse pas partie des entêtes globales
		self.parts.append('headers')
		self.parts.append(lignes)
		"""
		ça y est, on a l'entête !
		for n in lignes:
			print str(n) + ':' + self.data[n]
		"""
		# !!!! il faudra ici utiliser les donnes du pre-processing pour determiner s'il y a ou non plusieurs parties. !!!
		# car ici, l'analyse ne PEUT PAS fonctionner car on arrete la précedente dans le cas ou on trouve
		# un K: et la premiere recherche de matching est celle d'un P:
		debut = nLigne
		xdebut = nLigne
		lignes = []
		print self.data[debut]
		print self.data[xdebut]
		"""
		pre-precessing pour savoir combien de parties 
		"""
		nbParts = 0
		for l in self.data[xdebut:]:
			if re.match("^P:" , self.data[xdebut]):
				nbParts += 1
			xdebut += 1
		print 'nbParts : ' + str(nbParts)
		print 'len self.data = ' + str(len(self.data))
		xdebut = debut
		if nbParts > 0:
			xnbParts = 0
			while xnbParts < nbParts:
				lignes = []
				partie = ''
				while re.match("^[A-Z]:|^%" , self.data[xdebut]):
					print 'self.data[xdebut] : ' + self.data[xdebut] + ' / ' + str(xdebut)
					lignes.append(self.data[xdebut])
					if re.match("^P:" , self.data[xdebut]):
						partie = self.data[xdebut].split(':')[1].strip()
					xdebut += 1
				"""
				"""
				print 'avant music : self.data[xdebut] = ' + self.data[xdebut] + ' / ' + str(xdebut)
				# while xdebut < len(self.data) & (not re.match("^[A-Z]:" , self.data[xdebut])):
				# while xdebut < len(self.data):
				while (not re.match("^[A-Z]:" , self.data[xdebut])):
					print 'Music self.data[xdebut] : ' + self.data[xdebut] + ' / ' + str(xdebut)
					lignes.append(self.data[xdebut])
					xdebut += 1
					if xdebut == len(self.data):
						break
				"""
				"""
				self.parts.append(partie)
				self.parts.append(lignes)
				xnbParts += 1
		else:
			lignes = []
			for l in self.data[xdebut:]:
				lignes.append(l)
			self.parts.append('uniqPart')
			self.parts.append(lignes)
			print 'NB PARTS = 0'

		"""
		if not re.match("^K:" , self.data[nLigne]):
			for l in self.data[debut:]:
				lignes.append(nLigne)
				nLigne += 1
			self.parts.append('uniqPart')
			self.parts.append(lignes)
		else:
			nbParties = 0
			nouvellePartie = 0
			for l in self.data[debut:]:
				if re.match("^P:" ,l):
					if nouvellePartie == 1:
						self.parts.append(partie)
						self.parts.append(lignes)
						lignes = []
						nouvellePartie = 0
					nbParties += 1
					partie = l.split(':')[1].strip()
					lignes.append(nLigne)
					nLigne += 1
					nouvellePartie = 1
				else:
					lignes.append(nLigne)
					nLigne += 1
			if nouvellePartie == 1:
				self.parts.append(partie)
				self.parts.append(lignes)
				lignes = []
		# self.Header = self.parts[1]
		"""

				
	def printHeader(self):
		linesHeader = self.parts[1]
		for l in linesHeader:
			print self.data[l]

	def load(self , filename=None):
		"""
		When a abcTune is loaded, datas are put in two lists : data, dataNoComments
		data and dataNoComments are two attributes of the Tune :
		data : all the lines of the tune
		dataNoComments : all the lines except the lines which start with '%'
		"""
		fichier = open(filename)
		self.F = filename
		l = ""
		d = []
		for l in fichier.readlines():
			l = l.strip("\n")
			self.data.append(l)
		for l in self.data:
			if not re.match('^%', l):
				self.dataNoComments.append(l)

	def save(self , filename):
		if ((self.X != "") & (self.T != "")):
			print "On peut faire...."
			# fichier = open(filename , "w")
		else:
			raise abcFormatException('X: or T: field missing')

	def abcPlay(self) :
		pass

	def abcView(self):
		"voir à utiliser abcm2ps plutot que abc2ps"
		pass
	
	def abcChangeTempo(self,tempo = 0):
		"""
		pour modifier le champ Q: global d'un morceau"
		"""
		pass

def main():
	abcFile = sys.argv[1]
	a = abcTune()
	a.load(abcFile)
	# a.load("/Users/hardy/Music/ABC/01-Irlande/Reels/Banshee.abc")
	# a.abcPrintSource()
	a.analyseOnLoad()
	# print "Entetes...."
	# a.printHeader()
	# print "Fin Entetes...."
	# print a.Header
	# print '---'
	print a.parts
	print '---'
	print a.T
	print a.X
	print a.M
	print a.P
	print a.F
	a.Q = '180'
	# a.abcPrint()
	# a.save('azeazeaze')
	sys.exit(0)

if __name__ == '__main__':
	main()

