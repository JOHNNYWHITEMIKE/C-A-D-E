"""
Task Routing Engine
Analyzes freelance jobs and delegates to appropriate AI agents
"""
import re
from typing import List, Dict, Optional, Tuple
import spacy
from sentence_transformers import SentenceTransformer, util
import yaml
import os

class TaskRouter:
    """Routes freelance jobs to the most appropriate AI agent"""
    
    def __init__(self, agents_manifest_path: str = "agents/agents.yaml"):
        """
        Initialize the task router
        
        Args:
            agents_manifest_path: Path to the agents configuration file
        """
        # Load NLP model for text processing
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Downloading spaCy model...")
            os.system("python -m spacy download en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")
        
        # Load sentence transformer for semantic similarity
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Load agent configurations
        self.agents_manifest_path = agents_manifest_path
        self.agents = self._load_agents()
        
        # Skill taxonomy
        self.skill_categories = {
            "web_development": [
                "react", "vue", "angular", "html", "css", "javascript",
                "typescript", "node.js", "express", "django", "flask",
                "fastapi", "php", "laravel", "wordpress", "frontend", "backend"
            ],
            "data_science": [
                "python", "pandas", "numpy", "scikit-learn", "tensorflow",
                "pytorch", "machine learning", "ml", "ai", "data analysis",
                "visualization", "matplotlib", "seaborn", "jupyter"
            ],
            "mobile_development": [
                "react native", "flutter", "swift", "kotlin", "ios",
                "android", "mobile", "app development"
            ],
            "devops": [
                "docker", "kubernetes", "k8s", "ci/cd", "jenkins",
                "github actions", "aws", "azure", "gcp", "terraform",
                "ansible", "linux", "bash", "deployment"
            ],
            "api_development": [
                "rest", "api", "graphql", "websocket", "microservices",
                "postman", "swagger", "openapi"
            ],
            "database": [
                "postgresql", "mysql", "mongodb", "redis", "sql",
                "database", "orm", "sqlalchemy"
            ],
            "automation": [
                "selenium", "puppeteer", "playwright", "web scraping",
                "automation", "testing", "pytest", "jest"
            ],
            "design": [
                "ui", "ux", "figma", "sketch", "adobe", "design",
                "photoshop", "illustrator", "wireframe", "prototype"
            ]
        }
    
    def _load_agents(self) -> List[Dict]:
        """Load agent configurations from manifest file"""
        if not os.path.exists(self.agents_manifest_path):
            # Return default agents if manifest doesn't exist
            return self._get_default_agents()
        
        with open(self.agents_manifest_path, 'r') as f:
            manifest = yaml.safe_load(f)
            return manifest.get('agents', [])
    
    def _get_default_agents(self) -> List[Dict]:
        """Return default agent configurations"""
        return [
            {
                "id": "python-web-dev",
                "name": "Python Web Developer",
                "skills": ["Python", "Django", "FastAPI", "PostgreSQL", "Docker"],
                "categories": ["web_development", "api_development", "database"],
                "docker_image": "ghcr.io/johnnywhitemike/agents/python-web:latest",
                "performance_score": 0.95,
                "hourly_cost": 25
            },
            {
                "id": "web-scraper",
                "name": "Web Scraping Specialist",
                "skills": ["Python", "Selenium", "BeautifulSoup", "Scrapy"],
                "categories": ["automation", "data_science"],
                "docker_image": "ghcr.io/johnnywhitemike/agents/web-scraper:latest",
                "performance_score": 0.92,
                "hourly_cost": 20
            },
            {
                "id": "data-analyst",
                "name": "Data Analysis Expert",
                "skills": ["Python", "Pandas", "NumPy", "Matplotlib", "SQL"],
                "categories": ["data_science", "database"],
                "docker_image": "ghcr.io/johnnywhitemike/agents/data-analyst:latest",
                "performance_score": 0.90,
                "hourly_cost": 30
            },
            {
                "id": "react-developer",
                "name": "React Frontend Developer",
                "skills": ["React", "JavaScript", "TypeScript", "CSS", "HTML"],
                "categories": ["web_development"],
                "docker_image": "ghcr.io/johnnywhitemike/agents/react-dev:latest",
                "performance_score": 0.88,
                "hourly_cost": 28
            }
        ]
    
    def analyze_job(self, job_description: str, job_title: str = "") -> Dict:
        """
        Analyze a job posting to extract requirements
        
        Args:
            job_description: The full job description text
            job_title: Optional job title
            
        Returns:
            Dictionary containing parsed job requirements
        """
        # Combine title and description
        full_text = f"{job_title} {job_description}".lower()
        
        # Extract skills mentioned
        skills = self._extract_skills(full_text)
        
        # Classify job category
        categories = self._classify_categories(skills)
        
        # Extract budget information
        budget = self._extract_budget(full_text)
        
        # Extract timeline
        timeline = self._extract_timeline(full_text)
        
        # Estimate complexity
        complexity = self._estimate_complexity(full_text, skills)
        
        return {
            "skills_required": skills,
            "categories": categories,
            "budget": budget,
            "timeline": timeline,
            "complexity": complexity,
            "raw_text": full_text
        }
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract technical skills from job description"""
        skills_found = set()
        
        # Check all skill categories
        for category, skill_list in self.skill_categories.items():
            for skill in skill_list:
                # Use word boundaries to avoid partial matches
                pattern = r'\b' + re.escape(skill.lower()) + r'\b'
                if re.search(pattern, text):
                    skills_found.add(skill)
        
        return list(skills_found)
    
    def _classify_categories(self, skills: List[str]) -> List[str]:
        """Classify job into categories based on skills"""
        category_scores = {}
        
        for category, skill_list in self.skill_categories.items():
            # Count how many skills from this category are present
            overlap = len(set(skills) & set(skill_list))
            if overlap > 0:
                category_scores[category] = overlap
        
        # Return categories sorted by relevance
        sorted_categories = sorted(
            category_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [cat for cat, score in sorted_categories if score > 0]
    
    def _extract_budget(self, text: str) -> Optional[Dict]:
        """Extract budget information from text"""
        # Look for dollar amounts
        budget_patterns = [
            r'\$(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:to|-)\s*\$(\d+(?:,\d{3})*(?:\.\d{2})?)',
            r'\$(\d+(?:,\d{3})*(?:\.\d{2})?)',
            r'budget.*?\$?(\d+)',
        ]
        
        for pattern in budget_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                if len(match.groups()) == 2:
                    return {
                        "min": float(match.group(1).replace(',', '')),
                        "max": float(match.group(2).replace(',', '')),
                        "type": "range"
                    }
                else:
                    return {
                        "amount": float(match.group(1).replace(',', '')),
                        "type": "fixed"
                    }
        
        return None
    
    def _extract_timeline(self, text: str) -> Optional[str]:
        """Extract timeline/deadline from text"""
        timeline_patterns = [
            r'(\d+)\s+(?:days?|weeks?|months?)',
            r'deadline.*?(\d+/\d+/\d+)',
            r'asap|urgent|immediately'
        ]
        
        for pattern in timeline_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        
        return None
    
    def _estimate_complexity(self, text: str, skills: List[str]) -> str:
        """Estimate job complexity based on various factors"""
        complexity_score = 0
        
        # Factor 1: Number of skills required
        if len(skills) > 8:
            complexity_score += 3
        elif len(skills) > 4:
            complexity_score += 2
        else:
            complexity_score += 1
        
        # Factor 2: Keywords indicating complexity
        complex_keywords = [
            'scalable', 'enterprise', 'production', 'distributed',
            'high-performance', 'real-time', 'ml', 'ai', 'microservices'
        ]
        complexity_score += sum(1 for kw in complex_keywords if kw in text)
        
        # Factor 3: Integration requirements
        if 'integrate' in text or 'api' in text:
            complexity_score += 1
        
        # Classify complexity
        if complexity_score >= 6:
            return "high"
        elif complexity_score >= 3:
            return "medium"
        else:
            return "low"
    
    def find_best_agent(
        self,
        job_requirements: Dict,
        consider_availability: bool = True,
        consider_cost: bool = True
    ) -> Tuple[Optional[Dict], float]:
        """
        Find the best agent for a job based on requirements
        
        Args:
            job_requirements: Output from analyze_job()
            consider_availability: Factor in agent availability
            consider_cost: Factor in agent cost
            
        Returns:
            Tuple of (best_agent, confidence_score)
        """
        scores = []
        
        for agent in self.agents:
            score = self._score_agent(
                agent,
                job_requirements,
                consider_availability,
                consider_cost
            )
            scores.append((agent, score))
        
        # Sort by score descending
        scores.sort(key=lambda x: x[1], reverse=True)
        
        if scores:
            best_agent, confidence = scores[0]
            return best_agent, confidence
        
        return None, 0.0
    
    def _score_agent(
        self,
        agent: Dict,
        requirements: Dict,
        consider_availability: bool,
        consider_cost: bool
    ) -> float:
        """Score an agent's suitability for a job"""
        
        # Skill matching (40% weight)
        skill_score = self._calculate_skill_match(
            agent.get('skills', []),
            requirements.get('skills_required', [])
        )
        
        # Category matching (30% weight)
        category_score = self._calculate_category_match(
            agent.get('categories', []),
            requirements.get('categories', [])
        )
        
        # Performance history (20% weight)
        performance_score = agent.get('performance_score', 0.5)
        
        # Availability (10% weight if enabled)
        availability_score = 1.0 if agent.get('status', 'available') == 'available' else 0.0
        
        # Calculate weighted score
        if consider_availability and consider_cost:
            total_score = (
                skill_score * 0.40 +
                category_score * 0.30 +
                performance_score * 0.20 +
                availability_score * 0.10
            )
        elif consider_availability:
            total_score = (
                skill_score * 0.45 +
                category_score * 0.35 +
                performance_score * 0.10 +
                availability_score * 0.10
            )
        else:
            total_score = (
                skill_score * 0.50 +
                category_score * 0.35 +
                performance_score * 0.15
            )
        
        return total_score
    
    def _calculate_skill_match(self, agent_skills: List[str], required_skills: List[str]) -> float:
        """Calculate skill match score using semantic similarity"""
        if not required_skills:
            return 0.5  # Neutral score if no specific skills required
        
        if not agent_skills:
            return 0.0
        
        # Convert to lowercase for comparison
        agent_skills_lower = [s.lower() for s in agent_skills]
        required_skills_lower = [s.lower() for s in required_skills]
        
        # Simple overlap
        overlap = len(set(agent_skills_lower) & set(required_skills_lower))
        
        # Calculate Jaccard similarity
        union = len(set(agent_skills_lower) | set(required_skills_lower))
        jaccard_score = overlap / union if union > 0 else 0
        
        return jaccard_score
    
    def _calculate_category_match(self, agent_categories: List[str], job_categories: List[str]) -> float:
        """Calculate category match score"""
        if not job_categories:
            return 0.5
        
        if not agent_categories:
            return 0.0
        
        overlap = len(set(agent_categories) & set(job_categories))
        return overlap / len(job_categories) if job_categories else 0.0
    
    def estimate_task_duration(self, job_requirements: Dict, agent: Dict) -> float:
        """
        Estimate task duration in hours
        
        Args:
            job_requirements: Parsed job requirements
            agent: Selected agent
            
        Returns:
            Estimated hours
        """
        # Base hours by complexity
        base_hours = {
            "low": 4,
            "medium": 16,
            "high": 40
        }
        
        complexity = job_requirements.get('complexity', 'medium')
        hours = base_hours.get(complexity, 16)
        
        # Adjust based on agent performance
        performance_multiplier = 1.5 - (agent.get('performance_score', 0.5) * 0.5)
        adjusted_hours = hours * performance_multiplier
        
        return round(adjusted_hours, 1)
    
    def estimate_cost(self, hours: float, agent: Dict) -> float:
        """Estimate cost for the task"""
        hourly_cost = agent.get('hourly_cost', 25)
        return round(hours * hourly_cost, 2)


