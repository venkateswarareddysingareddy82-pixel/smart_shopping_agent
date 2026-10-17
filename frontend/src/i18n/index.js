// UI strings. Missing keys fall back to English. Add a language by adding a block here + backend phrases.py.
export const LANGS = [
  { code: 'en', native: 'English' }, { code: 'te', native: 'తెలుగు' }, { code: 'hi', native: 'हिन्दी' },
  { code: 'ta', native: 'தமிழ்' }, { code: 'kn', native: 'ಕನ್ನಡ' }, { code: 'ml', native: 'മലയാളം' },
  { code: 'bn', native: 'বাংলা' }, { code: 'mr', native: 'मराठी' },
]

const en = {
  home: 'Home', products: 'Products', search_ph: 'Search anything… e.g. phone under 15000', speak: '🎤 Speak', ask_assistant: '🤖 Ask Shopping Assistant',
  cart: 'Cart', wishlist: 'Wishlist', account: 'Account', login: 'Login', logout: 'Logout', register: 'Register', orders: 'Orders',
  hero_title: 'Shop by Speaking — Your AI Shopping Assistant', hero_sub: 'Say what you need in your own language. We find the right product and explain it simply.',
  hero_1: 'Speak in your language', hero_2: 'AI understands you', hero_3: 'Find the right product', hero_4: 'Get simple explanations',
  buy_products: '🛒 Buy Products', speak_search: '🎤 Speak to Search', my_orders: '📦 My Orders', my_wishlist: '❤️ My Wishlist', select_language: '🌐 Select Language',
  add_to_cart: '🛒 Buy / Add to Cart', buy_now: 'Buy Now', details: '📋 Product Details', explain: '🧠 Explain Simply', ask_product: '🎤 Ask About This Product',
  compare: '⚖️ Compare Products', explain_better: '🤖 Explain Which Is Better', listening: 'Listening…', speaking: 'Speaking…', thinking: 'Thinking…',
  stop: 'Stop', replay: '🔊 Replay', type_message: 'Type your question here…', send: 'Send', tap_speak: 'Tap and speak', mic_denied: 'Microphone permission is required. Please allow microphone access and try again.',
  mic_unsupported: 'Voice input is not supported in this browser. Please use Google Chrome or Microsoft Edge, or type your question.', no_speech: 'I did not hear anything. Please tap the microphone and try again.',
  ai_unavailable: 'The AI assistant is temporarily unavailable. You can still search products normally.', demo_mode: 'Demo mode: built-in smart rules are answering (no AI key set).',
  categories: 'Shop by Category', recommended: 'Recommended for you', deals: 'Great Deals', popular: 'Popular Products', simple_mode: 'Simple Mode', simple_on: 'Simple mode is ON',
  no_results: 'No products found. Try different words or a higher budget.', filters: 'Filters', sort: 'Sort', price: 'Price', brand: 'Brand', rating: 'Rating', in_stock: 'In stock only',
  discount: 'Discount', clear: 'Clear', checkout: 'Checkout', place_order: 'Place Order', total: 'Total', remove: 'Remove', qty: 'Quantity', track: 'Track Order', back: 'Back',
  voice_lang_title: 'Choose your language', voice_lang_sub: 'We will listen and answer in this language.', welcome_assistant: 'Hello! Tap the microphone and tell me what you want to buy.',
  login_first: 'Please log in to continue.', added_cart: 'Added to cart', added_wish: 'Added to wishlist', see_more: 'See more', view_all: 'View all',
}

