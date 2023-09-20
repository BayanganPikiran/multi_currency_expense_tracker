# Base Units
TILE_LENGTH = 8

# App Dimensions
APP_NUM_COLS = 64
APP_NUM_ROWS = 40


APP_WIDTH = TILE_LENGTH * APP_NUM_COLS
APP_HEIGHT = TILE_LENGTH * APP_NUM_ROWS

# Frame Dimensions
DATE_FRAME_ROWS = 5
DATE_FRAME_COLS = 64
DATE_FRAME_WIDTH = TILE_LENGTH * DATE_FRAME_COLS
DATE_FRAME_HEIGHT = TILE_LENGTH * DATE_FRAME_ROWS

# Widget Dimensions
ENTRY_ROWS = 5
ENTRY_COLS = 39
ENTRY_WIDTH = TILE_LENGTH * ENTRY_COLS
ENTRY_HEIGHT = TILE_LENGTH * ENTRY_ROWS

COMBOBOX_ROWS = 5
COMBOBOX_COLS = 23
COMBOBOX_WIDTH = TILE_LENGTH * COMBOBOX_COLS
COMBOBOX_HEIGHT = TILE_LENGTH * COMBOBOX_ROWS

QUERY_COLS = 5
QUERY_BOX_WIDTH = TILE_LENGTH * QUERY_COLS

BUTTON_ROWS = 5
BUTTON_COLS = 31
BUTTON_WIDTH = TILE_LENGTH * BUTTON_COLS
BUTTON_HEIGHT = TILE_LENGTH * BUTTON_ROWS

# Query Toplevel
QUERY_NUM_COLS = 90
QUERY_NUM_ROWS = 32

QUERY_WIDTH = TILE_LENGTH * APP_NUM_COLS
QUERY_HEIGHT = TILE_LENGTH * APP_NUM_ROWS



# Lists & Dictionaries
EXPENSE_TYPES = ['clothing', 'electricity', 'entertainment', 'fruit', 'groceries', 'health', 'household items',
                 'internet', 'misc', 'petrol', 'rent', 'restaurant', 'supplements', 'travel', 'visas']
CURRENCIES = ['IDR', 'MYR', 'PHP', 'SGD', 'THB', 'USD']
METRICS = ['percent', 'total']


AVAILABLE_CURRENCIES = {'AUD': 1.5298140043763675,
                         'BGN': 1.7831874544128374,
                         'BRL': 4.892778993435448,
                         'CAD': 1.3439095550692925,
                         'CHF': 0.8777352297592997,
                         'CNY': 7.205506929248723,
                         'CZK': 22.148978847556528,
                         'DKK': 6.793490153172867,
                         'EUR': 0.9117432530999271,
                         'GBP': 0.7857403355215171,
                         'HKD': 7.819657184536833,
                         'HUF': 354.1575492341357,
                         'IDR': 15191.384026258205,
                         'INR': 82.85877097009481,
                         'ISK': 131.74690007293947,
                         'JPY': 143.46280087527353,
                         'KRW': 1314.2505470459519,
                         'MXN': 17.150437636761488,
                         'MYR': 4.572027716994894,
                         'NOK': 10.217268417213713,
                         'NZD': 1.650528811086798,
                         'PHP': 56.2800875273523,
                         'PLN': 4.072757111597374,
                         'RON': 4.511305616338439,
                         'SEK': 10.685175054704596,
                         'SGD': 1.3458242159008023,
                         'THB': 34.9753829321663,
                         'TRY': 27.02935813274982,
                         'ZAR': 19.048231218088986}

# Fonts
BUTTON_FONT = ('Helvetica', 16, 'bold')
LABEL_FONT = ('Helvetica', 14, 'bold')
DATE_ENTRY_FONT = ('Helvetica', 12)
