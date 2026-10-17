"""DEMO DATA ONLY. Brands, products, prices and ratings below are fictional and exist to demonstrate the platform."""

CATEGORIES = [
    # (slug, name, group, emoji)
    ("smartphones", "Smartphones", "Electronics", "📱"), ("laptops", "Laptops", "Electronics", "💻"),
    ("headphones", "Headphones", "Electronics", "🎧"), ("earbuds", "Earbuds", "Electronics", "🎵"),
    ("smartwatches", "Smart Watches", "Electronics", "⌚"), ("tvs", "TVs", "Electronics", "📺"),
    ("cameras", "Cameras", "Electronics", "📷"),
    ("refrigerators", "Refrigerators", "Home Appliances", "🧊"), ("washing-machines", "Washing Machines", "Home Appliances", "🧺"),
    ("air-conditioners", "Air Conditioners", "Home Appliances", "❄️"), ("mixers", "Mixers", "Home Appliances", "🥤"),
    ("microwave-ovens", "Microwave Ovens", "Home Appliances", "🍲"), ("fans", "Fans", "Home Appliances", "🌀"),
    ("mens-clothing", "Men's Clothing", "Fashion", "👔"), ("womens-clothing", "Women's Clothing", "Fashion", "👗"),
    ("kids-clothing", "Kids Clothing", "Fashion", "🧒"), ("shoes", "Shoes", "Fashion", "👟"),
    ("watches", "Watches", "Fashion", "🕰️"), ("bags", "Bags", "Fashion", "🎒"),
    ("rice", "Rice", "Grocery", "🍚"), ("pulses", "Pulses", "Grocery", "🫘"), ("cooking-oil", "Cooking Oil", "Grocery", "🛢️"),
    ("snacks", "Snacks", "Grocery", "🍪"), ("beverages", "Beverages", "Grocery", "🍵"),
    ("skin-care", "Skin Care", "Beauty", "🧴"), ("hair-care", "Hair Care", "Beauty", "💇"), ("personal-care", "Personal Care", "Beauty", "🧼"),
    ("seeds", "Seeds", "Agriculture", "🌱"), ("fertilizers", "Fertilizers", "Agriculture", "🌾"),
    ("gardening-tools", "Gardening Tools", "Agriculture", "🪴"), ("sprayers", "Sprayers", "Agriculture", "💦"),
]

SELLERS = ["Sri Demo Traders", "Bharat Demo Mart", "Metro Demo Retail", "Kisan Demo Store", "Demo Home Hub"]

# ---- Smartphones: name, brand, price, orig, rating, reviews, stock, ram, storage, battery, camera, refresh, perf, charge W, screen, tags
PHONES = [
    ("Orbit Easy 4G", "Orbit", 6999, 7999, 3.9, 640, 55, 3, 32, 4000, 8, 60, 20, 10, 5.5, ["elderly-friendly", "budget", "big-text"]),
    ("Zenix Spark Lite 4G", "Zenix", 7499, 8999, 4.0, 1850, 80, 4, 64, 5000, 13, 60, 30, 10, 6.5, ["budget"]),
    ("Zenix Spark Plus", "Zenix", 9999, 11999, 4.1, 2210, 64, 4, 128, 5000, 50, 90, 40, 18, 6.6, ["budget"]),
    ("Aarav Power 7000", "Aarav", 13499, 15499, 4.2, 980, 30, 6, 128, 7000, 50, 90, 45, 25, 6.7, ["long-battery"]),
    ("Nova M2", "Nova", 12999, 15999, 4.3, 3120, 70, 6, 128, 6000, 50, 90, 52, 22, 6.6, ["long-battery"]),
    ("Nova M2 Pro", "Nova", 14999, 17999, 4.4, 2760, 48, 8, 128, 5500, 64, 120, 62, 33, 6.67, ["all-rounder"]),
    ("Aarav Click 5G", "Aarav", 17499, 19999, 4.5, 1540, 26, 8, 128, 5000, 108, 120, 68, 33, 6.7, ["camera-focus"]),
    ("Nova X5 5G", "Nova", 19999, 24999, 4.4, 2310, 40, 8, 256, 5000, 64, 120, 75, 45, 6.67, ["all-rounder"]),
    ("Zenix Play GT", "Zenix", 22999, 26999, 4.5, 1890, 22, 12, 256, 5000, 50, 144, 90, 66, 6.78, ["gaming"]),
    ("Orbit Pro 5G", "Orbit", 34999, 39999, 4.6, 870, 12, 12, 256, 5000, 200, 120, 92, 67, 6.8, ["premium", "camera-focus"]),
]

