from rest_framework import serializers
from . models import Blogpost

class BlogpostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Blogpost
        fields = ['post_id','title','head0','chead0','head1','chead1','head2','chead2','pub_date','thumbnail']
    