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

__date__ = "2011 11 20"
__author__ = "diabeteman"

DECRYPTOR_ATTRIBUTES = {
#   ME_mod     CHANCE_mod   PE_mod   RUNS_mod
    +3:        (1.1,        +3,      +0),
    +2:        (1.2,        +5,      +1),
    +1:        (1.0,        +4,      +2),
  None:        (1.0,        +0,      +0),
    -1:        (1.8,        +2,      +4),
    -2:        (0.6,        +1,      +9),
}

DECRYPTOR_INFO = {
#            typeID   CHANCE_mod   ME_mod   PE_mod   RUNS_mod  typeName
# Amarr Interface
    728: (
            (23178,   1.1,         3,       3,       0,        "Formation Layout"),
            (23179,   1.2,         2,       5,       1,        "Classic Doctrine"),
            (23180,   1.0,         1,       4,       2,        "Sacred Manifesto"),
            (23182,   1.8,        -1,       2,       4,        "War Strategon"),
            (23181,   0.6,        -2,       1,       9,        "Circular Logic")
         ),
# Minmatar Interface
    729: (
            (21579,   1.1,         3,       3,       0,        "Calibration Data"),
            (21580,   1.2,         2,       5,       1,        "Advanced Theories"),
            (21581,   1.0,         1,       4,       2,        "Operation Handbook"),
            (21583,   1.8,        -1,       2,       4,        "Assembly Instructions"),
            (21582,   0.6,        -2,       1,       9,        "Circuitry Schematics")
         ),
# Gallente Interface
    730: (
            (23183,   1.1,         3,       3,       0,        "Collision Measurements"),
            (23184,   1.2,         2,       5,       1,        "Test Reports"),
            (23185,   1.0,         1,       4,       2,        "Engagement Plan"),
            (23187,   1.8,        -1,       2,       4,        "Stolen Formulas"),
            (23186,   0.6,        -2,       1,       9,        "Symbiotic Figures")
         ),
# Caldalol Interface
    731: (
            (21573,   1.1,         3,       3,       0,        "Tuning Instructions"),
            (21574,   1.2,         2,       5,       1,        "Prototype Diagram"),
            (21575,   1.0,         1,       4,       2,        "User Manual"),
            (21577,   1.8,        -1,       2,       4,        "Installation Guide"),
            (21576,   0.6,        -2,       1,       9,        "Interface Alignment Chart")
         )
}
DATA_INTERFACES_GROUP_ID = 716

INTERFACES_DECRYPTOR_MAPPING = {
#   typeID   decryptorGroup   interfaceName
# Amarr
    25554:   728,             # Occult Data Interface
    25851:   728,             # Occult Ship Data Interface
    26603:   728,             # Occult Tuner Data Interface
# Minmatar
    25553:   729,             # Cryptic Data Interface
    25857:   729,             # Cryptic Ship Data Interface
    26597:   729,             # Cryptic Tuner Data Interface
# Gallente
    25556:   730,             # Incognito Data Interface
    25855:   730,             # Incognito Ship Data Interface
    26601:   730,             # Incognito Tuner Data Interface
# Caldalol
    25555:   731,             # Esoteric Data Interface
    25853:   731,             # Esoteric Ship Data Interface
    26599:   731,             # Esoteric Tuner Data Interface
}

BASE_MINERALS = [
    34, # Tritanium
    35, # Pyerite
    36, # Mexallon
    37, # Isogen
    38, # Nocxium
    39, # Zydrine
    40, # Megacyte
    11399, # Morphite
]

COMPOSITE_MATERIALS = [
    16670, # Crystalline Carbonide
    16671, # Titanium Carbide
    16672, # Tungsten Carbide
    16673, # Fernite Carbide
    16678, # Sylramic Fibers
    16679, # Fullerides
    16680, # Phenolic Composites
    16681, # Nanotransistors
    16682, # Hypersynaptic Fibers
    16683, # Ferrogel
    17317, # Fermionic Condensates
]

