"""
    Обертка над Pipeline.
    
    template.html:
        {% load pipeline_plus %}
        
        <head>
            ...
            {% include 'pipeline/_loadcss.html' %}
            
            {% block critical_css %}
                {% inline_stylesheet 'critical' %}
            {% endblock critical_css %}
            
            <!-- ОБЯЗАТЕЛЬНО ПОСЛЕ ВСЕХ "stylesheet" -->
            {% include 'pipeline/_preloadcss.html' %}
        </head>
"""

default_app_config = 'libs.pipeline.apps.Config'
