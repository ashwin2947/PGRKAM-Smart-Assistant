import os
import json
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# MongoDB setup
client = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017"))
db = client[os.getenv("DB_NAME", "pgrkam")]

# Collections
schemes_collection = db["schemes"]
training_collection = db["training_programs"]
news_collection = db["news_updates"]

# Government Schemes Data
schemes_data = [
    {
        "name": "Punjab Ghar Ghar Rozgar Scheme",
        "description": "Employment generation scheme providing job opportunities to every household in Punjab",
        "benefits": "Direct employment, skill training, financial assistance",
        "eligibility": "Punjab residents, age 18-45, unemployed",
        "category": "employment"
    },
    {
        "name": "Skill Development Program",
        "description": "Free skill training for unemployed youth in various trades",
        "benefits": "Free training, certification, job placement assistance",
        "eligibility": "Age 18-35, minimum 8th pass, unemployed",
        "category": "skill_development"
    },
    {
        "name": "Self Employment Scheme",
        "description": "Financial assistance for starting own business or enterprise",
        "benefits": "Loan up to 5 lakhs, subsidy, business mentoring",
        "eligibility": "Age 21-45, business plan required, Punjab resident",
        "category": "entrepreneurship"
    },
    {
        "name": "Women Empowerment Scheme",
        "description": "Special employment opportunities and skill training for women",
        "benefits": "Priority in jobs, free training, childcare support",
        "eligibility": "Women aged 18-50, Punjab resident",
        "category": "women_empowerment"
    },
    {
        "name": "Rural Employment Guarantee",
        "description": "Guaranteed 100 days employment in rural areas",
        "benefits": "Minimum wage guarantee, local employment",
        "eligibility": "Rural residents, willing to do manual work",
        "category": "rural_employment"
    },
    {
        "name": "Youth Entrepreneurship Scheme",
        "description": "Support for young entrepreneurs to start innovative businesses",
        "benefits": "Seed funding, incubation support, mentorship",
        "eligibility": "Age 18-30, innovative business idea, graduate",
        "category": "youth_entrepreneurship"
    },
    {
        "name": "Farmer Producer Organization Support",
        "description": "Support for farmers to form collectives and improve income",
        "benefits": "Technical support, market linkage, financial assistance",
        "eligibility": "Farmers, willing to form groups",
        "category": "agriculture"
    },
    {
        "name": "Digital Punjab Initiative",
        "description": "Digital literacy and online service delivery program",
        "benefits": "Free digital training, online services access",
        "eligibility": "All Punjab residents",
        "category": "digital_literacy"
    }
]

# Training Programs Data
training_data = [
    {
        "name": "Computer Training Program",
        "description": "Basic computer skills including MS Office, internet usage",
        "duration": "3 months",
        "certification": "Government certified",
        "eligibility": "Minimum 10th pass, age 18-40"
    },
    {
        "name": "Vocational Training",
        "description": "Trade-specific skills like plumbing, electrical, carpentry",
        "duration": "6 months",
        "certification": "NCVT certified",
        "eligibility": "Age 16-35, willing to learn trades"
    },
    {
        "name": "Digital Marketing Course",
        "description": "Online marketing, social media, e-commerce skills",
        "duration": "4 months",
        "certification": "Industry recognized",
        "eligibility": "Graduate, basic computer knowledge"
    },
    {
        "name": "Entrepreneurship Development",
        "description": "Business planning, financial management, marketing skills",
        "duration": "2 months",
        "certification": "EDI certified",
        "eligibility": "Age 21-45, business interest"
    },
    {
        "name": "Technical Skills Training",
        "description": "Industry 4.0 skills, automation, robotics basics",
        "duration": "8 months",
        "certification": "Technical board certified",
        "eligibility": "ITI/Diploma holders, age 18-30"
    },
    {
        "name": "Soft Skills Development",
        "description": "Communication, leadership, teamwork skills",
        "duration": "1 month",
        "certification": "Completion certificate",
        "eligibility": "All job seekers"
    },
    {
        "name": "Financial Literacy Program",
        "description": "Banking, insurance, investment awareness",
        "duration": "2 weeks",
        "certification": "Financial literacy certificate",
        "eligibility": "All adults"
    }
]

# News/Updates Data
news_data = [
    {
        "title": "New Job Opportunities in IT Sector",
        "content": "Punjab government announces 5000 new IT jobs in collaboration with tech companies",
        "date": "2024-01-15",
        "category": "job_announcement"
    },
    {
        "title": "Skill Development Centers Expansion",
        "content": "50 new skill development centers to be opened across Punjab districts",
        "date": "2024-01-10",
        "category": "infrastructure"
    },
    {
        "title": "Women Employment Drive",
        "content": "Special recruitment drive for women in government departments",
        "date": "2024-01-08",
        "category": "employment_drive"
    },
    {
        "title": "Digital Services Launch",
        "content": "New online portal for job applications and skill training registration",
        "date": "2024-01-05",
        "category": "digital_services"
    },
    {
        "title": "Rural Employment Scheme Update",
        "content": "Enhanced benefits and increased wage rates under rural employment guarantee",
        "date": "2024-01-03",
        "category": "scheme_update"
    }
]

def ingest_content():
    # Ingest schemes
    for scheme in schemes_data:
        scheme["source"] = "scheme"
        schemes_collection.update_one(
            {"name": scheme["name"]},
            {"$set": scheme},
            upsert=True
        )
    
    # Ingest training programs
    for program in training_data:
        program["source"] = "training"
        training_collection.update_one(
            {"name": program["name"]},
            {"$set": program},
            upsert=True
        )
    
    # Ingest news/updates
    for news in news_data:
        news["source"] = "news"
        news_collection.update_one(
            {"title": news["title"]},
            {"$set": news},
            upsert=True
        )
    
    # Create text indexes
    try:
        schemes_collection.create_index([("name", "text"), ("description", "text"), ("benefits", "text")])
        training_collection.create_index([("name", "text"), ("description", "text")])
        news_collection.create_index([("title", "text"), ("content", "text")])
        print("Text indexes created")
    except Exception:
        pass
    
    print(f"Ingested {len(schemes_data)} schemes")
    print(f"Ingested {len(training_data)} training programs")
    print(f"Ingested {len(news_data)} news updates")

if __name__ == "__main__":
    ingest_content()