# ---- Laptops: name, brand, price, orig, rating, reviews, stock, ram, storage_gb, battery_hours, perf, screen, tags
LAPTOPS = [
    ("Nova Lite 14", "Nova", 24999, 29999, 4.0, 720, 35, 8, 256, 7, 35, 14, ["budget", "student"]),
    ("Aarav Study Book 14", "Aarav", 31999, 36999, 4.2, 1320, 44, 8, 256, 8, 45, 14, ["student"]),
    ("Nova Code Pro 15", "Nova", 49999, 57999, 4.5, 960, 18, 16, 512, 9, 70, 15.6, ["coding"]),
    ("Zenix Slim Air 14", "Zenix", 58999, 66999, 4.4, 540, 14, 16, 512, 12, 65, 14, ["lightweight", "long-battery"]),
    ("Orbit Gamer 15", "Orbit", 79999, 92999, 4.5, 410, 9, 16, 1024, 5, 90, 15.6, ["gaming"]),
    ("Aarav Creator 16", "Aarav", 99999, 112999, 4.6, 230, 6, 32, 1024, 8, 95, 16, ["premium", "editing"]),
]

# ---- Generic: (category, subcategory, name, brand, price, orig, rating, reviews, stock, specs, metrics, tags)
G = []


def g(cat, sub, name, brand, price, orig, rating, reviews, stock, specs, metrics=None, tags=None):
    G.append((cat, sub, name, brand, price, orig, rating, reviews, stock, specs, metrics or {}, tags or []))


