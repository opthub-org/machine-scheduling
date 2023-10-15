import unittest
import json
from itertools import permutations, count, filterfalse
from jsonschema import ValidationError

from problem import load_val_json


class TestLoadValJSON(unittest.TestCase):
    def test_normal_load(self):
        """
        JSON文字列を正常に脱直列化および検証し，入力仕様に適合する場合，設計変数，時間変数それぞれに対応する2値を返す．
        """
        n_work = 4
        max_date = 9
        json_str = '{"schedule": [1, 2, 3, 4], "timeout": 500}'

        schedule_out, time_out = load_val_json(json_str, n_work, max_date)

        self.assertEqual([1, 2, 3, 4], schedule_out)
        self.assertEqual(500, time_out)

    def test_normal_schedule_len(self):
        """
        len(schedule) == n_work
        """
        max_date = 9
        n_works = list(range(1, 31))
        for n in n_works:
            schedule = [5 for _ in range(n)]
            data = dict(schedule=schedule, timeout=500)
            json_str = json.dumps(data)
            with self.subTest(n_work=n):
                try:
                    schedule_out, _ = load_val_json(json_str, n, max_date)
                except ValidationError:
                    self.fail("Unexpected Exception on Validation")

                self.assertEqual(len(schedule_out), n)

    def test_normal_schedule_date_range(self):
        """
        min(schedule) >= 1 and max(schedule) <= max_date
        """
        n_work = 4
        for date in range(1, 20):
            schedule = [date // 2 + 1 for _ in range(n_work)]
            data = dict(schedule=schedule, timeout=500)
            json_str = json.dumps(data)
            with self.subTest(max_date=date):
                try:
                    schedule_out, _ = load_val_json(json_str, n_work, date)
                except ValidationError:
                    self.fail("Unexpected Exception on Validation")

                self.assertGreaterEqual(min(schedule_out), 1)
                self.assertLessEqual(max(schedule_out), date)

    def test_normal_time_range(self):
        """
        5*60 <= timeout <= 8*60*60
        """
        n_work = 4
        max_date = 9
        times = [h * 60 * 60 for h in range(1, 9)]
        times.insert(0, 5 * 60)
        for t in times:
            json_str = '{"schedule": [1, 2, 3, 4], "timeout": %d}' % t
            with self.subTest(timeout=t):
                try:
                    _, timeout_out = load_val_json(json_str, n_work, max_date)
                except ValidationError:
                    self.fail("Unexpected Exception on Validation")

                self.assertGreaterEqual(timeout_out, 5 * 60)
                self.assertLessEqual(timeout_out, 8 * 60 * 60)

    def test_error_must_property(self):
        """
        `schedule`と`timeout`の2プロパティは必須．
        """
        n_work = 4
        max_date = 9
        json_str = '{"timeout": 500}'
        with self.subTest(prop="schedule"), self.assertRaises(ValidationError):
            load_val_json(json_str, n_work, max_date)

        json_str = '{"schedule": [1, 2, 3, 4]}'
        with self.subTest(prop="timeout"), self.assertRaises(ValidationError):
            load_val_json(json_str, n_work, max_date)

    def test_error_extra_property(self):
        """
        `schedule`と`timeout`の2プロパティ以外を許容しない．
        """
        n_work = 4
        max_date = 9
        json_str = '{"schedule": [1, 2, 3, 4], "timeout": 500, "favorite": "ramen"}'
        with self.assertRaises(ValidationError):
            load_val_json(json_str, n_work, max_date)

    def test_error_schedule_type(self):
        """
        scheduleの型はList[int]
        """
        n_work = 4
        max_date = 9

        json_str = '{"schedule": "[1, 2, 3, 4]", "timeout": 500}'
        with self.subTest(type="not array (str)"), self.assertRaises(ValidationError):
            load_val_json(json_str, n_work, max_date)

        json_str = '{"schedule": 1, "timeout": 500}'
        with self.subTest(type="not array (int)"), self.assertRaises(ValidationError):
            load_val_json(json_str, n_work, max_date)

        json_str = '{"schedule": {"work_date1":1,"work_date2":2,"work_date3":3,"work_date4":4}, "timeout": 500}'
        with self.subTest(type="not array (object)"), self.assertRaises(ValidationError):
            load_val_json(json_str, n_work, max_date)

        json_str = '{"schedule": [1.1, 2.1, 3.1, 4.1], "timeout": 500}'
        with self.subTest(type="List[float]"), self.assertRaises(ValidationError):
            load_val_json(json_str, n_work, max_date)

        json_str = '{"schedule": ["1", "2", "3", "4"], "timeout": 500}'
        with self.subTest(type="List[str]"), self.assertRaises(ValidationError):
            load_val_json(json_str, n_work, max_date)

        json_str = '{"schedule": [1, "2", 3.1, 4], "timeout": 500}'
        with self.subTest(type="List[Any]"), self.assertRaises(ValidationError):
            load_val_json(json_str, n_work, max_date)

    def test_error_schedule_len(self):
        """
        len(schedule) == n_work
        """
        max_date = 9
        for n, l in permutations(range(1, 11), 2):
            schedule = [5 for _ in range(l)]
            data = dict(schedule=schedule, timeout=500)
            json_str = json.dumps(data)
            with self.subTest(n_work=n, len=l), self.assertRaises(ValidationError):
                load_val_json(json_str, n, max_date)

    def test_error_schedule_date_range(self):
        """
        min(schedule) >= 1 and max(schedule) <= max_date
        """
        n_work = 4
        for max_date in range(1, 21):
            for date in set(range(max_date + 11)) - set(range(1, max_date + 1)):
                schedule = [date for _ in range(n_work)]
                data = dict(schedule=schedule, timeout=500)
                json_str = json.dumps(data)
                with self.subTest(max_date=max_date, date=date), self.assertRaises(ValidationError):
                    load_val_json(json_str, n_work, max_date)

    def test_error_time_range(self):
        """
        5*60 <= timeout <= 8*60*60
        """
        n_work = 4
        max_date = 9
        times = [1, 5 * 60 - 1, 8 * 60 * 60 + 1, 9 * 60 * 60]
        for t in times:
            json_str = '{"schedule": [1, 2, 3, 4], "timeout": %d}' % t
            with self.subTest(time=t), self.assertRaises(ValidationError):
                load_val_json(json_str, n_work, max_date)

    def test_error_time_type(self):
        """
        時間変数は整数で与えられる．
        """
        json_str = '{"schedule": [1, 2, 3, 4], "timeout": 500.1}'
        with self.subTest(type=float), self.assertRaises(ValidationError):
            load_val_json(json_str, 2)

        json_str = '{"schedule": [1, 2, 3, 4], "timeout": "500"}'
        with self.subTest(type=str), self.assertRaises(ValidationError):
            load_val_json(json_str, 2)

    def test_error_json_decode(self):
        """
        正常なJSON文字列である必要がある．
        """
        n_work = 4
        max_date = 9

        json_str = '{"schedule": 1, 2, 3, 4, "timeout": 500}'
        with self.subTest(type="bracket"), self.assertRaises(json.decoder.JSONDecodeError):
            load_val_json(json_str, n_work, max_date)

        json_str = """{'schedule': [1, 2, 3, 4], 'timeout': 500}"""
        with self.subTest(type="quotation"), self.assertRaises(json.decoder.JSONDecodeError):
            load_val_json(json_str, n_work, max_date)

        json_str = '{"schedule": [1, 2, 3, 4], "timeout": 500,}'
        with self.subTest(type="end-comma"), self.assertRaises(json.decoder.JSONDecodeError):
            load_val_json(json_str, n_work, max_date)


if __name__ == '__main__':
    unittest.main()
