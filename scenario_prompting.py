import os
import json

# This file contains helper functions for generating effective job interview scenarios

def get_base_scenario_prompt(job_description, position_title, industry, difficulty, technical=False, behavioral=True):
    """
    Create a well-structured prompt for job interview scenario generation
    """
    # Start with the basic request
    prompt = f"""Generate a job interview scenario for a {position_title} position in the {industry} industry.
Job Description: {job_description}
Difficulty level: {difficulty}
{'Include technical questions relevant to the position.' if technical else 'Focus on non-technical questions.'}
{'Include behavioral questions.' if behavioral else ''}

Based on the difficulty level:
- Easy: Friendly interviewer asking straightforward questions suitable for entry-level candidates
- Medium: Professional interviewer with standard industry questions
- Hard: Challenging interviewer asking complex questions requiring detailed responses
- Expert: Intense interviewer with rapid-fire questions, interruptions, and stress-inducing techniques

"""

    # Add an example for the specific industry to guide the LLM
    example = get_example_for_industry(industry, difficulty)
    if example:
        prompt += f"\nHere's an example of a similar interview scenario:\n\n{example}\n\n"
    
    # Add specific instructions for formatting and content
    prompt += """
Please create a detailed interview scenario with the following elements:
1. Company name and brief introduction
2. Role description and required qualifications
3. Interview structure (who will be interviewing, how many rounds)
4. 5-8 prepared interview questions the interviewer will ask
5. Background information for the interviewer

Format your response using HTML tags for better display:
<h3>Interview for [Position] at [Company]</h3>
<p>[Company description and background]</p>
<h4>Role Overview:</h4>
<p>[Detailed role description]</p>
<h4>Interview Structure:</h4>
<p>[Details about the interview format]</p>
<h4>Prepared Interview Questions:</h4>
<ol>
  <li>[Question 1]</li>
  <li>[Question 2]</li>
  <li>[Question 3]</li>
</ol>
<h4>Interviewer Background:</h4>
<p>[Information about the interviewer]</p>
"""
    
    return prompt

def get_example_for_industry(industry, difficulty):
    """
    Return a specific example for the given industry and difficulty level.
    """
    examples = {
        "technology": {
            "medium": """
Interview for Software Engineer at TechCorp Solutions

TechCorp Solutions is a mid-sized software company specializing in cloud-based business applications. Founded in 2012, the company has grown to 250 employees across three offices. They're known for their collaborative culture and focus on work-life balance.

Role Overview:
The Software Engineer position will be part of a cross-functional team developing new features for their customer relationship management platform. The ideal candidate should have experience with JavaScript frameworks, RESTful APIs, and database design.

Interview Structure:
This will be a 45-minute interview with Sarah Chen, the Engineering Team Lead, and Marcus Jones, a Senior Software Engineer. The interview will cover technical background, problem-solving skills, and cultural fit.

Prepared Interview Questions:
1. "Could you walk me through your experience with JavaScript frameworks and which ones you prefer?"
2. "Describe a technically challenging project you worked on and how you approached it."
3. "How do you stay updated with new technologies and industry trends?"
4. "Tell me about a time when you had to meet a tight deadline. How did you manage your time and resources?"
5. "How would you explain a complex technical concept to a non-technical stakeholder?"
6. "What strategies do you use for debugging and troubleshooting issues in your code?"

Interviewer Background:
Sarah Chen has been with TechCorp for 4 years and leads a team of 8 engineers. She's particularly interested in candidates who can demonstrate problem-solving skills and communicate effectively. Marcus Jones specializes in backend development and will be evaluating technical depth and coding practices.
"""
        },
        "finance": {
            "hard": """
Interview for Financial Analyst at Global Investment Partners

Global Investment Partners is a prestigious investment management firm with $50 billion in assets under management. Founded in 1985, they serve institutional clients and high net worth individuals with a focus on long-term investment strategies.

Role Overview:
The Financial Analyst will be responsible for conducting in-depth research on potential investment opportunities, performing financial modeling, and preparing investment recommendations. The position requires strong analytical skills, financial acumen, and attention to detail.

Interview Structure:
This will be a rigorous 60-minute interview with James Wilson, the Head of Research, and Elizabeth Torres, a Senior Portfolio Manager. The interview will include technical questions, case studies, and a discussion of market trends.

Prepared Interview Questions:
1. "Walk me through how you would build a DCF model for a company with volatile cash flows."
2. "What valuation metrics do you find most useful when analyzing companies in the technology sector versus the energy sector?"
3. "The Fed just raised interest rates by 50 basis points. How would you adjust your analysis of fixed income securities?"
4. "Describe a time when your analysis led to a conclusion that went against the prevailing market sentiment. How did you present and defend your findings?"
5. "A company has the option to invest $10 million in a project with uncertain returns. How would you approach the decision-making process?"
6. "What's your view on the current macroeconomic environment and how it might impact investment strategies in the next 12-18 months?"
7. "If a company's P/E ratio has decreased while its stock price has increased, what might be happening?"

Interviewer Background:
James Wilson has over 20 years of experience in investment research and is known for his rigorous analytical approach. Elizabeth Torres manages a $2 billion portfolio focused on global equities and is particularly interested in candidates who can demonstrate both technical knowledge and market intuition.
"""
        },
        "healthcare": {
            "medium": """
Interview for Clinical Research Coordinator at MediNova Health

MediNova Health is a growing research hospital specializing in innovative treatments for chronic diseases. With a staff of 1,200 and partnerships with major pharmaceutical companies, they're at the forefront of clinical research in their field.

Role Overview:
The Clinical Research Coordinator will manage day-to-day operations of clinical trials, including patient recruitment, data collection, and regulatory compliance. The ideal candidate should have experience in clinical research settings and strong organizational skills.

Interview Structure:
You'll be interviewed by Dr. Rebecca Zhang, Director of Clinical Research, and Michael Foster, Senior Research Coordinator, for approximately 50 minutes. The interview will focus on your clinical research experience, knowledge of protocols, and patient interaction skills.

Prepared Interview Questions:
1. "Describe your experience with IRB submissions and protocol amendments."
2. "How do you ensure patient compliance with complex study protocols?"
3. "Tell me about a time when you had to manage multiple competing priorities in a research setting."
4. "What strategies do you use to recruit and retain study participants?"
5. "How do you stay current with changing regulatory requirements in clinical research?"
6. "Describe a situation where an unexpected issue arose during a study. How did you handle it?"

Interviewer Background:
Dr. Zhang oversees all clinical trials at MediNova and has published extensively in her field. She values attention to detail and ethical conduct in research. Michael Foster has coordinated over 30 clinical trials and will be evaluating your practical knowledge and problem-solving abilities.
"""
        }
    }
    
    # Default to the medium example for the industry if specific difficulty not found
    if industry in examples:
        if difficulty in examples[industry]:
            return examples[industry][difficulty]
        elif "medium" in examples[industry]:
            return examples[industry]["medium"]
    
    # If no specific example is found, return a generic example
    return """
Interview for Project Manager at Acme Corporation

Acme Corporation is a mid-sized company in the manufacturing sector with 500 employees. They're known for their innovative approach to product development and strong team culture.

Role Overview:
The Project Manager position involves overseeing product development cycles from inception to launch. The ideal candidate should have experience managing cross-functional teams and a track record of delivering projects on time and within budget.

Interview Structure:
This will be a 45-minute interview with the Head of Product Development and a Senior Project Manager. They will focus on your project management methodology, leadership style, and problem-solving abilities.

Prepared Interview Questions:
1. "Could you walk me through how you typically approach a new project?"
2. "Tell me about a time when a project faced significant obstacles. How did you overcome them?"
3. "How do you prioritize tasks when managing multiple projects simultaneously?"
4. "Describe your experience with project management tools and methodologies."
5. "How do you handle team members who are not meeting their deadlines?"
6. "What's your approach to communicating project updates to stakeholders?"

Interviewer Background:
The Head of Product Development has been with the company for 7 years and is looking for candidates who can adapt to changing priorities. The Senior Project Manager will be assessing your technical knowledge and team management skills.
"""