# Example usage
if __name__ == "__main__":
    # Initialize router
    router = TaskRouter()
    
    # Example job posting
    job_description = """
    Need an experienced Python developer to build a web scraping tool
    that can extract product data from e-commerce websites.
    
    Requirements:
    - Python expertise
    - Experience with Selenium or BeautifulSoup
    - Ability to handle pagination and dynamic content
    - Export data to CSV format
    - Clean, maintainable code
    
    Budget: $300-$500
    Timeline: 1 week
    """
    
    job_title = "Python Web Scraper Development"
    
    # Analyze the job
    requirements = router.analyze_job(job_description, job_title)
    print("Job Analysis:")
    print(f"  Skills Required: {requirements['skills_required']}")
    print(f"  Categories: {requirements['categories']}")
    print(f"  Complexity: {requirements['complexity']}")
    print(f"  Budget: {requirements['budget']}")
    print(f"  Timeline: {requirements['timeline']}")
    
    # Find best agent
    best_agent, confidence = router.find_best_agent(requirements)
    
    if best_agent:
        print(f"\nBest Agent Match:")
        print(f"  Agent: {best_agent['name']}")
        print(f"  Confidence: {confidence:.2%}")
        print(f"  Skills: {best_agent['skills']}")
        
        # Estimate duration and cost
        duration = router.estimate_task_duration(requirements, best_agent)
        cost = router.estimate_cost(duration, best_agent)
        
        print(f"\nEstimates:")
        print(f"  Duration: {duration} hours")
        print(f"  Cost: ${cost}")
