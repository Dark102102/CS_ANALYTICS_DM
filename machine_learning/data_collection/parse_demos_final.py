#!/usr/bin/env python3
"""
Final Demo Parser - Properly maps deaths to rounds using tick ranges
Parses .dem files directly from the demos folder
"""

from demoparser2 import DemoParser
import pandas as pd
import numpy as np
from pathlib import Path
import warnings
import time
warnings.filterwarnings('ignore')

BASE_DIR = Path(__file__).parent
DEMOS_DIR = BASE_DIR / "demos"
OUTPUT_DIR = BASE_DIR / "hltv_data"
OUTPUT_DIR.mkdir(exist_ok=True)

def parse_demo_with_demoparser2(demo_file: Path) -> bool:
    """Parse a single demo file with proper round-death mapping"""
    print(f"\n  Parsing {demo_file.name}...")
    match_id = demo_file.stem

    try:
        parser = DemoParser(str(demo_file))

        # Get header info
        try:
            header = parser.parse_header()
            map_name = header.get('map_name', 'unknown')
            print(f"    Map: {map_name}")
        except:
            map_name = 'unknown'

        # ============================================================
        # 1. PARSE ROUND END EVENTS (with tick boundaries)
        # ============================================================
        try:
            round_events = parser.parse_event('round_end')
            if round_events.empty:
                print(f"    ✗ No rounds found")
                return False

            print(f"    Found {len(round_events)} rounds")
        except Exception as e:
            error_msg = str(e)
            if 'DemoEndsEarly' in error_msg:
                print(f"    ✗ Demo incomplete/corrupt (ends early)")
            elif 'range end index' in error_msg:
                print(f"    ✗ Demo corrupt (parsing error)")
            else:
                print(f"    ✗ Round parsing failed: {e}")
            return False

        try:

            # Build rounds dataframe with tick boundaries
            rounds_data = []
            for idx, event in round_events.iterrows():
                rounds_data.append({
                    'tick': event.get('tick', 0),
                    'winner': event.get('winner', ''),
                    'reason': event.get('reason', ''),
                    'winning_team': event.get('winning_team', event.get('winner', '')),
                })

            rounds_df = pd.DataFrame(rounds_data)
            rounds_df = rounds_df.sort_values('tick').reset_index(drop=True)
            rounds_df['round_num'] = range(1, len(rounds_df) + 1)

            # Calculate tick boundaries for each round
            rounds_df['tick_start'] = rounds_df['tick'].shift(1, fill_value=0)
            rounds_df['tick_end'] = rounds_df['tick']

        except Exception as e:
            print(f"    ✗ Round parsing failed: {e}")
            return False

        # ============================================================
        # 2. PARSE DEATH EVENTS (assign to rounds)
        # ============================================================
        try:
            death_events = parser.parse_event('player_death')

            if death_events.empty:
                print(f"    Warning: No deaths found")
                deaths_df = pd.DataFrame()
            else:
                print(f"    Found {len(death_events)} deaths")

                # Function to assign round number based on tick
                def assign_round_num(tick):
                    for _, r in rounds_df.iterrows():
                        if r['tick_start'] < tick <= r['tick_end']:
                            return r['round_num']
                    # If outside all rounds, assign to nearest
                    return rounds_df.iloc[(rounds_df['tick'] - tick).abs().argmin()]['round_num']

                # Assign round numbers
                death_events['round_num'] = death_events['tick'].apply(assign_round_num)

                # Build clean deaths dataframe
                deaths_df = pd.DataFrame({
                    'round_num': death_events['round_num'],
                    'tick': death_events['tick'],
                    'attacker_name': death_events.get('attacker_name', ''),
                    'attacker_steamid': death_events.get('attacker_steamid', ''),
                    'attacker_side': death_events.get('attacker_side', ''),
                    'victim_name': death_events.get('user_name', death_events.get('victim_name', '')),
                    'victim_steamid': death_events.get('user_steamid', death_events.get('victim_steamid', '')),
                    'victim_side': death_events.get('user_side', death_events.get('victim_side', '')),
                    'weapon': death_events.get('weapon', ''),
                    'headshot': death_events.get('headshot', False),
                    'penetrated': death_events.get('penetrated', 0),
                    'thrusmoke': death_events.get('thrusmoke', False),
                    'attackerblind': death_events.get('attackerblind', False),
                    'noscope': death_events.get('noscope', False),
                    'attackerinair': death_events.get('attackerinair', False),
                    'distance': death_events.get('distance', 0),
                    'dmg_health': death_events.get('dmg_health', 0),
                    'dmg_armor': death_events.get('dmg_armor', 0),
                    'hitgroup': death_events.get('hitgroup', 'generic'),
                    'assister_name': death_events.get('assister_name', ''),
                    'assister_steamid': death_events.get('assister_steamid', ''),
                    'assistedflash': death_events.get('assistedflash', False),
                })

                # Remove invalid deaths (suicides, world deaths)
                deaths_df = deaths_df[
                    (deaths_df['attacker_name'] != '') &
                    (deaths_df['victim_name'] != '') &
                    (deaths_df['attacker_name'] != deaths_df['victim_name'])
                ].reset_index(drop=True)

                print(f"    Cleaned to {len(deaths_df)} valid deaths across {deaths_df['round_num'].nunique()} rounds")

        except Exception as e:
            print(f"    Warning: Death parsing failed: {e}")
            deaths_df = pd.DataFrame()

        # ============================================================
        # 3. PARSE BOMB EVENTS
        # ============================================================
        bomb_planted_rounds = set()
        bomb_defused_rounds = set()
        bomb_exploded_rounds = set()

        try:
            bomb_planted = parser.parse_event('bomb_planted')
            if not bomb_planted.empty:
                for _, event in bomb_planted.iterrows():
                    tick = event.get('tick', 0)
                    for _, r in rounds_df.iterrows():
                        if r['tick_start'] < tick <= r['tick_end']:
                            bomb_planted_rounds.add(r['round_num'])
                            break
                print(f"    Found {len(bomb_planted)} bomb plants")
        except:
            pass

        try:
            bomb_defused = parser.parse_event('bomb_defused')
            if not bomb_defused.empty:
                for _, event in bomb_defused.iterrows():
                    tick = event.get('tick', 0)
                    for _, r in rounds_df.iterrows():
                        if r['tick_start'] < tick <= r['tick_end']:
                            bomb_defused_rounds.add(r['round_num'])
                            break
                print(f"    Found {len(bomb_defused)} bomb defuses")
        except:
            pass

        try:
            bomb_exploded = parser.parse_event('bomb_exploded')
            if not bomb_exploded.empty:
                for _, event in bomb_exploded.iterrows():
                    tick = event.get('tick', 0)
                    for _, r in rounds_df.iterrows():
                        if r['tick_start'] < tick <= r['tick_end']:
                            bomb_exploded_rounds.add(r['round_num'])
                            break
                print(f"    Found {len(bomb_exploded)} bomb explosions")
        except:
            pass

        # Add bomb info to rounds
        rounds_df['bomb_planted'] = rounds_df['round_num'].isin(bomb_planted_rounds)
        rounds_df['bomb_defused'] = rounds_df['round_num'].isin(bomb_defused_rounds)
        rounds_df['bomb_exploded'] = rounds_df['round_num'].isin(bomb_exploded_rounds)

        # ============================================================
        # 4. AGGREGATE PLAYER STATS
        # ============================================================
        if not deaths_df.empty:
            # Kills per player
            player_kills = deaths_df.groupby('attacker_steamid').agg({
                'attacker_name': 'first',
                'attacker_side': 'first',
                'victim_name': 'count',
                'headshot': 'sum',
                'distance': 'mean',
                'dmg_health': 'sum',
            }).rename(columns={
                'attacker_name': 'player_name',
                'attacker_side': 'side',
                'victim_name': 'kills',
                'headshot': 'headshot_kills',
                'distance': 'avg_kill_distance',
                'dmg_health': 'total_damage'
            })

            # Deaths per player
            player_deaths = deaths_df.groupby('victim_steamid').size()

            # Combine
            player_stats = player_kills.copy()
            player_stats['deaths'] = player_stats.index.map(lambda x: player_deaths.get(x, 0))
            player_stats['kd_ratio'] = player_stats['kills'] / player_stats['deaths'].replace(0, 1)
            player_stats['headshot_pct'] = (player_stats['headshot_kills'] / player_stats['kills'] * 100).round(1)
            player_stats = player_stats.reset_index()

            print(f"    Aggregated stats for {len(player_stats)} players")
        else:
            player_stats = pd.DataFrame()

        # ============================================================
        # 5. SAVE OUTPUT FILES
        # ============================================================

        # Add metadata
        rounds_df['match_id'] = match_id
        rounds_df['map_name'] = map_name
        deaths_df['match_id'] = match_id
        deaths_df['map_name'] = map_name
        if not player_stats.empty:
            player_stats['match_id'] = match_id
            player_stats['map_name'] = map_name

        # Save
        rounds_df.to_csv(OUTPUT_DIR / f"{match_id}_rounds.csv", index=False)
        print(f"    ✓ Saved {match_id}_rounds.csv ({len(rounds_df)} rounds)")

        if not deaths_df.empty:
            deaths_df.to_csv(OUTPUT_DIR / f"{match_id}_deaths.csv", index=False)
            print(f"    ✓ Saved {match_id}_deaths.csv ({len(deaths_df)} deaths)")

        if not player_stats.empty:
            player_stats.to_csv(OUTPUT_DIR / f"{match_id}_players.csv", index=False)
            print(f"    ✓ Saved {match_id}_players.csv ({len(player_stats)} players)")

        return True

    except Exception as e:
        print(f"  ✗ Error parsing {demo_file.name}: {e}")
        import traceback
        traceback.print_exc()
        return False

