import json
from datetime import datetime, timedelta
from commands.base import CommandHandler
import csv

file_paths = [
    "data/cloudAdminSchedule.json",
    "data/devops_schedule.json",
    "data/python_scedule.json"
]

class CohortDueDates(CommandHandler):
    async def assignment_due_dates(self, message, file_path, match_list=None):
        with open(file_path, 'r') as f:
            data = json.load(f)

        current_date = datetime.now().date()
        week_end_date = current_date + timedelta(days=7)
        items_due_this_week = []

        for unit in data['Course']['units']:
            if 'modules' in unit:
                for module in unit['modules']:
                    if module['moduleType'] in ['PROJECT', 'FORUM', 'QUIZ']:
                        # First, try the 'T' separated date-time format
                        try:
                            item_end_date = datetime.strptime(module['endDate'], '%Y-%m-%dT%H:%M:%S').date()
                        except ValueError:
                            try:
                                item_end_date = datetime.strptime(module['endDate'], '%Y-%m-%dT%H:%M').date()
                            except ValueError:
                                # If the above fails, try the AM/PM date-time format
                                try:
                                    item_end_date = datetime.strptime(module['endDate'], '%m/%d/%Y %I:%M %p').date()
                                except ValueError:
                                    # If all the above fail, skip items with empty or unrecognized date formats
                                    continue
                        
                        if current_date <= item_end_date <= week_end_date:
                            item_info = f"Item Type: {module['moduleType']}\n"
                            item_info += f"Item Name: {module['name']}\n"
                            item_info += f"Start Date: {module['startDate']}\n"
                            item_info += f"End Date: {module['endDate']}\n"
                            item_info += "-----------------------------\n"
                            items_due_this_week.append((item_end_date, item_info))

        items_due_this_week.sort(key=lambda x: x[0])
        sorted_items_info = [item[1] for item in items_due_this_week]
        response = "\n".join(sorted_items_info)
        
        return response

    async def handle_multiple_files(self, message, match_list=None):
        all_due_dates = []
        
        for file_path in file_paths:
            due_dates_for_file = await self.assignment_due_dates(message, file_path, match_list)
            if due_dates_for_file:  # Only append if there are due dates for this file
                all_due_dates.append(due_dates_for_file)
        
        combined_due_dates = "\n\n".join(all_due_dates)
        await self.bot.send_message(message['rid'], combined_due_dates)

    async def class_schedule(self, message, match_list=None):
        csv_file_path = "data/class_schedule.csv"
        with open(csv_file_path, 'r') as f:
            reader = csv.DictReader(f)
            class_data = [row for row in reader]

        current_date = datetime.now().date()
        current_day = current_date.strftime('%A')  # Get the current day name (e.g., "Tuesday")

        # Filter for class dates that fall within this week or match the current day
        relevant_classes = []
        for row in class_data:
            class_date_str = f"{row['Date']} {current_date.year}"  # Append the current year
            class_date = datetime.strptime(class_date_str, '%b %d %Y').date()
            
            if current_day in ["Tuesday", "Thursday", "Friday"] and class_date == current_date:
                relevant_classes.append(row)
            # If any class falls within this week
            elif current_date <= class_date <= current_date + timedelta(days=7):
                relevant_classes.append(row)

        if not relevant_classes:
            response = "No classes scheduled for today or this week."
        else:
            class_messages = []
            for row in relevant_classes:
                class_messages.append(f"Day: {row['Day']}\nDate: {row['Date']}\nRoom: {row['Room']}\n-----------------------------")
            response = "\n".join(class_messages)

        await self.bot.send_message(message['rid'], response)