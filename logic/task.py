from tasks.task_dict import tasks, task_types


async def get_all_points() -> int:
    print("def get_all_points")
    point_counter = 0
    for task in tasks:
        point_counter += tasks[task]["points"]
    return point_counter


async def get_num_of_tasks() -> int:
    print("def get_num_of_tasks")
    return len(tasks)
