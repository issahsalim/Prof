from django.contrib.sitemaps import Sitemap 
from django.urls import reverse 


class StaticViewsSitemap(Sitemap):
    changfreq="dialy"
    priority= 0.8 

    def items(self):
        return ['home']
    
    def location(self, item):
        return reverse(item) 
    
