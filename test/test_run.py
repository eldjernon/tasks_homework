
from tasks.tasks import run_task, task, BaseTask
from functools import reduce


TEST_FUNC_NAME = '__test_func'
TEST_CLASS_NAME = '__test_class'


@task(name=TEST_FUNC_NAME)
def multi_print(msg, count=10):
    return '\n'.join(msg for _ in range(count))


class Multiply(BaseTask):
    name = TEST_CLASS_NAME

    @staticmethod
    def run(operands):
        return reduce(lambda x, y: x*y, operands)


def test_run_decorated_func():
    assert run_task(TEST_FUNC_NAME, {"msg": "hello", "count": 2}) == 'hello\nhello', "Bad answer!"


def test_run_task_class():
    assert run_task(TEST_CLASS_NAME, {"operands": [3, 2, 8]}) == 48, "Bad answer!"
