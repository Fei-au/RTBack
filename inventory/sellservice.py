import pandas as pd
from utils.file import create_unique_filename
import zipfile
import os
import dotenv
from utils.file import get_export_dir
from utils.dt import get_date_prefix

dotenv.load_dotenv()

MEDIA_DOMAIN = os.getenv('MEDIA_DOMAIN')

def exportAuctionSummary(f):
    df = pd.read_csv(f)
    sum_df = df.loc[:, ['invnum', 'sequence', 'fullname', 'city', 'countryname', 'phone']]
    group_df = sum_df.groupby('invnum', as_index=False).last()
    zip_extension = '.csv'
    filename = 'summary'
    full_path = create_unique_filename(get_export_dir(), filename, zip_extension)
    print('full_path', full_path)
    group_df.to_csv(full_path, index=False)
    return full_path

def create_zip(f_list):
    zip_extension = '.zip'
    filename = 'Auction_Summary'
    export_dir = get_export_dir()
    full_path = create_unique_filename(export_dir, filename, zip_extension)
    with zipfile.ZipFile(full_path, 'w') as img_zip:
        for x in f_list:
            p = os.path.basename(x)
            img_zip.write(x, arcname=p)
    http_path = f'http://{MEDIA_DOMAIN}/export/{get_date_prefix()}/{filename}{zip_extension}'
    return http_path



