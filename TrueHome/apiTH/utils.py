class EnablePartianUpdateMixin():
    """Enable partial updates

    Override partial kwargs in UpdateModelMixin class
    """
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
    
    
    
    
