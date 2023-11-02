from data_processor import PersonDataProcessor
import os

def main():
    # Define the input file path
    input_file = 'input.txt'

    # Create an instance of the data_processor.py class
    data_processor = PersonDataProcessor(input_file)

    # Get the processed data
    person_data = data_processor.get_person_data()

    # Call the filter_strays method to filter the schedules for each person
    data_processor.filter_strays()

    # Define your desired meeting duration
    meeting_duration = 30

    # Calculate free time intervals for all persons
    free_time = data_processor.calculate_free_time_intervals_for_all(meeting_duration)

    # Find common free time intervals
    common_free_time_intervals = data_processor.find_matching_free_time_intervals_for_all(free_time)

    # Define the output file path
    output_file = 'output.txt'

    # if common_free_time_intervals:
    #     print("Common Free Time Intervals for All:")
    #     for interval in common_free_time_intervals:
    #         print(f"{interval[0]} to {interval[1]}")
    # else:
    #     print("No common free time intervals found for all.")

    # PRINTS FREE TIME INTERVALS FOR ALL
    # for person_schedule_key, intervals in free_time.items():
    #         person_name = person_schedule_key.replace("_Schedule", '')
    #         print(f"Free Time Intervals for {person_name}:")
    #
    #         for interval in intervals:
    #                 print(f"  - {interval[0]} to {interval[1]}")
    #
    #         print()

    # for interval in free_time:
    #         print(f"{interval[0]} - {interval[1]}")

    # PRINTS FILTERED SCHEDULE
    # for key, value in person_data.items():
    #     if key.endswith('_Schedule'):
    #         person_name = key.replace('_Schedule', '')  # Extract the person's name
    #         print(f"{person_name}'s Filtered Schedule:")
    #         for event in value:
    #             print(f"    {event[0]} - {event[1]}")

    # PRINTS SCHEDULE OF EVERYONE
    # for key, value in person_data.items():
    #     if '_Schedule' in key:
    #         print(f"{key}:", value)
    #     elif '_DailyAct' in key:
    #         print(f"{key}:", value)
    #     elif key == 'min_duration_of_meeting':
    #         print("Minimum Duration of Meeting:", value)

    if common_free_time_intervals:
        # Open the output file in 'w' mode to clear its content
        with open(output_file, 'w') as output:
            output.write("Here Are All The Available Time Slots For A Meeting\n")
            output.write("-----------------------------------------------------\n")

        # Append to the output file
        with open(output_file, 'a') as output:
            #
            for interval in common_free_time_intervals:
                output.write(f"[{interval[0]}, {interval[1]}]\n")
            output.write("\n")  # Add an extra newline between entries
        print("Common Free Time Intervals for All have been written to 'output.txt'.")
    else:
        print("No common free time intervals found for all.")

if __name__ == "__main__":
    main()



