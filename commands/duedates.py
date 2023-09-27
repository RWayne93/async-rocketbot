import json
from datetime import datetime, timedelta
from commands.base import CommandHandler

class CohortDueDates(CommandHandler):
    async def assignment_due_dates(self, message, match_list=None):
        file_path = 'data/cloudAdminSchedule.json'
        with open(file_path, 'r') as f:
            data = json.load(f)

        current_date = datetime.now().date()
        week_end_date = current_date + timedelta(days=7)
        items_due_this_week = []

        for unit in data['Course']['units']:
            if 'modules' in unit:
                for module in unit['modules']:
                    if module['moduleType'] in ['PROJECT', 'FORUM', 'QUIZ']:
                        try:
                            item_end_date = datetime.strptime(module['endDate'], '%Y-%m-%dT%H:%M:%S').date()
                        except ValueError:
                            item_end_date = datetime.strptime(module['endDate'], '%Y-%m-%dT%H:%M').date()
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
        await self.bot.send_message(message['rid'], response)
