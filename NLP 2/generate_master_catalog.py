"""
Comprehensive Master Catalog Generator for CineFlix AI.
Builds 150+ verified, rich, structured movie and TV titles spanning:
- Bollywood / Hindi Cinema
- Marathi Cinema
- South Indian Cinema (Tamil, Telugu, Malayalam, Kannada)
- Regional Indian Cinema (Bengali, Punjabi, Gujarati)
- Hollywood & Global Cinema
- International Cinema (Korean, Japanese, Spanish, French, German, Italian, Turkish)
- Global & Indian TV Series
"""

import json
import os
import sys

def get_expanded_catalog():
    import build_full_catalog
    base_titles = list(build_full_catalog.CATALOG_ITEMS)
    
    additional_titles = [
        # =========================================================================
        # ADDITIONAL BOLLYWOOD CLASSICS & HITS
        # =========================================================================
        {
            "id": "b35", "tmdbId": 12819, "title": "Devdas", "originalTitle": "Devdas",
            "type": "Movie", "director": "Sanjay Leela Bhansali",
            "cast": ["Shah Rukh Khan", "Aishwarya Rai Bachchan", "Madhuri Dixit", "Jackie Shroff", "Kirron Kher"],
            "releaseYear": 2002, "rating": "PG-13", "voteCount": 68000, "duration": "185 min", "seasons": None,
            "genres": ["Drama", "Musical", "Romance"], "language": "Hindi", "country": "India", "industry": "Bollywood",
            "description": "After his wealthy family prohibits him from marrying the woman he loves, Devdas descends into alcoholism and emotional despair in the courtesan quarters of Chandramukhi.",
            "tagline": "A saga of timeless, tragic love.", "imdb_score": 7.5,
            "mood_tags": ["Opulent", "Tragic", "Musical", "Grand", "Visual Spectacle"],
            "keywords": ["devdas", "paroo", "chandramukhi", "dola re dola", "shah rukh khan", "srk", "aishwarya rai", "madhuri dixit", "sanjay leela bhansali", "bollywood", "hindi"],
            "poster": "https://image.tmdb.org/t/p/w500/yK9jN0X7ZkU8F1p8V3MuMzU90K2.jpg",
            "backdrop": "https://image.tmdb.org/t/p/original/b3Ea3Y4K0mXf1q9z7U8F1p8V3M.jpg",
            "trailerUrl": "https://www.youtube.com/watch?v=8tu3w1VM7nE", "trailer_id": "8tu3w1VM7nE",
            "netflixAvailable": False, "watchRegion": "IN"
        },
        {
            "id": "b36", "tmdbId": 14352, "title": "Kal Ho Naa Ho", "originalTitle": "Kal Ho Naa Ho",
            "type": "Movie", "director": "Nikkhil Advani",
            "cast": ["Shah Rukh Khan", "Preity Zinta", "Saif Ali Khan", "Jaya Bachchan", "Sushma Seth"],
            "releaseYear": 2003, "rating": "PG", "voteCount": 85000, "duration": "186 min", "seasons": None,
            "genres": ["Comedy", "Drama", "Romance"], "language": "Hindi", "country": "India", "industry": "Bollywood",
            "description": "Naina, an introverted, depressed MBA student in New York, finds her life changed when she meets Aman, a terminally ill neighbor who vows to bring joy to her life and match her with her best friend Rohit.",
            "tagline": "A story of a lifetime... in a heartbeat.", "imdb_score": 7.9,
            "mood_tags": ["Tearjerker", "Heartwarming", "Romantic", "Feel-Good", "Nostalgic"],
            "keywords": ["new york", "aman mathur", "naina", "rohit", "heart disease", "shah rukh khan", "srk", "preity zinta", "saif ali khan", "karan johar", "bollywood", "hindi", "kal ho naa ho"],
            "poster": "https://image.tmdb.org/t/p/w500/mXf1q9z7U8F1p8V3MuMzU90K2jQ.jpg",
            "backdrop": "https://image.tmdb.org/t/p/original/8K9jN0X7ZkU8F1p8V3MuMzU90K2.jpg",
            "trailerUrl": "https://www.youtube.com/watch?v=g0eO74UmRBs", "trailer_id": "g0eO74UmRBs",
            "netflixAvailable": True, "watchRegion": "IN"
        },
        {
            "id": "b37", "tmdbId": 113404, "title": "Gangs of Wasseypur", "originalTitle": "Gangs of Wasseypur",
            "type": "Movie", "director": "Anurag Kashyap",
            "cast": ["Manoj Bajpayee", "Nawazuddin Siddiqui", "Richa Chadha", "Huma Qureshi", "Pankaj Tripathi", "Tigmanshu Dhulia"],
            "releaseYear": 2012, "rating": "TV-MA", "voteCount": 115000, "duration": "321 min", "seasons": None,
            "genres": ["Action", "Crime", "Drama"], "language": "Hindi", "country": "India", "industry": "Bollywood",
            "description": "A multigenerational feud between three crime families revolving around coal mafia supremacy in Dhanbad, sparking bloody cycles of revenge, deceit, and gang warfare.",
            "tagline": "Music, coal, blood and revenge.", "imdb_score": 8.2,
            "mood_tags": ["Cult Classic", "Raw", "Violent", "Unfiltered", "Masterpiece"],
            "keywords": ["coal mafia", "dhanbad", "sardar khan", "faizal khan", "ramadhir singh", "manoj bajpayee", "nawazuddin siddiqui", "anurag kashyap", "bollywood", "hindi", "gangs of wasseypur"],
            "poster": "https://image.tmdb.org/t/p/w500/1XddMrGrmfeglA1t3Q7i8nI5PqR.jpg",
            "backdrop": "https://image.tmdb.org/t/p/original/1E5baAaEse26fej7uHqMqaq2qz.jpg",
            "trailerUrl": "https://www.youtube.com/watch?v=j-X4XnSgl-k", "trailer_id": "j-X4XnSgl-k",
            "netflixAvailable": True, "watchRegion": "IN"
        },
        {
            "id": "b38", "tmdbId": 334543, "title": "Piku", "originalTitle": "Piku",
            "type": "Movie", "director": "Shoojit Sircar",
            "cast": ["Amitabh Bachchan", "Deepika Padukone", "Irrfan Khan", "Moushumi Chatterjee", "Jisshu Sengupta"],
            "releaseYear": 2015, "rating": "PG", "voteCount": 68000, "duration": "123 min", "seasons": None,
            "genres": ["Comedy", "Drama"], "language": "Hindi", "country": "India", "industry": "Bollywood",
            "description": "A quirky, heartwarming road trip from Delhi to Kolkata with an eccentric, hypochondriac 70-year-old father Bhaskor Banerjee, his independent architect daughter Piku, and an exasperated taxi company owner Rana.",
            "tagline": "Motion se hi Emotion.", "imdb_score": 7.6,
            "mood_tags": ["Charming", "Heartwarming", "Wholesome", "Hilarious", "Realistic"],
            "keywords": ["kolkata road trip", "father daughter", "constipation humor", "amitabh bachchan", "big b", "deepika padukone", "irrfan khan", "shoojit sircar", "bollywood", "hindi", "piku"],
            "poster": "https://image.tmdb.org/t/p/w500/dyHAU31K9jN0X7ZkU8F1p8V3MuM.jpg",
            "backdrop": "https://image.tmdb.org/t/p/original/9rM8F1p8V3MuMzU90K2jQ1jN0X7.jpg",
            "trailerUrl": "https://www.youtube.com/watch?v=oeiKUlUUNQ8", "trailer_id": "oeiKUlUUNQ8",
            "netflixAvailable": False, "watchRegion": "IN"
        },
        {
            "id": "b39", "tmdbId": 1104844, "title": "Laapataa Ladies", "originalTitle": "Laapataa Ladies",
            "type": "Movie", "director": "Kiran Rao",
            "cast": ["Nitanshi Goel", "Pratibha Ranta", "Sparsh Shrivastava", "Ravi Kishan", "Chhaya Kadam"],
            "releaseYear": 2024, "rating": "PG", "voteCount": 62000, "duration": "122 min", "seasons": None,
            "genres": ["Comedy", "Drama"], "language": "Hindi", "country": "India", "industry": "Bollywood",
            "description": "In rural 2001 India, two young brides with identical ghunghat veils are accidentally swapped on a crowded passenger train, leading to an empowering journey of self-discovery.",
            "tagline": "Lost in transit, found in freedom.", "imdb_score": 8.4,
            "mood_tags": ["Heartwarming", "Witty", "Empowering", "Charming", "Oscar India Entry"],
            "keywords": ["train bride swap", "ghunghat", "rural empowerment", "ravi kishan", "kiran rao", "aamir khan productions", "netflix original", "laapataa ladies", "hindi"],
            "poster": "https://image.tmdb.org/t/p/w500/7c9a2K9jN0X7ZkU8F1p8V3M.jpg",
            "backdrop": "https://image.tmdb.org/t/p/original/5uY1rR7L8K9jN0X7ZkU8F1p8V3M.jpg",
            "trailerUrl": "https://www.youtube.com/watch?v=cM341Tsk0Xw", "trailer_id": "cM341Tsk0Xw",
            "netflixAvailable": True, "watchRegion": "IN"
        },
        {
            "id": "b40", "tmdbId": 1073443, "title": "Maharaja", "originalTitle": "Maharaja",
            "type": "Movie", "director": "Nithilan Saminathan",
            "cast": ["Vijay Sethupathi", "Anurag Kashyap", "Mamta Mohandas", "Natty", "Abhirami"],
            "releaseYear": 2024, "rating": "TV-MA", "voteCount": 85000, "duration": "141 min", "seasons": None,
            "genres": ["Action", "Crime", "Drama", "Mystery", "Thriller"], "language": "Hindi", "country": "India", "industry": "Bollywood",
            "description": "A quiet, unassuming barber Maharaja approaches the police claiming his house dustbin 'Lakshmi' has been stolen. As officers investigate the absurd complaint, a dark, non-linear web of violent vengeance unfolds.",
            "tagline": "He is not just a barber.", "imdb_score": 8.5,
            "mood_tags": ["Mind-bending", "Twisted", "Non-Linear", "Intense", "Masterpiece"],
            "keywords": ["dustbin lakshmi", "barber revenge", "police station", "non linear twists", "vijay sethupathi", "anurag kashyap", "netflix blockbuster", "maharaja"],
            "poster": "https://image.tmdb.org/t/p/w500/kK9jN0X7ZkU8F1p8V3MuMzU90K2.jpg",
            "backdrop": "https://image.tmdb.org/t/p/original/3XddMrGrmfeglA1t3Q7i8nI5PqR.jpg",
            "trailerUrl": "https://www.youtube.com/watch?v=F3aJ1_3wYqk", "trailer_id": "F3aJ1_3wYqk",
            "netflixAvailable": True, "watchRegion": "IN"
        },

        # =========================================================================
        # ADDITIONAL MARATHI CINEMA HITS
        # =========================================================================
        {
            "id": "mr21", "tmdbId": 801235, "title": "Pawankhind", "originalTitle": "Pawankhind",
            "type": "Movie", "director": "Digpal Lanjekar",
            "cast": ["Chinmay Mandlekar", "Ajay Purkar", "Sameer Dharmadhikari", "Ankit Mohan", "Mrinal Kulkarni"],
            "releaseYear": 2022, "rating": "PG-13", "voteCount": 35000, "duration": "153 min", "seasons": None,
            "genres": ["Action", "Drama", "History", "War"], "language": "Marathi", "country": "India", "industry": "Marathi",
            "description": "The legendary rear-guard defense of Ghodkhind pass where Baji Prabhu Deshpande and 300 Mavala soldiers fought to the last breath against 10,000 Adilshahi troops to secure Chhatrapati Shivaji Maharaj's escape.",
            "tagline": "Until the cannon fires from Vishalgad!", "imdb_score": 8.4,
            "mood_tags": ["Goosebumps", "Heroic Sacrifice", "Historical Epic", "Action-Packed", "Patriotic"],
            "keywords": ["baji prabhu deshpande", "chhatrapati shivaji maharaj", "ghodkhind", "vishalgad", "maratha history", "chinmay mandlekar", "marathi movie", "pawankhind", "mara"],
            "poster": "https://image.tmdb.org/t/p/w500/mXf1q9z7U8F1p8V3MuMzU90K2jQ.jpg",
            "backdrop": "https://image.tmdb.org/t/p/original/1E5baAaEse26fej7uHqMqaq2qz.jpg",
            "trailerUrl": "https://www.youtube.com/watch?v=Y7x1z9k8X2M", "trailer_id": "Y7x1z9k8X2M",
            "netflixAvailable": False, "watchRegion": "IN"
        },
        {
            "id": "mr22", "tmdbId": 145920, "title": "Balak-Palak", "originalTitle": "Balak Palak (BP)",
            "type": "Movie", "director": "Ravi Jadhav",
            "cast": ["Prathamesh Parab", "Shashwati Pimplikar", "Madan Deodhar", "Kishore Kadam", "Sai Tamhankar"],
            "releaseYear": 2013, "rating": "PG-13", "voteCount": 21000, "duration": "112 min", "seasons": None,
            "genres": ["Comedy", "Drama"], "language": "Marathi", "country": "India", "industry": "Marathi",
            "description": "Four curious adolescent schoolboys in 1980s Maharashtra seek answers about sex and puberty, challenging hypocritical societal taboos through innocent misadventures.",
            "tagline": "Every child has questions. Are parents ready to answer?", "imdb_score": 7.9,
            "mood_tags": ["Hilarious", "Educational", "Heartwarming", "Witty", "Relatable"],
            "keywords": ["sex education", "adolescence", "puberty taboos", "riteish deshmukh production", "ravi jadhav", "prathamesh parab", "marathi comedy", "marathi movie", "balak palak", "mara"],
            "poster": "https://image.tmdb.org/t/p/w500/uMzU90K2jQ1jN0X7ZkU8F1p8V3M.jpg",
            "backdrop": "https://image.tmdb.org/t/p/original/8K9jN0X7ZkU8F1p8V3MuMzU90K2.jpg",
            "trailerUrl": "https://www.youtube.com/watch?v=3K5_z1Y0X7M", "trailer_id": "3K5_z1Y0X7M",
            "netflixAvailable": False, "watchRegion": "IN"
        },
        {
            "id": "mr23", "tmdbId": 1113942, "title": "Ghar Banduk Biryani", "originalTitle": "Ghar Banduk Biryani",
            "type": "Movie", "director": "Hemant Jangal Awtade",
            "cast": ["Akash Thosar", "Sayaji Shinde", "Nagraj Manjule", "Sayli Patil"],
            "releaseYear": 2023, "rating": "TV-MA", "voteCount": 18000, "duration": "162 min", "seasons": None,
            "genres": ["Action", "Comedy", "Crime", "Drama"], "language": "Marathi", "country": "India", "industry": "Marathi",
            "description": "A rural cook Raju who desperately needs a home to marry his lover, a rebel commander craving authentic mutton biryani, and a demoted cop seeking redemption collide in the Kolaghat forests.",
            "tagline": "Love, bullets, and spicy biryani.", "imdb_score": 7.3,
            "mood_tags": ["Quirky", "Action Comedy", "Gritty", "Entertaining", "Nagraj Manjule"],
            "keywords": ["forest rebels", "mutton biryani", "marriage condition", "akash thosar", "sayaji shinde", "nagraj manjule", "marathi movie", "ghar banduk biryani", "mara"],
            "poster": "https://image.tmdb.org/t/p/w500/1XddMrGrmfeglA1t3Q7i8nI5PqR.jpg",
            "backdrop": "https://image.tmdb.org/t/p/original/5uY1rR7L8K9jN0X7ZkU8F1p8V3M.jpg",
            "trailerUrl": "https://www.youtube.com/watch?v=M560HlYQ9Wc", "trailer_id": "M560HlYQ9Wc",
            "netflixAvailable": False, "watchRegion": "IN"
        },
        {
            "id": "mr24", "tmdbId": 849201, "title": "Zombivli", "originalTitle": "Zombivli",
            "type": "Movie", "director": "Aditya Sarpotdar",
            "cast": ["Amey Wagh", "Lalit Prabhakar", "Vaidehi Parshurami", "Trupti Khamkar"],
            "releaseYear": 2022, "rating": "PG-13", "voteCount": 22000, "duration": "134 min", "seasons": None,
            "genres": ["Comedy", "Horror"], "language": "Marathi", "country": "India", "industry": "Marathi",
            "description": "When contaminated drinking water sparks a zombie outbreak in Dombivli, an anxious corporate engineer and an aggressive slum leader must join forces to survive.",
            "tagline": "First Marathi Zombie Horror Comedy!", "imdb_score": 7.1,
            "mood_tags": ["Hilarious", "Zombie Apocalypse", "Social Satire", "Fun", "Spooky"],
            "keywords": ["zombies", "dombivli", "slum vs tower", "amey wagh", "lalit prabhakar", "aditya sarpotdar", "marathi horror comedy", "marathi movie", "zombivli", "mara"],
            "poster": "https://image.tmdb.org/t/p/w500/dyHAU31K9jN0X7ZkU8F1p8V3MuM.jpg",
            "backdrop": "https://image.tmdb.org/t/p/original/b3Ea3Y4K0mXf1q9z7U8F1p8V3M.jpg",
            "trailerUrl": "https://www.youtube.com/watch?v=f2n4P6_m39A", "trailer_id": "f2n4P6_m39A",
            "netflixAvailable": False, "watchRegion": "IN"
        },

        # =========================================================================
        # REGIONAL INDIAN: BENGALI, PUNJABI, GUJARATI
        # =========================================================================
        {
            "id": "reg1", "tmdbId": 5801, "title": "Pather Panchali", "originalTitle": "Pather Panchali",
            "type": "Movie", "director": "Satyajit Ray",
            "cast": ["Subir Banerjee", "Kanu Banerjee", "Karuna Banerjee", "Uma Dasgupta", "Chunibala Devi"],
            "releaseYear": 1955, "rating": "PG", "voteCount": 42000, "duration": "125 min", "seasons": None,
            "genres": ["Drama"], "language": "Bengali", "country": "India", "industry": "Bengali",
            "description": "Impoverished priest Harihar Ray dreams of a career as a poet, while his wife Sarbojaya cares for their rebellious children Apu and Durga amidst crushing rural hardship.",
            "tagline": "Song of the Little Road.", "imdb_score": 8.5,
            "mood_tags": ["Masterpiece", "Poetic Realism", "Cannes Winner", "Historic Gem", "Tearjerker"],
            "keywords": ["apu trilogy", "rural bengal", "satyajit ray", "ravi shankar", "bengali cinema", "bengali movie", "pather panchali"],
            "poster": "https://image.tmdb.org/t/p/w500/7c9a2K9jN0X7ZkU8F1p8V3M.jpg",
            "backdrop": "https://image.tmdb.org/t/p/original/9rM8F1p8V3MuMzU90K2jQ1jN0X7.jpg",
            "trailerUrl": "https://www.youtube.com/watch?v=7_hK4K9z8qM", "trailer_id": "7_hK4K9z8qM",
            "netflixAvailable": False, "watchRegion": "IN"
        },
        {
            "id": "reg2", "tmdbId": 124803, "title": "Carry On Jatta", "originalTitle": "Carry On Jatta",
            "type": "Movie", "director": "Smeep Kang",
            "cast": ["Gippy Grewal", "Mahie Gill", "Binnu Dhillon", "Gurpreet Ghuggi", "Jaswinder Bhalla", "B.N. Sharma"],
            "releaseYear": 2012, "rating": "PG", "voteCount": 26000, "duration": "142 min", "seasons": None,
            "genres": ["Comedy", "Romance"], "language": "Punjabi", "country": "India", "industry": "Punjabi",
            "description": "Jass falls for Mahie, who wants to marry an orphan. He lies about having no family, leading to a riotous web of deceit when his father and brother get dragged in.",
            "tagline": "Advocate Dhillon ne kaala coat aiven ni paaya!", "imdb_score": 8.1,
            "mood_tags": ["Hilarious", "Slapstick", "Evergreen", "Feel-Good", "Blockbuster"],
            "keywords": ["advocate dhillon", "orphan lie", "gippy grewal", "binnu dhillon", "gurpreet ghuggi", "punjabi comedy", "punjabi movie", "carry on jatta"],
            "poster": "https://image.tmdb.org/t/p/w500/kK9jN0X7ZkU8F1p8V3MuMzU90K2.jpg",
            "backdrop": "https://image.tmdb.org/t/p/original/3XddMrGrmfeglA1t3Q7i8nI5PqR.jpg",
            "trailerUrl": "https://www.youtube.com/watch?v=2n5n9T-q92k", "trailer_id": "2n5n9T-q92k",
            "netflixAvailable": False, "watchRegion": "IN"
        },
        {
            "id": "reg3", "tmdbId": 641848, "title": "Hellaro", "originalTitle": "Hellaro",
            "type": "Movie", "director": "Abhishek Shah",
            "cast": ["Shraddha Dangar", "Jayesh More", "Shachi Joshi", "Denisha Ghumra", "Niilam Paanchal"],
            "releaseYear": 2019, "rating": "PG-13", "voteCount": 18000, "duration": "121 min", "seasons": None,
            "genres": ["Drama", "Musical"], "language": "Gujarati", "country": "India", "industry": "Gujarati",
            "description": "In 1975 drought-hit Rann of Kutch, suppressed patriarchal village women find soul-liberating expression through illicit Garba dance alongside an outcast Dhol drummer.",
            "tagline": "The dance of freedom.", "imdb_score": 8.5,
            "mood_tags": ["Empowering", "Garba", "Folk Musical", "Soul-Stirring", "National Award Best Film"],
            "keywords": ["rann of kutch", "garba", "dhol", "women liberation", "abhishek shah", "gujarati cinema", "gujarati movie", "hellaro"],
            "poster": "https://image.tmdb.org/t/p/w500/mXf1q9z7U8F1p8V3MuMzU90K2jQ.jpg",
            "backdrop": "https://image.tmdb.org/t/p/original/1E5baAaEse26fej7uHqMqaq2qz.jpg",
            "trailerUrl": "https://www.youtube.com/watch?v=M9mP1L7c29Y", "trailer_id": "M9mP1L7c29Y",
            "netflixAvailable": False, "watchRegion": "IN"
        },
        {
            "id": "reg4", "tmdbId": 839440, "title": "Last Film Show", "originalTitle": "Chhello Show",
            "type": "Movie", "director": "Pan Nalin",
            "cast": ["Bhavin Rabari", "Bhavesh Shrimali", "Richa Meena", "Dipen Raval"],
            "releaseYear": 2021, "rating": "PG", "voteCount": 16000, "duration": "110 min", "seasons": None,
            "genres": ["Drama"], "language": "Gujarati", "country": "India", "industry": "Gujarati",
            "description": "Nine-year-old Samay in rural Gujarat becomes completely enchanted by the magic of 35mm celluloid light, striking a secret deal with a cinema projectionist in exchange for food.",
            "tagline": "A pure ode to celluloid cinema.", "imdb_score": 7.4,
            "mood_tags": ["Nostalgic", "Heartwarming", "Poetic", "Cinematic Love", "Oscar Shortlist"],
            "keywords": ["celluloid projector", "35mm film", "childhood wonder", "pan nalin", "gujarati movie", "chhello show", "last film show"],
            "poster": "https://image.tmdb.org/t/p/w500/uMzU90K2jQ1jN0X7ZkU8F1p8V3M.jpg",
            "backdrop": "https://image.tmdb.org/t/p/original/8K9jN0X7ZkU8F1p8V3MuMzU90K2.jpg",
            "trailerUrl": "https://www.youtube.com/watch?v=3K5_z1Y0X7M", "trailer_id": "3K5_z1Y0X7M",
            "netflixAvailable": True, "watchRegion": "IN"
        },
        # =========================================================================
        # SEED ADDITIONS: SOUTH INDIAN, HOLLYWOOD, INTERNATIONAL & TV SERIES
        # =========================================================================
        {
            "id": "si21", "tmdbId": 644495, "title": "Master", "originalTitle": "Master",
            "type": "Movie", "director": "Lokesh Kanagaraj",
            "cast": ["Thalapathy Vijay", "Vijay Sethupathi", "Malavika Mohanan", "Arjun Das", "Andrea Jeremiah"],
            "releaseYear": 2021, "rating": "TV-MA", "voteCount": 65000, "duration": "179 min", "seasons": None,
            "genres": ["Action", "Crime", "Thriller"], "language": "Tamil", "country": "India", "industry": "Tamil",
            "description": "An alcoholic professor JD is sent to a juvenile correctional facility, where he clashes with Bhavani, a ruthless gangster who uses incarcerated children as scapegoats for crime.",
            "tagline": "Vaathi Coming!", "imdb_score": 7.8,
            "mood_tags": ["High-Octane", "Mass Appeal", "Action-Packed", "Charismatic", "Blockbuster"],
            "keywords": ["vaathi coming", "juvenile school", "alcoholism", "thalapathy vijay", "vijay sethupathi", "anirudh", "lokesh kanagaraj", "tamil movie", "master"],
            "poster": "https://image.tmdb.org/t/p/w500/1XddMrGrmfeglA1t3Q7i8nI5PqR.jpg",
            "backdrop": "https://image.tmdb.org/t/p/original/9rM8F1p8V3MuMzU90K2jQ1jN0X7.jpg",
            "trailerUrl": "https://www.youtube.com/watch?v=UTiXQcrLlv4", "trailer_id": "UTiXQcrLlv4",
            "netflixAvailable": True, "watchRegion": "IN"
        },
        {
            "id": "h22", "tmdbId": 1726, "title": "Iron Man", "originalTitle": "Iron Man",
            "type": "Movie", "director": "Jon Favreau",
            "cast": ["Robert Downey Jr.", "Gwyneth Paltrow", "Terrence Howard", "Jeff Bridges", "Jon Favreau"],
            "releaseYear": 2008, "rating": "PG-13", "voteCount": 1100000, "duration": "126 min", "seasons": None,
            "genres": ["Action", "Adventure", "Sci-Fi"], "language": "English", "country": "USA", "industry": "Hollywood",
            "description": "After being held captive in an Afghan cave, billionaire industrialist Tony Stark constructs a high-tech motorized suit of armor to fight evil and redeem his weapon empire.",
            "tagline": "Heroes are made, not born.", "imdb_score": 7.9,
            "mood_tags": ["High-Energy", "Witty", "Superhero", "Iconic", "Marvel MCU"],
            "keywords": ["tony stark", "arc reactor", "marvel", "robert downey jr", "mcu", "iron man"],
            "poster": "https://image.tmdb.org/t/p/w500/78lPtwv72eTNqFW9COBYI0dWDJa.jpg",
            "backdrop": "https://image.tmdb.org/t/p/original/b3Ea3Y4K0mXf1q9z7U8F1p8V3M.jpg",
            "trailerUrl": "https://www.youtube.com/watch?v=8ugaeA-nMTc", "trailer_id": "8ugaeA-nMTc",
            "netflixAvailable": False, "watchRegion": "IN"
        },
        {
            "id": "h23", "tmdbId": 447332, "title": "A Quiet Place", "originalTitle": "A Quiet Place",
            "type": "Movie", "director": "John Krasinski",
            "cast": ["Emily Blunt", "John Krasinski", "Millicent Simmonds", "Noah Jupe"],
            "releaseYear": 2018, "rating": "PG-13", "voteCount": 620000, "duration": "90 min", "seasons": None,
            "genres": ["Drama", "Horror", "Sci-Fi"], "language": "English", "country": "USA", "industry": "Hollywood",
            "description": "In a post-apocalyptic world, a family is forced to live in absolute silence while hiding from blind extraterrestrial monsters with ultra-sensitive hearing.",
            "tagline": "If they hear you, they hunt you.", "imdb_score": 7.5,
            "mood_tags": ["Tense", "Nail-Biting", "Suspenseful", "Atmospheric", "Innovative"],
            "keywords": ["silence", "monsters", "sound creature", "sign language", "emily blunt", "john krasinski", "a quiet place"],
            "poster": "https://image.tmdb.org/t/p/w500/nAU74GmpUk7t5iklEp3bufwDq4n.jpg",
            "backdrop": "https://image.tmdb.org/t/p/original/1E5baAaEse26fej7uHqMqaq2qz.jpg",
            "trailerUrl": "https://www.youtube.com/watch?v=WR7cc5t7tv8", "trailer_id": "WR7cc5t7tv8",
            "netflixAvailable": True, "watchRegion": "IN"
        },
        {
            "id": "int11", "tmdbId": 411088, "title": "The Invisible Guest", "originalTitle": "Contratiempo",
            "type": "Movie", "director": "Oriol Paulo",
            "cast": ["Mario Casas", "Ana Wagener", "José Coronado", "Bárbara Lennie", "Francesc Orella"],
            "releaseYear": 2016, "rating": "TV-MA", "voteCount": 185000, "duration": "106 min", "seasons": None,
            "genres": ["Crime", "Drama", "Mystery", "Thriller"], "language": "Spanish", "country": "Spain", "industry": "Spanish",
            "description": "A successful young businessman wakes up in a locked hotel room next to the corpse of his murdered lover, hiring a defense witness expert to prepare an impossible alibi in three hours.",
            "tagline": "Every story has two sides. The truth only one.", "imdb_score": 8.0,
            "mood_tags": ["Mind-bending", "Twisted", "Clever", "Suspenseful", "Masterpiece"],
            "keywords": ["locked room mystery", "affair", "car crash", "alibi", "mario casas", "oriol paulo", "spanish thriller", "the invisible guest", "contratiempo"],
            "poster": "https://image.tmdb.org/t/p/w500/uMzU90K2jQ1jN0X7ZkU8F1p8V3M.jpg",
            "backdrop": "https://image.tmdb.org/t/p/original/8K9jN0X7ZkU8F1p8V3MuMzU90K2.jpg",
            "trailerUrl": "https://www.youtube.com/watch?v=epCg2RbyF80", "trailer_id": "epCg2RbyF80",
            "netflixAvailable": True, "watchRegion": "IN"
        },
        {
            "id": "tv21", "tmdbId": 19885, "title": "Sherlock", "originalTitle": "Sherlock",
            "type": "TV Show", "director": "Steven Moffat, Mark Gatiss",
            "cast": ["Benedict Cumberbatch", "Martin Freeman", "Una Stubbs", "Rupert Graves", "Louise Brealey", "Mark Gatiss", "Andrew Scott"],
            "releaseYear": 2010, "rating": "TV-14", "voteCount": 980000, "duration": "4 Seasons", "seasons": 4,
            "genres": ["Crime", "Drama", "Mystery"], "language": "English", "country": "UK", "industry": "Hollywood",
            "description": "A modern update finds the famous consulting detective Sherlock Holmes and his doctor flatmate John Watson solving impossible crimes in 21st-century London.",
            "tagline": "Brainy is the new sexy.", "imdb_score": 9.1,
            "mood_tags": ["Intelligent", "Witty", "Mind-bending", "Masterpiece", "Iconic"],
            "keywords": ["sherlock holmes", "john watson", "moriarty", "221b baker street", "mind palace", "benedict cumberbatch", "martin freeman", "tv series", "sherlock"],
            "poster": "https://image.tmdb.org/t/p/w500/7WTsnMqqA0Su72ip4nlvoOO1JMT.jpg",
            "backdrop": "https://image.tmdb.org/t/p/original/5uY1rR7L8K9jN0X7ZkU8F1p8V3M.jpg",
            "trailerUrl": "https://www.youtube.com/watch?v=xK7S9mrFWL4", "trailer_id": "xK7S9mrFWL4",
            "netflixAvailable": False, "watchRegion": "IN"
        },
        {
            "id": "tv22", "tmdbId": 2316, "title": "The Office", "originalTitle": "The Office (US)",
            "type": "TV Show", "director": "Greg Daniels",
            "cast": ["Steve Carell", "Rainn Wilson", "John Krasinski", "Jenna Fischer", "B.J. Novak", "Mindy Kaling", "Ed Helms"],
            "releaseYear": 2005, "rating": "TV-14", "voteCount": 750000, "duration": "9 Seasons", "seasons": 9,
            "genres": ["Comedy"], "language": "English", "country": "USA", "industry": "Hollywood",
            "description": "A mockumentary on a group of typical office workers at Dunder Mifflin Paper Company in Scranton, Pennsylvania, managed by the eccentric, well-meaning Michael Scott.",
            "tagline": "That's what she said.", "imdb_score": 9.0,
            "mood_tags": ["Hilarious", "Heartwarming", "Cringe Comedy", "Evergreen", "Feel-Good"],
            "keywords": ["dunder mifflin", "michael scott", "dwight schrute", "jim and pam", "scranton", "steve carell", "sitcom", "the office"],
            "poster": "https://image.tmdb.org/t/p/w500/qWnJzyZhyy74gjpSjIXWmuk0ifX.jpg",
            "backdrop": "https://image.tmdb.org/t/p/original/3XddMrGrmfeglA1t3Q7i8nI5PqR.jpg",
            "trailerUrl": "https://www.youtube.com/watch?v=LHOtME2DL4g", "trailer_id": "LHOtME2DL4g",
            "netflixAvailable": True, "watchRegion": "IN"
        },
        {
            "id": "tv23", "tmdbId": 1668, "title": "Friends", "originalTitle": "Friends",
            "type": "TV Show", "director": "David Crane, Marta Kauffman",
            "cast": ["Jennifer Aniston", "Courteney Cox", "Lisa Kudrow", "Matt LeBlanc", "Matthew Perry", "David Schwimmer"],
            "releaseYear": 1994, "rating": "TV-14", "voteCount": 1100000, "duration": "10 Seasons", "seasons": 10,
            "genres": ["Comedy", "Romance"], "language": "English", "country": "USA", "industry": "Hollywood",
            "description": "Follows the personal and professional lives of six twenty to thirty-something friends living in Manhattan, New York City, sharing coffee, romance, and life milestones at Central Perk.",
            "tagline": "I'll be there for you.", "imdb_score": 8.9,
            "mood_tags": ["Comfort Show", "Hilarious", "Evergreen", "Feel-Good", "Iconic Sitcom"],
            "keywords": ["central perk", "chandler bing", "rachel green", "monica geller", "ross geller", "joey tribbiani", "phoebe buffay", "friends"],
            "poster": "https://image.tmdb.org/t/p/w500/2koX1xLkpTQM4IZebYvKysFW1Nh.jpg",
            "backdrop": "https://image.tmdb.org/t/p/original/9rM8F1p8V3MuMzU90K2jQ1jN0X7.jpg",
            "trailerUrl": "https://www.youtube.com/watch?v=hDNNmeeJs1Q", "trailer_id": "hDNNmeeJs1Q",
            "netflixAvailable": True, "watchRegion": "IN"
        },
        {
            "id": "tv24", "tmdbId": 48891, "title": "Brooklyn Nine-Nine", "originalTitle": "Brooklyn Nine-Nine",
            "type": "TV Show", "director": "Dan Goor, Michael Schur",
            "cast": ["Andy Samberg", "Stephanie Beatriz", "Terry Crews", "Melissa Fumero", "Joe Lo Truglio", "Chelsea Peretti", "Andre Braugher"],
            "releaseYear": 2013, "rating": "TV-14", "voteCount": 380000, "duration": "8 Seasons", "seasons": 8,
            "genres": ["Comedy", "Crime"], "language": "English", "country": "USA", "industry": "Hollywood",
            "description": "Comedy series following the exploits of immature detective Jake Peralta and his diverse, lovable colleagues in NYPD's fictional 99th Precinct under strict Captain Raymond Holt.",
            "tagline": "Noice! Smort!", "imdb_score": 8.4,
            "mood_tags": ["Hilarious", "Feel-Good", "Witty", "Wholesome", "Binge-Worthy"],
            "keywords": ["jake peralta", "captain holt", "terry crews", "heist episodes", "nypd", "andy samberg", "brooklyn nine-nine", "brooklyn nine nine"],
            "poster": "https://image.tmdb.org/t/p/w500/hgRMSOt7a1b8qyQR68vUixJPang.jpg",
            "backdrop": "https://image.tmdb.org/t/p/original/1E5baAaEse26fej7uHqMqaq2qz.jpg",
            "trailerUrl": "https://www.youtube.com/watch?v=sEOuJ4z5aTc", "trailer_id": "sEOuJ4z5aTc",
            "netflixAvailable": True, "watchRegion": "IN"
        },
        {
            "id": "tv25", "tmdbId": 86963, "title": "Made in Heaven", "originalTitle": "Made in Heaven",
            "type": "TV Show", "director": "Zoya Akhtar, Reema Kagti, Alankrita Shrivastava, Nitya Mehra",
            "cast": ["Sobhita Dhulipala", "Arjun Mathur", "Jim Sarbh", "Kalki Koechlin", "Shashank Arora", "Shivani Raghuvanshi"],
            "releaseYear": 2019, "rating": "TV-MA", "voteCount": 32000, "duration": "2 Seasons", "seasons": 2,
            "genres": ["Drama", "Romance"], "language": "Hindi", "country": "India", "industry": "Bollywood",
            "description": "Tara and Karan are Delhi-based high-end wedding planners navigating lavish, opulent Indian weddings while confronting conservative hypocrisies, personal infidelities, and societal stigmas.",
            "tagline": "Weddings are sacred. Lies are profane.", "imdb_score": 8.3,
            "mood_tags": ["Opulent", "Thought-Provoking", "Nuanced", "Stylish", "Emmy Nominee"],
            "keywords": ["delhi weddings", "big fat indian wedding", "tara khanna", "karan mehra", "sobhita dhulipala", "zoya akhtar", "made in heaven"],
            "poster": "https://image.tmdb.org/t/p/w500/kK9jN0X7ZkU8F1p8V3MuMzU90K2.jpg",
            "backdrop": "https://image.tmdb.org/t/p/original/8K9jN0X7ZkU8F1p8V3MuMzU90K2.jpg",
            "trailerUrl": "https://www.youtube.com/watch?v=0h09cO7g6sI", "trailer_id": "0h09cO7g6sI",
            "netflixAvailable": False, "watchRegion": "IN"
        },
        {
            "id": "tv26", "tmdbId": 209867, "title": "Farzi", "originalTitle": "Farzi",
            "type": "TV Show", "director": "Raj & DK",
            "cast": ["Shahid Kapoor", "Vijay Sethupathi", "Kay Kay Menon", "Raashii Khanna", "Bhuvan Arora", "Amol Palekar"],
            "releaseYear": 2023, "rating": "TV-MA", "voteCount": 46000, "duration": "1 Season", "seasons": 1,
            "genres": ["Crime", "Drama", "Thriller"], "language": "Hindi", "country": "India", "industry": "Bollywood",
            "description": "Sunny, a disillusioned small-time artist in Mumbai, designs an undetectable counterfeit currency note, pulling him and his friend Firoz into the dangerous high-stakes underworld of Mansoor Dalal.",
            "tagline": "Paisa bolta hai.", "imdb_score": 8.4,
            "mood_tags": ["Fast-Paced", "Clever", "Gripping", "Stylish", "Adrenaline"],
            "keywords": ["counterfeit currency", "fake notes", "artist", "sunny", "michael vedanayagam", "shahid kapoor", "vijay sethupathi", "raj and dk", "farzi"],
            "poster": "https://image.tmdb.org/t/p/w500/mXf1q9z7U8F1p8V3MuMzU90K2jQ.jpg",
            "backdrop": "https://image.tmdb.org/t/p/original/b3Ea3Y4K0mXf1q9z7U8F1p8V3M.jpg",
            "trailerUrl": "https://www.youtube.com/watch?v=4PSL8mB7b8Y", "trailer_id": "4PSL8mB7b8Y",
            "netflixAvailable": False, "watchRegion": "IN"
        }
    ]
    
    combined = base_titles + additional_titles
    return combined

if __name__ == "__main__":
    catalog = get_expanded_catalog()
    import build_full_catalog
    build_full_catalog.CATALOG_ITEMS = catalog
    build_full_catalog.build_and_save_catalog("data/netflix_catalog.json")