const te = {
  home: 'హోమ్', search_ph: 'ఏదైనా వెతకండి… ఉదా: 15000 లోపు ఫోన్', speak: '🎤 మాట్లాడండి', ask_assistant: '🤖 షాపింగ్ అసిస్టెంట్‌ని అడగండి', cart: 'కార్ట్', wishlist: 'ఇష్టమైనవి', account: 'ఖాతా',
  login: 'లాగిన్', logout: 'లాగౌట్', register: 'నమోదు', orders: 'ఆర్డర్లు', hero_title: 'మాట్లాడి షాపింగ్ చేయండి — మీ AI షాపింగ్ అసిస్టెంట్',
  hero_sub: 'మీ భాషలో చెప్పండి. మీకు సరైన వస్తువును కనుగొని, సులభంగా వివరిస్తాము.', hero_1: 'మీ భాషలో మాట్లాడండి', hero_2: 'AI మిమ్మల్ని అర్థం చేసుకుంటుంది', hero_3: 'సరైన వస్తువును కనుగొనండి', hero_4: 'సులభమైన వివరణ పొందండి',
  buy_products: '🛒 వస్తువులు కొనండి', speak_search: '🎤 మాట్లాడి వెతకండి', my_orders: '📦 నా ఆర్డర్లు', my_wishlist: '❤️ నా ఇష్టమైనవి', select_language: '🌐 భాష ఎంచుకోండి',
  add_to_cart: '🛒 కొనండి / కార్ట్‌లో వేయండి', buy_now: 'ఇప్పుడే కొనండి', details: '📋 వస్తువు వివరాలు', explain: '🧠 సులభంగా వివరించు', ask_product: '🎤 ఈ వస్తువు గురించి అడగండి',
  compare: '⚖️ వస్తువులను పోల్చండి', explain_better: '🤖 ఏది మంచిదో చెప్పు', listening: 'వింటున్నాను…', speaking: 'మాట్లాడుతున్నాను…', thinking: 'ఆలోచిస్తున్నాను…', stop: 'ఆపండి', replay: '🔊 మళ్ళీ వినండి',
  type_message: 'ఇక్కడ టైప్ చేయండి…', send: 'పంపండి', tap_speak: 'నొక్కి మాట్లాడండి', mic_denied: 'మైక్రోఫోన్ అనుమతి అవసరం. దయచేసి అనుమతించి మళ్ళీ ప్రయత్నించండి.',
  no_speech: 'నాకు ఏమీ వినిపించలేదు. మైక్ నొక్కి మళ్ళీ ప్రయత్నించండి.', ai_unavailable: 'AI అసిస్టెంట్ ప్రస్తుతం అందుబాటులో లేదు. మీరు ఇంకా వస్తువులను వెతకవచ్చు.',
  categories: 'వర్గాల వారీగా కొనండి', recommended: 'మీ కోసం సూచనలు', deals: 'మంచి డీల్స్', popular: 'ప్రసిద్ధ వస్తువులు', simple_mode: 'సులభ మోడ్', no_results: 'వస్తువులు దొరకలేదు. వేరే పదాలు లేదా ఎక్కువ బడ్జెట్ ప్రయత్నించండి.',
  filters: 'ఫిల్టర్లు', sort: 'క్రమం', price: 'ధర', brand: 'బ్రాండ్', rating: 'రేటింగ్', in_stock: 'స్టాక్‌లో ఉన్నవి', checkout: 'చెక్అవుట్', place_order: 'ఆర్డర్ చేయండి', total: 'మొత్తం', remove: 'తొలగించు', track: 'ఆర్డర్ ట్రాక్',
  voice_lang_title: 'మీ భాషను ఎంచుకోండి', voice_lang_sub: 'ఈ భాషలో వింటాము, సమాధానం ఇస్తాము.', welcome_assistant: 'నమస్తే! మైక్ నొక్కి మీకు ఏమి కావాలో చెప్పండి.', login_first: 'కొనసాగడానికి దయచేసి లాగిన్ అవ్వండి.',
}

