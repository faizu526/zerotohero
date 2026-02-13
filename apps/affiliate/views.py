from django.shortcuts import render

def pricing(request):
	return render(request, 'affiliate/pricing.html')

def affiliate(request):
	return render(request, 'affiliate/affiliate.html')
