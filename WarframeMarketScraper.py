# This script scrapes the most recent 90-day-median prices for a list of items from https://warframe.market using the warframe.market API.
# The script was created by 1Xanaton4You on 28.09.2024
# This is an open source script under GNU GENERAL PUBLIC LICENSE Version 3.
#
# I wrote this scrip to get a easier overview over the current prices on the warframe.market.
#
# How to use this script on first use:
# 1. On windows open a command prompt by typing cmd into the windows seach field.
# 2. Type in phyton and press enter to check if you have phyton installed on your system.
#    2a. If you do not get something like this {Python 3.12.6 (tags/v3.12.6:a4a2d2b, Sep  6 2024, 20:11:23) [MSC v.1940 64 bit (AMD64)] on win32
#                                               Type "help", "copyright", "credits" or "license" for more information.}
#        you first have to install Phyton on your system (https://www.python.org/downloads/).
#    2b. If you have a Phyton version installed type exit() and press enter to leave the phyton prompt.
# 3. Alter the [Set this according to your needs] part of the sript according to your needs, or use the predefined lists.
# 4. Start the script by double klicking the WarframeMarketScraper.py 
# 5. Select if you want to scrape all defined item lists or select a specific list. Choose the list number, if you want to scrape a single list.
# 6. Wait for the results. You can save the scraped results in a CSV-file when the scraping is done, if you choose to do so.
#    The file will be created in the folder this script runs from.
import urllib.parse as parse
import urllib.request
from urllib.request import urlopen as req_url
import json
import string
#import webbrowser
import csv
import sys
from pathlib import Path
from datetime import datetime
import tracemalloc
from time import sleep

