def categorize_transaction(description):
    description = description.upper()

    categories = {
        "Food": [
            "SWIGGY", "ZOMATO", "DOMINOS", "PIZZA", "MCDONALD",
            "KFC", "RESTAURANT", "CAFE", "FOOD", "EAT"
        ],

        "Shopping": [
            "AMAZON", "FLIPKART", "MYNTRA", "AJIO", "SHOP",
            "RELIANCE RETAIL", "WALMART", "CLOTHING", "FASHION"
        ],

        "Transport": [
            "UBER", "OLA", "RAPIDO", "METRO", "IRCTC",
            "PETROL", "FUEL", "HPCL", "IOCL", "BPCL"
        ],

        "Entertainment": [
            "NETFLIX", "PRIME VIDEO", "SPOTIFY", "YOUTUBE",
            "HOTSTAR", "PVR", "INOX", "BOOKMYSHOW", "GAME"
        ],

        "Healthcare": [
            "APOLLO", "PHARMACY", "MEDICAL", "HOSPITAL",
            "CLINIC", "MEDPLUS", "1MG", "TATA 1MG"
        ],

        "Utilities": [
            "AIRTEL", "JIO", "VI ", "VODAFONE", "ELECTRICITY",
            "BSES", "WATER BILL", "GAS BILL", "BROADBAND",
            "RECHARGE", "UTILITY"
        ],

        "Education": [
            "COLLEGE", "UNIVERSITY", "SCHOOL", "COURSE",
            "UDEMY", "COURSERA", "EDUCATION", "EXAM FEE"
        ],

        "Salary": [
            "SALARY", "PAYROLL", "EMPLOYER"
        ],

        "Transfer": [
            "TRANSFER", "NEFT", "RTGS", "IMPS", "UPI TRANSFER"
        ]
    }

    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in description:
                return category

    return "Other"