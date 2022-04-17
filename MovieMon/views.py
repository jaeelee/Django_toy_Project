from django.shortcuts import render
from django.shortcuts import redirect
from . import data, settings
import random

message = 'title'
slot_selected = 0
moviedex_selected = 0

def TitleScreen(request):
	global slot_selected
	if request.method == 'POST':
		mdata = data.MoviemonData('')
		mdata.save_file('current')
		if 'button_a' in request.POST:
			return redirect('/worldmap/')
		elif 'button_b' in request.POST:
			slot_selected = 0
			return redirect('/options/load_game/')
	return render(request, 'MovieMon/TitleScreen.html')

def Worldmap(request):
	global message
	global moviedex_selected
	mdata = data.MoviemonData('current')
	tmp_player = [0, 0]
	tmp_player[0], tmp_player[1] = mdata.player[0], mdata.player[1]
	movement = False
	if request.method == 'POST':
		if 'button_start' in request.POST:
			return redirect ('/options/')
		elif 'button_select' in request.POST:
			moviedex_selected = 0
			return redirect ('/moviedex/')
		elif 'button_a' in request.POST:
			if message == 'moviemon':
				message = 'world'
				id = mdata.get_random_movie()['imdbID']
				return redirect(f'/battle/{id}/')
		elif 'button_top' in request.POST:
			tmp_player[0] -= 1
		elif 'button_bottom' in request.POST:
			tmp_player[0] += 1
		elif 'button_left' in request.POST:
			tmp_player[1] -= 1
		elif 'button_right' in request.POST:
			tmp_player[1] += 1
		if not data.is_player_out(tmp_player):
			mdata.player[0], mdata.player[1] = tmp_player[0], tmp_player[1]
			movement = True

	rand = 0
	message = 'world'
	if movement:
		rand = random.randint(0, 100)
		if rand < 10:
			mdata.movieball += 1
			message = "movieball"
		elif rand > 90 and mdata.get_random_movie() != None:
			message = 'moviemon'

	mdata.save_file('current')
	context = {
		'message': message,
		'movieball': mdata.movieball,
		'map_col': range(settings.map_size[0]),
		'map_row': range(settings.map_size[1]),
		'player_col': mdata.player[0],
		'player_row': mdata.player[1],
		'rand': rand,
	}
	return render(request, 'MovieMon/Worldmap.html', context)

def Battle(request, moviemon_id):
	mdata = data.MoviemonData('current')
	moviemon = mdata.get_movie(moviemon_id)
	global message
	win_rate = 50 - (float(moviemon['imdbRating']) * 10) + (mdata.get_strength() * 5)
	if win_rate < 1:
		win_rate = 1.0
	elif win_rate > 90:
		win_rate = 90.0
	if request.method == 'POST':
		if 'button_a' in request.POST:
			if mdata.movieball == 0 and moviemon['catch'] == False:
				message = 'out'
			elif mdata.movieball > 0 and moviemon['catch'] == False:
				mdata.movieball -= 1
				rand = random.randint(1, 100)
				if rand <= win_rate:
					moviemon['catch'] = True
					mdata.moviedex.append(moviemon)
					message = 'success_catch'
				else:
					message = 'fail_catch'
			else:
				message = 'none'
		if 'button_b' in request.POST:
			return redirect('/worldmap/')
	mdata.save_file('current')
	return render(request, 'MovieMon/Battle.html', {
		'm_poster' : moviemon['Poster'],
		'movieball' :mdata.movieball,
		'player_strength' : mdata.get_strength(),
		'winning_rate' : win_rate,
		'message':message
	})

def Moviedex(request):
	mdata = data.MoviemonData('current')
	global moviedex_selected
	if request.method == 'POST':
		if (('button_top' in request.POST)
			or ('button_left' in request.POST)) and moviedex_selected > 0:
				moviedex_selected -= 1
		if (('button_bottom' in request.POST)
			or ('button_right' in request.POST)) and moviedex_selected < len(mdata.moviedex) - 1:
				moviedex_selected += 1
		if 'button_select' in request.POST:
			return redirect('/worldmap/')
		if 'button_a' in request.POST:
			moviedex_selected_moviemon = mdata.moviedex[moviedex_selected]['imdbID']
			return redirect(f'/moviedex/{moviedex_selected_moviemon}/')

	return render(request, 'MovieMon/Moviedex.html', {
		'm_poster': [ m['Poster'] for m in mdata.moviedex],
		'selected': mdata.moviedex[moviedex_selected]['Poster'] if len(mdata.moviedex) != 0 else None
		})

def detail(request, moviemon):
	mdata = data.MoviemonData('current')
	movie = mdata.get_movie(moviemon)
	global moviedex_selected
	if request.method =='POST':
		if 'button_b' in request.POST:
			moviedex_selected = 0
			return redirect('/moviedex/')
	return render(request, 'MovieMon/detail.html', {
		'title':movie['Title'],
		'director':movie['Director'],
		'year':movie['Year'],
		'imdbRating':movie['imdbRating'],
		'actors':movie['Actors'],
		'plot':movie['Plot'],
		'poster':movie['Poster'],
	})

def Option(request):
	mdata = data.MoviemonData('current')
	global slot_selected
	global message
	mdata.save_file('current')
	if request.method =='POST':
		if 'button_start' in request.POST:
			return redirect('/worldmap/')
		elif 'button_a' in request.POST:
			slot_selected = 0
			message = 'option'
			return redirect('/options/save_game/')
		elif 'button_b' in request.POST:
			return redirect('/')
	return render(request, 'MovieMon/Option.html')

def Save(request):
	mdata = data.MoviemonData('current')
	global slot_selected
	global message
	if request.method =='POST':
		if 'button_top' in request.POST and slot_selected > 0:
			slot_selected -= 1
		elif 'button_bottom' in request.POST and slot_selected < 2:
			slot_selected += 1
		elif 'button_a' in request.POST:
			if message == 'save':
				filename = f'slot{chr(ord("A")+slot_selected)}_{len(mdata.moviedex)}_{len(mdata.moviemons)}'
				mdata.save_file(filename)
				message = 'game_is_saved'
		elif 'button_b' in request.POST:
			return redirect('/options/')
	pass_message = message
	message = 'save'
	return render(request, 'MovieMon/Save.html', {
		'slotA': data.find_file('slotA'),
		'slotB': data.find_file('slotB'),
		'slotC': data.find_file('slotC'),
		'selected': slot_selected,
		'message':pass_message,
	})

def Load(request):
	mdata = data.MoviemonData('current')
	global slot_selected
	global message
	if request.method =='POST':
		if 'button_top' in request.POST and slot_selected > 0:
			slot_selected -= 1
		elif 'button_bottom' in request.POST and slot_selected < 2:
			slot_selected += 1
		elif  'button_a' in request.POST:
			if message == 'game_is_loaded':
				return redirect('/worldmap/')
			else:
				message = 'game_is_loaded'
				mdata.load_file(f'slot{chr(ord("A")+slot_selected)}')
				mdata.save_file('current')
		elif 'button_b' in request.POST:
			return redirect('/')
	return render(request, 'MovieMon/Load.html', {
		'slotA':data.find_file('slotA'),
		'slotB':data.find_file('slotB'),
		'slotC':data.find_file('slotC'),
		'selected': slot_selected,
		'message':message,
	})
