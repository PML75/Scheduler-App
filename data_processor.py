class PersonDataProcessor:
    def __init__(self, input_file):
        self.input_file = input_file
        self.person_data = {}
        self.process_data()

    def process_data(self):
        with open(self.input_file, 'r') as my_file:
            data = my_file.read()

        # Split the data into individual person sections
        person_sections = data.strip().split('\n\n')

        # Counter for labeling persons
        person_counter = 1

        # Process each person's data
        for section in person_sections:
            # Split the section into lines
            lines = section.strip().split('\n')

            # Initialize variables for the person's data
            person_schedule = []
            person_daily_activity = []
            min_duration_of_meeting = 30  # Default value

            # Process each line in the section
            for line in lines:
                parts = [part.strip() for part in line.split('=')]
                if len(parts) == 2:
                    name, value = parts
                    value = eval(value)
                    if name == 'Schedule':
                        person_schedule = value
                    elif name == 'DailyAct':
                        person_daily_activity = value
                    elif name == 'min_duration_of_meeting':
                        min_duration_of_meeting = value

            # Use the person_counter as the name for each person
            person_name = f'person{person_counter}'

            # Check if the person_schedule is not empty before adding it to the dictionary
            if person_schedule:
                # Store the person's data in the dictionary with a counter label
                self.person_data[f'{person_name}_Schedule'] = person_schedule
                self.person_data[f'{person_name}_DailyAct'] = person_daily_activity

                # Increment the counter
                person_counter += 1

        # Add the min_duration_of_meeting to the dictionary
        self.person_data['min_duration_of_meeting'] = min_duration_of_meeting

    def time_to_minutes(self, time_str):
        # converted to minutes
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes

    def minutes_to_time(self, minutes):
        hours, mins = divmod(minutes, 60)
        return f'{hours:02}:{mins:02}'
    def filter_strays(self):
        for key in self.person_data:
            if key.endswith('_Schedule'):
                person_name = key.replace('_Schedule', '')  # Extract the person's name
                daily_activity_key = f"{person_name}_DailyAct"
                if daily_activity_key in self.person_data:
                    daily_activity = self.person_data[daily_activity_key]
                    schedule = self.person_data[key]

                    filtered_schedule = self.filter_strays_for_person(schedule, daily_activity)
                    self.person_data[key] = filtered_schedule

    def filter_strays_for_person(self, schedule, daily_activity):
        filtered_time = []

        range1 = self.time_to_minutes(daily_activity[0])
        range2 = self.time_to_minutes(daily_activity[1])

        for event in schedule:
            event_start = self.time_to_minutes(event[0])
            event_end = self.time_to_minutes(event[1])

            # Check if the event entirely falls outside the daily activity range
            if event_end <= range1 or event_start >= range2:
                continue  # Skip

            # Adjust the start time if it starts before the daily activity range
            if event_start < range1:
                event_start = range1

            filtered_time.append([self.minutes_to_time(event_start), self.minutes_to_time(event_end)])

        return filtered_time

    def calculate_free_time_intervals(self, person_name, meeting_duration):

        schedule_key = f"{person_name}_Schedule"
        daily_activity_key = f"{person_name}_DailyAct"



        schedule = self.person_data[schedule_key]
        daily_activity = self.person_data[daily_activity_key]

        schedule_gaps = []

        start_time_minutes = self.time_to_minutes(daily_activity[0])
        end_time_minutes = self.time_to_minutes(daily_activity[1])

        free_gap_start = start_time_minutes

        for event in schedule:
            event_start = self.time_to_minutes(event[0])
            event_end = self.time_to_minutes(event[1])

            if free_gap_start < event_start:
                while free_gap_start + meeting_duration <= event_start:
                    schedule_gaps.append(
                        [self.minutes_to_time(free_gap_start), self.minutes_to_time(free_gap_start + meeting_duration)])
                    free_gap_start += meeting_duration

            free_gap_start = max(free_gap_start, event_end)

        if free_gap_start + meeting_duration <= end_time_minutes:
            while free_gap_start + meeting_duration <= end_time_minutes:
                schedule_gaps.append(
                    [self.minutes_to_time(free_gap_start), self.minutes_to_time(free_gap_start + meeting_duration)])
                free_gap_start += meeting_duration

        return schedule_gaps

    def calculate_free_time_intervals_for_all(self, meeting_duration):
        free_time_intervals = {}

        for key in self.person_data:
            if key.endswith("_Schedule"):
                person_name = key.replace("_Schedule", '')  # Extract the person's name
                intervals = self.calculate_free_time_intervals(person_name, meeting_duration)
                free_time_intervals[key] = intervals

        return free_time_intervals

    def calculate_free_time_intervals_for_all(self, meeting_duration):
        free_time_intervals = {}

        for key in self.person_data:
            if key.endswith("_Schedule"):
                person_name = key.replace("_Schedule", '')  # Extract the person's name
                intervals = self.calculate_free_time_intervals(person_name, meeting_duration)
                free_time_intervals[key] = intervals

        return free_time_intervals

    def find_matching_free_time_intervals_for_all(self, free_time_intervals):
        common_free_time_intervals = None

        for intervals in free_time_intervals.values():
            if common_free_time_intervals is None:
                common_free_time_intervals = intervals
            else:
                common_free_time_intervals = self.find_matching_free_time_intervals(common_free_time_intervals, intervals)

        return common_free_time_intervals

    @staticmethod
    def find_matching_free_time_intervals(intervals1, intervals2):
        matching_time_slots = []

        for schedule1 in intervals1:
            for schedule2 in intervals2:
                start1, end1 = schedule1
                start2, end2 = schedule2

                # Check if the intervals overlap
                if start1 < end2 and start2 < end1:
                    # Calculate the overlapping time slot
                    overlap_start = max(start1, start2)
                    overlap_end = min(end1, end2)
                    matching_time_slots.append([overlap_start, overlap_end])

        return matching_time_slots

    def get_person_data(self):
        return self.person_data
