from datetime import datetime
from django.conf import settings
from django.core.cache import cache
import twitter
from django.db.models import Count

def latest_tweet(request):
	tweets = cache.get('tweets')
	if tweets:
		return {"tweets":tweets}

	tweets = twitter.Api().GetUserTimeline(settings.TWITTER_USER)
	for tweet in tweets:
		tweet.date = datetime.strptime( tweet.created_at, "%a %b %d %H:%M:%S +0000 %Y" )
	cache.set( 'tweets', tweets, settings.TWITTER_TIMEOUT )
	return {"tweets": tweets}


def top_rated_items(request):
	# Models
	from vivilox.apps.store.models import item , purchases

	_top_rated_items = cache.get('ctxpro_top_rated_items')
	if _top_rated_items:
		return {'ctxpro_top_rated_items':_top_rated_items}
	
	_top_rated_items = item.objects.annotate(item_sold = Count('purchases')).filter(item_sold__exact=0,top_rated=True).order_by('-id')[:10]
	cache.set('ctxpro_top_rated_items',_top_rated_items,360)
	return {'ctxpro_top_rated_items':_top_rated_items}

def categories(request):
	from vivilox.apps.contests.models import category

	_categories = cache.get('ctxpro_contests_categories')

	if _categories:
		return {'ctxpro_contests_categories':_categories}
	_categories = category.objects.filter(status=True).order_by('id')
 	cache.set('ctxpro_contests_categories',_categories,360)
 	return {'ctxpro_contests_categories':_categories}


def top_rated_contest(request):
	from vivilox.apps.contests.models import contest

	_contest = cache.get('ctxpro_top_rated_contest')
	if _contest:
		return {'ctxpro_top_rated_contest':_contest}
	_contest = contest.objects.filter(active=True,finished=False,toprate=True).order_by('-id')[:10]
	cache.set('ctxpro_top_rated_contest',_contest,360)
	return {'ctxpro_top_rated_contest':_contest}