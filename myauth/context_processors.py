def show_me(request):
    context = {}
    context['company'] = "Stemgon"    
    context['domain'] = "stemgon.co.za"    
    context['tel1'] = "+27 67 735 2242"    
    context['tel2'] = "+27 63 859 9481"    
    return context