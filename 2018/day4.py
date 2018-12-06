import re

class Day4:
    def __init__(self, lines):
        self.lines = lines
        
    def minutes_between_dates(self, d1, d2):
        if d1['year'] != d2['year']:
            print("different years")
            return None
        if d1['month'] != d2['month']:
            print("different months")
            return None
        if d1['day'] != d2['day']:
            print("different days")
            return None
        if d1['hour'] != d2['hour']:
            print("different hours")
            return None
        return abs(d1['minute'] - d2['minute'])
    
    def minutes_asleep(self, entry):
        asleep = None
        minutes = 0
        for evt in entry['events']:
            if evt['action'] == 'asleep':
                asleep = evt
            elif evt['action'] == 'awake':
                minutes += self.minutes_between_dates(asleep['date'], evt['date'])
        return minutes
        
    def load(self, lines):
        items = []
        context = {}
        assembly = {'events': []}
        for line in lines:
            item = self.parse(line)
            if not item: continue
            if item['action'] == 'begin':
                if len(assembly['events']) > 0:
                    items.append(assembly)
                assembly = {'events': [], 'guard': item['guard']}
                
            assembly['events'].append(item)

        if len(assembly) > 0:
            items.append(assembly)
            
        return items            
            
            
    def parse(self, line):
        m = re.search(r'\[(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+) (?P<hour>\d+):(?P<minute>\d+)]', line)
        if not m: 
            print(f"Could not parse line {line}")
            return None
        
        date = {}
        for key in ['year', 'month', 'day', 'minute', 'hour']:
            date[key] = int(m.group(key))
        
        m = re.search(r'Guard #(?P<guard>\d+) begins shift', line)
        if m:
            return {'guard': int(m.group('guard')), 'action': 'begin', 'date': date}
        
        m = re.search(r'falls asleep', line)
        if m:
            return {'action': 'asleep', 'date': date}

        m = re.search(r'wakes up', line)
        if m:
            return {'action': 'awake', 'date': date}

        return None
    
    def load_entries(self):
        self.entries = self.load(self.lines)
        print(f"loaded {len(self.entries)} entries")
        
    def get_entry_with_max_asleep(self, grouped):
        entry_max = None
        for g, entry in grouped.items():
            if not entry_max:
                entry_max = entry
            if entry_max['minutes_asleep'] < entry['minutes_asleep']:
                entry_max = entry
        return entry_max
    
    def fill_sleep_time(self):
        for entry in self.entries:
            minutes = self.minutes_asleep(entry)
            entry['minutes_asleep'] = minutes
            
    def grouped_by_guard(self):
        by_guard = {}
        for entry in self.entries:
            g = entry['guard']
            if g not in by_guard:
                by_guard[g] = {'items': [], 'guard': g}
            by_guard[g]['items'].append(entry)            
            
        for k, guard_entry in by_guard.items():
            asleep = 0
            for entry in guard_entry['items']:
                m = entry['minutes_asleep']
                if m > 0:
                    asleep += m
            guard_entry['minutes_asleep'] = asleep
            
        return by_guard
    
    def get_entries_for_guard(self, guard):
        return [entry for entry in self.entries if entry['guard'] == guard]
    
    def get_most_common_minute(self, entries):
        minutes = []
        for i in range(61):
            minutes.append(0)
        for entry in entries:
            asleep = None
            for evt in entry['events']:
                if evt['action'] == 'asleep':
                    asleep = evt
                elif evt['action'] == 'awake':
                    start = asleep['date']['minute']
                    end = evt['date']['minute']
                    for m in range(start, end):
                        minutes[m] += 1

        max_i = 0
        for i in range(len(minutes)):
            if minutes[i] > minutes[max_i]:
                max_i = i

        print(minutes)
        return max_i

    def strategy2(self, by_guard):
        max_entry = {'guard': -1, 'count': -1, 'minute': None}
        for g, grouped in by_guard.items():
            asleep = None
            minute_table = {}
            for item in grouped['items']:
                print(f'@@@ ITEM {item}')
                for evt in item['events']:
                    if evt['action'] == 'asleep':
                        asleep = evt['date']
                    elif evt['action'] == 'awake':
                        awake = evt['date']
                        for m in range(asleep['minute'], awake['minute']):
                            if m not in minute_table:
                                minute_table[m] = 0
                            minute_table[m] += 1
                for minute, count in minute_table.items():
                    if count > max_entry['count']:
                        max_entry = {'guard': g, 'count': count, 'minute': minute}
        
        if max_entry['guard'] < 0: return None
        return max_entry
    
    def run(self):
        self.load_entries()
        self.fill_sleep_time()
        by_guard = self.grouped_by_guard()
        
        # print(f"by guard: {by_guard[list(by_guard)[0]]}")
        
        entry_max = self.get_entry_with_max_asleep(by_guard)
        entries = entry_max['items']
        print(f"Got {len(entries)} entries for guard {entry_max['guard']}")
        max_minute = self.get_most_common_minute(entries)
        checksum = max_minute * entry_max['guard']

        self.entry_max = entry_max;
              
        print(f"Asleep for {entry_max['minutes_asleep']} minutes, most often during minute {max_minute}, checksum {checksum}: {entries}")

        self.strat2 = self.strategy2(by_guard)

        print(f"According to strategy2 checksum: {self.strat2['guard'] * self.strat2['minute']} data: {self.strat2}")
        
        
        return checksum
    
if __name__ == '__main__':              
    with open('day4.sorted.input') as f:
        Day4([line for line in list(f)]).run()

# answer a: 101194
# answer b: 102095    