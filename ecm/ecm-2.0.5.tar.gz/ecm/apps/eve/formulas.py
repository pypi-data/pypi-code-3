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

__date__ = '2012 3 10'
__author__ = 'diabeteman'


#------------------------------------------------------------------------------
def apply_material_level(base, me_level, waste_factor, round_result=False):
    """
    Calculate the quantity needed for a material
    considering the waste factor and the material efficiency of the blueprint involved.
    """
    if me_level < 0:
        value = base * (1.0 - ((me_level - 1) * (waste_factor * 0.01)))
    else:
        value = base * (1.0 + ((waste_factor * 0.01) / (1.0 + me_level)))
    if round_result:
        return int(round(value))
    else:
        return value

#------------------------------------------------------------------------------
def apply_production_level(base, pe_level, base_productivity_modifier, round_result=False):
    """
    Calculate the duration (in seconds) needed for the manufacturing of an item
    considering the production efficiency of the item's blueprint.
    """
    base_time = 0.8 * base # we consider the industry skill is at level 5
    productivity_modifier = base_productivity_modifier / float(base)
    if pe_level < 0:
        value = base_time * (1.0 - (productivity_modifier * (pe_level - 1.0)))
    else:
        value = base_time * (1.0 - (productivity_modifier * pe_level / (1.0 + pe_level)))
    if round_result:
        return int(round(value))
    else:
        return value

#------------------------------------------------------------------------------
def calc_invention_chance(base, encryption_skill_lvl=5, science1_skill_lvl=5,
                          science2_skill_lvl=5, decryptor_mod=1, meta_item=0):
    """
    Calculate the chance of successfully inventing a tech2 blueprint.
    """
    encryption = 0.01 * encryption_skill_lvl
    science = 0.1 * (science1_skill_lvl + science2_skill_lvl) / (5 - meta_item)
    return base * (1 + encryption) * (1 + science) * decryptor_mod


#------------------------------------------------------------------------------
def invented_bpc_runs(input_t1_runs, t1_max_runs, t2_max_runs, decryptor_bonus=0):
    """
    Calculate the number of runs in an invented BPC.
    """
    t1_ratio = input_t1_runs / float(t1_max_runs)
    t2_ratio = t2_max_runs / 10.0
    return min(max(1, int( t1_ratio * t2_ratio + decryptor_bonus)), t2_max_runs)




