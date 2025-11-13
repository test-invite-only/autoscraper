"""Public API for the :mod:`autoscraper` package."""

from autoscraper.auto_scraper import AutoScraper


def scrape(
    url=None,
    wanted_list=None,
    *,
    wanted_dict=None,
    html=None,
    request_args=None,
    mode="similar",
    text_fuzz_ratio=1.0,
):
    """Build and run a scraper in a single call.

    This helper keeps the most common workflow simple: provide an example page
    together with the content you care about and immediately get the results
    back.  Under the hood it uses :class:`AutoScraper`, so you can still switch
    to the class-based API later on if you need more control.

    Parameters
    ----------
    url: str, optional
        URL of the page to scrape.  You should provide either ``url`` or
        ``html``.
    wanted_list: list, optional
        A list of sample values you would like to extract.  Either
        ``wanted_list`` or ``wanted_dict`` must be supplied.
    wanted_dict: dict, optional
        Mapping of aliases to sample values.  Useful when you want to fetch
        multiple pieces of information at once and keep their names.
    html: str, optional
        Raw HTML content.  You can pass this instead of ``url``.
    request_args: dict, optional
        Additional parameters forwarded to :func:`requests.get`.
    mode: {"similar", "exact", "both"}, optional
        Controls which results are returned.  ``"similar"`` (default) returns
        the deduplicated list learned during the build step.  ``"exact"``
        preserves ordering and aligns with the behaviour of
        :meth:`AutoScraper.get_result_exact`.  ``"both"`` returns the pair of
        (similar, exact) results from :meth:`AutoScraper.get_result`.
    text_fuzz_ratio: float, optional
        Fuzziness threshold used while learning the rules.  Matches the
        ``text_fuzz_ratio`` parameter on :meth:`AutoScraper.build`.

    Returns
    -------
    list or tuple
        Depending on ``mode`` this will be a list of strings, or a tuple of two
        lists when ``mode`` is ``"both"``.

    Raises
    ------
    ValueError
        If neither ``wanted_list`` nor ``wanted_dict`` are provided, or if an
        unsupported ``mode`` is requested.
    """

    scraper = AutoScraper()
    build_kwargs = dict(
        url=url,
        html=html,
        request_args=request_args,
        update=False,
        text_fuzz_ratio=text_fuzz_ratio,
    )

    if wanted_dict is not None:
        build_kwargs["wanted_dict"] = wanted_dict
    elif wanted_list is not None:
        build_kwargs["wanted_list"] = wanted_list
    else:
        raise ValueError("You must provide wanted_list or wanted_dict.")

    result = scraper.build(**build_kwargs)
    mode = (mode or "similar").lower()

    if mode == "similar":
        return result

    fetch_kwargs = dict(request_args=request_args)
    if html is not None:
        fetch_kwargs["html"] = html
    elif url is not None:
        fetch_kwargs["url"] = url

    if mode == "exact":
        return scraper.get_result_exact(**fetch_kwargs)

    if mode == "both":
        return scraper.get_result(**fetch_kwargs)

    raise ValueError("mode must be 'similar', 'exact', or 'both'.")


__all__ = ["AutoScraper", "scrape"]
