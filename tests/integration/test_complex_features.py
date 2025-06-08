import pytest
import re
from autoscraper import AutoScraper

HTML_COMPLEX = """
<div id="main">
  <ul class="fruits">
    <li class="item"><span class="name">Banana</span><a href="/banana" class="link">More</a></li>
    <li class="item"><span class="name">Apple</span><a href="/apple" class="link">More</a></li>
    <li class="item"><span class="name">Orange</span><a href="/orange" class="link">More</a></li>
    <li class="item"><span class="name">Banana</span></li>
  </ul>
  <p class="info">Fresh fruits</p>
  <a class="external" href="/shop">Shop Now</a>
</div>
"""


def test_extract_relative_link():
    scraper = AutoScraper()
    url = "https://example.com/index.html"
    result = scraper.build(url=url, html=HTML_COMPLEX, wanted_list=["https://example.com/apple"])
    assert "https://example.com/apple" in result
    similar = scraper.get_result_similar(
        url=url, html=HTML_COMPLEX, contain_sibling_leaves=True, unique=True
    )
    assert set(similar) == {
        "https://example.com/banana",
        "https://example.com/apple",
        "https://example.com/orange",
    }
    exact = scraper.get_result_exact(url=url, html=HTML_COMPLEX)
    assert exact == ["https://example.com/apple"]


def test_build_with_regex():
    scraper = AutoScraper()
    scraper.build(html=HTML_COMPLEX, wanted_list=[re.compile("Ban.*")])
    result = scraper.get_result_exact(html=HTML_COMPLEX)
    assert "Banana" in result[0]


def test_update_appends_rules():
    scraper = AutoScraper()
    scraper.build(html=HTML_COMPLEX, wanted_list=["Banana"])
    count = len(scraper.stack_list)
    scraper.build(html=HTML_COMPLEX, wanted_list=["Apple"], update=True)
    assert len(scraper.stack_list) == count + 1


def test_remove_rules():
    scraper = AutoScraper()
    scraper.build(html=HTML_COMPLEX, wanted_list=["Banana"])
    scraper.build(html=HTML_COMPLEX, wanted_list=["Apple"], update=True)
    rule_ids = [s["stack_id"] for s in scraper.stack_list]
    to_remove = rule_ids[0]
    scraper.remove_rules([to_remove])
    remaining = [s["stack_id"] for s in scraper.stack_list]
    assert to_remove not in remaining
    assert len(remaining) == len(rule_ids) - 1


def test_keep_blank_returns_empty():
    scraper = AutoScraper()
    scraper.build(html=HTML_COMPLEX, wanted_list=["/shop"])
    html_blank = HTML_COMPLEX.replace('href="/shop"', 'href=""')
    result = scraper.get_result_exact(html=html_blank, keep_blank=True)
    assert result == [""]


def test_attr_fuzz_ratio():
    html_base = '<div><a class="btn-primary" href="/item">Buy</a></div>'
    html_variant = '<div><a class="btn-prime" href="/item">Buy</a></div>'
    scraper = AutoScraper()
    scraper.build(html=html_base, wanted_list=["Buy"])
    res = scraper.get_result_exact(html=html_variant, attr_fuzz_ratio=0.8)
    assert res == ["Buy"]


COMPLEX_HTML_XPATH = """
<div id="content">
  <section class="products">
    <div class="item featured" data-sku="123">
      <div class="header">
        <h2 class="name">Banana</h2>
        <span class="price">$1</span>
      </div>
      <div class="meta">
        <span class="rating">4.5</span>
        <a href="/banana" class="link">View</a>
      </div>
    </div>
    <div class="item" data-sku="456">
      <div class="header">
        <h2 class="name">Apple</h2>
        <span class="price">$2</span>
      </div>
      <div class="meta">
        <span class="rating">4.2</span>
        <a href="/apple" class="link">View</a>
      </div>
    </div>
  </section>
</div>
"""


def test_get_rule_xpaths_complex_html():
    scraper = AutoScraper()
    scraper.build(html=COMPLEX_HTML_XPATH, wanted_list=["Apple", "$2", "4.2"])
    rule_xpaths = scraper.get_rule_xpaths()
    expected = {
        "/div[1]/section[@class=\"products\"][1]/div[@class=\"item\"][1]/div[@class=\"header\"][1]/h2[@class=\"name\"][1]",
        "/div[1]/section[@class=\"products\"][1]/div[@class=\"item\"][1]/div[@class=\"header\"][1]/span[@class=\"price\"][1]",
        "/div[1]/section[@class=\"products\"][1]/div[@class=\"item\"][1]/div[@class=\"meta\"][1]/span[@class=\"rating\"][1]",
    }
    assert set(rule_xpaths.values()) == expected

