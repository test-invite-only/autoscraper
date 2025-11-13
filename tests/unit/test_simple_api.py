from autoscraper import scrape


HTML = "<ul><li>Banana</li><li>Apple</li><li>Orange</li></ul>"
HTML_COMPLEX_ORDER = """
<div class='products'>
  <h2>Banana</h2>
  <p class='price'>$1</p>
  <h2>Apple</h2>
  <p class='price'>$2</p>
</div>
"""


def test_scrape_similar():
    assert scrape(html=HTML, wanted_list=["Banana"]) == ["Banana"]


def test_scrape_exact():
    assert scrape(
        html=HTML_COMPLEX_ORDER,
        wanted_list=["Banana", "$2"],
        mode="exact",
    ) == ["Banana", "$2"]


def test_scrape_both():
    similar, exact = scrape(html=HTML, wanted_list=["Banana"], mode="both")
    assert similar == ["Banana"]
    assert exact == ["Banana"]