const hi = {
  home: 'होम', search_ph: 'कुछ भी खोजें… जैसे 15000 तक का फोन', speak: '🎤 बोलिए', ask_assistant: '🤖 शॉपिंग असिस्टेंट से पूछें', cart: 'कार्ट', wishlist: 'पसंदीदा', account: 'खाता', login: 'लॉगिन', logout: 'लॉगआउट', register: 'रजिस्टर', orders: 'ऑर्डर',
  hero_title: 'बोलकर शॉपिंग करें — आपका AI शॉपिंग असिस्टेंट', hero_sub: 'अपनी भाषा में बताइए। हम सही प्रोडक्ट ढूँढकर आसान भाषा में समझाएँगे।', hero_1: 'अपनी भाषा में बोलें', hero_2: 'AI आपको समझता है', hero_3: 'सही प्रोडक्ट पाएँ', hero_4: 'आसान जानकारी पाएँ',
  buy_products: '🛒 सामान खरीदें', speak_search: '🎤 बोलकर खोजें', my_orders: '📦 मेरे ऑर्डर', my_wishlist: '❤️ मेरी पसंद', select_language: '🌐 भाषा चुनें', add_to_cart: '🛒 खरीदें / कार्ट में डालें', buy_now: 'अभी खरीदें',
  details: '📋 प्रोडक्ट की जानकारी', explain: '🧠 आसान भाषा में समझाएँ', ask_product: '🎤 इस प्रोडक्ट के बारे में पूछें', compare: '⚖️ प्रोडक्ट की तुलना', explain_better: '🤖 बताइए कौन बेहतर है', listening: 'सुन रहा हूँ…', speaking: 'बोल रहा हूँ…', thinking: 'सोच रहा हूँ…',
  stop: 'रोकें', replay: '🔊 फिर सुनें', type_message: 'यहाँ लिखें…', send: 'भेजें', tap_speak: 'दबाकर बोलें', mic_denied: 'माइक्रोफोन की अनुमति ज़रूरी है। कृपया अनुमति दें और फिर कोशिश करें।', no_speech: 'मुझे कुछ सुनाई नहीं दिया। माइक दबाकर फिर कोशिश करें।',
  ai_unavailable: 'AI असिस्टेंट अभी उपलब्ध नहीं है। आप सामान्य रूप से प्रोडक्ट खोज सकते हैं।', categories: 'श्रेणी के अनुसार खरीदें', recommended: 'आपके लिए सुझाव', deals: 'बढ़िया डील्स', popular: 'लोकप्रिय प्रोडक्ट', simple_mode: 'आसान मोड',
  no_results: 'कोई प्रोडक्ट नहीं मिला। दूसरे शब्द या ज़्यादा बजट आज़माएँ।', filters: 'फ़िल्टर', sort: 'क्रम', price: 'कीमत', brand: 'ब्रांड', rating: 'रेटिंग', in_stock: 'सिर्फ़ स्टॉक में', checkout: 'चेकआउट', place_order: 'ऑर्डर करें', total: 'कुल', remove: 'हटाएँ', track: 'ऑर्डर ट्रैक',
  voice_lang_title: 'अपनी भाषा चुनें', voice_lang_sub: 'हम इसी भाषा में सुनेंगे और जवाब देंगे।', welcome_assistant: 'नमस्ते! माइक दबाकर बताइए आपको क्या खरीदना है।', login_first: 'आगे बढ़ने के लिए कृपया लॉगिन करें।',
}

