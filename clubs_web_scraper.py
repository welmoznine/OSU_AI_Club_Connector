import requests
from bs4 import BeautifulSoup
import re
import csv

# Ideal-Logic URLs
urls = [
    # Page 1
    "https://apps.ideal-logic.com/worker/execute?embed_start=1&e=WGYG-S6DT4&o=9N97-T52XV&id=embed_go_a2944c5f31baaa0f_e913b746&c=&account=a2944c5f31baaa0f&a=W899-6T3Y4&type=full&uid=TQHS1T6K3YZTDG5SW3X1&embed_full=1&source_url=https%3A%2F%2Fclubs.oregonstate.edu%2Ffindclubs&json=1&v=&s_app=&s_org=&s_account=&target_id=&original_url=&page_mode=&window_id=&events=&sw=0&ui=tablet&w=1092&h=1205&recent_workers=&reqid=QBXF3T34PK54D44GR519GZ7C",
    # Page 2
    "https://apps.ideal-logic.com/worker/execute?e=WGYG-S6DT4&o=9N97-T52XV&id=embed_go_a2944c5f31baaa0f_e913b746&c=&account=a2944c5f31baaa0f&a=W899-6T3Y4&type=full&uid=21DWT-9169_TQHS1T6K3YZTDG5SW3X1&embed_full=1&source_url=https%3A%2F%2Fclubs.oregonstate.edu%2Ffindclubs&json=1&v=&s_app=253KJ-6K95&s_org=F3T9-25VWY&s_account=9N97-T52XV&target_id=r_21dcd444&original_url=&page_mode=&window_id=&events=&sw=0&performance=0.00s%20queue%2C%200.49s%20server%2C%200.20s%20network%2C%200.08s%20render%2C%200.77s%20total&s=21DWT-9169_TQHS1T6K3YZTDG5SW3X1&page=pf6ca3114&go=aa29a8b49d9a4&ui=tablet&w=1092&h=1205&recent_workers=serenity1.worker_clone.1396417&reqid=54YCCW9TK519HVWKM7JPFJ17",
    # Page 3
    "https://apps.ideal-logic.com/worker/execute?e=WGYG-S6DT4&o=9N97-T52XV&id=embed_go_a2944c5f31baaa0f_e913b746&c=&account=a2944c5f31baaa0f&a=W899-6T3Y4&type=full&uid=21DWT-9169_TQHS1T6K3YZTDG5SW3X1&embed_full=1&source_url=https%3A%2F%2Fclubs.oregonstate.edu%2Ffindclubs&json=1&v=&s_app=253KJ-6K95&s_org=F3T9-25VWY&s_account=9N97-T52XV&target_id=r_b6c726e9&original_url=&page_mode=&window_id=&events=&sw=0&performance=0.00s%20queue%2C%200.51s%20server%2C%200.30s%20network%2C%200.10s%20render%2C%200.91s%20total&s=21DWT-9169_TQHS1T6K3YZTDG5SW3X1&page=p03b90184&go=ae75c4d44b0b3&ui=tablet&w=1092&h=1205&recent_workers=serenity1.worker_clone.1396417&reqid=G9KT9YRPTXNPXYXSSHGKB5S5",
    # Page 4
    "https://apps.ideal-logic.com/worker/execute?e=WGYG-S6DT4&o=9N97-T52XV&id=embed_go_a2944c5f31baaa0f_e913b746&c=&account=a2944c5f31baaa0f&a=W899-6T3Y4&type=full&uid=21DWT-9169_TQHS1T6K3YZTDG5SW3X1&embed_full=1&source_url=https%3A%2F%2Fclubs.oregonstate.edu%2Ffindclubs&json=1&v=&s_app=253KJ-6K95&s_org=F3T9-25VWY&s_account=9N97-T52XV&target_id=r_05afdf9c&original_url=&page_mode=&window_id=&events=&sw=0&performance=0.00s%20queue%2C%200.52s%20server%2C%200.16s%20network%2C%200.10s%20render%2C%200.78s%20total&s=21DWT-9169_TQHS1T6K3YZTDG5SW3X1&page=p45b43f06&go=a3bb169d47c13&ui=tablet&w=1092&h=1205&recent_workers=serenity1.worker_clone.1396417&reqid=VWSVPCJDGN5F9JF6CBQNWWY7",
    # Page 5
    "https://apps.ideal-logic.com/worker/execute?e=WGYG-S6DT4&o=9N97-T52XV&id=embed_go_a2944c5f31baaa0f_e913b746&c=&account=a2944c5f31baaa0f&a=W899-6T3Y4&type=full&uid=21DWT-9169_TQHS1T6K3YZTDG5SW3X1&embed_full=1&source_url=https%3A%2F%2Fclubs.oregonstate.edu%2Ffindclubs&json=1&v=&s_app=253KJ-6K95&s_org=F3T9-25VWY&s_account=9N97-T52XV&target_id=r_3bba3ecf&original_url=&page_mode=&window_id=&events=&sw=0&performance=0.00s%20queue%2C%200.51s%20server%2C%200.17s%20network%2C%200.10s%20render%2C%200.78s%20total&s=21DWT-9169_TQHS1T6K3YZTDG5SW3X1&page=pcec92200&go=aefd698ce5567&ui=tablet&w=1092&h=1205&recent_workers=serenity1.worker_clone.1396417&reqid=F7XCVK41Q7SYZKZM5R92JYR5",
    # Page 6
    "https://apps.ideal-logic.com/worker/execute?e=WGYG-S6DT4&o=9N97-T52XV&id=embed_go_a2944c5f31baaa0f_e913b746&c=&account=a2944c5f31baaa0f&a=W899-6T3Y4&type=full&uid=21DWT-9169_TQHS1T6K3YZTDG5SW3X1&embed_full=1&source_url=https%3A%2F%2Fclubs.oregonstate.edu%2Ffindclubs&json=1&v=&s_app=253KJ-6K95&s_org=F3T9-25VWY&s_account=9N97-T52XV&target_id=r_eee6e07b&original_url=&page_mode=&window_id=&events=&sw=0&performance=0.00s%20queue%2C%200.52s%20server%2C%200.16s%20network%2C%200.07s%20render%2C%200.75s%20total&s=21DWT-9169_TQHS1T6K3YZTDG5SW3X1&page=p3601d9dd&go=adc67666a915d&ui=tablet&w=1092&h=1205&recent_workers=serenity1.worker_clone.1396417&reqid=SJ3HTR9N2QSJSY24GHV141SX",
    # Page 7
    "https://apps.ideal-logic.com/worker/execute?e=WGYG-S6DT4&o=9N97-T52XV&id=embed_go_a2944c5f31baaa0f_e913b746&c=&account=a2944c5f31baaa0f&a=W899-6T3Y4&type=full&uid=21DWT-9169_TQHS1T6K3YZTDG5SW3X1&embed_full=1&source_url=https%3A%2F%2Fclubs.oregonstate.edu%2Ffindclubs&json=1&v=&s_app=253KJ-6K95&s_org=F3T9-25VWY&s_account=9N97-T52XV&target_id=r_e85817e2&original_url=&page_mode=&window_id=&events=&sw=0&performance=0.00s%20queue%2C%200.52s%20server%2C%200.10s%20network%2C%200.08s%20render%2C%200.70s%20total&s=21DWT-9169_TQHS1T6K3YZTDG5SW3X1&page=p8968299d&go=aae5ab91f74bf&ui=tablet&w=1092&h=1205&recent_workers=serenity1.worker_clone.1396417&reqid=4H31T34STCPJL1MDW1XNCYNB",
    # Page 8
    "https://apps.ideal-logic.com/worker/execute?e=WGYG-S6DT4&o=9N97-T52XV&id=embed_go_a2944c5f31baaa0f_e913b746&c=&account=a2944c5f31baaa0f&a=W899-6T3Y4&type=full&uid=21DWT-9169_TQHS1T6K3YZTDG5SW3X1&embed_full=1&source_url=https%3A%2F%2Fclubs.oregonstate.edu%2Ffindclubs&json=1&v=&s_app=253KJ-6K95&s_org=F3T9-25VWY&s_account=9N97-T52XV&target_id=r_e9631458&original_url=&page_mode=&window_id=&events=&sw=0&performance=0.00s%20queue%2C%200.54s%20server%2C%200.13s%20network%2C%200.10s%20render%2C%200.77s%20total&s=21DWT-9169_TQHS1T6K3YZTDG5SW3X1&page=pf19b0b7a&go=a74fe2823dceb&ui=tablet&w=1092&h=1205&recent_workers=serenity1.worker_clone.1396417&reqid=LKVMYGDRFGT8J2F5C9QPS3C6",
    # Page 9
    "https://apps.ideal-logic.com/worker/execute?e=WGYG-S6DT4&o=9N97-T52XV&id=embed_go_a2944c5f31baaa0f_e913b746&c=&account=a2944c5f31baaa0f&a=W899-6T3Y4&type=full&uid=21DWT-9169_TQHS1T6K3YZTDG5SW3X1&embed_full=1&source_url=https%3A%2F%2Fclubs.oregonstate.edu%2Ffindclubs&json=1&v=&s_app=253KJ-6K95&s_org=F3T9-25VWY&s_account=9N97-T52XV&target_id=r_670baeaf&original_url=&page_mode=&window_id=&events=&sw=0&performance=0.00s%20queue%2C%200.55s%20server%2C%200.15s%20network%2C%200.09s%20render%2C%200.78s%20total&s=21DWT-9169_TQHS1T6K3YZTDG5SW3X1&page=pcc9e91e2&go=a27519c514622&ui=tablet&w=1092&h=1205&recent_workers=serenity1.worker_clone.1396417&reqid=85LGP47N39MVPKG6ZHB1D1LS",
    # Page 10
    "https://apps.ideal-logic.com/worker/execute?e=WGYG-S6DT4&o=9N97-T52XV&id=embed_go_a2944c5f31baaa0f_e913b746&c=&account=a2944c5f31baaa0f&a=W899-6T3Y4&type=full&uid=21DWT-9169_TQHS1T6K3YZTDG5SW3X1&embed_full=1&source_url=https%3A%2F%2Fclubs.oregonstate.edu%2Ffindclubs&json=1&v=&s_app=253KJ-6K95&s_org=F3T9-25VWY&s_account=9N97-T52XV&target_id=r_ac061cd7&original_url=&page_mode=&window_id=&events=&sw=0&performance=0.00s%20queue%2C%200.51s%20server%2C%200.14s%20network%2C%200.10s%20render%2C%200.75s%20total&s=21DWT-9169_TQHS1T6K3YZTDG5SW3X1&page=p12bf9d14&go=ae582561cea25&ui=tablet&w=1092&h=1205&recent_workers=serenity1.worker_clone.1396417&reqid=9L72BK1NCCYG2Z521G8LMFCF",
    # Page 11
    "https://apps.ideal-logic.com/worker/execute?e=WGYG-S6DT4&o=9N97-T52XV&id=embed_go_a2944c5f31baaa0f_e913b746&c=&account=a2944c5f31baaa0f&a=W899-6T3Y4&type=full&uid=21DWT-9169_TQHS1T6K3YZTDG5SW3X1&embed_full=1&source_url=https%3A%2F%2Fclubs.oregonstate.edu%2Ffindclubs&json=1&v=&s_app=253KJ-6K95&s_org=F3T9-25VWY&s_account=9N97-T52XV&target_id=r_82b10f5a&original_url=&page_mode=&window_id=&events=&sw=0&performance=0.00s%20queue%2C%200.53s%20server%2C%200.14s%20network%2C%200.10s%20render%2C%200.78s%20total&s=21DWT-9169_TQHS1T6K3YZTDG5SW3X1&page=p03c3b723&go=a7ff63f004943&ui=tablet&w=1092&h=1205&recent_workers=serenity1.worker_clone.1396417&reqid=WKCGL954RDJJK58RXHK97CPQ",
    # Page 12
    "https://apps.ideal-logic.com/worker/execute?e=WGYG-S6DT4&o=9N97-T52XV&id=embed_go_a2944c5f31baaa0f_e913b746&c=&account=a2944c5f31baaa0f&a=W899-6T3Y4&type=full&uid=21DWT-9169_TQHS1T6K3YZTDG5SW3X1&embed_full=1&source_url=https%3A%2F%2Fclubs.oregonstate.edu%2Ffindclubs&json=1&v=&s_app=253KJ-6K95&s_org=F3T9-25VWY&s_account=9N97-T52XV&target_id=r_b09fb6fa&original_url=&page_mode=&window_id=&events=&sw=0&performance=0.00s%20queue%2C%200.51s%20server%2C%200.17s%20network%2C%200.10s%20render%2C%200.77s%20total&s=21DWT-9169_TQHS1T6K3YZTDG5SW3X1&page=pa195c57a&go=af2455bc910ed&ui=tablet&w=1092&h=1205&recent_workers=serenity1.worker_clone.1396417&reqid=B13LTJ381PH8V2MB1B9DL7ZW",
    # Page 13
    "https://apps.ideal-logic.com/worker/execute?e=WGYG-S6DT4&o=9N97-T52XV&id=embed_go_a2944c5f31baaa0f_e913b746&c=&account=a2944c5f31baaa0f&a=W899-6T3Y4&type=full&uid=21DWT-9169_TQHS1T6K3YZTDG5SW3X1&embed_full=1&source_url=https%3A%2F%2Fclubs.oregonstate.edu%2Ffindclubs&json=1&v=&s_app=253KJ-6K95&s_org=F3T9-25VWY&s_account=9N97-T52XV&target_id=r_e454f092&original_url=&page_mode=&window_id=&events=&sw=0&performance=0.00s%20queue%2C%200.52s%20server%2C%200.16s%20network%2C%200.10s%20render%2C%200.78s%20total&s=21DWT-9169_TQHS1T6K3YZTDG5SW3X1&page=p7c39b1dc&go=a7ea5335c60d3&ui=tablet&w=1092&h=1205&recent_workers=serenity1.worker_clone.1396417&reqid=3YNXWZNPXF71WSTW83NSX7JR",
    # Page 14
    "https://apps.ideal-logic.com/worker/execute?e=WGYG-S6DT4&o=9N97-T52XV&id=embed_go_a2944c5f31baaa0f_e913b746&c=&account=a2944c5f31baaa0f&a=W899-6T3Y4&type=full&uid=21DWT-9169_TQHS1T6K3YZTDG5SW3X1&embed_full=1&source_url=https%3A%2F%2Fclubs.oregonstate.edu%2Ffindclubs&json=1&v=&s_app=253KJ-6K95&s_org=F3T9-25VWY&s_account=9N97-T52XV&target_id=r_28ffa6e2&original_url=&page_mode=&window_id=&events=&sw=0&performance=0.00s%20queue%2C%200.49s%20server%2C%200.13s%20network%2C%200.07s%20render%2C%200.69s%20total&s=21DWT-9169_TQHS1T6K3YZTDG5SW3X1&page=p6d40cd33&go=a175050f2d368&ui=tablet&w=1092&h=1205&recent_workers=serenity1.worker_clone.1396417&reqid=4TBJCVFNVC7G689T899DSNB2",
    # Page 15
    "https://apps.ideal-logic.com/worker/execute?e=WGYG-S6DT4&o=9N97-T52XV&id=embed_go_a2944c5f31baaa0f_e913b746&c=&account=a2944c5f31baaa0f&a=W899-6T3Y4&type=full&uid=21DWT-9169_TQHS1T6K3YZTDG5SW3X1&embed_full=1&source_url=https%3A%2F%2Fclubs.oregonstate.edu%2Ffindclubs&json=1&v=&s_app=253KJ-6K95&s_org=F3T9-25VWY&s_account=9N97-T52XV&target_id=r_022f9062&original_url=&page_mode=&window_id=&events=&sw=0&performance=0.00s%20queue%2C%200.51s%20server%2C%200.10s%20network%2C%200.10s%20render%2C%200.72s%20total&s=21DWT-9169_TQHS1T6K3YZTDG5SW3X1&page=pe7b5f899&go=a8ecae93a0731&ui=tablet&w=1092&h=1205&recent_workers=serenity1.worker_clone.1396417&reqid=YJC7DB4XKR43ZNGJS1FG5NCT",
]

