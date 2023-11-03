from answer_rocket import AnswerRocketClient, AnswerRocketClientError


def test_client_init():
    # this test is mostly here as a pointless placeholder just to have something that runs a bit of our code
    # in the test step of the build while we flesh out real tests. no reason to keep it once those exist.
    try:
        arc = AnswerRocketClient()
        assert False
    except AnswerRocketClientError:
        # init should fail with no url
        assert True
