from prefect import flow

from housing.task.tiger.download_coastlines import download_coastlines


@flow(name='Download TIGER source files', persist_result=True)
def download_tiger(tiger_year: int = 2023):
    tiger_ftp_block_id = f'tiger-ftp-{tiger_year}'
    tiger_local_block_id = f'tiger-local-{tiger_year}'

    download_coastlines(tiger_year, tiger_ftp_block_id, tiger_local_block_id)
