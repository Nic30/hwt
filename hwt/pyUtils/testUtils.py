from itertools import product


class TestMatrix():
    """
    Class which instance is a decorator which executes unittest.TestCase
    test method with every combination of argumets
    """

    def __init__(self, *args, **kwargs):
        """
        :note: args, kwargs are lists of arguments which should be passed as a test
            arguments
        """
        self.args = args
        kwargs = sorted(kwargs.items(), key=lambda x: x[0])
        self.kwargs_keys = [x[0] for x in kwargs]
        self.kwargs_values = [x[1] for x in kwargs]
        self.test_arg_values = list(product(*args, *self.kwargs_values))

    def split_args_kwargs(self, args):
        kwargs_cnt = len(self.kwargs_keys)
        if kwargs_cnt:
            _args = args[:kwargs_cnt]
            kwargs = {k: v for k, v in zip(
                self.kwargs_keys, args[:kwargs_cnt])}
            return _args, kwargs
        else:
            return args, {}

    def __call__(self, test_fn):
        test_matrix = self

        def test_wrap(self):
            for args in test_matrix.test_arg_values:
                args, kwargs = test_matrix.split_args_kwargs(args)
                try:
                    test_fn(self, *args, **kwargs)
                except Exception as e:
                    # add note to an exception about which test arguments were
                    # used
                    # import traceback
                    # traceback.print_exc()
                    msg_buff = []
                    for a in args:
                        msg_buff.append("%r" % (a,))
                    for k in test_matrix.kwargs_keys:
                        msg_buff.append("%s=%r" % (k, kwargs[k]))
                    raise Exception(
                        "Test failed %s" % (", ".join(msg_buff)), ) from e
        return test_wrap