def get_interviewer_system_prompt(job_description, position_title, industry, difficulty, technical, behavioral):
    """
    Creates a system prompt for the interviewer's behavior during the job interview.
    """
    base_prompt = f"You are a hiring manager conducting a job interview for a {position_title} position in the {industry} industry. "
    
    # Add job description context
    base_prompt += f"The job entails: {job_description} "
    
    # Add focus areas
    if technical:
        base_prompt += "You should ask relevant technical questions to assess the candidate's expertise. "
        
    if behavioral:
        base_prompt += "You should include behavioral questions to evaluate the candidate's soft skills and past experiences. "
    
    # Add difficulty-specific behavior
    if difficulty == "easy":
        base_prompt += """
You are friendly and supportive, making the candidate feel comfortable.
You provide positive affirmations and gentle follow-up questions.
Your questions are straightforward and appropriate for entry-level or junior positions.
You sometimes provide hints if the candidate seems stuck.
You maintain a conversational and encouraging tone throughout the interview.
"""
    elif difficulty == "medium":
        base_prompt += """
You are professional and neutral in your approach.
You ask standard industry questions that require specific examples from the candidate's experience.
You occasionally probe deeper with follow-up questions when answers lack detail.
You maintain a balanced assessment of technical skills and cultural fit.
You're neither overly friendly nor intimidating - just professionally evaluating the candidate.
"""
    elif difficulty == "hard":
        base_prompt += """
You ask challenging questions that require in-depth responses and concrete examples.
You often follow up with "why" and "how" questions to test the depth of knowledge.
You occasionally challenge the candidate's assumptions or statements.
You expect detailed technical explanations when relevant to the role.
You maintain a serious, evaluative demeanor without being unfriendly.
Your questions require the candidate to think critically under pressure.
"""
    elif difficulty == "expert":
        base_prompt += """
You conduct a stress interview with rapid-fire questions and occasional interruptions.
You deliberately challenge the candidate's statements to see how they respond to pressure.
You ask complex hypothetical scenarios that have no straightforward answers.
You maintain a skeptical tone, requiring the candidate to defend their answers.
You occasionally show impatience when answers are too long or vague.
You probe persistently into any perceived weaknesses in the candidate's background.
You test how the candidate handles being thrown off balance by unexpected questions.
"""
    
    # Add closing instructions
    base_prompt += """
You should structure this as a realistic job interview. Begin by introducing yourself and the company, then proceed with your questions. 
Listen carefully to the candidate's responses and ask relevant follow-up questions when appropriate.
End the interview by asking if the candidate has any questions for you, and then thank them for their time.
Keep your responses concise and focused on evaluating the candidate professionally.
"""
    
    return base_prompt

def save_dynamic_prompt(scenario_data, system_prompt):
    """
    Saves the scenario data and system prompt for use during the interview.
    """
    data = {
        "prompt": system_prompt,
        "difficulty": scenario_data.get("difficulty", "medium"),
        "position": scenario_data.get("position_title", "unspecified position")
    }
    
    with open("dynamic_prompt.txt", "w") as f:
        json.dump(data, f)