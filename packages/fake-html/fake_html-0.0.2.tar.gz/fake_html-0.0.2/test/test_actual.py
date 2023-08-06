import pytest

from fake_html import fake_html
from fake_html.markov import HTMLMarkov


@pytest.mark.unittest
class TestActualUse:
    @pytest.mark.parametrize(['seed'], [(i,) for i in range(10, 31, 10)])
    def test_actual_use(self, default_model: HTMLMarkov, seed):
        h1 = default_model.fake_html(seed=seed)
        h2 = default_model.fake_html(seed=seed)
        assert h1 == h2

    @pytest.mark.parametrize(['seed'], [(i,) for i in range(10, 31, 10)])
    def test_fake_html(self, seed):
        assert fake_html(seed=seed) == fake_html(seed=seed)
