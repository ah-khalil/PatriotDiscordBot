from pprint import PrettyPrinter
from bot.core.PatriotBot import patriot_bot
from bot.core.config import Config
from bot.core.managers.TaskManager import TaskManager


@patriot_bot.event
async def on_ready():
    print(f"Logged in as {patriot_bot.user.name}")
    print("=========================================================")

if __name__ == "__main__":
    pp: PrettyPrinter = PrettyPrinter()
    task_m: TaskManager = TaskManager()
    patriot_bot.load_extensions()
    task_m.run_tasks()
    patriot_bot.run(Config.CoreConfig.get_token())