def process_demos_final():
    """Process all demos with proper error handling"""
    print("="*80)
    print("CS2 DEMO PARSER - PROPER ROUND MAPPING")
    print("="*80)

    if not DEMOS_DIR.exists():
        print(f"\n✗ Demos directory {DEMOS_DIR} does not exist!")
        return

    # Get all .dem files (filter out empty ones)
    all_demos = sorted(DEMOS_DIR.glob('*.dem'))
    demo_files = [d for d in all_demos if d.stat().st_size > 1000000]  # At least 1MB

    print(f"\nFound {len(all_demos)} demo files total")
    print(f"Filtering to {len(demo_files)} valid demos (>1MB)")
    print(f"Output directory: {OUTPUT_DIR}\n")

    if not demo_files:
        print("✗ No valid demo files found!")
        return

    successful = 0
    stats = {'rounds': 0, 'deaths': 0, 'players': 0}

    # Process each demo
    for i, demo_file in enumerate(demo_files, 1):
        print(f"{'='*80}")
        print(f"[{i}/{len(demo_files)}] {demo_file.name}")
        print('='*80)

        if parse_demo_with_demoparser2(demo_file):
            successful += 1

            # Count generated data
            match_id = demo_file.stem
            rounds_file = OUTPUT_DIR / f"{match_id}_rounds.csv"
            deaths_file = OUTPUT_DIR / f"{match_id}_deaths.csv"
            players_file = OUTPUT_DIR / f"{match_id}_players.csv"

            if rounds_file.exists():
                stats['rounds'] += len(pd.read_csv(rounds_file))
            if deaths_file.exists():
                stats['deaths'] += len(pd.read_csv(deaths_file))
            if players_file.exists():
                stats['players'] += len(pd.read_csv(players_file))

    # Summary
    print("\n" + "="*80)
    print("PARSING COMPLETE")
    print("="*80)
    print(f"\nSuccessfully parsed: {successful}/{len(demo_files)} demos")
    print(f"\nTotal data extracted:")
    print(f"  - Rounds: {stats['rounds']}")
    print(f"  - Deaths: {stats['deaths']}")
    print(f"  - Unique players: {stats['players']}")

    if successful > 0:
        print(f"\nAverages per match:")
        print(f"  - Rounds: {stats['rounds']/successful:.1f}")
        print(f"  - Deaths: {stats['deaths']/successful:.1f}")
        print(f"  - Players: {stats['players']/successful:.1f}")

    # List output files
    output_files = sorted(OUTPUT_DIR.glob('*.csv'))
    print(f"\nGenerated {len(output_files)} CSV files in {OUTPUT_DIR}")

    # Show file summary
    rounds_files = list(OUTPUT_DIR.glob('*_rounds.csv'))
    deaths_files = list(OUTPUT_DIR.glob('*_deaths.csv'))
    players_files = list(OUTPUT_DIR.glob('*_players.csv'))

    print(f"  - {len(rounds_files)} rounds files")
    print(f"  - {len(deaths_files)} deaths files")
    print(f"  - {len(players_files)} players files")

if __name__ == "__main__":
    process_demos_final()