const core = (o) => o
const ta = core({
  speak: '🎤 பேசுங்கள்', ask_assistant: '🤖 ஷாப்பிங் உதவியாளரிடம் கேளுங்கள்', cart: 'கார்ட்', wishlist: 'விருப்பப்பட்டியல்', account: 'கணக்கு', login: 'உள்நுழை', logout: 'வெளியேறு', hero_title: 'பேசி ஷாப்பிங் செய்யுங்கள் — உங்கள் AI உதவியாளர்',
  hero_sub: 'உங்கள் மொழியில் சொல்லுங்கள். சரியான பொருளை கண்டுபிடித்து எளிமையாக விளக்குவோம்.', buy_products: '🛒 பொருட்கள் வாங்க', speak_search: '🎤 பேசி தேடுங்கள்', my_orders: '📦 என் ஆர்டர்கள்', my_wishlist: '❤️ என் விருப்பங்கள்', select_language: '🌐 மொழி தேர்வு',
  add_to_cart: '🛒 வாங்கு / கார்ட்டில் சேர்', details: '📋 பொருள் விவரங்கள்', explain: '🧠 எளிதாக விளக்கு', ask_product: '🎤 இந்த பொருளைப் பற்றி கேளுங்கள்', compare: '⚖️ பொருட்களை ஒப்பிடு', listening: 'கேட்கிறேன்…', speaking: 'பேசுகிறேன்…', thinking: 'யோசிக்கிறேன்…',
  stop: 'நிறுத்து', replay: '🔊 மீண்டும் கேள்', type_message: 'இங்கே தட்டச்சு செய்யுங்கள்…', mic_denied: 'மைக்ரோஃபோன் அனுமதி தேவை. அனுமதித்து மீண்டும் முயலுங்கள்.', categories: 'வகை வாரியாக', recommended: 'உங்களுக்கான பரிந்துரைகள்', deals: 'சிறந்த சலுகைகள்', popular: 'பிரபல பொருட்கள்', simple_mode: 'எளிய முறை',
  voice_lang_title: 'உங்கள் மொழியைத் தேர்ந்தெடுங்கள்', welcome_assistant: 'வணக்கம்! மைக்கை தட்டி என்ன வாங்க வேண்டும் என்று சொல்லுங்கள்.',
})
const kn = core({
  speak: '🎤 ಮಾತನಾಡಿ', ask_assistant: '🤖 ಶಾಪಿಂಗ್ ಸಹಾಯಕನನ್ನು ಕೇಳಿ', cart: 'ಕಾರ್ಟ್', wishlist: 'ಇಷ್ಟಪಟ್ಟವು', account: 'ಖಾತೆ', login: 'ಲಾಗಿನ್', logout: 'ಲಾಗೌಟ್', hero_title: 'ಮಾತನಾಡಿ ಶಾಪಿಂಗ್ ಮಾಡಿ — ನಿಮ್ಮ AI ಸಹಾಯಕ',
  hero_sub: 'ನಿಮ್ಮ ಭಾಷೆಯಲ್ಲಿ ಹೇಳಿ. ಸರಿಯಾದ ವಸ್ತುವನ್ನು ಹುಡುಕಿ ಸರಳವಾಗಿ ವಿವರಿಸುತ್ತೇವೆ.', buy_products: '🛒 ವಸ್ತುಗಳನ್ನು ಖರೀದಿಸಿ', speak_search: '🎤 ಮಾತನಾಡಿ ಹುಡುಕಿ', my_orders: '📦 ನನ್ನ ಆರ್ಡರ್‌ಗಳು', my_wishlist: '❤️ ನನ್ನ ಇಷ್ಟಗಳು', select_language: '🌐 ಭಾಷೆ ಆಯ್ಕೆ',
  add_to_cart: '🛒 ಖರೀದಿಸಿ / ಕಾರ್ಟ್‌ಗೆ ಸೇರಿಸಿ', details: '📋 ವಸ್ತುವಿನ ವಿವರ', explain: '🧠 ಸರಳವಾಗಿ ವಿವರಿಸಿ', ask_product: '🎤 ಈ ವಸ್ತುವಿನ ಬಗ್ಗೆ ಕೇಳಿ', compare: '⚖️ ವಸ್ತುಗಳನ್ನು ಹೋಲಿಸಿ', listening: 'ಕೇಳುತ್ತಿದ್ದೇನೆ…', speaking: 'ಮಾತನಾಡುತ್ತಿದ್ದೇನೆ…', thinking: 'ಯೋಚಿಸುತ್ತಿದ್ದೇನೆ…',
  stop: 'ನಿಲ್ಲಿಸಿ', replay: '🔊 ಮತ್ತೆ ಕೇಳಿ', type_message: 'ಇಲ್ಲಿ ಟೈಪ್ ಮಾಡಿ…', mic_denied: 'ಮೈಕ್ರೋಫೋನ್ ಅನುಮತಿ ಬೇಕು. ಅನುಮತಿಸಿ ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.', categories: 'ವರ್ಗದ ಪ್ರಕಾರ', recommended: 'ನಿಮಗಾಗಿ ಸಲಹೆಗಳು', deals: 'ಉತ್ತಮ ಡೀಲ್‌ಗಳು', popular: 'ಜನಪ್ರಿಯ ವಸ್ತುಗಳು', simple_mode: 'ಸರಳ ಮೋಡ್',
  voice_lang_title: 'ನಿಮ್ಮ ಭಾಷೆ ಆಯ್ಕೆಮಾಡಿ', welcome_assistant: 'ನಮಸ್ಕಾರ! ಮೈಕ್ ಒತ್ತಿ ನಿಮಗೆ ಏನು ಬೇಕು ಹೇಳಿ.',
})
const ml = core({
  speak: '🎤 സംസാരിക്കൂ', ask_assistant: '🤖 ഷോപ്പിംഗ് സഹായിയോട് ചോദിക്കൂ', cart: 'കാർട്ട്', wishlist: 'ഇഷ്ടങ്ങൾ', account: 'അക്കൗണ്ട്', login: 'ലോഗിൻ', logout: 'ലോഗൗട്ട്', hero_title: 'സംസാരിച്ച് ഷോപ്പ് ചെയ്യൂ — നിങ്ങളുടെ AI സഹായി',
  hero_sub: 'നിങ്ങളുടെ ഭാഷയിൽ പറയൂ. ശരിയായ ഉൽപ്പന്നം കണ്ടെത്തി ലളിതമായി വിശദീകരിക്കാം.', buy_products: '🛒 സാധനങ്ങൾ വാങ്ങൂ', speak_search: '🎤 സംസാരിച്ച് തിരയൂ', my_orders: '📦 എന്റെ ഓർഡറുകൾ', my_wishlist: '❤️ എന്റെ ഇഷ്ടങ്ങൾ', select_language: '🌐 ഭാഷ തിരഞ്ഞെടുക്കൂ',
  add_to_cart: '🛒 വാങ്ങൂ / കാർട്ടിൽ ചേർക്കൂ', details: '📋 ഉൽപ്പന്ന വിവരങ്ങൾ', explain: '🧠 ലളിതമായി വിശദീകരിക്കൂ', ask_product: '🎤 ഈ ഉൽപ്പന്നത്തെക്കുറിച്ച് ചോദിക്കൂ', compare: '⚖️ ഉൽപ്പന്നങ്ങൾ താരതമ്യം ചെയ്യൂ', listening: 'കേൾക്കുന്നു…', speaking: 'സംസാരിക്കുന്നു…', thinking: 'ആലോചിക്കുന്നു…',
  stop: 'നിർത്തൂ', replay: '🔊 വീണ്ടും കേൾക്കൂ', type_message: 'ഇവിടെ ടൈപ്പ് ചെയ്യൂ…', mic_denied: 'മൈക്രോഫോൺ അനുമതി ആവശ്യമാണ്. അനുവദിച്ച് വീണ്ടും ശ്രമിക്കൂ.', categories: 'വിഭാഗം അനുസരിച്ച്', recommended: 'നിങ്ങൾക്കുള്ള നിർദ്ദേശങ്ങൾ', deals: 'മികച്ച ഡീലുകൾ', popular: 'ജനപ്രിയ ഉൽപ്പന്നങ്ങൾ', simple_mode: 'ലളിത മോഡ്',
  voice_lang_title: 'നിങ്ങളുടെ ഭാഷ തിരഞ്ഞെടുക്കൂ', welcome_assistant: 'നമസ്കാരം! മൈക്ക് അമർത്തി എന്താണ് വേണ്ടതെന്ന് പറയൂ.',
})
const bn = core({
  speak: '🎤 বলুন', ask_assistant: '🤖 শপিং সহকারীকে জিজ্ঞাসা করুন', cart: 'কার্ট', wishlist: 'পছন্দের তালিকা', account: 'অ্যাকাউন্ট', login: 'লগইন', logout: 'লগআউট', hero_title: 'বলে শপিং করুন — আপনার AI সহকারী',
  hero_sub: 'আপনার ভাষায় বলুন। আমরা সঠিক পণ্য খুঁজে সহজ ভাষায় বুঝিয়ে দেব।', buy_products: '🛒 পণ্য কিনুন', speak_search: '🎤 বলে খুঁজুন', my_orders: '📦 আমার অর্ডার', my_wishlist: '❤️ আমার পছন্দ', select_language: '🌐 ভাষা বেছে নিন',
  add_to_cart: '🛒 কিনুন / কার্টে রাখুন', details: '📋 পণ্যের বিবরণ', explain: '🧠 সহজে বুঝিয়ে দিন', ask_product: '🎤 এই পণ্য সম্পর্কে জিজ্ঞাসা করুন', compare: '⚖️ পণ্য তুলনা করুন', listening: 'শুনছি…', speaking: 'বলছি…', thinking: 'ভাবছি…',
  stop: 'থামুন', replay: '🔊 আবার শুনুন', type_message: 'এখানে লিখুন…', mic_denied: 'মাইক্রোফোনের অনুমতি দরকার। অনুমতি দিয়ে আবার চেষ্টা করুন।', categories: 'বিভাগ অনুযায়ী', recommended: 'আপনার জন্য প্রস্তাব', deals: 'দারুণ অফার', popular: 'জনপ্রিয় পণ্য', simple_mode: 'সহজ মোড',
  voice_lang_title: 'আপনার ভাষা বেছে নিন', welcome_assistant: 'নমস্কার! মাইক চেপে বলুন কী কিনতে চান।',
})
const mr = core({
  speak: '🎤 बोला', ask_assistant: '🤖 शॉपिंग सहाय्यकाला विचारा', cart: 'कार्ट', wishlist: 'आवडती', account: 'खाते', login: 'लॉगिन', logout: 'लॉगआउट', hero_title: 'बोलून शॉपिंग करा — तुमचा AI सहाय्यक',
  hero_sub: 'तुमच्या भाषेत सांगा. आम्ही योग्य वस्तू शोधून सोप्या भाषेत समजावून सांगू.', buy_products: '🛒 वस्तू खरेदी करा', speak_search: '🎤 बोलून शोधा', my_orders: '📦 माझे ऑर्डर', my_wishlist: '❤️ माझी आवड', select_language: '🌐 भाषा निवडा',
  add_to_cart: '🛒 खरेदी करा / कार्टमध्ये टाका', details: '📋 वस्तूची माहिती', explain: '🧠 सोप्या भाषेत सांगा', ask_product: '🎤 या वस्तूबद्दल विचारा', compare: '⚖️ वस्तूंची तुलना', listening: 'ऐकत आहे…', speaking: 'बोलत आहे…', thinking: 'विचार करत आहे…',
  stop: 'थांबवा', replay: '🔊 पुन्हा ऐका', type_message: 'इथे लिहा…', mic_denied: 'मायक्रोफोनची परवानगी आवश्यक आहे. परवानगी देऊन पुन्हा प्रयत्न करा.', categories: 'श्रेणीनुसार', recommended: 'तुमच्यासाठी सूचना', deals: 'उत्तम ऑफर्स', popular: 'लोकप्रिय वस्तू', simple_mode: 'सोपा मोड',
  voice_lang_title: 'तुमची भाषा निवडा', welcome_assistant: 'नमस्कार! माइक दाबून तुम्हाला काय हवे ते सांगा.',
})

export const STRINGS = { en, te, hi, ta, kn, ml, bn, mr }
export const translate = (lang, key) => (STRINGS[lang] && STRINGS[lang][key]) || en[key] || key

// Sample spoken sentences shown on the hero to demonstrate each language
export const SAMPLES = {
  en: 'I need a phone under 15000 with a good camera', te: 'నాకు 15000 లోపు మంచి ఫోన్ కావాలి', hi: 'मुझे 15000 तक का अच्छा फोन चाहिए',
  ta: '15000க்குள் நல்ல போன் வேண்டும்', kn: '15000 ಒಳಗೆ ಒಳ್ಳೆಯ ಫೋನ್ ಬೇಕು', ml: '15000-ത്തിൽ താഴെ നല്ല ഫോൺ വേണം', bn: '১৫০০০ টাকার মধ্যে ভালো ফোন চাই', mr: '15000 पर्यंत चांगला फोन हवा आहे',
}
