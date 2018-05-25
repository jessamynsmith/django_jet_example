from django.contrib import admin
from django.utils.safestring import mark_safe

from people import models


class PeopleAdmin(admin.ModelAdmin):
    list_display = ('name', 'button')

    class Media:
        js = ('people/admin.js',
              'https://cdnjs.cloudflare.com/ajax/libs/js-cookie/2.2.0/js.cookie.min.js')

    def button(self, *args, **kwargs):
        html = """
        <input type="button" class="tag_button" value="Add Tag">
        <div class="dialog-form" title="Tag Person">
            <p class="validateTips">All form fields are required.</p>
            <fieldset>
              <label for="tag">Tag</label>
              <input type="text" name="tag" class="text ui-widget-content ui-corner-all">
              
              <!-- Allow form submission with keyboard without duplicating the dialog button -->
              <input type="submit" tabindex="-1" style="position:absolute; top:-1000px">
            </fieldset>
        </div>
        """
        return mark_safe(html)
    button.short_description = 'Click'
    button.allow_tags = True


admin.site.register(models.Person, PeopleAdmin)
