import re


def clean_description(description):
    """
    Clean and normalize transaction descriptions.
    """

    description = str(description).upper().strip()

    # Replace punctuation with spaces
    description = re.sub(r"[^A-Z0-9\s]", " ", description)

    # Remove extra spaces
    description = re.sub(r"\s+", " ", description)

    return description


def ai_categorize_transaction(description):

    description = clean_description(description)

    # ==================================================
    # MERCHANT RECOGNITION
    # ==================================================

    merchants = {

        # ------------------------------
        # Shopping
        # ------------------------------

        "AMAZON": ("Amazon", "Shopping"),
        "AJIO": ("AJIO", "Shopping"),
        "FLIPKART": ("Flipkart", "Shopping"),
        "MYNTRA": ("Myntra", "Shopping"),
        "RELIANCE DIGITAL": ("Reliance Digital", "Shopping"),
        "CROMA": ("Croma", "Shopping"),
        "DMART": ("DMart", "Shopping"),
        "DECATHLON": ("Decathlon", "Shopping"),
        "NYKAA": ("Nykaa", "Shopping"),

        # ------------------------------
        # Food
        # ------------------------------

        "SWIGGY": ("Swiggy", "Food"),
        "ZOMATO": ("Zomato", "Food"),
        "DOMINOS": ("Dominos", "Food"),
        "MCDONALD": ("McDonald's", "Food"),
        "KFC": ("KFC", "Food"),
        "BURGER KING": ("Burger King", "Food"),
        "STARBUCKS": ("Starbucks", "Food"),
        "SUBWAY": ("Subway", "Food"),
        "PIZZA HUT": ("Pizza Hut", "Food"),

        # ------------------------------
        # Transport
        # ------------------------------

        "UBER": ("Uber", "Transport"),
        "OLA": ("Ola", "Transport"),
        "RAPIDO": ("Rapido", "Transport"),
        "IRCTC": ("IRCTC", "Transport"),
        "BLUSMART": ("BluSmart", "Transport"),

        # ------------------------------
        # Entertainment
        # ------------------------------

        "NETFLIX": ("Netflix", "Entertainment"),
        "SPOTIFY": ("Spotify", "Entertainment"),
        "YOUTUBE": ("YouTube", "Entertainment"),
        "PVR": ("PVR", "Entertainment"),
        "INOX": ("INOX", "Entertainment"),
        "BOOKMYSHOW": ("BookMyShow", "Entertainment"),
        "SONY LIV": ("SonyLIV", "Entertainment"),
        "PRIME VIDEO": ("Prime Video", "Entertainment"),

        # ------------------------------
        # Healthcare
        # ------------------------------

        "APOLLO": ("Apollo", "Healthcare"),
        "MEDPLUS": ("MedPlus", "Healthcare"),
        "TATA 1MG": ("Tata 1mg", "Healthcare"),
        "MAX HOSPITAL": ("Max Hospital", "Healthcare"),
        "FORTIS": ("Fortis", "Healthcare"),

        # ------------------------------
        # Utilities
        # ------------------------------

        "AIRTEL": ("Airtel", "Utilities"),
        "JIO": ("Jio", "Utilities"),
        "VODAFONE": ("Vodafone", "Utilities"),
        "VI": ("Vi", "Utilities"),
        "BSES": ("BSES", "Utilities"),

        # ------------------------------
        # Salary / Income
        # ------------------------------

        "SALARY": ("Salary", "Salary"),
        "PAYROLL": ("Payroll", "Salary"),

        # ------------------------------
        # Transfers
        # ------------------------------

        "NEFT": ("NEFT", "Transfer"),
        "RTGS": ("RTGS", "Transfer"),
        "IMPS": ("IMPS", "Transfer"),
    }

    # ==================================================
    # MERCHANT MATCHING
    # ==================================================

    for keyword, (merchant, category) in merchants.items():

        # Match complete words instead of partial text
        pattern = r"\b" + re.escape(keyword) + r"\b"

        if re.search(pattern, description):

            return {
                "merchant": merchant,
                "category": category,
                "method": "Merchant Recognition"
            }

    # ==================================================
    # CONTEXT-BASED CATEGORIES
    # ==================================================

    context_categories = {

        "Entertainment": [

            "STAND UP COMEDY",
            "COMEDY SHOW",
            "CONCERT",
            "LIVE SHOW",
            "MOVIE",
            "MOVIE TICKET",
            "THEATRE",
            "THEATER",
            "EVENT TICKET",
            "MUSIC",
            "CINEMA",
            "OTT",
            "STREAMING",
            "AMUSEMENT PARK"
        ],

        "Food": [

            "RESTAURANT",
            "CAFE",
            "FOOD",
            "DINNER",
            "LUNCH",
            "BREAKFAST",
            "BAKERY",
            "PIZZA",
            "COFFEE",
            "DHABA",
            "DINING"
        ],

        "Shopping": [

            "CLOTHING",
            "FASHION",
            "ELECTRONICS",
            "SHOPPING",
            "RETAIL",
            "GROCERY",
            "SUPERMARKET",
            "DEPARTMENT STORE",
            "MARKET"
        ],

        "Transport": [

            "PETROL",
            "FUEL",
            "METRO",
            "BUS",
            "TAXI",
            "CAB",
            "PARKING",
            "FLIGHT",
            "AIRLINE",
            "TRAIN",
            "TOLL",
            "FASTAG"
        ],

        "Healthcare": [

            "PHARMACY",
            "MEDICINE",
            "MEDICAL",
            "HOSPITAL",
            "CLINIC",
            "DOCTOR",
            "HEALTHCARE",
            "DIAGNOSTIC",
            "LABORATORY",
            "LAB TEST"
        ],

        "Utilities": [

            "ELECTRICITY",
            "WATER BILL",
            "GAS BILL",
            "BROADBAND",
            "RECHARGE",
            "MOBILE BILL",
            "INTERNET BILL",
            "UTILITY BILL"
        ],

        "Education": [

            "SCHOOL",
            "COLLEGE",
            "UNIVERSITY",
            "COURSE",
            "EDUCATION",
            "EXAM FEE",
            "TUITION",
            "ACADEMY",
            "TRAINING"
        ]
    }

    # ==================================================
    # CONTEXT MATCHING
    # ==================================================

    for category, keywords in context_categories.items():

        for keyword in keywords:

            pattern = r"\b" + re.escape(keyword) + r"\b"

            if re.search(pattern, description):

                return {
                    "merchant": "Unknown",
                    "category": category,
                    "method": "Context Recognition"
                }

    # ==================================================
    # DEFAULT CATEGORY
    # ==================================================

    return {
        "merchant": "Unknown",
        "category": "Other",
        "method": "Unrecognized"
    }