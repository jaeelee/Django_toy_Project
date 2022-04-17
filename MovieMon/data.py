import requests, pickle, random, os
from . import settings
import requests, random, os, pickle

# Data Management

def find_file(filename):
	if not os.path.exists('saved_game'):
		return 'FREE'
	files = os.listdir('saved_game')
	for file in files:
		if file.startswith(filename) and file.endswith('.mmg'):
			return file[:-4]
	return 'FREE'

def is_player_out(player):
	if (player[0] >= 0 and player[0] < settings.map_size[0]
	and player[1] >= 0 and player[1] < settings.map_size[1]):
		return False
	else:
		return True

class MoviemonData:

	def __init__(self, filename=''):
		self.player = settings.player
		self.movieball = settings.movieball
		self.moviedex = []
		self.moviemons = []
		if filename == '':
			self.load_default_settings()
		else:
			self.load_file(filename)

	def load(self, game_data):
		loaded = pickle.loads(game_data)
		self.player = loaded.player
		self.movieball = loaded.movieball
		self.moviedex = loaded.moviedex
		self.moviemons = loaded.moviemons
		return (self)

	def dump(self):
		return (pickle.dumps(self))

	def get_random_movie(self):
		if all(i['catch'] for i in self.moviemons):
			return None
		while True:
			rand = self.moviemons[random.randrange(0, len(self.moviemons))]
			if rand not in self.moviedex:
				return (rand)

	def load_default_settings(self):
		session = requests.Session()
		URL = f'http://www.omdbapi.com/?apikey={settings.apikey}'
		for i in settings.movies:
			r = session.get(url=URL, params={'i':i})
			data = r.json()
			data.update(catch=False)
			self.moviemons.append(data)
		r.raise_for_status()
		return (self)

	def get_strength(self):
		return len(self.moviedex)

	def get_movie(self, moviemon_id):
		for i in self.moviemons:
			if i['imdbID'] == moviemon_id:
				return i
		return None

	def save_file(self, filename):
		try:
			if not os.path.exists('saved_game'):
				os.makedirs('saved_game')
			for i in [0, 1, 2]:
				if filename.startswith(f'slot{chr(ord("A")+i)}'):
					remove = find_file(f'slot{chr(ord("A")+i)}')
					os.remove(f'saved_game/{remove}')
		except OSError:
			print ('ERROR: Failed to save file')
		with open(f'saved_game/{filename}.mmg', 'wb') as f:
			f.write(self.dump())

	def load_file(self, filename):
		filename = find_file(filename)
		if filename == 'FREE':
			return None
		try:
			with open(f'saved_game/{filename}.mmg', 'rb') as f:
				self.load(f.read())
		except Exception as e:
			print(f'ERROR: {e}')

## moviemons Key ##
# Title : 영화 제목
# imdbID : 영화 ID
# Director : 감독
# Poster : 포스터 URL
# Year : 개봉 연도
# imdbRating : 평점
# Plot : 시놉시스
# Actors : 배우
