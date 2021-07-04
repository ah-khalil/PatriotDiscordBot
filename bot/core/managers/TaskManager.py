from bot.core.PatriotTask import PatriotTask


class TaskManager:
    def __init__(self):
        self.task_list = []

    def add_task(self, func, interval, **kwargs):
        target_name = kwargs.get('name', func.__name__)

        if hasattr(self.task_list, target_name):
            raise AttributeError(f"\'{target_name}\' is already registered as a task")

        pt_task = PatriotTask(name=target_name, target=func, interval=interval, **kwargs)

        if pt_task is not None:
            self.task_list[target_name] = pt_task

    def run_tasks(self):
        try:
            for target_name in self.task_list:
                self.__run_task(target_name)
        except Exception as e:
            raise Exception("An error occurred trying to run all tasks" + e.__str__())

    def __run_task(self, target_name):
        try:
            if target_name in self.task_list:
                if not self.task_list[target_name].is_running():
                    self.task_list[target_name].run()
        except Exception as e:
            raise Exception("An error occurred trying to run task" + target_name + e.__str__())
