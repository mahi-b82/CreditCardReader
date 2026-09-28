def ai_categorize_transaction(description):
    description = str(description).upper().strip()

    merchants = {
        "AMAZON": ("Amazon", "Shopping"),
        "AJIO": ("AJIO", "Shopping"),
        "FLIPKART": ("Flipkart", "Shopping"),
        "MYNTRA": ("Myntra", "Shopping"),
        "RELIANCE DIGITAL": ("Reliance Digital", "Shopping"),

        "SWIGGY": ("Swiggy", "Food"),
        "ZOMATO": ("Zomato", "Food"),
        "DOMINOS": ("Dominos", "Food"),
        "MCDONALD": ("McDonald's", "Food"),
        "KFC": ("KFC", "Food"),

        "UBER": ("Uber", "Transport"),
        "OLA": ("Ola", "Transport"),
        "RAPIDO": ("Rapido", "Transport"),
        "IRCTC": ("IRCTC", "Transport"),

        "NETFLIX": ("Netflix", "Entertainment"),
        "SPOTIFY": ("Spotify", "Entertainment"),
        "YOUTUBE": ("YouTube", "Entertainment"),
        "PVR": ("PVR", "Entertainment"),
        "INOX": ("INOX", "Entertainment"),
        "BOOKMYSHOW": ("BookMyShow", "Entertainment"),

        "APOLLO": ("Apollo", "Healthcare"),
        "MEDPLUS": ("MedPlus", "Healthcare"),
        "TATA 1MG": ("Tata 1mg", "Healthcare"),

        "AIRTEL": ("Airtel", "Utilities"),
        "JIO": ("Jio", "Utilities"),
        "VODAFONE": ("Vodafone", "Utilities"),
        "BSES": ("BSES", "Utilities"),

        "SALARY": ("Salary", "Salary"),
        "PAYROLL": ("Payroll", "Salary"),

        "NEFT": ("NEFT", "Transfer"),
        "RTGS": ("RTGS", "Transfer"),
        "IMPS": ("IMPS", "Transfer")
    }

    for keyword, (merchant, category) in merchants.items():
        if keyword in description:
            return {
                "merchant": merchant,
                "category": category,
                "method": "Merchant Recognition"
            }

    context_categories = {
        "Entertainment": [
            "STAND UP COMEDY", "COMEDY SHOW",
            "CIRCUS", "CONCERT", "LIVE SHOW",
            "MOVIE", "MOVIE TICKET", "THEATRE",
            "THEATER", "EVENT TICKET", "SHOW",
            "MUSIC", "GAME"
        ],
        "Food": [
            "RESTAURANT", "CAFE", "FOOD",
            "DINNER", "LUNCH", "BREAKFAST",
            "BAKERY", "PIZZA"
        ],
        "Shopping": [
            "CLOTHING", "FASHION", "ELECTRONICS",
            "SHOPPING", "RETAIL", "GROCERY"
        ],
        "Transport": [
            "PETROL", "FUEL", "METRO", "BUS",
            "TAXI", "CAB", "PARKING",
            "FLIGHT", "AIRLINE", "TRAIN"
        ],
        "Healthcare": [
            "PHARMACY", "MEDICINE", "MEDICAL",
            "HOSPITAL", "CLINIC", "DOCTOR",
            "HEALTHCARE"
        ],
        "Utilities": [
            "ELECTRICITY", "WATER BILL",
            "GAS BILL", "BROADBAND",
            "RECHARGE", "MOBILE BILL"
        ],
        "Education": [
            "SCHOOL", "COLLEGE", "UNIVERSITY",
            "COURSE", "EDUCATION", "EXAM FEE",
            "TUITION"
        ]
    }

    for category, keywords in context_categories.items():
        for keyword in keywords:
            if keyword in description:
                return {
                    "merchant": "Unknown",
                    "category": category,
                    "method": "Context Recognition"
                }

    return {
        "merchant": "Unknown",
        "category": "Other",
        "method": "Unrecognized"
    }