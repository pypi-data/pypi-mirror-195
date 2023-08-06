from ngoto.core.clt import CLT


def test_task_dup_id():
    """
        Check there are no duplicate task ids
    """
    ngotoCLT = CLT()
    # get list of all actions
    tasks = []
    for task in ngotoCLT.tasks.tasks:
        tasks.append(task.id)
    # check for duplicates
    if len(tasks) == len(set(tasks)):
        assert True
    else:
        duplicates = []
        for task in tasks:
            if tasks.count(task) > 1:
                duplicates.append(task)
        print('Duplicate tasks found: ' + str(duplicates))
        assert False
