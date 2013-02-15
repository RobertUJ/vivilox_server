from django.conf.urls.defaults import patterns,url

urlpatterns = patterns('vivilox.apps.contests.views',
	url(r'^contest/new/$','new_contest',name='new_contest_view'),
	url(r'^contest.all/$','view_all_contest',name='all_contest_view'),
	url(r'^contest.top/$','view_top_contest',name='top_contest_view'),
	url(r'^contest.detail/(\d{1,6})/$','contest_details',name='contest_details_view'),
	

	url(r'^contest.new/$','get_categories',name='new_add_contest_view'),
	url(r'^contest.cat/$','define_category',name='set_category_contest_view'),
	url(r'^contest.build/$','buid_contest',name='build_contest_new_view'),
	url(r'^contest.edit/(\d{1,6})/$','edit_contest',name='edit_contest_new_view'),
	url(r'^contest.new/resume/$','resume_contest',name='resume_contest_new_view'),
	

	url(r'^contest.all/buyer/(\d{1,6})/$','contest_buyer',name='all_contest_buyer_view'),
	
	url(r'^proposal.new/(\d{1,6})/$','add_proposal',name='add_new_proposal_form'),
	url(r'^proposal.winner/(\d{1,6})/(\d{1,6})/(\d{1,6})/(\d{1,6})/$','flagWinner',name='winner_view'),
	url(r'^proposal.details/(\d{1,6})/$','proposal_details',name='proposal_details_view'),
	url(r'^proposal.discard/(\d{1,6})/$','proposal_discard',name='proposal_discard_view'),

)
