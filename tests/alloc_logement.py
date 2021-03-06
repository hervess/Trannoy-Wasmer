# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# Exemple of a simple simulation


import datetime

from openfisca_core import model
import openfisca_france
openfisca_france.init_country()
from openfisca_core.simulations import ScenarioSimulation


def get_alloc(maxrev = 30000, conj = False, nbenf = 0, zone_apl = 1, loyer_mensuel = 500, nmen = 21):

    # Creating a case_study household with one individual whose taxable income (salaire imposable, sali
    # varies from 0 to maxrev = 100000 in nmen = 3 steps
    simulation = ScenarioSimulation()
    simulation.set_config(year = 2013,
                          nmen = nmen,
                          maxrev = maxrev,
                          x_axis = 'sali')


    scenario = simulation.scenario
    if conj:
    # Adding a husband/wife on the same tax sheet (ie foyer, as conj) and of course same family (as part)
        scenario.addIndiv(1, datetime.date(1975, 1, 1), 'conj', 'part')

    for i in range(nbenf):
    # Adding 3 kids on the same tax sheet and family
        scenario.addIndiv(1 + conj + i, datetime.date(2001, 1, 1), 'pac', 'enf')

    # Add caracteristics of menage
    scenario.menage[0]['loyer'] = loyer_mensuel
    scenario.menage[0]['zone_apl'] = zone_apl

    # Set legislative parameters
    simulation.set_param()

    # Compute the pandas dataframe of the household case_study
    df = simulation.get_results_dataframe()
    df2 = df.transpose()[['Salaires imposables', 'Prestations logement']]
    return df2


def my_example():
    df_single = get_alloc(loyer_mensuel = 500, zone_apl = 1, conj = False)
    df_couple_without = get_alloc(loyer_mensuel = 500, zone_apl = 1, conj = True) 
    df_couple_with = get_alloc(loyer_mensuel = 500, zone_apl = 1, conj = True, nbenf = 1) 
    
    df = df_couple_with - df_couple_without
    print df.to_string()

def test1():
    df = get_alloc(loyer_mensuel = 500, zone_apl = 1, conj = False)
    print df.to_string()
    df2 = get_alloc(loyer_mensuel = 500, zone_apl = 1, conj = True)
    print df2.to_string()

    df3 = df2 - df
    print df3
    
    print df3.to_string()
    
    df4 = get_alloc(loyer_mensuel = 500, zone_apl = 2, conj = False)
    
    df5 = df - df4
    print df5
    
    df5.to_excel("tran.xls")

if __name__ == '__main__':
    
    df_single = get_alloc(loyer_mensuel = 500, zone_apl = 1, conj = False)
    print df_single
    
    df_couple = get_alloc(loyer_mensuel = 500, zone_apl = 1, conj = True)
    
    print df_couple
    
    df_couple_with_child = get_alloc(loyer_mensuel = 500, zone_apl = 1, conj = True, nbenf = 1)
    print df_couple_with_child
    
    df_single.to_excel ("single.xls")
    df_couple.to_excel ("couple.xls")
    df_couple_with_child.to_excel ("withchild.xls")
    

    
    
    
    
    
    
    
    
    
    
    