# Headers for the HTTP requests
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Origin': 'https://clubs.oregonstate.edu',
    'Referer': 'https://clubs.oregonstate.edu/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
}

# Initialize a list to hold the information about the clubs
clubs = []

# Iterate through the list of URLs
for url in urls:
    # Make a POST request to each URL with the specified headers
    response = requests.post(url, headers=headers)

    # Store the JSON data
    data = response.json()

    # Extract the HTML content related to OSU clubs & organizations
    club_info_html = data['sections'][0]['content']

    # Parse the HTML content with BeautifulSoup to navigate and search the document tree
    soup = BeautifulSoup(club_info_html, 'html.parser')

    # Iterate over each club entry found in the parsed HTML
    for club_tag in soup.find_all('span', class_='link L', style='font-weight:bold;'):
        # Get the club name
        club_name = club_tag.text.strip()

        # Get the description
        description = club_tag.find_next('div', class_='S').text.strip()

        # Get the sponsor
        sponsor_tag = club_tag.find_next('i')
        sponsor = sponsor_tag.text.strip() if sponsor_tag else 'N/A'

        # Get the email
        email_tag = club_tag.find_next('a', href=re.compile(r'mailto:'))
        email = email_tag['href'].replace('mailto:', '') if email_tag else 'N/A'

        # Get the recognition year
        recognition_tag = club_tag.find_next('b')
        recognition_year = recognition_tag.text.strip() if recognition_tag else 'N/A'

        # Append the collected club data to the 'clubs' array
        clubs.append({
            'name': club_name,
            'description': description,
            'sponsor': sponsor,
            'email': email,
            'recognition_year': recognition_year
        })

# Define the file name for the output CSV
csv_filename = 'osu_clubs_data.csv'

# Open the CSV file and write the aggregated club details
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    # Define the CSV column headers
    fieldnames = ['club name', 'club description', 'club sponsor', 'club email', 'club recognition_year']

    # Initialize a CSV writer object with the specified fieldnames
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    # Write the column headers to the CSV file
    writer.writeheader()

    # Iterate through the clubs array and write each club's details as a row in the CSV file
    for club in clubs:
        writer.writerow(club)

# Print a message indicating that the CSV file has been successfully created
print(f'The CSV file "{csv_filename}" has successfully been created.')

