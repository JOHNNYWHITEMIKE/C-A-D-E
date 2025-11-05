"""
Sample data for C-A-D-E
Initialize with example agents and projects
"""

def get_sample_agents():
    """Return sample AI agents for demonstration"""
    return [
        {
            "id": "hello-world",
            "name": "Hello World Agent",
            "description": "A simple agent that greets the world. Perfect for testing the platform.",
            "category": "Autonomous Agents",
            "framework": "Custom",
            "language": "Python",
            "code": """# Hello World Agent
def main():
    message = "Hello from C-A-D-E!"
    print(message)
    return {
        "status": "success",
        "message": message,
        "platform": "C-A-D-E v1.0"
    }

if __name__ == "__main__":
    result = main()
    print(result)
"""
        },
        {
            "id": "data-analyzer",
            "name": "Data Analyzer",
            "description": "Analyzes data and generates insights using statistical methods.",
            "category": "Data Analysis",
            "framework": "Custom",
            "language": "Python",
            "code": """# Data Analyzer Agent
import json

def analyze_data(data):
    # Basic statistical analysis
    if not data:
        return {"error": "No data provided"}
    
    total = sum(data)
    avg = total / len(data)
    max_val = max(data)
    min_val = min(data)
    
    return {
        "count": len(data),
        "total": total,
        "average": avg,
        "maximum": max_val,
        "minimum": min_val
    }

def main():
    sample_data = [10, 20, 30, 40, 50]
    result = analyze_data(sample_data)
    print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    main()
"""
        },
        {
            "id": "code-generator",
            "name": "Code Generator",
            "description": "Generates boilerplate code for common programming tasks.",
            "category": "Code Generation",
            "framework": "Custom",
            "language": "Python",
            "code": """# Code Generator Agent
def generate_class(class_name, attributes):
    code = f"class {class_name}:\\n"
    code += "    def __init__(self"
    
    for attr in attributes:
        code += f", {attr}"
    code += "):\\n"
    
    for attr in attributes:
        code += f"        self.{attr} = {attr}\\n"
    
    return code

def main():
    class_name = "Person"
    attributes = ["name", "age", "email"]
    
    generated_code = generate_class(class_name, attributes)
    print("Generated Code:")
    print(generated_code)
    
    return {
        "status": "success",
        "code": generated_code
    }

if __name__ == "__main__":
    main()
"""
        },
        {
            "id": "text-summarizer",
            "name": "Text Summarizer",
            "description": "Summarizes long text into concise key points.",
            "category": "NLP & Chat",
            "framework": "Custom",
            "language": "Python",
            "code": """# Text Summarizer Agent
def summarize_text(text, max_sentences=3):
    # Simple extractive summarization
    sentences = text.split('.')
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Return first N sentences as summary
    summary = '. '.join(sentences[:max_sentences]) + '.'
    
    return {
        "original_length": len(text),
        "summary_length": len(summary),
        "summary": summary
    }

def main():
    sample_text = '''
    Artificial Intelligence is transforming industries. 
    Machine learning enables computers to learn from data. 
    Deep learning uses neural networks for complex tasks. 
    AI agents can automate repetitive work. 
    The future of AI is promising and exciting.
    '''
    
    result = summarize_text(sample_text.strip())
    print(f"Summary: {result['summary']}")
    return result

if __name__ == "__main__":
    main()
"""
        },
        {
            "id": "web-scraper",
            "name": "Web Scraper",
            "description": "Extracts and processes data from web pages.",
            "category": "Web Automation",
            "framework": "Custom",
            "language": "Python",
            "code": """# Web Scraper Agent
# Note: This is a simplified example
# In production, use libraries like requests, beautifulsoup4

def scrape_data(url):
    # Simulated scraping (placeholder)
    return {
        "url": url,
        "status": "success",
        "data": {
            "title": "Sample Page",
            "links": ["link1", "link2", "link3"],
            "paragraphs": 5
        }
    }

def main():
    target_url = "https://example.com"
    result = scrape_data(target_url)
    
    print(f"Scraped {target_url}")
    print(f"Found {len(result['data']['links'])} links")
    
    return result

if __name__ == "__main__":
    main()
"""
        },
        {
            "id": "task-scheduler",
            "name": "Task Scheduler",
            "description": "Schedules and manages automated tasks.",
            "category": "Workflow Automation",
            "framework": "Custom",
            "language": "Python",
            "code": """# Task Scheduler Agent
from datetime import datetime, timedelta

class TaskScheduler:
    def __init__(self):
        self.tasks = []
    
    def add_task(self, name, schedule_time):
        task = {
            "name": name,
            "scheduled_for": schedule_time,
            "status": "pending"
        }
        self.tasks.append(task)
        return task
    
    def get_pending_tasks(self):
        return [t for t in self.tasks if t["status"] == "pending"]

def main():
    scheduler = TaskScheduler()
    
    # Add sample tasks
    scheduler.add_task("Daily Backup", "09:00")
    scheduler.add_task("Report Generation", "17:00")
    scheduler.add_task("Data Sync", "12:00")
    
    pending = scheduler.get_pending_tasks()
    print(f"Pending tasks: {len(pending)}")
    
    for task in pending:
        print(f"- {task['name']} at {task['scheduled_for']}")
    
    return {
        "total_tasks": len(scheduler.tasks),
        "pending_tasks": len(pending)
    }

if __name__ == "__main__":
    main()
"""
        }
    ]

def get_sample_projects():
    """Return sample projects for demonstration"""
    return [
        {
            "id": "demo-project",
            "name": "Demo Project",
            "description": "A sample project showcasing C-A-D-E capabilities",
            "agents": ["hello-world", "data-analyzer"]
        },
        {
            "id": "automation-suite",
            "name": "Automation Suite",
            "description": "Collection of automation agents",
            "agents": ["web-scraper", "task-scheduler"]
        }
    ]
