# Copyright (c) 2010-2012 Robin Jarry
#
# This file is part of EVE Corporation Management.
#
# EVE Corporation Management is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# EVE Corporation Management is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# EVE Corporation Management. If not, see <http://www.gnu.org/licenses/>.

__date__ = "2011-03-13"
__author__ = "diabeteman"


from django.views.decorators.cache import cache_page
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseNotFound, HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist
from django.template.context import RequestContext as Ctx

from ecm.views.decorators import check_user_access
from ecm.views import extract_datatable_params, datatable_ajax_data
from ecm.apps.common.models import ColorThreshold
from ecm.apps.hr.models import Title, Member
from ecm.apps.hr.views import get_members

#------------------------------------------------------------------------------
@check_user_access()
def members(request, titleID):
    data = {
        'title' : get_object_or_404(Title, titleID=int(titleID)),
        'colorThresholds' : ColorThreshold.as_json(),
        'directorAccessLvl' : Member.DIRECTOR_ACCESS_LVL
    }
    return render_to_response("titles/title_members.html", data, Ctx(request))


#------------------------------------------------------------------------------
@check_user_access()
@cache_page(60 * 60) # 1 hour cache
def members_data(request, titleID):
    try:
        params = extract_datatable_params(request)
        title = Title.objects.get(titleID=int(titleID))
    except KeyError:
        return HttpResponseBadRequest()
    except ObjectDoesNotExist:
        return HttpResponseNotFound()

    total_members,\
    filtered_members,\
    members = get_members(query=title.members.filter(corped=True),
                          first_id=params.first_id,
                          last_id=params.last_id,
                          search_str=params.search,
                          sort_by=params.column,
                          asc=params.asc)
    
    return datatable_ajax_data(members, params.sEcho, total_members, filtered_members)

