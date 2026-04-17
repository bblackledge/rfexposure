
from django.shortcuts import render
from django.views import View


class Instructions(View):
    """
    Main Entry Point and Instructions for RF Exposure Application
    re_path('/', Main.as_view(), name="main"),
    State: Unstable
    """

    def __init__(self, **kwargs):
        super(Instructions, self).__init__(**kwargs)
        self.template = 'instructions.html'


    def get(self, request):
        """
        Render Main RF Exposure Instructions
        :param request: Request Object
        :returns: Render Compute Exposure Form
        Status: Stable
        """

        return render(request, self.template)
