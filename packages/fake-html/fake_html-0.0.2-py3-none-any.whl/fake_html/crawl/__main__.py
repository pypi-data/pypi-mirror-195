import os.path
from functools import partial
from typing import Tuple, List

import click

from ..dataset import DATASET_DIR
from ..utils import GLOBAL_CONTEXT_SETTINGS, get_page_html
from ..utils import print_version as _origin_print_version
from ..utils.selenium import _need_install

print_version = partial(_origin_print_version, 'fake_html.crawl')


@click.group(context_settings={**GLOBAL_CONTEXT_SETTINGS},
             help='Crawl html code as dataset.')
@click.option('-v', '--version', is_flag=True,
              callback=print_version, expose_value=False, is_eager=True,
              help="Show version information.")
def cli():
    pass  # pragma: no cover


@cli.command('download', help='Crawl html code as dataset.',
             context_settings={**GLOBAL_CONTEXT_SETTINGS})
@click.option('--url', '-u', 'urls', type=(str, str), multiple=True,
              help='Urls to download.')
@click.option('--output_dir', '-O', 'output_dir', type=click.Path(file_okay=False), default=DATASET_DIR,
              help='Output path of dataset.', show_default=True)
@click.option('--no_render', 'no_render', type=bool, is_flag=True, default=False,
              help='No not render page in selenium, just get original page source.')
def download(urls: List[Tuple[str, str]], output_dir: str, no_render):
    try:
        from tqdm.auto import tqdm
    except ImportError:
        _need_install('tqdm')
        return

    os.makedirs(output_dir, exist_ok=True)
    urls_tqdm = tqdm(urls)
    for name, url in urls_tqdm:
        urls_tqdm.set_description(name)
        source = get_page_html(url, render=not no_render)
        with open(os.path.join(output_dir, f'{name}.html'), 'w') as f:
            print(source, file=f)


if __name__ == '__main__':
    cli()