# Audio & wearables
g("headphones", "Over-ear", "Orbit Bass Pro Headphones", "Orbit", 2499, 3999, 4.3, 1840, 60, {"Type": "Over-ear wireless", "Battery": "40 hours", "Warranty": "1 year"}, {"battery_hours": 40, "sound_score": 8}, ["bass"])
g("headphones", "On-ear", "Aarav Studio Lite Headphones", "Aarav", 1499, 2299, 4.0, 920, 75, {"Type": "On-ear wired", "Cable": "1.2 m", "Warranty": "6 months"}, {"sound_score": 6}, ["budget"])
g("headphones", "Over-ear", "Zenix Quiet ANC Headphones", "Zenix", 5999, 8999, 4.5, 610, 18, {"Type": "Over-ear wireless with noise cancelling", "Battery": "30 hours", "Warranty": "1 year"}, {"battery_hours": 30, "sound_score": 9}, ["noise-cancelling", "premium"])
g("earbuds", "True wireless", "Nova Buds Air", "Nova", 1299, 2499, 4.1, 3320, 120, {"Type": "True wireless", "Battery": "24 hours with case", "Warranty": "1 year"}, {"battery_hours": 24, "sound_score": 6}, ["budget"])
g("earbuds", "True wireless", "Orbit Buds Pro", "Orbit", 3499, 5499, 4.4, 1280, 52, {"Type": "True wireless with noise cancelling", "Battery": "36 hours with case", "Warranty": "1 year"}, {"battery_hours": 36, "sound_score": 8}, ["noise-cancelling"])
g("earbuds", "Neckband", "Zenix Neckband Bass", "Zenix", 899, 1499, 4.0, 4100, 90, {"Type": "Wireless neckband", "Battery": "30 hours", "Warranty": "6 months"}, {"battery_hours": 30, "sound_score": 6}, ["budget", "long-battery"])
g("smartwatches", "Fitness", "Nova Fit Watch 2", "Nova", 2999, 4999, 4.2, 2190, 70, {"Display": "1.7 inch", "Battery": "7 days", "Features": "Heart rate, steps, sleep tracking", "Warranty": "1 year"}, {"battery_hours": 168}, ["fitness"])
g("smartwatches", "Calling", "Aarav Call Watch", "Aarav", 3999, 6499, 4.1, 1330, 40, {"Display": "1.83 inch", "Battery": "5 days", "Features": "Bluetooth calling, heart rate", "Warranty": "1 year"}, {"battery_hours": 120}, ["calling"])
g("smartwatches", "Premium", "Orbit Active Pro", "Orbit", 8999, 12999, 4.5, 540, 20, {"Display": "1.4 inch AMOLED", "Battery": "10 days", "Features": "GPS, heart rate, sleep", "Warranty": "1 year"}, {"battery_hours": 240}, ["premium", "fitness"])
# TVs
g("tvs", "32 inch", "Aarav 32 HD Smart TV", "Aarav", 10999, 16999, 4.1, 5210, 40, {"Screen": "32 inch HD", "Smart": "Yes", "Warranty": "1 year", "Sound": "20 W"}, {"screen_inch": 32, "sound_score": 6}, ["budget"])
g("tvs", "43 inch", "Nova 43 4K Smart TV", "Nova", 24999, 36999, 4.4, 2980, 28, {"Screen": "43 inch 4K", "Smart": "Yes", "Warranty": "1 year", "Sound": "30 W"}, {"screen_inch": 43, "sound_score": 7}, ["4k"])
g("tvs", "50 inch", "Zenix 50 4K Smart TV", "Zenix", 31999, 44999, 4.3, 1780, 19, {"Screen": "50 inch 4K", "Smart": "Yes", "Warranty": "1 year", "Sound": "40 W"}, {"screen_inch": 50, "sound_score": 8}, ["4k"])
g("tvs", "55 inch", "Orbit 55 QLED Smart TV", "Orbit", 47999, 69999, 4.5, 860, 11, {"Screen": "55 inch QLED 4K", "Smart": "Yes", "Warranty": "2 years", "Sound": "50 W"}, {"screen_inch": 55, "sound_score": 9}, ["premium"])
g("cameras", "Mirrorless", "Aarav Snap M200 Camera", "Aarav", 42999, 49999, 4.4, 310, 8, {"Type": "Mirrorless", "Megapixels": "24 MP", "Video": "4K", "Warranty": "2 years"}, {"camera_mp": 24}, ["photography"])
g("cameras", "Action", "Nova Action Cam 4K", "Nova", 9999, 14999, 4.2, 620, 26, {"Type": "Action camera", "Megapixels": "16 MP", "Video": "4K", "Waterproof": "10 m", "Warranty": "1 year"}, {"camera_mp": 16}, ["travel"])
# Home appliances
g("refrigerators", "Single door", "Aarav Cool 190L Refrigerator", "Aarav", 13499, 16999, 4.1, 2760, 30, {"Capacity": "190 L", "Type": "Single door", "Energy rating": "3 star", "Warranty": "1 year + 10 years compressor"}, {"capacity": 190, "capacity_unit": "L", "star_rating": 3}, ["small-family"])
g("refrigerators", "Double door", "Nova Frost 260L Refrigerator", "Nova", 24999, 31999, 4.4, 1890, 20, {"Capacity": "260 L", "Type": "Double door", "Energy rating": "3 star", "Warranty": "1 year + 10 years compressor"}, {"capacity": 260, "capacity_unit": "L", "star_rating": 3}, ["family"])
g("refrigerators", "Double door", "Zenix Frost 340L Refrigerator", "Zenix", 33999, 42999, 4.3, 1240, 14, {"Capacity": "340 L", "Type": "Double door", "Energy rating": "4 star", "Warranty": "1 year + 10 years compressor"}, {"capacity": 340, "capacity_unit": "L", "star_rating": 4}, ["family", "energy-saving"])
g("refrigerators", "Side by side", "Orbit Grand 550L Refrigerator", "Orbit", 74999, 94999, 4.5, 330, 5, {"Capacity": "550 L", "Type": "Side by side", "Energy rating": "3 star", "Warranty": "1 year + 10 years compressor"}, {"capacity": 550, "capacity_unit": "L", "star_rating": 3}, ["large-family", "premium"])
g("washing-machines", "Semi-automatic", "Aarav Wash 6 Semi-Auto", "Aarav", 8999, 11999, 4.0, 3310, 45, {"Capacity": "6 KG", "Type": "Semi-automatic top load", "Spin speed": "1300 RPM", "Energy rating": "3 star", "Warranty": "2 years"}, {"capacity": 6, "capacity_unit": "KG", "star_rating": 3}, ["budget", "easy-to-use"])
g("washing-machines", "Top load", "Nova Wash 7 Top Load", "Nova", 15999, 20999, 4.3, 2540, 34, {"Capacity": "7 KG", "Type": "Fully automatic top load", "Spin speed": "740 RPM", "Energy rating": "5 star", "Warranty": "2 years"}, {"capacity": 7, "capacity_unit": "KG", "star_rating": 5}, ["family", "energy-saving"])
g("washing-machines", "Front load", "Zenix Wash 8 Front Load", "Zenix", 24999, 33999, 4.4, 1760, 21, {"Capacity": "8 KG", "Type": "Fully automatic front load", "Spin speed": "1200 RPM", "Energy rating": "5 star", "Warranty": "2 years"}, {"capacity": 8, "capacity_unit": "KG", "star_rating": 5}, ["family", "energy-saving"])
g("washing-machines", "Front load", "Orbit Wash 9 Front Load", "Orbit", 36999, 49999, 4.5, 690, 10, {"Capacity": "9 KG", "Type": "Fully automatic front load", "Spin speed": "1400 RPM", "Energy rating": "5 star", "Warranty": "3 years"}, {"capacity": 9, "capacity_unit": "KG", "star_rating": 5}, ["large-family", "premium"])
g("air-conditioners", "Split 1 ton", "Aarav Breeze 1T Split AC", "Aarav", 28999, 38999, 4.1, 1980, 25, {"Capacity": "1 ton", "Type": "Split", "Energy rating": "3 star", "Suits room size": "up to 110 sq ft", "Warranty": "1 year + 5 years compressor"}, {"star_rating": 3}, ["small-room"])
g("air-conditioners", "Split 1.5 ton", "Nova Chill 1.5T Inverter AC", "Nova", 38999, 52999, 4.4, 1450, 16, {"Capacity": "1.5 ton", "Type": "Inverter split", "Energy rating": "5 star", "Suits room size": "up to 180 sq ft", "Warranty": "1 year + 10 years compressor"}, {"star_rating": 5}, ["energy-saving", "family"])
g("air-conditioners", "Split 1.5 ton", "Zenix Cool 1.5T Split AC", "Zenix", 33999, 45999, 4.2, 890, 12, {"Capacity": "1.5 ton", "Type": "Split", "Energy rating": "3 star", "Suits room size": "up to 180 sq ft", "Warranty": "1 year + 5 years compressor"}, {"star_rating": 3}, ["family"])
g("mixers", "Mixer grinder", "Aarav Mix 500W 3 Jar", "Aarav", 2299, 3499, 4.2, 6120, 85, {"Power": "500 W", "Jars": "3", "Warranty": "2 years"}, {}, ["kitchen", "budget"])
g("mixers", "Mixer grinder", "Nova Mix 750W 4 Jar", "Nova", 3999, 5999, 4.4, 3490, 50, {"Power": "750 W", "Jars": "4", "Warranty": "2 years"}, {}, ["kitchen", "family"])
g("mixers", "Mixer grinder", "Orbit Wet Grinder 2L", "Orbit", 5499, 7499, 4.3, 1210, 30, {"Capacity": "2 L", "Use": "Idli and dosa batter", "Warranty": "2 years"}, {}, ["kitchen", "batter"])
g("microwave-ovens", "Solo", "Aarav Solo 20L Microwave", "Aarav", 5499, 7499, 4.1, 2210, 36, {"Capacity": "20 L", "Type": "Solo", "Warranty": "1 year"}, {"capacity": 20, "capacity_unit": "L"}, ["small-family", "easy-to-use"])
g("microwave-ovens", "Convection", "Nova Convection 30L Microwave", "Nova", 11999, 15999, 4.4, 1330, 22, {"Capacity": "30 L", "Type": "Convection (bake, grill, reheat)", "Warranty": "1 year"}, {"capacity": 30, "capacity_unit": "L"}, ["family", "baking"])
g("fans", "Ceiling fan", "Aarav Air 1200mm Ceiling Fan", "Aarav", 1799, 2499, 4.1, 5530, 110, {"Sweep": "1200 mm", "Speed": "370 RPM", "Warranty": "2 years"}, {"star_rating": 3}, ["budget"])
g("fans", "Ceiling fan", "Nova Eco BLDC Ceiling Fan", "Nova", 3499, 4999, 4.5, 2840, 60, {"Sweep": "1200 mm", "Type": "BLDC motor, saves electricity", "Warranty": "5 years"}, {"star_rating": 5}, ["energy-saving", "remote"])
g("fans", "Table fan", "Zenix Table Fan 400mm", "Zenix", 1199, 1699, 4.0, 3110, 95, {"Sweep": "400 mm", "Speeds": "3", "Warranty": "1 year"}, {}, ["budget", "portable"])
# Fashion
g("mens-clothing", "Shirt", "Aarav Cotton Formal Shirt", "Aarav", 899, 1799, 4.1, 2210, 120, {"Material": "100% cotton", "Fit": "Regular", "Sizes": "S-XXL"}, {}, ["formal", "cotton"])
g("mens-clothing", "T-shirt", "Nova Everyday T-Shirt Pack of 2", "Nova", 599, 1199, 4.0, 4320, 200, {"Material": "Cotton blend", "Fit": "Regular", "Sizes": "S-XXL"}, {}, ["casual", "budget"])
g("mens-clothing", "Jeans", "Zenix Stretch Jeans", "Zenix", 1299, 2499, 4.2, 1880, 90, {"Material": "Stretch denim", "Fit": "Slim", "Sizes": "28-38"}, {}, ["casual"])
g("womens-clothing", "Saree", "Orbit Silk Blend Saree", "Orbit", 1999, 3999, 4.3, 1450, 55, {"Material": "Silk blend", "Length": "5.5 m with blouse piece"}, {}, ["festive"])
g("womens-clothing", "Kurti", "Aarav Printed Cotton Kurti", "Aarav", 699, 1399, 4.1, 3110, 140, {"Material": "Cotton", "Sizes": "S-XXL"}, {}, ["casual", "cotton"])
g("womens-clothing", "Dress", "Nova A-Line Dress", "Nova", 1299, 2599, 4.2, 970, 70, {"Material": "Rayon", "Sizes": "S-XL"}, {}, ["casual"])
g("kids-clothing", "T-shirt", "Zenix Kids Cartoon T-Shirt Set", "Zenix", 549, 999, 4.2, 2210, 150, {"Material": "Soft cotton", "Age": "4-10 years", "Pack": "3 pieces"}, {}, ["kids", "cotton"])
g("kids-clothing", "Dress", "Nova Kids Party Frock", "Nova", 899, 1799, 4.3, 760, 60, {"Material": "Cotton blend", "Age": "3-9 years"}, {}, ["kids", "festive"])
g("kids-clothing", "Set", "Aarav Kids Night Suit", "Aarav", 499, 899, 4.1, 1340, 110, {"Material": "Soft cotton", "Age": "3-12 years"}, {}, ["kids", "budget"])
g("shoes", "Running", "Nova Runner Sports Shoes", "Nova", 1799, 3499, 4.3, 3880, 80, {"Type": "Running shoes", "Sole": "Cushioned", "Sizes": "6-11"}, {}, ["sports", "comfortable"])
g("shoes", "Casual", "Aarav Daily Walk Shoes", "Aarav", 999, 1999, 4.1, 5210, 130, {"Type": "Casual walking shoes", "Sole": "Light and flexible", "Sizes": "6-11"}, {}, ["budget", "comfortable"])
g("shoes", "Kids", "Zenix Kids School Shoes", "Zenix", 799, 1499, 4.2, 2640, 100, {"Type": "School shoes", "Closure": "Velcro", "Sizes": "Kids 1-5"}, {}, ["kids", "school", "budget"])
g("shoes", "Kids", "Orbit Kids Sports Shoes", "Orbit", 1199, 2199, 4.3, 1180, 70, {"Type": "Kids sports shoes", "Closure": "Laces", "Sizes": "Kids 1-5"}, {}, ["kids", "sports"])
g("shoes", "Formal", "Zenix Leather Formal Shoes", "Zenix", 2299, 3999, 4.2, 890, 40, {"Type": "Formal shoes", "Material": "Leather", "Sizes": "6-11"}, {}, ["formal"])
g("watches", "Analog", "Aarav Classic Analog Watch", "Aarav", 1499, 2999, 4.1, 1220, 60, {"Type": "Analog", "Strap": "Leather", "Warranty": "1 year"}, {}, ["classic"])
g("watches", "Digital", "Nova Sports Digital Watch", "Nova", 999, 1999, 4.0, 1960, 85, {"Type": "Digital", "Water resistance": "50 m", "Warranty": "1 year"}, {}, ["sports"])
g("watches", "Analog", "Orbit Steel Chronograph", "Orbit", 3999, 6999, 4.4, 410, 20, {"Type": "Analog chronograph", "Strap": "Steel", "Warranty": "2 years"}, {}, ["premium", "gift"])
g("bags", "Backpack", "Aarav School Backpack 30L", "Aarav", 799, 1599, 4.2, 3220, 90, {"Capacity": "30 L", "Material": "Water-resistant polyester"}, {}, ["school", "kids"])
g("bags", "Laptop bag", "Nova Laptop Backpack 25L", "Nova", 1299, 2399, 4.3, 1580, 65, {"Capacity": "25 L", "Fits": "Laptops up to 15.6 inch"}, {}, ["office", "travel"])
g("bags", "Handbag", "Orbit Women's Handbag", "Orbit", 1599, 2999, 4.1, 760, 45, {"Material": "Synthetic leather", "Compartments": "3"}, {}, ["gift"])
# Grocery
g("rice", "Sona Masoori", "Kisan Demo Sona Masoori Rice 26 kg", "Kisan Demo", 1399, 1599, 4.3, 2210, 80, {"Weight": "26 kg", "Type": "Sona Masoori"}, {}, ["staple"])
g("rice", "Basmati", "Bharat Demo Basmati Rice 5 kg", "Bharat Demo", 749, 899, 4.4, 1850, 100, {"Weight": "5 kg", "Type": "Long grain basmati"}, {}, ["staple"])
g("rice", "Brown rice", "Kisan Demo Brown Rice 5 kg", "Kisan Demo", 549, 649, 4.1, 620, 60, {"Weight": "5 kg", "Type": "Brown rice"}, {}, ["healthy"])
g("pulses", "Toor dal", "Bharat Demo Toor Dal 1 kg", "Bharat Demo", 169, 199, 4.2, 3210, 150, {"Weight": "1 kg", "Type": "Toor dal"}, {}, ["staple"])
g("pulses", "Moong dal", "Kisan Demo Moong Dal 1 kg", "Kisan Demo", 149, 179, 4.3, 2110, 140, {"Weight": "1 kg", "Type": "Moong dal"}, {}, ["staple", "protein"])
g("pulses", "Chana dal", "Bharat Demo Chana Dal 1 kg", "Bharat Demo", 119, 139, 4.1, 1820, 160, {"Weight": "1 kg", "Type": "Chana dal"}, {}, ["staple"])
g("cooking-oil", "Groundnut", "Kisan Demo Groundnut Oil 1 L", "Kisan Demo", 219, 249, 4.4, 2640, 100, {"Volume": "1 L", "Type": "Groundnut oil"}, {}, ["staple"])
g("cooking-oil", "Sunflower", "Bharat Demo Sunflower Oil 5 L", "Bharat Demo", 849, 999, 4.2, 1810, 70, {"Volume": "5 L", "Type": "Refined sunflower oil"}, {}, ["staple"])
g("cooking-oil", "Coconut", "Kisan Demo Coconut Oil 1 L", "Kisan Demo", 299, 349, 4.3, 1220, 90, {"Volume": "1 L", "Type": "Coconut oil"}, {}, ["staple"])
g("snacks", "Chips", "Bharat Demo Potato Chips Family Pack", "Bharat Demo", 99, 120, 4.0, 5120, 200, {"Weight": "200 g"}, {}, ["snack"])
g("snacks", "Biscuits", "Kisan Demo Whole Wheat Biscuits", "Kisan Demo", 55, 65, 4.1, 3220, 250, {"Weight": "250 g"}, {}, ["snack", "kids"])
g("snacks", "Namkeen", "Bharat Demo Mixture Namkeen 400 g", "Bharat Demo", 129, 149, 4.2, 2120, 180, {"Weight": "400 g"}, {}, ["snack"])
g("beverages", "Tea", "Kisan Demo Strong Tea 500 g", "Kisan Demo", 249, 289, 4.3, 3880, 130, {"Weight": "500 g", "Type": "Black tea leaves"}, {}, ["tea"])
g("beverages", "Coffee", "Bharat Demo Filter Coffee 500 g", "Bharat Demo", 349, 399, 4.4, 2310, 90, {"Weight": "500 g", "Type": "Filter coffee powder"}, {}, ["coffee"])
g("beverages", "Juice", "Kisan Demo Mango Juice 1 L", "Kisan Demo", 99, 119, 4.0, 1990, 160, {"Volume": "1 L"}, {}, ["juice", "kids"])
# Beauty
g("skin-care", "Moisturizer", "Nova Daily Moisturizer 200 ml", "Nova", 299, 449, 4.2, 2210, 120, {"Volume": "200 ml", "Skin type": "All skin types"}, {}, ["daily"])
g("skin-care", "Sunscreen", "Aarav Sunscreen SPF 50", "Aarav", 399, 599, 4.3, 1760, 90, {"Volume": "80 ml", "SPF": "50"}, {}, ["sun-protection"])
g("skin-care", "Face wash", "Zenix Neem Face Wash", "Zenix", 149, 199, 4.1, 3320, 180, {"Volume": "100 ml", "Skin type": "Oily skin"}, {}, ["daily"])
g("hair-care", "Shampoo", "Nova Anti-Dandruff Shampoo", "Nova", 249, 349, 4.2, 2860, 130, {"Volume": "340 ml"}, {}, ["daily"])
g("hair-care", "Hair oil", "Kisan Demo Herbal Hair Oil", "Kisan Demo", 179, 229, 4.3, 1920, 110, {"Volume": "200 ml"}, {}, ["herbal"])
g("hair-care", "Conditioner", "Aarav Smooth Conditioner", "Aarav", 299, 399, 4.0, 880, 70, {"Volume": "250 ml"}, {}, ["daily"])
g("personal-care", "Soap", "Bharat Demo Sandal Soap Pack of 4", "Bharat Demo", 189, 240, 4.2, 2210, 190, {"Pack": "4 x 125 g"}, {}, ["daily"])
g("personal-care", "Trimmer", "Zenix Cordless Trimmer", "Zenix", 999, 1799, 4.2, 4410, 80, {"Battery": "60 minutes use", "Warranty": "1 year"}, {}, ["grooming", "gift"])
g("personal-care", "Toothpaste", "Nova Fresh Toothpaste Family Pack", "Nova", 149, 189, 4.1, 3120, 210, {"Weight": "300 g"}, {}, ["daily"])
# Agriculture
g("seeds", "Vegetable", "Kisan Demo Tomato Seeds Hybrid", "Kisan Demo", 149, 199, 4.2, 980, 140, {"Pack": "10 g", "Season": "All seasons"}, {}, ["vegetable", "farming"])
g("seeds", "Vegetable", "Kisan Demo Chilli Seeds", "Kisan Demo", 129, 169, 4.1, 760, 120, {"Pack": "10 g", "Season": "Kharif and Rabi"}, {}, ["vegetable", "farming"])
g("seeds", "Flower", "Bharat Demo Marigold Seeds", "Bharat Demo", 79, 99, 4.0, 540, 160, {"Pack": "5 g"}, {}, ["flower", "garden"])
g("fertilizers", "Organic", "Kisan Demo Organic Compost 5 kg", "Kisan Demo", 349, 449, 4.3, 1210, 90, {"Weight": "5 kg", "Type": "Organic compost"}, {}, ["organic", "farming"])
g("fertilizers", "NPK", "Bharat Demo NPK 19-19-19 1 kg", "Bharat Demo", 299, 379, 4.2, 860, 100, {"Weight": "1 kg", "Type": "Water-soluble NPK"}, {}, ["farming"])
g("fertilizers", "Vermicompost", "Kisan Demo Vermicompost 10 kg", "Kisan Demo", 449, 549, 4.4, 1530, 75, {"Weight": "10 kg", "Type": "Vermicompost"}, {}, ["organic", "garden"])
g("gardening-tools", "Tool kit", "Bharat Demo Garden Tool Kit 5 pc", "Bharat Demo", 599, 899, 4.2, 720, 60, {"Pieces": "5", "Material": "Steel with rubber grip"}, {}, ["garden"])
g("gardening-tools", "Pruner", "Kisan Demo Pruning Shears", "Kisan Demo", 349, 499, 4.3, 910, 80, {"Material": "Hardened steel blade"}, {}, ["garden", "farming"])
g("sprayers", "Hand pump", "Kisan Demo Hand Pump Sprayer 2 L", "Kisan Demo", 399, 599, 4.1, 1330, 70, {"Capacity": "2 L", "Type": "Manual pressure pump"}, {}, ["garden", "farming"])
g("sprayers", "Knapsack", "Bharat Demo Knapsack Sprayer 16 L", "Bharat Demo", 1599, 2299, 4.3, 1860, 50, {"Capacity": "16 L", "Type": "Manual knapsack"}, {}, ["farming"])
g("sprayers", "Battery", "Kisan Demo Battery Sprayer 16 L", "Kisan Demo", 3299, 4499, 4.4, 1240, 28, {"Capacity": "16 L", "Type": "Battery powered", "Run time": "Up to 6 hours per charge"}, {"battery_hours": 6}, ["farming", "battery-powered"])

COUPONS = [
    ("WELCOME10", "10% off on orders above ₹999 (max ₹500)", 10, 500, 999),
    ("SMART5", "5% off on any order (max ₹300)", 5, 300, 0),
    ("FESTIVE15", "15% off on orders above ₹5,000 (max ₹1,500)", 15, 1500, 5000),
]
