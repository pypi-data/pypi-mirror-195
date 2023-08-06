from injection import postcondition, precondition
from ossapi import Ossapi

class TestOssapi(Ossapi):
    @postcondition
    def beatmap_scores(bmscores):
        for score in bmscores.scores:
            assert score._user is not None
            assert score._user.country is not None
            assert score._user.cover is not None

    @precondition
    def beatmap_scores(bmscores):
        pass


@given(Replay)
def replay_beatmap_id(r):
    assert r.map_id == r.map_info.beatmap_id
