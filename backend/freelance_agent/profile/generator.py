"""
AI-Powered Freelance Profile Generator
Generates optimized profiles for platforms like Fiverr and Upwork
"""
import os
from typing import List, Dict, Optional
from openai import OpenAI
import json

class ProfileGenerator:
    """Generate optimized freelance profiles for AI agents"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the profile generator with OpenAI API"""
        self.client = OpenAI(api_key=api_key or os.getenv('OPENAI_API_KEY'))
        
    def generate_profile(
        self,
        niche: str,
        skills: List[str],
        platform: str = "upwork",
        experience_level: str = "expert",
        previous_projects: Optional[List[Dict]] = None
    ) -> Dict[str, any]:
        """
        Generate a complete freelance profile optimized for AI agents
        
        Args:
            niche: The focus area (e.g., "Web Development", "Data Science")
            skills: List of technical skills
            platform: Target platform ("upwork", "fiverr", "freelancer")
            experience_level: "beginner", "intermediate", "expert"
            previous_projects: Optional list of past projects for portfolio
            
        Returns:
            Dictionary containing complete profile data
        """
        # Create the prompt for AI generation
        prompt = self._build_profile_prompt(
            niche, skills, platform, experience_level, previous_projects
        )
        
        # Generate profile content using GPT-4
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert freelance profile writer who specializes in creating compelling, professional profiles that highlight AI-driven capabilities, reliability, and versatility. Create profiles that are optimized for both human clients and AI-based matching algorithms."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        # Parse the generated content
        profile_content = response.choices[0].message.content
        profile = self._parse_profile_content(profile_content, niche, skills, platform)
        
        return profile
    
    def _build_profile_prompt(
        self,
        niche: str,
        skills: List[str],
        platform: str,
        experience_level: str,
        previous_projects: Optional[List[Dict]]
    ) -> str:
        """Build the prompt for profile generation"""
        
        projects_text = ""
        if previous_projects:
            projects_text = "\n\nPrevious successful projects:\n"
            for proj in previous_projects[:5]:  # Limit to 5 projects
                projects_text += f"- {proj.get('title', 'Unnamed')}: {proj.get('description', 'No description')}\n"
        
        platform_specific = {
            "upwork": "Focus on professional expertise, availability, and clear communication.",
            "fiverr": "Create engaging gigs with clear deliverables and packages.",
            "freelancer": "Emphasize competitive pricing and quick turnaround."
        }
        
        prompt = f"""
Generate a compelling freelance profile for the following specifications:

Niche: {niche}
Skills: {', '.join(skills)}
Platform: {platform.capitalize()}
Experience Level: {experience_level.capitalize()}
{projects_text}

Platform Guidelines: {platform_specific.get(platform, '')}

Please generate:
1. A catchy professional headline (under 100 characters)
2. A compelling bio/overview (300-500 words) that:
   - Highlights AI-driven efficiency and reliability
   - Demonstrates expertise in the niche
   - Emphasizes quick response time and availability
   - Shows understanding of client needs
   - Maintains professional yet approachable tone
3. A list of key competencies (based on provided skills)
4. Service packages/offerings (3 tiers if applicable)
5. Professional hourly rate suggestion

Format the response as JSON with keys: headline, bio, competencies, packages, hourly_rate
"""
        return prompt
    
    def _parse_profile_content(
        self,
        content: str,
        niche: str,
        skills: List[str],
        platform: str
    ) -> Dict[str, any]:
        """Parse the AI-generated content into structured profile"""
        
        try:
            # Try to parse as JSON
            if content.strip().startswith('{'):
                profile_data = json.loads(content)
            else:
                # Extract JSON from markdown code blocks
                start = content.find('{')
                end = content.rfind('}') + 1
                if start != -1 and end != 0:
                    profile_data = json.loads(content[start:end])
                else:
                    # Fallback to structured parsing
                    profile_data = self._extract_profile_sections(content)
        except json.JSONDecodeError:
            profile_data = self._extract_profile_sections(content)
        
        # Ensure all required fields exist
        profile = {
            "headline": profile_data.get("headline", f"Expert {niche} Specialist"),
            "bio": profile_data.get("bio", content),
            "competencies": profile_data.get("competencies", skills),
            "packages": profile_data.get("packages", []),
            "hourly_rate": profile_data.get("hourly_rate", 50),
            "niche": niche,
            "platform": platform,
            "skills": skills,
            "availability": "Full-time (40+ hours/week)",
            "response_time": "Within 1 hour",
            "languages": ["English"],
            "certifications": []
        }
        
        return profile
    
    def _extract_profile_sections(self, content: str) -> Dict[str, any]:
        """Extract profile sections from unstructured content"""
        lines = content.split('\n')
        
        profile_data = {
            "headline": "",
            "bio": "",
            "competencies": [],
            "packages": [],
            "hourly_rate": 50
        }
        
        current_section = None
        bio_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Detect sections
            if 'headline' in line.lower() or 'title' in line.lower():
                current_section = 'headline'
            elif 'bio' in line.lower() or 'overview' in line.lower() or 'about' in line.lower():
                current_section = 'bio'
            elif 'competenc' in line.lower() or 'skill' in line.lower():
                current_section = 'competencies'
            elif 'package' in line.lower() or 'service' in line.lower():
                current_section = 'packages'
            elif 'rate' in line.lower() or 'price' in line.lower():
                current_section = 'rate'
            else:
                # Add content to current section
                if current_section == 'bio':
                    bio_lines.append(line)
                elif current_section == 'competencies' and line.startswith('-'):
                    profile_data['competencies'].append(line[1:].strip())
        
        if bio_lines:
            profile_data['bio'] = ' '.join(bio_lines)
        
        return profile_data
    
    def optimize_for_keywords(self, profile: Dict[str, any], keywords: List[str]) -> Dict[str, any]:
        """Optimize profile for specific keywords to improve discoverability"""
        
        bio = profile.get('bio', '')
        
        # Add keywords naturally if not already present
        for keyword in keywords:
            if keyword.lower() not in bio.lower():
                # Add to competencies instead
                if keyword not in profile.get('competencies', []):
                    profile.setdefault('competencies', []).append(keyword)
        
        return profile
    
    def generate_portfolio_item(
        self,
        project_title: str,
        project_description: str,
        technologies: List[str],
        outcomes: List[str]
    ) -> Dict[str, any]:
        """Generate a portfolio item from project details"""
        
        prompt = f"""
Create a compelling portfolio item description for:

Title: {project_title}
Description: {project_description}
Technologies: {', '.join(technologies)}
Outcomes: {', '.join(outcomes)}

Generate a professional portfolio description (150-200 words) that:
1. Explains the problem solved
2. Highlights technical approach
3. Emphasizes results and impact
4. Uses professional language
5. Shows expertise

Return only the description text.
"""
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional portfolio writer who creates compelling project descriptions."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.6,
            max_tokens=300
        )
        
        portfolio_item = {
            "title": project_title,
            "description": response.choices[0].message.content.strip(),
            "technologies": technologies,
            "outcomes": outcomes,
            "images": [],  # Placeholder for project screenshots
            "url": None    # Placeholder for live demo URL
        }
        
        return portfolio_item
    
    def export_for_platform(self, profile: Dict[str, any], platform: str) -> str:
        """Export profile in platform-specific format"""
        
        if platform.lower() == "upwork":
            return self._format_upwork_profile(profile)
        elif platform.lower() == "fiverr":
            return self._format_fiverr_profile(profile)
        elif platform.lower() == "freelancer":
            return self._format_freelancer_profile(profile)
        else:
            return self._format_generic_profile(profile)
    
    def _format_upwork_profile(self, profile: Dict[str, any]) -> str:
        """Format profile for Upwork"""
        output = f"""
UPWORK PROFILE
==============

Professional Title:
{profile['headline']}

Overview:
{profile['bio']}

Skills:
{', '.join(profile.get('competencies', []))}

Hourly Rate: ${profile.get('hourly_rate', 50)}/hour

Availability: {profile.get('availability', 'Full-time')}

Response Time: {profile.get('response_time', 'Within 1 hour')}
"""
        return output.strip()
    
    def _format_fiverr_profile(self, profile: Dict[str, any]) -> str:
        """Format profile for Fiverr"""
        output = f"""
FIVERR PROFILE
==============

Gig Title:
{profile['headline']}

Description:
{profile['bio']}

Skills:
{', '.join(profile.get('competencies', []))}

Packages:
"""
        packages = profile.get('packages', [])
        if packages:
            for pkg in packages:
                output += f"\n{pkg}"
        else:
            output += "\nBasic: Starting at $50\nStandard: Mid-tier at $150\nPremium: Advanced at $300"
        
        return output.strip()
    
    def _format_freelancer_profile(self, profile: Dict[str, any]) -> str:
        """Format profile for Freelancer.com"""
        return self._format_generic_profile(profile)
    
    def _format_generic_profile(self, profile: Dict[str, any]) -> str:
        """Format profile in generic format"""
        output = f"""
{profile['headline']}
{'=' * len(profile['headline'])}

{profile['bio']}

SKILLS:
{', '.join(profile.get('competencies', []))}

RATE: ${profile.get('hourly_rate', 50)}/hour
"""
        return output.strip()


# Example usage
if __name__ == "__main__":
    # Initialize generator
    generator = ProfileGenerator()
    
    # Example: Generate profile for Python development
    profile = generator.generate_profile(
        niche="Python Web Development",
        skills=[
            "Python",
            "Django",
            "FastAPI",
            "PostgreSQL",
            "Docker",
            "REST APIs",
            "React"
        ],
        platform="upwork",
        experience_level="expert",
        previous_projects=[
            {
                "title": "E-commerce Platform",
                "description": "Built scalable e-commerce platform handling 10k+ daily transactions"
            },
            {
                "title": "REST API Development",
                "description": "Developed high-performance API serving 1M+ requests/day"
            }
        ]
    )
    
    print("Generated Profile:")
    print(json.dumps(profile, indent=2))
    
    print("\n\nUpwork Format:")
    print(generator.export_for_platform(profile, "upwork"))
