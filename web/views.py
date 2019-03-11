import urllib.request
import json
import html
import datetime
import numpy as np

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

def escape(word):
	return word.replace(' ', '%20')

def get_images(searchword, title=None, date_range=None, location=None, photographer=None):
	root = 'https://images-api.nasa.gov'
	api = root + '/search?'
	if searchword:
		searchword = escape(searchword)
		api += 'q={0}'.format(searchword)
	else:
		api += 'q=NASA'
	if title:
		title = escape(title)
		print(title)
		api += '&title={0}'.format(html.escape(title))
	if date_range[0] != "" and date_range[1] != "": 
		date_range = (escape(date_range[0]), escape(date_range[1]))
		api += '&year_start={0}'.format(html.escape(date_range[0]))
		api += '&year_end={0}'.format(html.escape(date_range[1]))
	if location:
		location = escape(location)
		api += '&location={0}'.format(html.escape(location))
	if photographer:
		photographer = escape(photographer)
		api += '&photographer={0}'.format(html.escape(photographer))
	print(api)
	with urllib.request.urlopen(api) as url:
		data = json.loads(url.read().decode())
	i = 0
	ids = []
	titles = []
	src = []
	tags = []
	date_created = []
	for item in data["collection"]["items"]:
		if "links" not in item:
			continue
		titles.append(item["data"][0]["title"])
		if "keywords" in item["data"][0]:
			keywords = item["data"][0]["keywords"]
			if len(keywords):
				tmp = keywords[:min(3,len(keywords))]
				# tmp = [t[:20] + "..." if len(t) > 20 else t for t in tmp]
				tags.append(tmp)
			else:
				tags.append([])
		else:
			tags.append([])
		if "date_created" in item["data"][0]:
			date_created.append(datetime.datetime.strptime(item["data"][0]["date_created"],
				"%Y-%m-%dT%XZ").strftime("%B %d, %Y"))
		else:
			date_created.append([])
		for link in item["links"]:
			if link["rel"] == "preview":
				src.append(html.escape(link["href"]))
				break
		ids.append(i)
		i += 1
	ids += [-1]*((3 - (len(ids) % 3)) % 3)
	ids = np.array(ids).reshape((3, len(ids)//3)).tolist()
	return ids, titles, tags, src, date_created

def index_view(request):
	data = {}
	return render(request, 'web/index.html', data)

def search_tags_view(request):
	data = {}
	tag = request.GET.get('tag', '')
	data['searchword'] = tag
	data['ids'], data['titles'], data['tags'], data['links'], data['date_created'] = get_images(
		tag, title="", date_range=("",""), location="", photographer=""
	)
	data['num_results'] = len(data['titles'])
	return render(request, 'web/results.html', data)

def fastsearch_view(request):
	data = {}
	searchword = request.POST['searchword']
	title = request.POST['title'].strip()
	location = request.POST['location'].strip()
	photographer = request.POST['location'].strip()
	date = (request.POST['start_date'].strip(), request.POST['end_date'].strip())
	data['searchword'] = searchword
	data['ids'], data['titles'], data['tags'], data['links'], data['date_created'] = get_images(
		searchword, title=title, date_range=date, location=location, photographer=photographer
	)
	data['num_results'] = len(data['titles'])
	return render(request, 'web/results.html', data)

def search_view(request):
	data = {}
	searchword = request.POST['searchword']
	title = request.POST['title'].strip()
	location = request.POST['location'].strip()
	photographer = request.POST['location'].strip()
	date = (request.POST['start_date'].strip(), request.POST['end_date'].strip())
	data['searchword'] = searchword
	data['ids'], data['titles'], data['tags'], data['links'], data['date_created'] = get_images(
		searchword, title=title, date_range=date, location=location, photographer=photographer
	)
	data['num_results'] = len(data['titles'])
	return render(request, 'web/results.html', data)