DATACORES = [
    11496, # Datacore - Defensive Subsystems Engineering
    20114, # Datacore - Propulsion Subsystems Engineering
    20115, # Datacore - Engineering Subsystems Engineering
    20116, # Datacore - Electronic Subsystems Engineering
    20171, # Datacore - Hydromagnetic Physics
    20172, # Datacore - Minmatar Starship Engineering
    20410, # Datacore - Gallentean Starship Engineering
    20411, # Datacore - High Energy Physics
    20412, # Datacore - Plasma Physics
    20413, # Datacore - Laser Physics
    20414, # Datacore - Quantum Physics
    20415, # Datacore - Molecular Engineering
    20416, # Datacore - Nanite Engineering
    20417, # Datacore - Electromagnetic Physics
    20418, # Datacore - Electronic Engineering
    20419, # Datacore - Graviton Physics
    20420, # Datacore - Rocket Science
    20421, # Datacore - Amarrian Starship Engineering
    20423, # Datacore - Nuclear Physics
    20424, # Datacore - Mechanical Engineering
    20425, # Datacore - Offensive Subsystems Engineering
    25887, # Datacore - Caldari Starship Engineering
]
DECRYPTORS = [
    21573, # Tuning Instructions
    21574, # Prototype Diagram
    21575, # User Manual
    21576, # Interface Alignment Chart
    21577, # Installation Guide
    21579, # Calibration Data
    21580, # Advanced Theories
    21581, # Operation Handbook
    21582, # Circuitry Schematics
    21583, # Assembly Instructions
    23178, # Formation Layout
    23179, # Classic Doctrine
    23180, # Sacred Manifesto
    23181, # Circular Logic
    23182, # War Strategon
    23183, # Collision Measurements
    23184, # Test Reports
    23185, # Engagement Plan
    23186, # Symbiotic Figures
    23187, # Stolen Formulas
]
SLAVAGE = [
    25588, # Scorched Telemetry Processor
    25589, # Malfunctioning Shield Emitter
    25590, # Contaminated Nanite Compound
    25591, # Contaminated Lorentz Fluid
    25592, # Defective Current Pump
    25593, # Smashed Trigger Unit
    25594, # Tangled Power Conduit
    25595, # Alloyed Tritanium Bar
    25596, # Broken Drone Transceiver
    25597, # Damaged Artificial Neural Network
    25598, # Tripped Power Circuit
    25599, # Charred Micro Circuit
    25600, # Burned Logic Circuit
    25601, # Fried Interface Circuit
    25602, # Thruster Console
    25603, # Melted Capacitor Console
    25604, # Conductive Polymer
    25605, # Armor Plates
    25606, # Ward Console
    25607, # Telemetry Processor
    25608, # Intact Shield Emitter
    25609, # Nanite Compound
    25610, # Lorentz Fluid
    25611, # Current Pump
    25612, # Trigger Unit
    25613, # Power Conduit
    25614, # Single-crystal Superalloy I-beam
    25615, # Drone Transceiver
    25616, # Artificial Neural Network
    25617, # Power Circuit
    25618, # Micro Circuit
    25619, # Logic Circuit
    25620, # Interface Circuit
    25621, # Impetus Console
    25622, # Capacitor Console
    25623, # Conductive Thermoplastic
    25624, # Intact Armor Plates
    25625, # Enhanced Ward Console
]
ICE_PRODUCTS = [
    16272, # Heavy Water
    16273, # Liquid Ozone
    16274, # Helium Isotopes
    16275, # Strontium Clathrates
    17887, # Oxygen Isotopes
    17888, # Nitrogen Isotopes
    17889, # Hydrogen Isotopes
]
PLANETARY_MATERIALS = [
    44, # Enriched Uranium
    2312, # Supertensile Plastics
    2317, # Oxides
    2319, # Test Cultures
    2321, # Polyaramids
    2327, # Microfiber Shielding
    2328, # Water-Cooled CPU
    2329, # Biocells
    2344, # Condensates
    2345, # Camera Drones
    2346, # Synthetic Synapses
    2348, # Gel-Matrix Biopaste
    2349, # Supercomputers
    2351, # Smartfab Units
    2352, # Nuclear Reactors
    2354, # Neocoms
    2358, # Biotech Research Reports
    2360, # Industrial Explosives
    2361, # Hermetic Membranes
    2366, # Hazmat Detection Systems
    2367, # Cryoprotectant Solution
    2389, # Plasmoids
    2390, # Electrolytes
    2392, # Oxidizing Compound
    2393, # Bacteria
    2395, # Proteins
    2396, # Biofuels
    2397, # Industrial Fibers
    2398, # Reactive Metals
    2399, # Precious Metals
    2400, # Toxic Metals
    2401, # Chiral Structures
    2463, # Nanites
    2867, # Broadcast Node
    2868, # Integrity Response Drones
    2869, # Nano-Factory
    2870, # Organic Mortar Applicators
    2871, # Recursive Computing Module
    2872, # Self-Harmonizing Power Core
    2875, # Sterile Conduits
    2876, # Wetware Mainframe
    3689, # Mechanical Parts
    3691, # Synthetic Oil
    3693, # Fertilizer
    3695, # Polytextiles
    3697, # Silicate Glass
    3725, # Livestock
    3775, # Viral Agent
    3779, # Biomass
    3828, # Construction Blocks
    9828, # Silicon
    9830, # Rocket Fuel
    9832, # Coolant
    9834, # Guidance Systems
    9836, # Consumer Electronics
    9838, # Superconductors
    9840, # Transmitter
    9842, # Miniature Electronics
    9846, # Planetary Vehicles
    9848, # Robotics
    12836, # Transcranial Microcontrollers
    15317, # Genetically Enhanced Livestock
    17136, # Ukomi Superconductors
    17392, # Data Chips
    17898, # High-Tech Transmitters
    28974, # Vaccines
]
