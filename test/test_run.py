from tasks import task, BaseTask
from tasks import run_task
from functools import reduce

TEST_FUNC_NAME = '__test_func'
TEST_FUNC_SCHEMA = {'type': 'object',
                    'properties': {
                        'msg': {'type': 'string'},
                        'count': {'type': 'integer', 'minimum': 1}
                    },
                    'required': ['msg']}
TEST_CLASS_NAME = '__test_class'
TEST_CLASS_SCHEMA = {'type': 'object',
                     'properties': {
                         'operands': {'type': 'array',
                                      'minItems': 1,
                                      'items': {'type': 'number'}}
                     },
                     'required': ['operands']}


@task(name=TEST_FUNC_NAME, json_schema=TEST_FUNC_SCHEMA)
def multi_print(msg, count=10):
    return '\n'.join(msg for _ in range(count))


class Multiply(BaseTask):
    name = TEST_CLASS_NAME
    json_schema = TEST_CLASS_SCHEMA

    @staticmethod
    def run(operands):
        return reduce(lambda x, y: x * y, operands)


def test_run_decorated_func():
    assert run_task(TEST_FUNC_NAME, {"msg": "hello", "count": 2}) == 'hello\nhello', "Bad answer!"


def test_run_task_class():
    assert run_task(TEST_CLASS_NAME, {"operands": [3, 2, 8]}) == 48, "Bad answer!"