def warframeMarketScraper(mode):
	# --------------------------------------- [START: Set this according to your needs] ---------------------------------------------
	# Switches for debugging (only for debug)
	enableDebugDump = 0 # Set this 1, if you want to dump all the received data or 2 if you only want the final find data into a txt-file.
	enableDebugTestList = 0 # Set this 1, if you want to use a test list for debugging at selection 9.
	if mode == "manually":
		if enableDebugDump > 0:
			print("enableDebugDump=" + str(enableDebugDump))
		if enableDebugTestList == 1:
			print("Waht are you interested in [1-WarframeSets, 2-WeaponSets, 3-SentinelAndAwSets, 4-NonPrimeWeapons, 5-Arcane, 6-Mods, 9-TestList(DEBUG)]?")
		else:
			print("Waht are you interested in [1-WarframeSets, 2-WeaponSets, 3-SentinelAndAwSets, 4-NonPrimeWeapons, 5-Arcane, 6-Mods]?")
		answer = input()
	else:
		answer = mode
	#breakpoint()
	# Define the name of the itemList
	# Define a list of items you want to scape from warfram.market.
	# Just search for a item on the website and check how the items is named in the url and fill in the name 
	# of the item. For example if you search for "Glaive Prime Set" the warfram.market url
	# would be https://warframe.market/items/glaive_prime_set and you would add 'glaive_prime_set' to the my_itemList.
	if answer == "1":
		# This is a list of all currently available probe warframe sets
		listName = "WarframeSets"
		# List from https://warframe.fandom.com/wiki/Warframes
		my_itemList = ['ash_prime_set', 'atlas_prime_set', 'banshee_prime_set', 'baruuk_prime_set', 'chroma_prime_set', 
		'ember_prime_set', 'equinox_prime_set', 'frost_prime_set', 'gara_prime_set', 'garuda_prime_set', 
		'gauss_prime_set', 'grendel_prime_set', 'harrow_prime_set', 'hildryn_prime_set', 'hydroid_prime_set', 
		'inaros_prime_set', 'ivara_prime_set', 'khora_prime_set', 'limbo_prime_set', 'loki_prime_set', 
		'mag_prime_set', 'mesa_prime_set', 'mirage_prime_set', 'nekros_prime_set', 'nezha_prime_set', 
		'nidus_prime_set', 'nova_prime_set', 'nyx_prime_set', 'oberon_prime_set', 'octavia_prime_set', 
		'protea_prime_set', 'revenant_prime_set', 'rhino_prime_set', 'saryn_prime_set', 'sevagoth_prime', 
		'titania_prime_set', 'trinity_prime_set', 'valkyr_prime_set', 'vauban_prime_set', 'volt_prime_set', 
		'wisp_prime_set', 'wukong_prime_set', 'zephyr_prime_set']
	elif answer == "2":
		listName = "WeaponSets"
		# List from https://warframe.fandom.com/wiki/Category:Primary_Weapons 
		#, https://warframe.fandom.com/wiki/Category:Secondary_Weapons
		#, https://warframe.fandom.com/wiki/Category:Melee_Weapons
		#, https://warframe.fandom.com/wiki/Category:Archwing_Weapons
		my_itemList = ['acceltra_prime_set', 'astilla_prime_set', 'baza_prime_set', 'boar_prime_set', 'boltor_prime_set', 
		'braton_prime_set', 'burston_prime_set', 'cernos_prime_set', 'corinth_prime_set', 'fulmin_prime_set', 
		'gotva_prime', 'latron_prime_set', 'panthera_prime_set', 'paris_prime_set', 'phantasma_prime_set', 
		'scourge_prime_set', 'soma_prime_set', 'stradavar_prime_set', 'strun_prime_set', 'sybaris_prime_set', 
		'tenora_prime_set', 'tiberon_prime_set', 'tigris_prime_set', 'vectis_prime_set', 'zhuge_prime_set', 
		'afuris_prime_set', 'akarius_prime_set', 'akbolto_prime_set', 'akbronco_prime_set', 'akjagara_prime_set', 
		'aklex_prime_set', 'akmagnus_prime', 'akstiletto_prime_set', 'akvasto_prime_set', 'ballistica_prime_set', 
		'bronco_prime_set', 'epitaph_prime', 'euphona_prime_set', 'hikou_prime_set', 'hystrix_prime_set', 
		'knell_prime_set', 'lex_prime_set', 'magnus_prime_set', 'pandero_prime_set', 'pyrana_prime_set', 
		'sicarus_prime_set', 'spira_prime_set', 'vasto_prime_set', 'zakti_prime_set', 'zylok_prime_set', 
		'ankyros_prime_set', 'bo_prime_set', 'cobra_and_crane_prime_set', 'dakra_prime_set', 'destreza_prime_set', 
		'dual_kamas_prime_set', 'dual_keres_prime_set', 'fang_prime_set', 'fragor_prime_set', 'galatine_prime_set', 
		'glaive_prime_set', 'gram_prime_set', 'guandao_prime_set', 'gunsen_prime_set', 'karyst_prime_set', 
		'kogake_prime_set', 'kronen_prime_set', 'masseter_prime_set', 'nami_skyla_prime_set', 'nikana_prime_set', 
		'ninkondi_prime_set', 'okina_prime_set', 'orthos_prime_set', 'pangolin_prime_set', 'reaper_prime_set', 
		'redeemer_prime_set', 'scindo_prime_set', 'silva_and_aegis_prime_set', 'tatsu_prime_set', 'tekko_prime_set', 
		'tipedo_prime_set', 'venka_prime_set', 'volnus_prime_set']
	elif answer == "3":
		listName = "SentinelAndAW"
		my_itemList = ['carrier_prime_set', 'dethcube_prime_set', 'helios_prime_set', 'nautilus_prime', 'shade_prime_set', 
		'wyrm_prime_set', 
		'odonata_prime_set', 'corvas_prime_set', 'larkspur_prime_set']
	elif answer == "4":
		listName = "NonPrimeWeapons"
		my_itemList = ['strun_wraith_set', 'machete_wraith', 'twin_vipers_wraith_set', 'gorgon_wraith_set', 'latron_wraith_set', 
		'karak_wraith_set', 'vulkar_wraith', 'furax_wraith_set', 'viper_wraith', 'halikar_wraith', 
		'prisma_angstrum', 'prisma_dual_cleavers', 'prisma_gorgon' , 'prisma_grakata', 
		'prisma_grinlok', 'prisma_lenz', 'prisma_machete', 'prisma_obex', 'prisma_ohma', 
		'prisma_skana', 'prisma_tetra', 'prisma_twin_gremlins', 
		'rakta_ballistica', 'rakta_cernos', 'rakta_dark_dagger', 
		'sancti_castanas', 'sancti_magistar', 'sancti_tigris', 
		'telos_akbolto', 'telos_boltace', 'telos_boltor', 
		'synoid_gammacor', 'synoid_heliocor', 'synoid_simulor', 
		'secura_dual_cestra', 'secura_lecta', 'secura_penta', 
		'braton_vandal_set', 'dera_vandal_set', 'lato_vandal_set', 'spectra_vandal_set', 
		'opticor_vandal', 'quanta_vandal', 'supra_vandal', 'glaxion_vandal', 
		'gotva_prime', 'mara_detron', 'carmine_penta_set', 'vastilok', 'vericres', 
		'sporothrix_set', 'pathocyst_set', 'stahlta_set', 'stropha_set', 'broken_war_set', 
		'sarofang_set', 'shedu_set', 'aeolak_set', 'perigale_set', 'steflos_set', 
		'corufell_set', 'wolf_sledge_set', 
		'basmu_blueprint', 'quellor_blueprint', 'pennant_blueprint', 
		'imperator_vandal_set', 'prisma_dual_decurions', 'prisma_veritux', 
		'corvas_set', 'cyngas_set', 'dual_decurion_set', 'fluctus_set', 'mandonel_set', 
		'morgha_set', 'phaedra_set', 'velocitus_set', 'agkuza_set', 
		'centaur_set', 'kaszas_set', 'onorix_set', 'rathbone_set']
	elif answer == "5":
		listName = "Arcane"
		# List from https://warframe.fandom.com/wiki/Arcane_Enhancement
		my_itemList = ['arcane_acceleration', 'arcane_aegis', 'arcane_agility', 'arcane_arachne', 'arcane_avenger', 
		'arcane_awakening', 'arcane_barrier','arcane_battery','arcane_blade_charger','arcane_blessing', 
		'arcane_bodyguard','arcane_consequence','arcane_deflection','arcane_double_back','arcane_energize', 
		'arcane_eruption','arcane_fury','arcane_grace','arcane_guardian','arcane_healing', 
		'arcane_ice','arcane_ice_storm','arcane_intention','arcane_momentum','arcane_nullifier', 
		'arcane_phantasm','arcane_pistoleer','arcane_power_ramp','arcane_precision','arcane_primary_charger', 
		'arcane_pulse','arcane_rage','arcane_reaper','arcane_resistance','arcane_rise',
		'arcane_steadfast','arcane_strike','arcane_tanker','arcane_tempo','arcane_trickery',
		'arcane_ultimatum','arcane_velocity','arcane_victory','arcane_warmth', 
		'theorem_contagion','theorem_demulcent','theorem_infection', 
		'molt_augmented','molt_efficiency','molt_reconstruct','molt_vigor', 
		'magus_vigor','magus_husk','magus_cadence','magus_cloud','magus_replenish', 
		'magus_elevate','magus_nourish','magus_overload','magus_glitch','magus_revert', 
		'magus_firewall','magus_drive','magus_lockdown','magus_destruct','magus_anomaly', 
		'magus_melt','magus_accelerant','magus_repair','magus_aggress', 
		'emergence_dissipate','emergence_renewed','emergence_renewed','emergence_savior', 
		'exodia_brave','exodia_force','exodia_hunt','exodia_might','exodia_triumph',
		'exodia_valor','exodia_contagion','exodia_epidemic', 
		'pax_bolt','pax_charge','pax_seeker','pax_soar', 
		'residual_boils','residual_malodor','residual_shock','residual_viremia', 
		'virtuos_null','virtuos_tempo','virtuos_fury','virtuos_strike','virtuos_shadow',
		'virtuos_ghost','virtuos_trojan','virtuos_surge','virtuos_spike','virtuos_forge',
		'eternal_eradicate','eternal_logistics','eternal_onslaught', 
		'primary_blight','primary_deadhead','primary_dexterity','primary_exhilarate','primary_merciless',
		'primary_frostbite','primary_obstruct','primary_plated_round', 
		'fractalized_reset','longbow_sharpshot','shotgun_vendetta', 
		'secondary_deadhead','secondary_dexterity','secondary_fortifier','secondary_merciless','secondary_encumber',
		'secondary_kinship','secondary_outburst','secondary_shiver','secondary_surge', 
		'cascadia_accuracy','cascadia_empowered','cascadia_flare','cascadia_overcharge', 
		'conjunction_voltage','akimbo_slip_shot', 
		'melee_afflictions','melee_animosity','melee_crescendo','melee_duplicate','melee_exposure',
		'melee_fortification','melee_influence','melee_retaliation','melee_vortex']
	elif answer == "6":
		listName = "Mods"
		# List from https://warframe.fandom.com/wiki/Mod/List_of_Mods#All_Mod_Variants_and_Classes
		# Used WarframeWikiScraper.py to generate the list.
		my_itemList = ['adaptation', 'adept_surge', 'adrenaline_boost', 'aero_vantage', 'agility_drift', 
		'air_thrusters', 'anti_flak_plating', 'anticipation', 'antitoxin', 'armored_acrobatics', 
		'armored_agility', 'armored_evade', 'armored_recovery', 'augur_accord', 'augur_message', 
		'augur_reach', 'augur_secrets', 'aviator', 'battering_maneuver', 'blind_rage', 
		'calculated_spring', 'carnis_carapace', 'coaction_drift', 'constitution', 'continuity',
		'cunning_drift', 'diamond_skin', 'endurance_drift', 'enemy_sense',
		'energy_conversion', 'energy_nexus', 'equilibrium', 'fast_deflection', 'final_act', 
		'firewalker', 'flame_repellent', 'fleeting_expertise', 'flow', 'follow_through', 
		'fortitude', 'gladiator_aegis', 'gladiator_finesse', 'gladiator_resolve', 'handspring', 
		'hastened_steps', 'health_conversion', 'heavy_impact', 'heightened_reflexes', 'hunter_adrenaline', 
		'ice_spring', 'insulation', 'intensify', 'lightning_dash', 
		'lightning_rod', 'maglev', 'master_thief', 'mecha_pulse', 'mobilize', 
		'motus_signal', 'narrow_minded', 'natural_talent', 'no_current_leap', 'overcharge_detectors', 
		'overcharged', 'overextended', 'pain_threshold', 'patagium', 'peculiar_bloom', 
		'peculiar_growth', 'piercing_step', 'power_drift', 'preparation', 'primed_continuity', 
		'primed_flow', 'primed_sure_footed', 'proton_pulse', 'provoked', 
		'quick_charge', 'quick_thinking', 'rage', 'rapid_resilience', 'redirection', 
		'reflection', 'reflex_guard', 'rending_turn', 'retribution', 'rime_vault', 
		'rising_skill', 'rolling_guard', 'rush', 'searing_leap', 'shock_absorbers', 
		'speed_drift', 'stealth_drift', 'steel_fiber', 'strain_consume', 'streamline', 
		'streamlined_form', 'stretch', 'sure_footed', 'surplus_diverters', 'synth_reflex', 
		'tactical_retreat', 'tek_collateral', 'tempered_bound', 'thiefs_wit', 
		'toxic_flight', 'transient_fortitude', 'undying_will', 'venomous_rise', 'vigilante_pursuit', 
		'vigilante_vigor', 'vigor', 'vigorous_swap', 'vital_systems_bypass', 'vitality', 'voltaic_lance', 
		'warm_coat', 'aerodynamic', 'brief_respite', 'combat_discipline', 'corrosive_projection', 
		'dead_eye', 'dreamers_bond', 'emp_aura', 'empowered_blades', 
		'enemy_radar', 'energy_siphon', 'growing_power', 'holster_amp', 'infested_impedance', 
		'loot_detector', 'mecha_empowered', 'melee_guidance', 'physique', 
		'pistol_amp', 'pistol_scavenger', 'power_donation', 'ready_steel', 'rejuvenation', 
		'rifle_amp', 'rifle_scavenger', 'shepherd', 'shield_disruption', 'shotgun_amp', 
		'shotgun_scavenger', 'sniper_scavenger', 'sprint_boost', 'stand_united', 'steel_charge', 
		'swift_momentum', 'toxin_resistance', 'aero_periphery', 'hunter_munitions', 'hunter_track', 
		'shivering_contagion', 'vigilante_armaments', 'vigilante_fervor', 'vigilante_offense', 
		'vigilante_supplies', 'adhesive_blast', 'agile_aim', 'ammo_drum', 
		'apex_predator', 'argon_scope', 'bane_of_corpus', 'bane_of_corrupted', 'bane_of_grineer', 
		'bane_of_infested', 'bladed_rounds', 'catalyzer_link', 'cautious_shot', 'combustion_beam', 
		'comet_rounds', 'continuous_misery', 'crash_course', 'critical_delay', 'cryo_rounds', 'eagle_eye', 
		'fanged_fusillade', 'fast_hands', 'firestorm', 'hammer_shot', 'heavy_caliber', 
		'hellfire', 'high_voltage', 'hush', 'infected_clip', 'lucky_shot', 
		'magazine_warp', 'malignant_force', 'metal_auger', 'piercing_caliber', 'piercing_hit', 
		'point_strike', 'primed_bane_of_corpus', 'primed_bane_of_corrupted', 'primed_bane_of_grineer', 'primed_bane_of_infested', 
		'primed_cryo_rounds', 'primed_fast_hands', 'primed_firestorm', 'primed_magazine_warp', 
		'proton_jet', 'recover', 'rifle_aptitude', 'rime_rounds', 'ripper_rounds', 
		'rupture', 'sawtooth_clip', 'serrated_rounds', 'serration', 'shred', 
		'sinister_reach', 'speed_trigger', 'split_chamber', 'stabilizer', 'stormbringer', 
		'terminal_velocity', 'thermite_rounds', 'twitch', 'vanquished_prey', 'vile_acceleration', 
		'vile_precision', 'vital_sense', 'wildfire', 'deft_tempo', 'guided_ordnance', 
		'gun_glide', 'hydraulic_gauge', 'loose_hatch', 'maximum_capacity', 'overview', 
		'rifle_ammo_mutation', 'primed_rifle_ammo_mutation', 'spring_loaded_chamber', 'tactical_reload', 'tainted_mag', 
		'accelerated_blast', 'ammo_stock', 'blaze', 'blunderbuss', 
		'bounty_hunter', 'breach_loader', 'broad_eye', 'burdened_magazine', 'charged_shell', 
		'chilling_grasp', 'chilling_reload', 'cleanse_corpus', 'cleanse_corrupted', 'cleanse_grineer', 
		'cleanse_infested', 'contagious_spread', 'crash_shot', 'critical_deceleration', 'disruptor', 
		'double_barrel_drift', 'fatal_acceleration', 'flak_shot', 'flechette', 'frail_momentum', 
		'frigid_blast', 'full_contact', 'hells_chamber', 'hydraulic_chamber', 'incendiary_coat', 
		'kill_switch', 'laser_sight', 'lingering_torment', 'loaded_capacity', 'lock_and_load', 
		'loose_chamber', 'momentary_pause', 'motus_setup', 'nano_applicator', 'narrow_barrel', 
		'point_blank', 'primed_ammo_stock', 'primed_charged_shell', 'primed_chilling_grasp', 
		'primed_cleanse_corpus', 'primed_cleanse_corrupted', 'primed_cleanse_grineer', 'primed_cleanse_infested', 'primed_ravage', 
		'primed_point_blank', 'primed_shotgun_ammo_mutation', 'primed_tactical_pump', 'prize_kill', 'ravage', 
		'repeater_clip', 'scattering_inferno', 'seeking_force', 'seeking_fury', 'shell_compression', 
		'shell_shock', 'shotgun_ammo_mutation', 'shotgun_savvy', 'shotgun_barrage', 'shrapnel_shot', 
		'shred_shot', 'shredder', 'silent_battery', 'snap_shot', 'soft_hands', 
		'sweeping_serration', 'tactical_pump', 'tainted_shell', 'toxic_barrage', 'vicious_spread', 
		'aero_agility', 'charged_chamber', 'depleted_reload', 'emergent_aftermath', 'harkonar_scope', 
		'lie_in_wait', 'primed_chamber', 'primed_sniper_ammo_mutation', 'sharpshooter', 'sniper_ammo_mutation', 
		'target_acquired', 'arrow_mutation', 'feathered_arrows', 'plan_b', 'soaring_strike', 
		'split_flights', 'thunderbolt', 'air_recon', 
		'augur_pact', 'augur_seeker', 'barrel_diffusion', 'blind_shot', 'bore', 
		'calculated_victory', 'carnis_stinger', 'concealed_explosives', 'concussion_rounds', 'convulsion', 
		'creeping_bullseye', 'deep_freeze', 'eject_magazine', 'embedded_catalyzer', 'expel_corpus', 
		'expel_corrupted', 'expel_grineer', 'expel_infested', 'frostbite', 'full_capacity', 
		'fulmination', 'galvanized_crosshairs', 'galvanized_diffusion', 'galvanized_shot', 
		'gunslinger', 'hawk_eye', 'heated_charge', 'heavy_warhead', 'hollow_point', 
		'hornet_strike', 'hydraulic_barrel', 'hydraulic_crosshairs', 'ice_storm', 'impaler_munitions', 
		'jolt', 'jugulus_spines', 'lethal_momentum', 'lethal_torrent', 'loose_magazine', 
		'magnum_force', 'maim', 'meteor_munitions', 'night_stalker', 'no_return', 
		'pathogen_rounds', 'perpetual_agony', 'pistol_ammo_mutation', 'pistol_gambit', 'pistol_pestilence', 
		'pressurized_magazine', 'primed_expel_corpus', 'primed_expel_corrupted', 'primed_expel_grineer', 'primed_expel_infested', 
		'primed_fulmination', 'primed_heated_charge', 'primed_pistol_ammo_mutation', 'primed_pistol_gambit', 'primed_quickdraw', 
		'primed_slip_magazine', 'primed_target_cracker', 'pummel', 'quickdraw', 'razor_munitions', 
		'razor_shot', 'recuperate', 'reflex_draw', 'ruinous_extension', 'saxum_spittle', 
		'scorch', 'secondary_wind', 'seeker', 'sharpened_bullets', 'slip_magazine', 
		'spry_sights', 'steady_hands', 'strafing_slide', 'stunning_speed', 'suppress', 
		'sure_shot', 'synth_charge', 'tainted_clip', 'target_cracker', 'targeting_subsystem', 
		'trick_mag', 'auger_strike', 'berserker_fury', 'blood_rush', 
		'body_count', 'buzz_kill', 'collision_force', 'condition_overload', 'corrupt_charge', 
		'counterweight', 'covert_lethality', 'dispatch_overdrive', 'drifting_contact', 'enduring_affliction', 
		'enduring_strike', 'energy_channel', 'explosive_demise', 'fever_strike', 'finishing_touch', 
		'focus_energy', 'focused_defense', 'fury', 'gladiator_might', 'gladiator_rush', 
		'gladiator_vice', 'guardian_derision', 'healing_return', 'heartseeker', 'heavy_trauma', 
		'impenetrable_offense', 'jagged_edge', 'killing_blow', 'lasting_sting', 'life_strike', 
		'maiming_strike', 'martial_fury', 'melee_prowess', 'molten_impact', 'mortal_conduct', 
		'motus_impact', 'north_wind', 'organ_shatter', 'parry', 'power_throw', 
		'pressure_point', 'primed_fever_strike', 'primed_fury', 'primed_heavy_trauma', 
		'primed_pressure_point', 'primed_reach', 'primed_smite_corpus', 'primed_smite_corrupted', 'primed_smite_grineer', 
		'primed_smite_infested', 'proton_snap', 'quick_return', 'quickening', 'reach', 
		'rebound', 'reflex_coil', 'relentless_assault', 'relentless_combination', 'rending_strike', 
		'seismic_wave', 'serrated_edges', 'sharpened_blade', 
		'shattering_impact', 'shocking_touch', 'smite_corpus', 'smite_corrupted', 
		'smite_grineer', 'smite_infested', 'spoiled_strike', 'spring_loaded_blade', 'stand_ground', 
		'strain_infection', 'sundering_strike', 'sword_alone', 'tek_gravity', 'true_punishment', 
		'true_steel', 'vicious_frost', 'virulent_scourge', 'volcanic_edge', 'voltaic_strike', 
		'weeping_wounds', 'whirlwind', 'argent_scourge', 'astral_twilight', 'atlantis_vulcan', 
		'biting_piranha', 'bleeding_willow', 'blind_justice', 'brutal_tide', 'bullet_dance', 
		'burning_wasp', 'butchers_revelry', 'carving_mantis', 'celestial_nightfall', 'clashing_forest', 
		'cleaving_whirlwind', 'coiling_viper', 'crashing_havoc', 'crashing_timber', 'crimson_dervish', 
		'crossing_snakes', 'crushing_ruin', 'cunning_aspect', 'cyclone_kraken', 'decisive_judgement', 
		'defiled_snapdragon', 'dividing_blades', 'eleventh_storm', 'fateful_truth', 'final_harbinger', 
		'flailing_branch', 'four_riders', 'fracturing_wind', 'gaias_tragedy', 'galeforce_dawn', 
		'gemini_cross', 'gleaming_talon', 'gnashing_payara', 'grim_fury', 'high_noon', 
		'homing_fang', 'iron_phoenix', 'lashing_coil', 'last_herald', 'mafic_rain', 
		'malicious_raptor', 'mountains_edge', 'noble_cadence', 'piercing_fury', 'pointed_wind', 
		'quaking_hand', 'reaping_spiral', 'rending_crane', 'rending_wind', 'rising_steel', 
		'scarlet_hurricane', 'seismic_palm', 'shadow_harvest', 'shattering_storm', 'shimmering_blight', 
		'sinking_talon', 'slicing_feathers', 'sovereign_outcast', 'spinning_needle', 'stalking_fan', 
		'star_divide', 'stinging_thorn', 'sundering_weave', 'swirling_tiger', 'swooping_falcon', 
		'tainted_hydra', 'tempo_royale', 'tranquil_cleave', 'twirling_spire', 'vengeful_revenant', 
		'vermillion_storm', 'vicious_approach', 'votive_onslaught', 'vulpine_mask', 'wise_razor', 
		'aerial_bond', 'animal_instinct', 'astral_bond', 'calculated_redirection', 'contagious_bond', 
		'covert_bond', 'duplex_bond', 'enhanced_vitality', 'link_fiber', 'link_redirection', 
		'link_vitality', 'loyal_companion', 'medi_pet_kit', 'metal_fiber', 'momentous_bond', 
		'mystic_bond', 'pack_leader', 'primed_animal_instinct', 'primed_pack_leader', 'reinforced_bond', 
		'restorative_bond', 'seismic_bond', 'synth_deconstruct', 'synth_fiber', 'tenacious_bond', 
		'vicious_bond', 'anti_grav_array', 'coolant_leak', 'guardian', 'manifold_bond', 
		'medi_ray', 'sanctuary', 'shield_charger', 'vacuum', 'accelerated_deflection', 'ambush', 
		'ammo_case', 'arc_coil', 'assault_mode', 'auto_omni', 'botanist', 
		'calculated_shot', 'cordon', 'crowd_dispersion', 'detect_vulnerability', 'electro_pulse', 
		'energy_generator', 'fatal_attraction', 'fired_up', 'ghost', 'investigator', 
		'looter', 'molecular_conversion', 'negate', 'odomedic', 'primed_regen', 
		'reawaken', 'regen', 'repair_kit', 'revenge', 'sacrifice', 
		'scan_aquatic_lifeforms', 'scan_matter', 'self_destruct', 'spare_parts', 
		'targeting_receptor', 'thumper', 'vaporize', 'anti_grav_grenade', 'security_override', 
		'shockwave_actuators', 'stasis_field', 'tractor_beam', 'whiplash_mine', 'bite', 
		'fetch', 'flame_gland', 'frost_jaw', 'hastened_deflection', 
		'hunter_command', 'hunter_recovery', 'hunter_synergy', 'maul', 'scavenge', 
		'shelter', 'shock_collar', 'tandem_bond', 'venom_teeth', 'dig', 
		'ferocity', 'howl', 'hunt', 'mecha_overdrive', 'mecha_recharge', 
		'neutralize', 'proboscis', 'protect', 'retrieve', 'savagery', 
		'stalk', 'strain_eruption', 'strain_fever', 'trample', 'unleashed', 
		'cats_eye', 'charm', 'draining_bite', 'mischief', 'pounce', 
		'reflect', 'sense_danger', 'sharpened_claws', 'swipe', 'tek_assault', 
		'tek_enhance', 'territorial_aggression', 'transfusion', 'acidic_spittle', 'anabolic_pollination', 
		'endoparasitic_vector', 'iatric_mycelium', 'infectious_bite', 'paralytic_spores', 
		'volatile_parasite', 'crescent_charge', 'crescent_devolution', 'martyr_symbiosis', 
		'panzer_devolution', 'sly_devolution', 'survival_instinct', 'viral_quills', 'aerial_prospectus', 
		'diversified_denial', 'equilibrium_audit', 'evasive_denial', 'focused_prospectus', 'null_audit', 
		'reflex_denial', 'repo_audit', 'synergized_prospectus', 'afterburner', 'argon_plating', 
		'auxiliary_power', 'cold_snap', 'efficient_transferral', 'energy_amplifier', 'energy_field', 
		'energy_inversion', 'enhanced_durability', 'hyperion_thrusters', 'kinetic_diversion', 'morphic_transformer', 
		'primed_morphic_transformer', 'superior_defenses', 'system_reroute', 'ammo_chain', 'archgun_ace', 
		'automatic_trigger', 'ballista_measure', 'charged_bullets', 'combustion_rounds', 'comet_blast', 
		'containment_breach', 'contamination_casing', 'critical_focus', 'deadly_efficiency', 
		'dual_rounds', 'electrified_barrel', 'hollowed_bullets', 'hypothermic_shell', 'magazine_extension', 
		'magma_chamber', 'marked_target', 'modified_munitions', 'parallax_scope', 'polar_magazine', 
		'primed_deadly_efficiency', 'primed_dual_rounds', 'primed_rubedo_lined_barrel', 'quasar_drill', 'quick_reload', 
		'resolute_focus', 'rubedo_lined_barrel', 'sabot_rounds', 'shell_rush', 'venomous_clip', 
		'zodiac_shred', 'astral_autopsy', 'astral_slash', 'blazing_steel', 'bleeding_edge', 
		'critical_meltdown', 'cryo_coating', 'cutting_edge', 'extend', 
		'furor', 'conductive_blade', 'glacial_edge', 'infectious_injection', 'ion_infusion', 
		'meteor_crash', 'nebula_bore', 'poisonous_sting', 'searing_steel', 'sudden_impact', 
		'tempered_blade', 'necramech_augur', 'necramech_aviator', 'necramech_blitz', 'necramech_continuity', 
		'necramech_deflection', 'necramech_drift', 'necramech_efficiency', 'necramech_enemy_sense', 'necramech_flow', 
		'necramech_friction', 'necramech_fury', 'necramech_hydraulics', 'necramech_intensify', 'necramech_pressure_point', 
		'necramech_rage', 'necramech_reach', 'necramech_rebuke', 'necramech_redirection', 'necramech_refuel', 
		'necramech_repair', 'necramech_seismic_wave', 'necramech_slipstream', 'necramech_steel_fiber', 'necramech_streamline', 
		'necramech_stretch', 'necramech_thrusters', 'necramech_vitality', 'air_time', 'bomb_the_landin', 
		'cold_arrival', 'extreme_velocity', 'inertia_dampeners', 'juice', 'kinetic_friction', 
		'mad_stack', 'mag_locks', 'nitro_boost', 'perfect_balance', 
		'pop_top', 'poppin_vert', 'primo_flair', 'quick_escape', 'rail_guards', 
		'slay_board', 'sonic_boost', 'thrash_landing', 'trail_blazer', 'vapor_trail', 
		'venerdo_hoverdrive', 'seeking_shuriken', 'smoke_shadow', 'fatal_teleport', 'rising_storm', 
		'rubble_heap', 'path_of_statues', 'tectonic_fracture', 'ore_gaze', 'rumbled', 
		'titanic_rumbler', 'sonic_fracture', 'resonance', 'savage_silence', 'resonating_quake', 
		'elusive_retribution', 'endless_lullaby', 'reactive_storm', 'afterburn', 'everlasting_ward', 
		'guardian_armor', 'vexing_retaliation', 'guided_effigy', 'recrystalize', 'spectral_spirit', 
		'fireball_frenzy', 'immolated_radiance', 'healing_flame', 'purifying_flames', 'exothermic', 
		'duality', 'calm_and_frenzy', 'peaceful_provocation', 'energy_transfer', 
		'purging_slash', 'surging_dash', 'radiant_finish', 'furious_javelin', 'chromatic_blade', 
		'warriors_rest', 'biting_frost', 'freeze_force', 'ice_wave_impedance', 'chilling_globe', 'icy_avalanche', 
		'mending_splinters', 'spectrosiphon', 'shattered_storm', 'dread_ward', 'blood_forge', 
		'blending_talons', 'mach_crash', 'thermal_transfer', 'gourmand', 'hearty_nourishment', 
		'catapult', 'cathode_current', 'tribunal', 'warding_thurible', 'lasting_covenant', 
		'balefire_surge', 'blazing_pillage', 'viral_tempest', 'tidal_impunity', 'rousing_plunder', 
		'pilfering_swarm', 'desiccations_curse', 'elemental_sandstorm', 'negation_armor', 
		'empowered_quiver', 'power_of_three', 'piercing_navigator', 'infiltrate', 'concentrated_arrow', 
		'accumulating_whipclaw', 'venari_bodyguard', 'pilfering_strangledome', 
		'wrath_of_ukko', 'valence_formation', 'swift_bite', 'rift_haven', 'rift_torrent', 'cataclysmic_continuum', 
		'damage_decoy', 'deceptive_bond', 'savior_decoy', 'hushed_invisibility', 'safeguard_switch', 'irradiating_disarm', 
		'greedy_pull', 'magnetized_discharge', 'counter_pulse', 'fracturing_crush', 
		'ballistic_bullseye', 'muzzle_flash', 'staggering_shield', 'mesas_waltz',
		'hall_of_malevolence', 'explosive_legerdemain', 'total_eclipse', 'prism_guard', 
		'soul_survivor', 'creeping_terrify', 'despoil', 'shield_of_shadows', 
		'controlled_slide', 'pyroclastic_flow', 'reaping_chakram', 'safeguard', 'divine_retribution', 
		'abundant_mutation', 'teeming_virulence', 'larva_burst', 'parasitic_vitality', 'insatiable', 
		'neutron_star', 'antimatter_absorb', 'escape_velocity', 'molecular_fission', 
		'mind_freak', 'pacifying_bolts', 'chaos_sphere', 'assimilate', 'singularity', 
		'smite_infusion', 'hallowed_eruption', 'phoenix_renewal', 'hallowed_reckoning', 
		'partitioned_mallet', 'conductor', 'temporal_artillery', 'repair_dispensary', 'temporal_erosion', 
		'wrecking_wall', 'thrall_pact', 'blinding_reave', 'mesmer_shield', 
		'ironclad_charge', 'iron_shrapnel', 'piercing_roar', 'reinforcing_stomp', 
		'revealing_spores', 'venom_dose', 'regenerative_molt', 'contagion_cloud', 
		'shadow_haze', 'dark_propagation', 'axios_javelineers', 'intrepid_stand', 
		'ironclad_flight', 'spellbound_harvest', 'beguiling_lantern', 'razorwing_blitz', 
		'pool_of_life', 'vampire_leech', 'abating_link', 'champions_blessing', 
		'swing_line', 'eternal_war', 'prolonged_paralysis', 'enraged', 'hysterical_assault', 
		'tesla_bank', 'photon_repeater', 'repelling_bastille', 'shock_trooper', 'shocking_speed', 'recharge_barrier', 
		'transistor_shield', 'capacitance', 'ulfruns_endurance', 'fused_reservoir', 'critical_surge', 
		'celestial_stomp', 'enveloping_cloud', 'primal_rage', 'vampiric_grasp', 'the_relentless_lost', 
		'surging_blades', 'loyal_merulina', 'merulina_guardian', 'anchored_glide', 'target_fixation', 'airburst_rounds', 
		'jet_stream', 'funnel_clouds', 'eroding_blight', 'gleaming_blight', 'toxic_blight', 'stockpiled_blight', 
		'entropy_burst', 'entropy_flight', 'entropy_spike', 'entropy_detonation', 'justice_blades', 'scattered_justice', 
		'shattering_justice', 'neutralizing_justice', 'bright_purity', 'lasting_purity', 'winds_of_purity', 
		'disarming_purity', 'deadly_sequence', 'sequence_burn', 'toxic_sequence', 'voltage_sequence', 'blade_of_truth', 
		'gilded_truth', 'stinging_truth', 'avenging_truth', 'tether_grenades', 'flux_overdrive', 'thermagnetic_shells', 
		'static_discharge', 'kinetic_ricochet', 'electromagnetic_shielding', 'vulcan_blitz', 'acid_shells', 'rift_strike', 
		'nightwatch_napalm', 'fomorian_accelerant', 'hunters_bonesaw', 'bursting_mass', 'napalm_grenades', 'wild_frenzy', 
		'efficient_beams', 'exposing_harpoon', 'meticulous_aim', 'deadly_maneuvers', 'dizzying_rounds', 'precision_strike', 
		'combat_reload', 'range_advantage', 'critical_precision', 'vile_discharge', 'eximus_advantage', 'metamorphic_magazine', 
		'sentient_barrage', 'sentient_surge', 'critical_mutation', 'volatile_variant', 'clip_delegation', 'photon_overcharge', 
		'burning_hate', 'unseen_dread', 'ambush_optics', 'brain_storm', 'directed_convergence', 'double_tap', 
		'focused_acceleration', 'shrapnel_rounds', 'skull_shots', 'spring_loaded_broadhead', 
		'damzav_vati', 'zazvat_kar', 'bhisaj_bal', 'hata_satya', 'antimatter_mine', 
		'defiled_reckoning', 'discharge_strike', 'hysterical_fixation', 'kinetic_collision', 
		'push_and_pull', 'sapping_reach', 'shield_overload', 'signal_flare', 'tear_gas', 'ward_recovery', 
		'draining_gloom', 'final_tap', 'gorgon_frenzy', 'grinloked', 'measured_burst', 
		'precision_munition', 'static_alacrity', 'sudden_justice', 'thundermiter', 'triple_tap'
		'resourceful_retriever', 'sepsis_claws', 'frenzied_posture', 'magnetic_strike', 'immunity_resistance', 
		'bell_ringer', 'galvanized_reflex', 'galvanized_steel', 'galvanized_elementalist', 'assassin_posture' 
		'protector_posture', 'persistent_posture', 'shocking_claws' , 'chilling_claws', 'burning_claws', 
		'disabling_conditioning', 'brute_conditioning', 'prosperous_retriever', 'elusive_posture', 'balanced_posture'
		'loyal_retriever', 'precision_conditioning', 'cull_the_weak', 'bloodthirst']
	elif answer == "9" and enableDebugTestList == 1:
		listName = "Test"
		my_itemList = ['volnus_prime_set', 'corvas_prime_set']
		#my_itemList = ['Magus Revert']
	else:
		print("Error: Nothing to scrape. Only viable options are 1, 2 or 3!")
		answer = input()
		sys.exit()
	# --------------------------------------- [END: Set this according to your needs] ---------------------------------------------
	# Initialisation of variables
	my_data = [['Date','Volume','Minimum', 'Maximum', 'Median', 'Item']]
	#newLine = []
	maxMedianLineIndex = 1
	currentLineIndex = 1
	maxMedian = 0
	parseDataStr = ""
	if enableDebugDump > 0:
		debugJonsonDump = ""
	fileNameAddon = ""
	#breakpoint()
	# The scipt starts here
	if answer == "9":
		fileNameAddon = "DEBUG_"
	if enableDebugDump == 1:
		parseDataStr = "fileNameAddon=" + fileNameAddon + "\n"
		print(parseDataStr)
		debugJonsonDump = debugJonsonDump + parseDataStr
		parseDataStr = "Used item list " + answer + " =" + str(my_itemList) + "\n\n"
		print(parseDataStr)
		debugJonsonDump = debugJonsonDump + parseDataStr
	# Loop through the item list and extract the desired data
	for item in my_itemList:
		# scrape the current item prices from warframe.market
		itemStr = string.capwords(item.replace('_', ' '))
		try:
			main_url = req_url('https://api.warframe.market/v1/items/' + item + '/statistics')
		except:
			main_url = None
			parseDataStr = "Error: The item [" + item + "] does not exist on warframe.market!"
			print(parseDataStr)
			if enableDebugDump > 1:
				debugJonsonDump = debugJonsonDump + (parseDataStr + "\n")
			# Load default values
			parsed_min = 0
			parsed_max = 0
			parsed_median = 0
			parsed_volume = 0
			date_time = "9999-99-99"
		else:
			#breakpoint()
			
			data = main_url.read()
			main_url = None
			parsed = json.loads(data)
			data = None
			# Uncomment the next 4 lines to check what data the website returns
			if enableDebugDump == 1:
				if currentLineIndex == 1:
					parseDataStr = "Received data for item " + itemStr + " [" + json.dumps(parsed) + "]\n"
				else:
					parseDataStr = "\nReceived data for item " + itemStr + " [" + json.dumps(parsed) + "]\n"
				print(parseDataStr)
				debugJonsonDump = debugJonsonDump + parseDataStr
			#breakpoint()
			dataSetIndex = -1 # by default use the last set which is the last recorded day
			try:
				nbrOfSets = int(len(parsed['payload']['statistics_closed']['90days']))
			except:
				parseDataStr = "Error: Number of sets could not be extracted. Skipping [mod_rank=0 search."
				print(parseDataStr)
				if enableDebugDump == 1:
					debugJonsonDump = debugJonsonDump + (parseDataStr + "\n")
			else: 
				if listName == "Arcane" or listName == "Mods":
					# Only for Arcane and Mods parse the mod_rank of the last set
					if enableDebugDump == 1:
						parseDataStr = "Start search for [mod_rank=0].\nNbr. of sets to search= " + str(nbrOfSets) + "\n"
						print(parseDataStr)
						debugJonsonDump = debugJonsonDump + parseDataStr
					#breakpoint()
					while (nbrOfSets + dataSetIndex) > 0:
						if enableDebugDump == 1:
							parseDataStr = " " + str(nbrOfSets) + " + " + str(dataSetIndex) + " > 0\n"
							print(parseDataStr)
							debugJonsonDump = debugJonsonDump + parseDataStr
						try:
							parsed_modRank = parsed['payload']['statistics_closed']['90days'][dataSetIndex]['mod_rank']
						except:
							parseDataStr = "Error: Parsing error of [mod_rank] for " + itemStr + "!"
							print(parseDataStr)
							parsed_modRank = 0
							if enableDebugDump == 1:
								debugJonsonDump = debugJonsonDump + parseDataStr
							break
						if enableDebugDump == 1:
							parseDataStr = "  " + str(nbrOfSets + dataSetIndex) + "(" + str(dataSetIndex) + ")" + ": " + str(parsed['payload']['statistics_closed']['90days'][dataSetIndex]) + "\n"
							print(parseDataStr)
							debugJonsonDump = debugJonsonDump + parseDataStr
							parseDataStr = "  parsed_modRank=" + str(parsed_modRank) + "\n"
							print(parseDataStr)
							debugJonsonDump = debugJonsonDump + parseDataStr
						# If the last set is not mod_rank=0 select the set -2 from end to parse
						if parsed_modRank == 0:
							break
						else:
							dataSetIndex -= 1
					#END while (nbrOfSets + dataSetIndex) > 0:
					parsed_modRank = None
					#breakpoint()
				if enableDebugDump == 1:
					parseDataStr = "Used set at index " + str(nbrOfSets + dataSetIndex) + ": " + str(parsed['payload']['statistics_closed']['90days'][dataSetIndex]) + "\n"
					print(parseDataStr)
					debugJonsonDump = debugJonsonDump + parseDataStr
			# END else:
			#breakpoint()
			# parse min. price
			try:
				parsed_min = parsed['payload']['statistics_closed']['90days'][dataSetIndex]['min_price']
			except:
				parseDataStr = "Error: Parsing error of [min_price] for " + itemStr + "!"
				print(parseDataStr)
				parsed_min = 0
				if enableDebugDump == 1:
					debugJonsonDump = debugJonsonDump + (parseDataStr + "\n")
			# parse max. price
			try:
				parsed_max = parsed['payload']['statistics_closed']['90days'][dataSetIndex]['max_price']
			except:
				parseDataStr = "Error: Failed parsing of [max_price] for " + itemStr + "!"
				print(parseDataStr)
				parsed_max = 0
				if enableDebugDump == 1:
					debugJonsonDump = debugJonsonDump + (parseDataStr + "\n")
			# parse median price
			try:
				parsed_median = parsed['payload']['statistics_closed']['90days'][dataSetIndex]['median']
				parsed_median = round(parsed_median)
			except:
				parseDataStr = "Error: Failed parsing of [median] for " + itemStr + "!"
				print(parseDataStr)
				parsed_median = 0
				if enableDebugDump == 1:
					debugJonsonDump = debugJonsonDump + (parseDataStr + "\n")
			# parse sold volume
			try:
				parsed_volume = parsed['payload']['statistics_closed']['90days'][dataSetIndex]['volume']
			except:
				parseDataStr = "Error: Failed parsing of [volume] for " + itemStr + "!"
				print(parseDataStr)
				parsed_volume = 0
				if enableDebugDump == 1:
					debugJonsonDump = debugJonsonDump + (parseDataStr + "\n")
			# parse date
			try:
				date_time = parsed['payload']['statistics_closed']['90days'][dataSetIndex]['datetime']
			except:
				parseDataStr = "Error: Failed parsing of [datetime] for " + itemStr + "!"
				print(parseDataStr)
				date_time = "9999-99-99"
				if enableDebugDump == 1:
					debugJonsonDump = debugJonsonDump + (parseDataStr + "\n")
			parsed = None
		#Since there are exeption on warframe market, where for example the sevagoth prime set is just calles "sevagoth prime"
		# we manually add the set here to have it uniform wit hthe rest or the frame sets
		#breakpoint()
		if itemStr == 'Sevagoth Prime':
			itemStr = 'Sevagoth Prime Set'
		elif itemStr == 'Epitaph Prime':
			itemStr = 'Epitaph Prime Set'
		elif itemStr == 'Nautilus Prime':
			itemStr = 'Nautilus Prime Set'
		parseDataStr = "The price on " + date_time[:10] + " for a sold volume of " + str(parsed_volume) + " is " + str(parsed_min) + " to " + str(parsed_max) + " (median " + str(parsed_median) + ") platinum for " + itemStr
		print(parseDataStr)
		if enableDebugDump == 1:
			debugJonsonDump = debugJonsonDump + (parseDataStr + "\n")
		#breakpoint()
		# Add the new data line with the scraped data
		newDataLine = [date_time[:10], str(parsed_volume), str(parsed_min), str(parsed_max), str(parsed_median), itemStr]
		my_data.append(newDataLine)
		if enableDebugDump == 1:
			parseDataStr = "parsed_median=" + str(parsed_median) + " > maxMedian=" + str(maxMedian) + " ?\n"
			print(parseDataStr)
			debugJonsonDump = debugJonsonDump + parseDataStr
		if parsed_median > maxMedian:
			maxMedian = parsed_median
			maxMedianLineIndex = currentLineIndex
			if enableDebugDump == 1:
				parseDataStr = " Yes -> maxMedianLineIndex=" + str(maxMedianLineIndex) + "\n"
				print(parseDataStr)
				debugJonsonDump = debugJonsonDump + parseDataStr
		elif enableDebugDump == 1:
			parseDataStr = " No\n"
			print(parseDataStr)
			debugJonsonDump = debugJonsonDump + parseDataStr
		currentLineIndex += 1
		sleep(0.1) # wait 300 ms
	#END for item in my_itemList:
	my_itemList = None
	dataSetIndex = None
	itemStr = None
	item = None
	maxMedian = None
	currentLineIndex = None
	parsed_min = None
	parsed_max = None
	parsed_median = None
	parsed_volume = None
	date_time = None
	try:
		parseDataStr = "\nThe most valuable item currently is " + my_data[maxMedianLineIndex][5] + " with a median of " + my_data[maxMedianLineIndex][4] + " platinum.\n"
		maxMedianLineIndex = None
		print(parseDataStr)
		if enableDebugDump == 1:
			debugJonsonDump = debugJonsonDump + parseDataStr
	except:
		parseDataStr = "Error: Failed to scrape anything!\n"
		print(parseDataStr)
		if enableDebugDump == 1:
			debugJonsonDump = debugJonsonDump + parseDataStr
	else:
		if enableDebugDump == 1:
			parseDataStr = "my_data=" + str(my_data) + "\n"
			print(parseDataStr)
			debugJonsonDump = debugJonsonDump + parseDataStr
	# End else:
	#breakpoint()
	script_dir = str(Path( __file__ ).parent.absolute()) + "/"
	# Store the received data in a txt-file (only for debug)
	if enableDebugDump > 0:
		fileName = script_dir + fileNameAddon + listName + "_DebugDump.txt"
		parseDataStr = "\nStore debug dump into [" + fileName + "]."
		print(parseDataStr)
		debugJonsonDump = debugJonsonDump + parseDataStr
		with open(fileName, 'w') as debugDumpFile:
			debugDumpFile.write(debugJonsonDump)
	# Store the extracted data in a csv-file
	#breakpoint()
	now = datetime.now() # current date and time
	parseDataStr = now.strftime("%Y-%m-%d")
	fileName = script_dir + fileNameAddon + listName + "_" + parseDataStr +".csv"
	now = None
	# In manual mode ask the user if he wants to save the data
	if mode == "manually":
		print("Save the results to " + fileName + "? y/n")
		answer = input()
	else:
		print("Save the results to " + fileName + ".\n")
		answer = "y"
	
	if answer == "y":
		with open(fileName, 'w', newline='') as outputFile:
			wr = csv.writer(outputFile, dialect='excel')
			try:
				wr.writerows(my_data)
			except:
				print("Error: Failed to create the CSV-file!")
			else:
				print("Successfully created the CSV-file.")
	script_dir = None
	my_data = None
	parseDataStr = None
	fileNameAddon = None
	if enableDebugDump > 0:
		debugJonsonDump = None
	if mode == "manually":
		print("Goodbye...")
		answer = input() # A quick and dirty "Press anny key to quit"
	mode = None


# Request to open search on warframe.market (not used)
#	def browser_open():
#		print('Would you like to buy/sell ' + string.capwords(search) + "? y/n")
#		browser_answer = input()
#		if browser_answer == "y":
#			webbrowser.open_new('https://warframe.market/items/' + search.replace(' ', '_'))
#		#if browser_answer == "n":
#	browser_open()

# Start the script (used to build everything or select a list)
def start_script():
	print('You can either scrape everything or select a specific item list.\nDo you want to scrape the whole warframe.market (takes some time)? y/n')
	answer = input()
	if answer == "y":
		warframeMarketScraper("1")
		warframeMarketScraper("2")
		warframeMarketScraper("3")
		warframeMarketScraper("4")
		warframeMarketScraper("5")
		warframeMarketScraper("6")
		print("Goodbye...")
		answer = input() # A quick and dirty "Press anny key to quit"
	elif answer == "n":
		warframeMarketScraper("manually")
	else:
		print("Goodbye...")
		answer = input() # A quick and dirty "Press anny key to quit"

start_script()

