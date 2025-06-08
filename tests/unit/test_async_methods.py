import asyncio

from autoscraper import AutoScraper, AsyncAutoScraper

HTML = "<ul><li>Banana</li><li>Apple</li><li>Orange</li></ul>"


def test_async_methods_match_sync():
    sync_scraper = AutoScraper()
    expected_build = sync_scraper.build(html=HTML, wanted_list=["Banana"])
    expected_similar = sync_scraper.get_result_similar(html=HTML, contain_sibling_leaves=True)
    expected_exact = sync_scraper.get_result_exact(html=HTML)
    expected_pair = sync_scraper.get_result(html=HTML)

    async def run():
        scraper = AsyncAutoScraper()
        build_res = await scraper.build(html=HTML, wanted_list=["Banana"])
        assert build_res == expected_build
        similar = await scraper.get_result_similar(html=HTML, contain_sibling_leaves=True)
        assert similar == expected_similar
        exact = await scraper.get_result_exact(html=HTML)
        assert exact == expected_exact
        pair = await scraper.get_result(html=HTML)
        assert pair == expected_pair

    asyncio.run(run())
