# AirBnB Price Extractor

![Logo of the Project](https://cdn.pixabay.com/photo/2018/05/08/21/28/airbnb-3384008_1280.png)

This is a Python script that utilizes web scraping techniques to extract information from AirBnB listings in a specific location. The script uses Selenium and BeautifulSoup libraries to automate browsing and parsing of web pages.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Installing
1. Make sure you have Python installed on your system (version 3.6 or later).

2. Clone the repository to your local machine
```
git clone https://github.com/JiGro/AirBnB_Price_Extractor.git
```

3. Install the required packages
```
pip install -r requirements.txt
```

4. Set Location and start url
```
########################################################################
INPUT_URL = 'https://www.airbnb.de/s/London/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&price_filter_input_type=0&price_filter_num_nights=28&query=London%2C%20Vereinigtes%20K%C3%B6nigreich&date_picker_type=flexible_dates&flexible_trip_lengths%5B%5D=one_month&adults=2&source=structured_search_input_header&search_type=autocomplete_click&room_types%5B%5D=Entire%20home%2Fapt&place_id=ChIJdd4hrwug2EcRmSrV3Vo6llI'
INPUT_DESTINATION = "London"
########################################################################
```

5. Run the code using the following command:
```
python price_extractor.py
```

## Authors
- **Jimmy (JiGro)** - *Initial work* - [My Github Profile](https://github.com/JiGro)
